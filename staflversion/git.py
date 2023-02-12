"""
staflversion base module.

This is the principal module of the staflversion project.
here you put your main classes and objects.
"""

import subprocess

from typing import List, Optional

class GitRunResult:

    def __init__(self, stdout: str, stderr: str, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def raise_on_error(self) -> 'GitRunResult':
        if self.exit_code != 0:
            raise RuntimeError(self)
        return self

class GitWrapper:

    def __init__(self, working_directory: Optional[str]):
        self.working_directory = working_directory

    def get_tags(self) -> List[str]:
        tag_result = self._run("tag").raise_on_error()
        return tag_result.stdout.splitlines()

    def get_head_commit_message(self) -> str:
        return self._run("log", "-1", "--format=%s").raise_on_error().stdout.strip()


    def _run(self, *args: str) -> GitRunResult:
        git_args = ["git"]
        git_args.extend(args)

        result = subprocess.run(git_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.working_directory)
        return GitRunResult(result.stdout.decode(), result.stderr.decode(), result.returncode)


