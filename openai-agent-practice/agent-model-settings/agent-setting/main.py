from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper,Runner,StopAtTools, function_tool, enable_verbose_stdout_logging, ModelSettings
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

from pydantic import BaseModel
class User(BaseModel):
    user_name: str
    age: int

user_data = ""
def set_instrtuctios(ctx : RunContextWrapper[User],  agent : Agent)-> str:
    """
    Set instructions for the agent based on the context.
    """
    # global user_data 
    user_data = f"User name: {ctx.context.user_name}, User age: {ctx.context.age}"
    return f"You are a helpful assistant. {user_data} Your task is to assist the user with their queries. Respond in a friendly and informative manner."

@function_tool
async def greet(u_name: str):
    """
    A simple function tool that greets the user.
    """
    return f"Hello, {u_name}!"


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
    model="gemini-2.0-flash",
)
user_context = User(user_name="Alice", age=30)

agent = Agent(
    name = "Helpful Assistant",
    instructions=[set_instrtuctios],
    model = model,
    # output_type=User,
    # tools = [greet, get_weather]
    # model_settings=ModelSettings(temperature=0.2, parallel_tool_calls=False)
    # tool_use_behavior=StopAtTools(stop_at_tool_names=[get_weather])
)


result = Runner.run_sync(agent, "hi, check the context i given you", context=user_context, )

pprint(result.final_output)
print("Done!")
print(f"\nUser name: {user_context.user_name}\n")
print(f"\nUser age: {user_context.age}")