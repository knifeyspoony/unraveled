import asyncio
from dataclasses import dataclass
from pathlib import Path

import httpx
from pydantic_ai import Agent, RunContext

ctf_prompt = """
You are an expert reverse engineer participating in a Capture the Flag (CTF) competition.

All you are given is the location of a challenge.

Through the use of the provided tools, you will discover the flag for the challenge.

Between usages of our tools, output your progress report, plan of action, next step, and notes in the format described.

Your goal is to finally output the flag for the challenge.
"""


@dataclass
class CTFAgentDeps:
    http_client: httpx.AsyncClient
    socket_reader: asyncio.StreamReader | None = None
    socket_writer: asyncio.StreamWriter | None = None


ctf_agent = Agent(
    "gemini-1.5-flash-latest",
    system_prompt=ctf_prompt,
    result_type=str,
)


@ctf_agent.tool
async def http_request(ctx: RunContext[CTFAgentDeps], url: str, method: str):
    """
    Make an HTTP request to the given URL with the given method

    Args:
        ctx (RunContext[CTFAgentDeps]): Agent dependencies
        url (str): The URL to request
        method (str): The HTTP method to use

    Returns:
        (str): The response body
    """
    response = await ctx.deps.http_client.request(method, url)
    response.raise_for_status()
    return response.text


@ctf_agent.tool_plain
def list_all_files(input_dir: str) -> list[str]:
    """
    List all files in the input directory

    Args:
        input_dir (str): The directory to list files from

    Returns:
        (list[str]): A list of all file paths in the input directory
    """
    return [str(path) for path in Path(input_dir).glob("**/*")]


@ctf_agent.tool_plain
def list_glob(input_dir: str, glob_pattern: str) -> list[str]:
    """
    List all files matching the glob pattern in the input directory

    Args:
        input_dir (str): The directory to list files from
        glob_pattern (str): The glob pattern to match files against

    Returns:
        (list[str]): A list of all file paths matching the glob pattern in the input directory
    """
    return [str(path) for path in Path(input_dir).glob(glob_pattern)]


@ctf_agent.tool_plain
def get_file_contents_as_str(file_path: str, encoding: str = "utf-8") -> str:
    """
    Read the contents of a file as a string

    Args:
        file_path (str): The path to the file to read
        encoding (str): The encoding to use when reading the file

    Returns:
        (str): The contents of the file as a string
    """
    return Path(file_path).read_bytes().decode(encoding)


@ctf_agent.tool_plain
def get_file_contents_as_bytes(file_path: str) -> bytes:
    """
    Read the contents of a file as bytes

    Args:
        file_path (str): The path to the file to read

    Returns:
        (bytes): The contents of the file as bytes
    """
    return Path(file_path).read_bytes()


@ctf_agent.tool
async def socket_connect(ctx: RunContext[CTFAgentDeps], host: str, port: int) -> str:
    """
    Connect to a remote socket and send/receive data

    Args:
        ctx (RunContext[CTFAgentDeps]): Agent dependencies
        host (str): The host to connect to
        port (int): The port to connect to

    Returns:
        (str): A message indicating the connection status
    """
    reader, writer = await asyncio.open_connection(host, port)
    ctx.deps.socket_reader = reader
    ctx.deps.socket_writer = writer
    return "Connected to socket"


@ctf_agent.tool
async def socket_send(ctx: RunContext[CTFAgentDeps], data: str) -> str:
    """
    Send data to the socket

    Args:
        ctx (RunContext[CTFAgentDeps]): Agent dependencies
        data (str): The data to send to the socket

    Returns:
        (str): A message indicating the data was sent
    """
    if ctx.deps.socket_writer is None:
        return "Socket writer is not connected. Must connect to a socket first."
    ctx.deps.socket_writer.write(data.encode())
    await ctx.deps.socket_writer.drain()
    return "Data sent to socket"


@ctf_agent.tool
async def socket_receive(
    ctx: RunContext[CTFAgentDeps], count: int, timeout: float = 1.0
) -> str:
    """
    Receive data from the socket

    Args:
        ctx (RunContext[CTFAgentDeps]): Agent dependencies
        count (int): The number of bytes to receive
        timeout (float): The timeout to use when receiving data

    Returns:
        (str): The data received from the socket
    """
    if ctx.deps.socket_reader is None:
        return "Socket reader is not connected. Must connect to a socket first."

    async with asyncio.timeout(timeout):
        return await ctx.deps.socket_reader.read(count)


__all__ = ["ctf_agent"]
