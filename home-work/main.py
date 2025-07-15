# from galileo.handlers.openai_agents import GalileoTracingProcessor
from agents import (
    set_trace_processors,
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
)
import os
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv, find_dotenv
# Load environment variables from .env file 
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-1.5-flash",
   
)
# Create a class with BaseModel to validate output types
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# Create math tutor agent to answer math questions
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="""
    You provide help with math problems.
    Explain your reasoning at each step and include examples
    """,
)

# Create history tutor agent to answer history questions
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="""
    You provide assistance with historical queries.
    Explain important events and context clearly.
    """,
)

# Create Guardrail agent to determine if input question
# is homework-related
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput
)

# Set tripwire to filter out non-homework questions with Guardrail agent
async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, 
                              input_data,
                              context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(output_info=final_output, 
        tripwire_triggered=not final_output.is_homework)

# Create Triage agent to determine which tutor agent to use
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    model=model,
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail)
    ],
)


# Use the Runner to run the agents and get the answers
async def main():
    # Set the trace processor to the Galileo trace processor
    # set_trace_processors([])
    result = await Runner.run(triage_agent, 
        "who was the first president of the united states?")
    print(result.final_output)
   

    # result = await Runner.run(triage_agent, "what is life?")
    # print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())