import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, RunContextWrapper, function_tool
from agents.run import RunConfig
from pydantic import BaseModel


# enable_verbose_stdout_logging()
# Load the environment variables from the .env file
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

class User(BaseModel):
    name: str
    age: int
    city: str


#Reference: https://ai.google.dev/gemini-api/docs/openai
def get_ai_prompt(ctx : RunContextWrapper[User], agent : Agent[User]) -> str:
    """
    This function generates a prompt for the AI agent based on the context and agent information.
    It includes the user's name, age, city, and the context of the conversation.
    """
    print("\n[CONTEXT]" , ctx.context)
    print(f"\n[AGENT]" , agent)
    user_context = User(name=ctx.context.name, age=ctx.context.age, city=ctx.context.city)
    print(f"\n[USER CONTEXT] {user_context}")
    user_info = ctx.context
    user_name = user_info.name
    user_age = user_info.age
    user_city = user_info.city
    print(f"User Info: Name={user_name}, Age={user_age}, City={user_city}")
    print(f"\n[AGENT NAME] {agent.name}")
    print(f"\n[AGENT INSTRUCTIONS] {agent.instructions}")
    # print(f"\n[AGENT MODEL] {agent.model}")

    return f"you are a helpfull assistent and reply user query, {user_context} " \
    

# @function_tool()


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

agent: Agent = Agent(name="Assistant", 
                     instructions=get_ai_prompt
                     )

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config, context=User(name="John", age=30, city="New York"))

# print("\nCALLING AGENT\n")
print(result.final_output)