
from multi_agent.multi_agents import agent
from agents import  Runner






res = Runner.run_sync(starting_agent=agent, input="What is a list in python?, just give me a simple example")

print(res.final_output)