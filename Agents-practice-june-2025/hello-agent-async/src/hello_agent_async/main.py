
from dataclasses import dataclass
# from lib2to3.fixes.fix_input import context
from dotenv import load_dotenv
from agents.run import RunConfig
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import asyncio
import os

# @dataclass
# class CountryOfSouthAsia:
    # name: str
    # capital: str
    # population: int

load_dotenv()

gemini_api_key = os.getenv("GEMINI-API-KEY")

set_tracing_disabled(True)


async def main():

    
    



    provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

    model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)
  
    

    agent1 = Agent(
    name = "Agent 1",
    model = model,
    instructions= "You are a helpful assistant",
    # tools=[get_south_asian_countries_and_capitals],
    )

    run_config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )
    response = await Runner.run(
       agent1,
       "What are the name of south asian countries along with their capitals?",
       
     
)

    print(response.raw_responses)


if __name__ == "__main__":
    asyncio.run(main())


