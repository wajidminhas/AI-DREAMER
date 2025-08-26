

from agents import Runner, set_tracing_disabled
from my_agent.api_agent import gen_agent


set_tracing_disabled(True)

result = Runner.run_sync(starting_agent=gen_agent, input="give the data of user who have id 4")

print(result.final_output)