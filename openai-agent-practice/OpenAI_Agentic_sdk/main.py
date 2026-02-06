

from decouple import config
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner

GEMINI_API_KEY = config("GEMINI_API_KEY")
BASE_URL = config("BASE_URL", default="https://generativelanguage.googleapis.com/v1beta/openai/")


gemini_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

MODEL = OpenAIChatCompletionsModel(
    openai_client=gemini_client, model="gemini-2.5-flash"
)


agent = Agent(
    name="Python Tutor",
    instructions="You are a helpful coding assistant that helps people learn Python programming. "
                 "You provide clear explanations and code examples to help users understand Python concepts.",
    model=MODEL)


res = Runner.run_sync(starting_agent=agent, input="What is a list comprehension in Python? Can you provide an example?")

print(res.final_output)