
from agents import Runner
from agent_layer.agent_4 import memory_agent
# import sys
# print(sys.path)  # see where Python is looking

# from agent_layer.agent_1 import agent


# result = Runner.run_sync(starting_agent=agent, input="Hello, what about agentic ai, describe yourself?")
# print(result.final_output)

MAX_HISTORY = 20

async def run_conversation():

    
    
    while True:
        history = []
        user_input = input("User:").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting conversation.")
            break
        history.append({"role": "user", "content": user_input})
        
        if len(history) > MAX_HISTORY:
            history = history[-MAX_HISTORY:]
        
        result = await Runner.run(
            starting_agent=memory_agent,
            input=history
        )
        
        response = result.final_output
        print(f"\nAgent: {response}\n")
        
        history.append({"role": "assistant", "content": response})

        