

from agents import Runner
from agent_layer.agent_10 import knowledge_agent
from configuration_layer.db_config import init_vector_db

def run_day_10_pipeline(prompt: str):
    print("\n--- Day 10 Setup Lifecycle ---")
    # Verify vector table architectures are in place before execution
    init_vector_db()
    
    print(f"\nExecuting Runtime Loop for Prompt: '{prompt}'")
    result = Runner.run(
        agent=knowledge_agent,
        input=prompt
    )
    
    return result.final_output