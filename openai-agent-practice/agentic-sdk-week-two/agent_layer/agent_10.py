

from agents import Agent
from tools_layer.tools_10 import semantic_knowledge_retrieval

# Define the persona and map the decoupled tool
knowledge_agent = Agent(
    name="Platform Architecture Specialist",
    instructions=(
        "You are an expert system architecture agent. "
        "When handling user requests regarding platform constraints or API structures, "
        "always use 'semantic_knowledge_retrieval' first to check factual reference documents."
    ),
    tools=[semantic_knowledge_retrieval]
)