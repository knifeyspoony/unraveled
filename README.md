# unraveled

this is a simple CTF bot project using pydantic-ai and gemini-1.5-flash to solve challenges.

## plans

- incorporate reverse engineering capabilities into the agent using ghidra.
- rop chain generation, shellcode generation, etc.
- when streaming for gemini is fixed in pydantic-ai, stream everything including the tool calls and tool outputs.

## setup

1. clone
2. if you don't have `uv`, install it with `pip install uv`
3. in the repo dir, run `uv sync`
4. create a `.env` file in the root of the repo with the following:

```bash
GEMINI_API_KEY=<your-gemini-api-key>
```

5. run the agent with `uv run src/unraveled/ctf_bot/context_challenge.py --challenge_location <dir/socket/uri>`
