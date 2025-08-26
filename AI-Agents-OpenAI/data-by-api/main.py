

from agents import Runner, set_tracing_disabled, enable_verbose_stdout_logging
from my_agent.api_agent import general_agent

# enable_verbose_stdout_logging()
set_tracing_disabled(True)

result = Runner.run_sync(starting_agent=general_agent, 
                         input="give the data of user who have id 4",
                         max_turns=1)

print(result.final_output)