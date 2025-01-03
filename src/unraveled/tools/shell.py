import shlex
import subprocess

from floki.tool import tool
from pydantic import BaseModel


class ShellOutput(BaseModel):
    stdout: str
    stderr: str


@tool
def execute_shell_command(command: str) -> ShellOutput:
    """
    Execute a shell command and return the output.

    Args:
        command (str): The shell command to execute.

    Returns:
        ShellOutput: The output of the shell command.
    """

    args = shlex.split(command)
    result = subprocess.run(
        args=args,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return ShellOutput(stdout=result.stdout, stderr=result.stderr)
