
import asyncio
import os
from dotenv import load_dotenv
import chainlit as cl
from chainlit.types import AskFileResponse
from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionModel, RunConfig
from openai import OpenAI
import google.generativeai as genai


#load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini API client
external_client = AsyncOpenAI(api_key=gemini_api_key,
                              base_url="https://generativelanguage.googleapis.com",)

model = OpenAIChatCompletionModel(
    model="gemini-1.5-flash",
    client=external_client,
)

sheff = Agent(
    name="Sheff",
    model=model,
    description="A helpful sheff assistant about pakistani food and recipes so you would answer questions and provide information.",)

config = RunConfig(
    model=model,
    default_client=external_client,
    set_tracing_disabled=True
)


@cl.on_message
async def handle_message(message : cl.Message):
    """
    Handle incoming messages from Chainlit.
    """
    if message.content:
        response = await Runner.run_sync(
            sheff,
            message.content,
            config=config
        )
        await cl.Message(content=response).send()