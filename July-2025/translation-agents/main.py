from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent


gemini_api_key = os.getenv("GEMINI_API_KEY")

base_url = os.getenv("BASE_URL")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")


external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= base_url
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model_name="gemini-1.5-flash",
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
)


synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
)


async def main():
    # create input message 
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
