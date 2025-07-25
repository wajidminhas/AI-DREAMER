from agents import Agent,OpenAIChatCompletionsModel,Runner,function_tool, AgentHooks, enable_verbose_stdout_logging, RunHooks, ModelSettings, RunContextWrapper
from openai import AsyncOpenAI
from dotenv import get_key,find_dotenv
from pprint import pprint
import requests
from pydantic import BaseModel
from typing import Any

gemini_api_key=get_key(find_dotenv(),"GEMINI_API_KEY")

# enable_verbose_stdout_logging()


client=AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key

)

# ---   
class TestHooks(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "TestHooks"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")
    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")

class TestAgHooks(AgentHooks):
    def __init__(self, ag_display_name):
        self.event_counter = 0
        self.ag_display_name = ag_display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")

start_hook = TestHooks()

class WeatherData(BaseModel):
    city: str
    temperature: float
    condition: str

    def __str__(self):
        return f"The current weather in {self.city} is {self.temperature}°C with {self.condition}."

@function_tool
def get_weather(city: RunContextWrapper[WeatherData])->str:
    """
    Get the current weather for a given city.
    """
    # Simulate a weather API call
    # In a real scenario, you would replace this with an actual API call to a weather service.
    weather_data = WeatherData(city=city, temperature=25.0, condition="sunny")
    return str(weather_data)

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

agent:Agent=Agent(
    name="Content Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",

    # instructions="You are a weather agent. You can provide weather information and forecasts.",
    model=model,
    tools=[get_weather],
    # tool_use_behavior="sequential",
   
    model_settings=ModelSettings(tool_choice= "none"),
    reset_tool_choice=False,
    hooks=TestAgHooks(ag_display_name="Content Moderator Agent"),
    # output_type=WeatherData,  # Specify the output type for the agent
)
async def main():

    result = await Runner.run(
      agent,
      hooks=start_hook,
      input=f"<tweet>Will Agentic AI Die at end of 2025?.</tweet>"
  )

    # print("Agent Response:")
    pprint(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())