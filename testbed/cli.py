"""Agent runner CLI for problem suite benchmarks."""

import os
import sys
import time

from utils.logger import info, warn, error, debug
from sandbox.sandbox_manager import SandboxManager
from problem_suites.polyglot.polyglot_suite import PolyglotSuite
from problem_suites.swebench_verified.swebench_verified_suite import SWEBenchVerifiedSuite


def run_agent_on_problem(suite_name, problem_name, agent_file):
    suite_configs = {
        "polyglot": {
            "class": PolyglotSuite,
            "path": "../problem_suites/polyglot"
        },
        "swebench_verified": {
            "class": SWEBenchVerifiedSuite,
            "path": "../problem_suites/swebench_verified"
        }
    }
    
    if suite_name not in suite_configs:
        error(f"Unknown suite: {suite_name}. Available suites: {list(suite_configs.keys())}")
        return 1

    config = suite_configs[suite_name]
    suite = config["class"](config["path"])
    
    test_count = suite.get_problem_test_count(problem_name)
    if test_count > 150:
        error(f"Problem {problem_name} has {test_count} tests (>150)")
        return 1
    
    info(f"Problem {problem_name} has {test_count} tests")
    
    sandbox_manager = SandboxManager()

    with open(agent_file, "r") as f:
        agent_source_code = f.read()

    

    def on_finish(result):
        print()
        print()
        print()

        if (result["status"] == "success"):
            n = len(result.get("diff", "").splitlines())
            print(f"========== DIFF ({n} line{'s' if n != 1 else ''}) ==========")
            print(result.get("diff", ""))

            n = len(result.get("logs", "").splitlines())
            print(f"========== LOGS ({n} line{'s' if n != 1 else ''}) ==========")
            # print(result.get("logs", ""))

            print()
            print()
            print()
            
            diff = result["diff"]
            
            def on_finish(result):
                print()
                print()
                print()

                if result["status"] == "success":
                    print("========== TEST RESULTS ==========")
                    test_results = result.get("test_results", [])
                    tests_passed = sum(1 for test in test_results if test["status"] == "pass")
                    tests_failed = sum(1 for test in test_results if test["status"] == "fail")
                    tests_skipped = sum(1 for test in test_results if test["status"] == "skip")
                    print(f"{tests_passed} passed, {tests_failed} failed, {tests_skipped} skipped")

                    n = len(result.get("logs", "").splitlines())
                    print(f"========== LOGS ({n} line{'s' if n != 1 else ''}) ==========")
                    # print(result["logs"])
                else:
                    print("========== ERROR ==========")
                    print(result.get("error", ""))
                    
                    print("========== TRACEBACK ==========")
                    print(result.get("traceback", ""))

                    print("========== LOGS ==========")
                    print(result.get("logs", ""))

                print()
                print()
                print()
            
            suite.evaluate_solution_diff(sandbox_manager, problem_name, diff, on_finish)
        else:
            print("========== ERROR ==========")
            print(result.get("error", ""))

            print("========== TRACEBACK ==========")
            print(result.get("traceback", ""))

            print("========== DIFF ==========")
            print(result.get("diff", ""))

            print("========== LOGS ==========")
            print(result.get("logs", ""))
    


    suite.run_agent_in_sandbox_for_problem(sandbox_manager, problem_name, agent_source_code, on_finish)
    


    time.sleep(5)
    while sandbox_manager.get_num_sandboxes() > 0:
        time.sleep(1)
    


    return 0



def main():
    if len(sys.argv) != 4:
        print("Usage: python cli.py <suite_name> <problem_name> <agent_file>")
        print()
        print("Available suites: polyglot, swebench_verified")
        print()
        print("Examples:")
        print("  python cli.py polyglot affine-cipher my_agent.py")
        print("  python cli.py swebench_verified django__django-12308 my_agent.py")
        return 1
    
    suite_name = sys.argv[1]
    problem_name = sys.argv[2] 
    agent_file = sys.argv[3]
    
    return run_agent_on_problem(suite_name, problem_name, agent_file)



if __name__ == "__main__":
    sys.exit(main())