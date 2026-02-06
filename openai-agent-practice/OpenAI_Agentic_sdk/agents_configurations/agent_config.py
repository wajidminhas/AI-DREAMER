
from decouple import config
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

GEMINI_API_KEY = config("GEMINI_API_KEY")
BASE_URL = config("BASE_URL", default="https://generativelanguage.googleapis.com/v1beta/openai/")


gemini_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

MODEL = OpenAIChatCompletionsModel(
    openai_client=gemini_client, model="gemini-2.5-flash"
)
