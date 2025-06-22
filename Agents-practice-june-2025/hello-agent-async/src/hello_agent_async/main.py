
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
import asyncio
import os

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
    instructions= "You are a helpful assistant that can answer questions and help with tasks.",
    
    

)

    response = await Runner.run(
       agent1,
    "What is the capital of the islamabad?"
)

    print(response.last_agent)


if __name__ == "__main__":
    asyncio.run(main())


