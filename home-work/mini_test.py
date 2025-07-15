from langfuse import Langfuse, langfuse_context
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

    @langfuse_context
    async def generate(self, prompt, **kwargs):
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        return {
            "choices": [{"message": {"content": response.text}}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        }

# Initialize model
model = GeminiModel(model_name="gemini-1.5-flash")

# Your agent definitions
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
    result = await Runner.run(triage_agent, 
        "who was the first president of the united states?")
    print(result.final_output)
    
    # Flush Langfuse traces
    langfuse.flush()

if __name__ == "__main__":
    asyncio.run(main())