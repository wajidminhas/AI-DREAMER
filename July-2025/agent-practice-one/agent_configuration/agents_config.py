import os
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI

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