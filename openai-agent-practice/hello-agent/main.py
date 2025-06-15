import os
from typing import Dict
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI
import google.generativeai as genai
from chainlit.types import AskFileResponse

# Load environment variables
load_dotenv()

# Initialize clients
client = None
is_gemini = False

# Check for API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        client = genai.GenerativeModel('gemini-1.5-flash')  # Adjust model name if needed
        is_gemini = True
        print("Initialized Gemini client successfully")
    except Exception as e:
        print(f"Failed to initialize Gemini client: {str(e)}")
elif openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
        print("Initialized OpenAI client successfully")
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {str(e)}")
else:
    raise ValueError("No valid API key found for Gemini or OpenAI")

# Store conversation history
conversation_history: Dict[str, list] = {}

@cl.on_chat_start
async def start_chat():
    """
    Initialize the chat session with custom settings and welcome message.
    """
    session_id = cl.user_session.get("id")
    if session_id is None:
        raise ValueError("Session ID is not set")
    
    conversation_history[session_id] = []
    
    # Set default model based on client
    default_model = "gemini-pro" if is_gemini else "gpt-3.5-turbo"
    cl.user_session.set("model", default_model)
    
    # Send welcome message
    elements = [
        cl.Image(
            name="logo",
            display="inline",
            url="https://raw.githubusercontent.com/Chainlit/chainlit/main/logo.png"
        )
    ]
    
    await cl.Message(
        content="Welcome to CustomAI Chat! How can I assist you today?",
        elements=elements
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming messages with enhanced features.
    """
    session_id = cl.user_session.get("id")
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    # Update conversation history
    conversation_history[session_id].append({
        "role": "user",
        "content": message.content
    })
    
    try:
        msg = cl.Message(content="")
        
        if is_gemini:
            # Format history for Gemini
            gemini_history = []
            for msg_entry in conversation_history[session_id]:
                role = 'user' if msg_entry['role'] == 'user' else 'model'
                gemini_history.append({
                    'role': role,
                    'parts': [{'text': msg_entry['content']}]
                })
            
            # Generate response with Gemini
            response = client.generate_content(
                gemini_history,
                stream=True
            )
            
            # Stream response
            for chunk in response:
                if chunk.text:
                    await msg.stream_token(chunk.text)
        
        else:
            # OpenAI client
            response = client.chat.completions.create(
                model=cl.user_session.get("model"),
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    *conversation_history[session_id]
                ],
                stream=True
            )
            
            # Stream response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    await msg.stream_token(chunk.choices[0].delta.content)
        
        # Update conversation history with assistant response
        conversation_history[session_id].append({
            "role": "assistant",
            "content": msg.content
        })
        
        await msg.send()
        
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        await cl.Message(
            content=error_msg,
            author="Error"
        ).send()

@cl.on_settings_update
async def setup_agent(settings):
    """
    Handle settings updates from the UI.
    """
    valid_models = ["gemini-pro", "gpt-3.5-turbo", "gpt-4"] if is_gemini else ["gpt-3.5-turbo", "gpt-4"]
    model = settings.get("model", "gemini-pro" if is_gemini else "gpt-3.5-turbo")
    
    if model not in valid_models:
        await cl.Message(content=f"Invalid model selected. Available models: {', '.join(valid_models)}").send()
        return
    
    cl.user_session.set("model", model)
    await cl.Message(content=f"Settings updated! Now using model: {model}").send()

@cl.on_chat_end
async def end_chat():
    """
    Clean up when chat ends.
    """
    session_id = cl.user_session.get("id")
    if session_id in conversation_history:
        del conversation_history[session_id]