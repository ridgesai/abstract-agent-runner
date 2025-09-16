# Abstract Agent Runner

<br>

## Introduction

Abstract Agent Runner is a comprehensive testing framework designed to evaluate AI coding agents against standardized programming challenges. The system provides a sandboxed environment where agents can attempt to solve problems from well-established benchmark suites, including Polyglot programming challenges and SWE-Bench Verified real-world software engineering tasks.

The framework isolates agent execution in Docker containers, ensuring safe and reproducible testing while providing agents with access to complete development environments. It supports multiple problem domains, from algorithmic puzzles to complex software maintenance tasks, making it an ideal tool for researchers and developers working on automated code generation and program synthesis.

<br>



## Requirements

- **Docker**: Required for creating isolated sandbox environments
- **Python 3.11+**: For running the testbed framework
- **UV**: Python package manager for virtual environment management
- **Node.js**: For fetching SWE-Bench datasets
- **Git**: Required for repository operations and dataset management

<br>



## Setup

### Creating Virtual Environment with UV

First, create and activate a virtual environment using UV:

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate
```



## Usage

The framework is controlled through the CLI located in the root directory. The basic usage pattern is:

```bash
python cli.py <suite_name> <problem_name> <agent_file> <gateway_url>
```

### Examples

**Running an agent on a Polyglot problem:**
```bash
python cli.py polyglot affine-cipher test_agent.py http://localhost:8000
```

**Running an agent on a SWE-Bench problem:**
```bash
python cli.py swebench_verified django__django-12308 test_agent.py http://localhost:8000
```

**Available suites:**
- `polyglot`: Algorithmic programming challenges
- `swebench_verified`: Real-world software engineering tasks

**Optional flags:**
- `--log-docker-to-stdout`: Print Docker container logs to stdout in real-time
- `--include-solution`: Expose the solution to the agent at `/sandbox/solution.diff`
- `--verbose`: Enable verbose (debug) logging

**Examples with flags:**
```bash
python cli.py polyglot affine-cipher test_agent.py --include-solution --log-docker-to-stdout --verbose
```

### Agent Implementation

See `docs/agent_environment.md` for a description of how agents should look like and what their environment exposes.

<br>



## Limitations

The Polyglot suite is complete.

The SWE-Bench Verified suite currently only works correctly with `django` problems. A custom test runner will have to be provided for the remaining 11 repositories, see `problem_suites/swebench_verified/TEST_RUNNER.py`.

A watchdog has yet to be added to ensure that agent executions and test evaluations do not run indefinitely.

The inference proxy server has stub endpoints that need to be extended to actually proxy inference requests.