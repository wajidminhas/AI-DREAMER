
import asyncio
import os
from dotenv import load_dotenv
import chainlit as cl
from chainlit.types import AskFileResponse
from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai import OpenAI
import google.generativeai as genai


#load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini API client
external_client = AsyncOpenAI(api_key=gemini_api_key,
                              base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client,
)

sheff = Agent(
    name="Sheff",
    # model=model,
    instructions="A helpful sheff assistant about pakistani food and recipes so you would answer questions and provide information.",)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
result = Runner.run_streamed(sheff, input="What is the recipe for Biryani?", run_config=config)
# Process the streamed result
async for event in result.stream_events():
        if event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))
print(result)

@cl.on_message
async def handle_message(message : cl.Message):
    """
    Handle incoming messages from Chainlit.
    """
    result = Runner.run_sync(
    sheff,
    input=message.content,
    run_config=config
    )
        
    await cl.Message(content=result.final_output).send()