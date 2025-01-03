import pathlib
import subprocess
import tempfile

from floki.tool import tool
from pydantic import BaseModel


class PythonScriptOutput(BaseModel):
    stdout: str
    stderr: str
    exception: str = None


@tool
def execute_python_script(content: str) -> PythonScriptOutput:
    """
    Execute a python script and return the output.

    Args:
        content (str): The content of the script.

    Returns:
        (str): The output of the script.
    """
    try:
        file_path = pathlib.Path(tempfile.mktemp())
        file_path.write_text(content)
        result = subprocess.run(
            ["python", file_path],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
        return PythonScriptOutput(stdout=result.stdout, stderr=result.stderr)
    except subprocess.TimeoutExpired as e:
        return PythonScriptOutput(
            stdout=e.stdout, stderr=e.stderr, exception="TimeoutExpired"
        )
    except Exception as e:
        return PythonScriptOutput(
            stdout="", stderr=f"Runtime exception: {e}", exception=e.__class__.__name__
        )


__all__ = ["execute_python_script"]
