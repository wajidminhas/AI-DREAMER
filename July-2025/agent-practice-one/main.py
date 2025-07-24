
from agents import Agent, OpenAIChatCompletionsModel, Runner, RunConfig, enable_verbose_stdout_logging, AsyncOpenAI, function_tool
from dotenv import load_dotenv
load_dotenv()
import os
enable_verbose_stdout_logging()

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
async def get_weather(city: str) -> str:
    # Simulate a weather API call
    return f"The weather in {city} is sunny with a high of 25°C."
@function_tool
def get_location(location: str, region: str):
    """
    get the location which about user is asking
    """

    return f"you {location } is location in {region}"

agent : Agent = Agent(
    name = "Heplful Assistant",
    instructions= "You are a helpful assistant. Answer the user's questions to the best of your ability.",
    model=model,
    tools = [get_weather, get_location],
    # model_settings= 
    

)

async def main():
    result = await Runner.run(agent, "what is weather in karachi and where is location of lahore in region", max_turns=2)
    print(result.new_items)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())