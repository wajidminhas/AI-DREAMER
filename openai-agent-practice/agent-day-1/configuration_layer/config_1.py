

import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner
# from decouple import Config


load_dotenv()

# api_key = Config("GEMINI_API_KEY")
key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")


gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)