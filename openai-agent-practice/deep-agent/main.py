import os
from dotenv import load_dotenv
load_dotenv()
from typing import Literal
from langchain_groq import ChatGroq
from tavily import TavilyClient
from deepagents import create_deep_agent

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
# groq_model = os.environ.get("GROQ_API_KEY", model="llama-3.3-70b-versatile")
groq_api_key = os.environ["GROQ_API_KEY"]

groq_model = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature= 0
)

# def internet_search(
#     query: str,
#     max_results: int = 5,
#     topic: Literal["general", "news", "finance"] = "general",
#     include_raw_content: bool = False,
#     ):
#     """Run a web search using Tavily.

#     Args:
#         query: The search query string.
#         max_results: Maximum number of results to return.
#         topic: Search category — general, news, or finance.
#         include_raw_content: Whether to include full raw page content.
#     """
#     return tavily_client.search(
#         query,
#         max_results=max_results,
#         include_raw_content=include_raw_content,
#         topic=topic,
#     )
def internet_search(query: str):
    """Run a web search using Tavily.

    Args:
        query: The search query string.
    """
    return tavily_client.search(query, max_results=5, topic="general")
    


# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model=groq_model,
    tools=[internet_search],
    system_prompt=research_instructions,
)



result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})

# Print the agent's response
print(result["messages"][-1].content)