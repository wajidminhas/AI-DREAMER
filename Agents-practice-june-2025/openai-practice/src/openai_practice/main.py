import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionsModel, function_tool , enable_verbose_stdout_logging, ModelSettings
from agents.run import RunConfig


load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@function_tool()
def greet(name: str):
    """
    whenever user 'call him by good name' interact with you than greet him/her warmly and unique method

    agr 
    name : str

    """
    return (f"Name : {name}")

@function_tool()
def get_weather(city : str) -> str:
    """
    provide weather detail of country which mentiond at input 

    """
    return (f"the weather of {city} is cloudy")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    # tracing_disabled=True
)

agent: Agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant, reply in poetry style", 
    model=model, 
    tools =[greet, get_weather],
    # tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(tool_choice="auto"),
    reset_tool_choice=False
    )

result = Runner.run_sync(agent, "Hello from john doe", run_config=config, max_turns=1)
print(result.final_output)

