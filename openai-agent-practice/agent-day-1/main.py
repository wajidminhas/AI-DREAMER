
from agents import Runner

# from runner_layer.runner_1 import result
from agent_layer.agent_1 import shop_agent

res = Runner.run_sync(
    starting_agent=shop_agent,
    input="Find me a laptop and check its price"
)

print("Final Result:", res.final_output)
