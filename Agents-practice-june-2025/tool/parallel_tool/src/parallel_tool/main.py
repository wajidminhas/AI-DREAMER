
import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, function_tool, AsyncOpenAI, Runner, RunContextWrapper, enable_verbose_stdout_logging
from agents.run import RunConfig
from pydantic import BaseModel
from typing import ClassVar
from dataclasses import dataclass


load_dotenv()
@dataclass
class Person:
    name : str
    age : int
    national : str


gemini_api_key = os.getenv("GEMINI_API_KEY")

@function_tool
async def employe(wrapper : RunContextWrapper[Person]) -> str:
    """
    Retrieves and formats the name and age details of a person from the context.
    """
    print("DEBUG: employe tool was called.") # Debugging print
    # Corrected: return the string, not await it
    return f"Person Detail: User {wrapper.context.name} with age {wrapper.context.age}"

@function_tool
async def employee_location(wrapper : RunContextWrapper[Person]) -> str:
    """
    Retrieves and formats the nationality detail of a person from the context.
    """
    print("DEBUG: employee_location tool was called.") # Debugging print
    # Corrected: return the string, not await it
    return f"User with detail {wrapper.context.name} belongs to {wrapper.context.national}"

async def main():

    personal_info = Person(name="wajid minhas", age=24, national="Pakistan")
    provider = AsyncOpenAI(
        api_key = gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    
    model = OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gemini-1.5-flash",
    )


    triage_agent : Agent = Agent(
        name = "Triage Agent",
        model=model,
        instructions="you are a triage agent that classifies the type of request and assigns it to the appropriate agent or tool call",
        output_type=str,
        tools=[employe, employee_location]
    )

    config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )

    result = await Runner.run(triage_agent, 
                                    "I need help with my account",
                                    run_config=config)
    
    result = await Runner.run(triage_agent, 
                              "give detail of person who belong pakistan",
                            #   run_config=config,
                              context=personal_info,
                              max_turns=2
                              
                              )
    
    print(f"\nFinal Output\n")
    print(result.final_output.content)
    print(result.context_wrapper)
    print(f"\n\n Raw Responses:\n")
    print(result.raw_responses)

    
    # print(f"\n\n Raw Responses output:\n")
    # print(result.raw_responses.__format__( dict=True))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())