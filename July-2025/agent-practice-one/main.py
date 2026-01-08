
from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, enable_verbose_stdout_logging, AsyncOpenAI, function_tool
from dotenv import load_dotenv
load_dotenv()
import os
enable_verbose_stdout_logging()
from my_agents.gemini_agent import agent




async def main():
    result = await Runner.run(agent, "what is weather in karachi and where is location of lahore in region", max_turns=2)
    print(result.new_items)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())