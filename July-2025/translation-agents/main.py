from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, trace, enable_verbose_stdout_logging, Runner, ItemHelpers, MessageOutputItem, RunConfig, set_tracing_disabled

set_tracing_disabled(True)  # Disable tracing for this example
enable_verbose_stdout_logging()
load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 🔑 Get your API key from environment
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# base_url = os.getenv("BASE_URL")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set in the environment variables.")


external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash",
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
    model=model,
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
    model=model,
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
    model=model,
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    model=model,
   
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
    model=model,
)
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     # tracing_disabled=True
# )

async def main():
    # create input message 
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator Evaluator"):
        orchestrator_result = await Runner.run(
            orchestrator_agent,
            msg
        )
        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"  - Translation step : {text}")

        synthesizer_result = await Runner.run(
            synthesizer_agent,
            orchestrator_result.to_input_list()
        )

    print(f"\n\nFinal Result: \n{synthesizer_result.final_output}")

# # async def main():
# #     msg = input("Hi! What would you like translated, and to which languages? ")

# #     # Run the entire orchestration in a single trace
# #     with trace("Orchestrator evaluator"):
# #         orchestrator_result = await Runner.run(orchestrator_agent, msg)

# #         for item in orchestrator_result.new_items:
# #             if isinstance(item, MessageOutputItem):
# #                 text = ItemHelpers.text_message_output(item)
# #                 if text:
# #                     print(f"  - Translation step: {text}")

# #         synthesizer_result = await Runner.run(
# #             synthesizer_agent, orchestrator_result.to_input_list()
# #         ),
# #     config= config

# #     print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


# # if __name__ == "__main__":
# #     import asyncio
# #     asyncio.run(main())

# result = Runner.run_sync(
#     orchestrator_agent,
#     "hello meaning in spanish",
#     # config=RunConfig(model=model, model_provider=external_client)
# )
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
