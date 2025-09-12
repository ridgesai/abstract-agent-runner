# Agent Environment

The agents run in a Docker image which is based off of `python:3.11-slim`. There are various packages installed which are likely to be of use to the agents. These are outlined in `/testbed/sandbox/sandbox_requirements.txt`. See `/testbed/sandbox/Dockerfile` for more information.

Here is the directory structure that an agent can expect to see. This is unified across *all* problem sets.

```
/sandbox (Current Working Directory)
    # System files for running the actual agent, not to be used
    input.json
    output.json
    AGENT_RUNNER.py

    # The actual agent source code
    agent.py

    # If include_solution (--include-solution) is set
    solution.diff



    # The repository that the agent should work in (has .git/, etc.)
    repo/
        # The contents of this directory are specific to the suite and problem
```

Here is the how the agent should be structured.

```py
def agent_main(input):
    run_id = input.get("run_id") # UUID for the current evaluation run
    problem_statement = input.get("problem_statement") # The problem statement, likely in Markdown format

    # Actual agent logic should be here, which ultimately generates a Git diff as a string

    return diff;
```

The agents can also make requests for inference and embedding.

