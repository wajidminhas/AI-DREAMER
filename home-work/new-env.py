from langfuse import Langfuse
from agents import (
    set_trace_processors,
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    Runner
)
import os
import google.generativeai as genai
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify environment variables
required_env_vars = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "GEMINI_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Environment variable {var} is not set")

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host="https://cloud.langfuse.com"  # Or self-hosted URL
)

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Custom Gemini model wrapper
class GeminiModel:
    def __init__(self, model_name):
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name  # Add for compatibility
        # Mimic OpenAI's chat.completions namespace
        self.chat = type('Chat', (), {'completions': self})()

    async def create(self, messages, **kwargs):
        # Convert OpenAI-style messages to Gemini prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        trace = langfuse.trace(name="gemini_call", input=prompt)
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            result = {
                "choices": [{"message": {"content": response.text, "role": "assistant"}}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
            trace.update(output=result["choices"][0]["message"]["content"])
            return type('Response', (), result)()  # Return object mimicking OpenAI response
        except Exception as e:
            trace.update(output=f"Error: {str(e)}")
            print(f"Gemini API error: {e}")
            raise

    async def generate(self, prompt, **kwargs):
        # Fallback for direct prompt calls
        trace = langfuse.trace(name="gemini_call", input=prompt)
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            result = {
                "choices": [{"message": {"content": response.text, "role": "assistant"}}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            }
            trace.update(output=result["choices"][0]["message"]["content"])
            return type('Response', (), result)()
        except Exception as e:
            trace.update(output=f"Error: {str(e)}")
            print(f"Gemini API error: {e}")
            raise

# Initialize model
model = GeminiModel(model_name="gemini-1.5-flash")

# Agent definitions
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="""
    You provide help with math problems.
    Explain your reasoning at each step and include examples
    """,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="""
    You provide assistance with historical queries.
    Explain important events and context clearly.
    """,
)

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(output_info=final_output, 
        tripwire_triggered=not final_output.is_homework)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    model=model,
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail)
    ],
)

async def main():
    # Remove GalileoTracingProcessor
    set_trace_processors([])
    
    # Run the agent with Langfuse tracing
    try:
        result = await Runner.run(triage_agent, 
            "who was the first president of the united states?")
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")
    
    # Flush Langfuse traces
    langfuse.flush()

if __name__ == "__main__":
    asyncio.run(main())