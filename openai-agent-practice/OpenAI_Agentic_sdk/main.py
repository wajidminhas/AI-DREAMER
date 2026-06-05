
from multi_agent.multi_agents import gemini_agent 
from agents import  Runner






res = Runner.run_sync(starting_agent=gemini_agent, input="What is a list in python?")

print(res.final_output)