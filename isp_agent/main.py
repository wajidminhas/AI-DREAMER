from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
import os
from pprint import pprint
from pydantic import BaseModel
from dataclasses import dataclass

load_dotenv()
# Load environment variables from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables")


@dataclass
class ServieArea:
    city: str
    # service_area: str 



# ************** Tools **************
# Here you can define tools that the agent can use



@function_tool
def fetch_weather(ctx : RunContextWrapper[ServieArea])-> str :
    """
    fetch the weather of specific city which you will provide.
    """
    return ( f"The weather of {ctx.context.city} is sunny.")



external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-1.5-flash",
)
agent = Agent(
    name="Assistent Agent",
    instructions="you are helpful assistent to response user query.",
    model=model,
    tools=[fetch_weather],
)

result = Runner.run(agent, "are you human?")

print(result.final_output)
