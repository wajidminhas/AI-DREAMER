from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, enable_verbose_stdout_logging, ModelSettings
from pprint import pprint
import os
import asyncio
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Enable verbose logging to stdout
enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# if gemini_api_key is None:
    # raise ValueError("GEMINI_API_KEY environment variable is not set.")

base_url = os.getenv("BASE_URL")

if base_url is None:
    raise ValueError("BASE_URL environment variable is not set.")

@function_tool
async def greet(name: str) -> str:
    """
    A simple function tool that greets the user.
    """
    return f"Hello, {name}!"


@function_tool
async def get_weather(city : str) -> str:
    """"A simple function tool that returns the weather for a given city.
    agruments:
        city (str): The name of the city.
    returns:
        str: A string describing the weather in the city.
    """
    return f"The weather in {city} is sunny with a chance of rain."

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-1.5-flash",
)

agent = Agent(
    name = "Helpful Assistant",
    instructions="alway reply of user query in haiku format",
    model = model,
    tools = [greet, get_weather],
    model_settings=ModelSettings(temperature=0.2, parallel_tool_calls=False)
)

result = Runner.run_sync(agent, "hi, greet to user, what is the weather in lahore?", )


pprint(result.final_output)