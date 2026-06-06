

import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner
# from decouple import Config


load_dotenv()

# api_key = Config("GEMINI_API_KEY")
key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

groq_api_key = os.getenv("GROQ_API_KEY")
groq_base_url = os.getenv("GROQ_BASE_URL")


groq_client = AsyncOpenAI(api_key=groq_api_key, base_url=groq_base_url)

groq_model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=groq_client)

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(model="gemini-3.5-flash", openai_client=gemini_client)