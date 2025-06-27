
import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, function_tool, AsyncOpenAI, Runner, RunContextWrapper, enable_verbose_stdout_logging
from agents.run import RunConfig
from pydantic import BaseModel
from typing import ClassVar
from dataclasses import dataclass


load_dotenv()
@dataclass
class Person:
    name : str
    age : int
    national : str


gemini_api_key = os.getenv("GEMINI_API_KEY")

@function_tool
async def employe(wrapper : RunContextWrapper[Person]) -> str:
    """
    Retrieves and formats the name and age details of a person from the context.

    and greet the user with their name and age.
    if the user is not provided, it will return a default message.
    and if user age is above 20 call him with "Mr." otherwise call him with "Youngster".
    This function is designed to be used as a tool in an agent's workflow.
    It uses the RunContextWrapper to access the context and retrieve the person's details.
    if user login the asked him name and age
    """
    print("DEBUG: employe tool was called.") # Debugging print
    # Corrected: return the string, not await it
    # return f"Person Detail: User {wrapper.context.name} with age {wrapper.context.age}"
    if wrapper.context.age > 20:
        print("DEBUG: User is above 20 years old.") # Debugging print
        return f"Mr. {wrapper.context.name} is {wrapper.context.age} years old."
    else:
        print("DEBUG: User is 20 years old or younger.")
        return f"Youngster {wrapper.context.name} is {wrapper.context.age} years old."
    # return f"Person Detail: User {wrapper.context.name} with age {wrapper.context.age}"

@function_tool
async def employee_location(wrapper : RunContextWrapper[Person]) -> str:
    """
    Retrieves and formats the nationality detail of a person from the context.
    This function is designed to be used as a tool in an agent's workflow.
    if user is from any islamic country the greet him with "Assalam o Alaikum" otherwise greet him with "Hello"
    """
    print("DEBUG: employee_location tool was called.") # Debugging print
    if wrapper.context.national.lower() in ["pakistan", "saudi arabia", "egypt", "turkey"]:
        print("DEBUG: User is from an Islamic country.")
        return f"Assalam o Alaikum, User with detail {wrapper.context.name} belongs to {wrapper.context.national}"
    else:
        print("DEBUG: User is not from an Islamic country.")
        return f"Hello, User with detail {wrapper.context.name} belongs to {wrapper.context.national}"
    # Corrected: return the string, not await it
    # return f"User with detail {wrapper.context.name} belongs to {wrapper.context.national}"

async def main():

    personal_info = Person(name="wajid minhas", age=24, national="Pakistan")
    provider = AsyncOpenAI(
        api_key = gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    
    model = OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gemini-2.0-flash",
    )

    person_agent : Agent = Agent(
        name = "Person Agent",
        model=model,
        # instructions="you are a person agent that provide personal information of user",
        output_type=str,
        tools=[employe, employee_location],
        handoff_description= "You are a person agent that provide personal information of user.",
    )

    triage_agent : Agent = Agent(
        name = "Triage Agent",
        model=model,
        # instructions="you are a triage agent that classifies the type of request and assigns it to the appropriate agent or tool call",
        output_type=str,
        # tools=[employe, employee_location]
        handoffs=[person_agent],
        handoff_description= "You are a triage agent that classifies the type of request and assigns it to the appropriate agent or tool call. If the request is about personal information, hand it off to the person agent.",
        # handoff_condition=lambda response: "personal information" in response.content.lower()
    )

    config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )

    result = await Runner.run(triage_agent, 
                                    "hi, wajid from pakistan",
                                    context=personal_info,
                                    run_config=config)
    
    # result = await Runner.run(triage_agent, 
    #                           "give detail of person who belong pakistan",
    #                         #   run_config=config,
    #                           context=personal_info,
    #                           max_turns=2
                              
                            #   )
    
    # print(f"\nFinal Output\n")
    # print(result.final_output.content)
    print(result.new_items)
    # print(f"\n\n Raw Responses:\n")
    # print(result.raw_responses)

    
    # print(f"\n\n Raw Responses output:\n")
    # print(result.raw_responses.__format__( dict=True))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())