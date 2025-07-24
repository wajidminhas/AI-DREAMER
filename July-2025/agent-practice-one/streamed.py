from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled, Runner, RunConfig, enable_verbose_stdout_logging, AsyncOpenAI, ItemHelpers, function_tool
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

import asyncio

load_dotenv()
import os
enable_verbose_stdout_logging()
# set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

base_url = os.getenv("BASE_URL")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)
model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.0-flash",
)
@function_tool
async def how_many_jokes() -> str:
    """
    Ask the user how many jokes they want to hear.
    """
    return "How many jokes would you like to hear? Please respond with a number."

async def main():
    agent = Agent(
        name="Joke Teller",
        model=model,
        instructions="You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())