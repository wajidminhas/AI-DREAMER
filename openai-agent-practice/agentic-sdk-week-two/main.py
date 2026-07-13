


import sys
from runner_layer.runner_10 import run_day_10_pipeline

def main():
    # Simple explicit testing query
    sample_prompt = "What are the configuration specifications for our endpoint routers?"
    
    response = run_day_10_pipeline(prompt=sample_prompt)
    
    print("\n=== Final Response from System ===")
    print(response)

if __name__ == "__main__":
    main()