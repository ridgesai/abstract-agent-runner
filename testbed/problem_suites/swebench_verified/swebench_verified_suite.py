"""The SWE-Bench Verified problem suite."""

import os
import json
import shutil

from utils.diff import apply_diff
from utils.logger import debug, info, warn, error
from problem_suites.problem_suite import ProblemSuite
from utils.git import clone_repo_at_commit, verify_commit_exists



class SWEBenchVerifiedSuite(ProblemSuite):
    def __init__(self, problem_suite_path):
        super().__init__(problem_suite_path)



    def load_problems(self, problem_suite_path):
        """Load problems from swebench_verified.json and verify directory structure."""

        if not os.path.exists(problem_suite_path):
            error(f"[SWEBENCH] Problem suite directory not found: {problem_suite_path}")
            raise FileNotFoundError(f"Problem suite directory not found: {problem_suite_path}")
            
        json_path = os.path.join(problem_suite_path, "swebench_verified.json")
        if not os.path.exists(json_path):
            error(f"[SWEBENCH] swebench_verified.json not found at: {json_path}")
            raise FileNotFoundError(f"swebench_verified.json not found at: {json_path}")
            
        try:
            with open(json_path, "r") as f:
                problems_list = json.load(f)
            
            info(f"[SWEBENCH] Loaded {len(problems_list)} problems from {json_path}")
            
            # Count unique repositories
            unique_repos = set()
            for problem in problems_list:
                repo = problem.get("repo")
                if repo:
                    unique_repos.add(repo)
            
            debug(f"[SWEBENCH] Found {len(unique_repos)} unique repositories")
            
            # Check that all repositories exist in the repos/ directory
            repos_dir = os.path.join(problem_suite_path, "repos")
            if not os.path.exists(repos_dir):
                error(f"[SWEBENCH] repos/ directory not found at: {repos_dir}")
                raise FileNotFoundError(f"repos/ directory not found at: {repos_dir}")
            
            missing_repos = []
            for repo in unique_repos:
                # Convert repository format from "owner/name" to directory name format "owner_name"
                repo_dir_name = repo.replace("/", "_")
                repo_path = os.path.join(repos_dir, repo_dir_name)
                if not os.path.exists(repo_path):
                    missing_repos.append(repo)
            
            if missing_repos:
                error(f"[SWEBENCH] Missing repositories in repos/ directory: {missing_repos}")
                raise FileNotFoundError(f"Missing repositories in repos/ directory: {missing_repos}")
            
            debug(f"[SWEBENCH] All {len(unique_repos)} repositories found in repos/ directory")
            
            # Process each problem
            for problem in problems_list:
                instance_id = problem.get("instance_id")
                
                repo = problem.get("repo")
                base_commit = problem.get("base_commit")
                
                # # Verify commit exists in repository
                # repo_dir_name = repo.replace("/", "_")
                # repo_path = os.path.join(repos_dir, repo_dir_name)
                
                # if not verify_commit_exists(repo_path, base_commit):
                #     error(f"[SWEBENCH] Problem {instance_id}: commit {base_commit} not found in repository {repo}")
                #     raise ValueError(f"Problem {instance_id}: commit {base_commit} not found in repository {repo}")
                
                # debug(f"[SWEBENCH] Verified commit {base_commit} exists in {repo} for problem {instance_id}")
                
                self._add_problem(
                    instance_id, 
                    problem_statement=problem.get("problem_statement"), 
                    solution_diff=problem.get("patch"), 
                    tests={
                        "pass_to_pass": json.loads(problem.get("PASS_TO_PASS")),
                        "fail_to_pass": json.loads(problem.get("FAIL_TO_PASS"))
                    },
                    extra={
                        "repo": repo,
                        "base_commit": base_commit,
                        "test_patch": problem.get("test_patch")
                    }
                )
            
            info(f"[SWEBENCH] Successfully loaded {len(self.problems)} problems")
            
        except Exception as e:
            error(f"[SWEBENCH] Failed to load problems: {e}")
            raise e



    def copy_problem_files_to_directory(self, problem_name, dir, *, include_tests=False, include_solution=False):
        """Copy problem files to the given directory."""
        
        problem = self.get_problem(problem_name)
        if not problem:
            error(f"[SWEBENCH] Problem {problem_name} not found")
            raise ValueError(f"Problem {problem_name} not found")

        # Get repository and commit information from metadata
        repo = problem.get("repo")
        base_commit = problem.get("base_commit")

        # Convert repository format from "owner/name" to directory name format "owner_name"
        repo_dir_name = repo.replace("/", "_")
        repo_path = os.path.join(self.problem_suite_path, "repos", repo_dir_name)
        
        # Clone the appropriate repository at the specific commit that the problem requires
        debug(f"[SWEBENCH] Cloning {repo} at commit {base_commit} to {dir} for {problem_name}")
        success, error_msg = clone_repo_at_commit(repo_path, base_commit, dir)
        if not success:
            error(f"[SWEBENCH] Failed to clone repository for {problem_name}: {error_msg}")
            raise RuntimeError(f"Failed to clone repository for {problem_name}: {error_msg}")
        debug(f"[SWEBENCH] Successfully copied repository files for {problem_name}")

        # Copy test files if requested
        if include_tests:
            test_patch = problem.get("test_patch")
            debug(f"[SWEBENCH] Applying test patch for {problem_name}")
            success, error_msg = apply_diff(test_patch, dir)
            if not success:
                error(f"[SWEBENCH] Failed to apply test patch for {problem_name}: {error_msg}")
                raise RuntimeError(f"Failed to apply test patch for {problem_name}: {error_msg}")
            debug(f"[SWEBENCH] Successfully applied test patch for {problem_name}")
        
        # Copy solution files if requested
        if include_solution:
            # Write solution.diff file
            with open(os.path.join(dir, "solution.diff"), "w") as f:
                f.write(problem["solution_diff"])
            debug(f"[SWEBENCH] Created solution.diff in {dir} for {problem_name}")



    def get_test_runner_path(self):
        return os.path.join(os.path.dirname(__file__), "TEST_RUNNER.py")

    def get_problem_test_count(self, problem_name):
        problem = self.get_problem(problem_name)
        if not problem:
            return 0
        
        tests = problem.get("tests", {})
        pass_to_pass = tests.get("pass_to_pass")
        fail_to_pass = tests.get("fail_to_pass")
        
        return len(pass_to_pass) + len(fail_to_pass)