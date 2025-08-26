
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from decouple import config


gemmini_api_key = config("GEMINI_API_KEY")
gemini_base_url = config("GEMINI_BASE_URL")



gemini_client = AsyncOpenAI(
    api_key=gemmini_api_key,
    base_url=gemini_base_url

)

gemini_model = OpenAIChatCompletionsModel(
    openai_client=gemini_client,
    model='gemini-2.5-flash'
)