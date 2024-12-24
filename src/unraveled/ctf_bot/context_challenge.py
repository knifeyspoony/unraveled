from argparse import ArgumentParser
from pathlib import Path

import httpx
from dotenv import load_dotenv

from unraveled.ctf_bot.agents.ctf_agent import CTFAgentDeps, ctf_agent

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


async def main():
    parser = ArgumentParser()
    parser.add_argument("--challenge_location", type=str, required=True)
    args = parser.parse_args()

    challenge_location = args.challenge_location

    async with httpx.AsyncClient() as client:
        deps = CTFAgentDeps(http_client=client)
        response = await ctf_agent.run(
            f"Please solve this challenge: {challenge_location}", deps=deps
        )
        print(response.data)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
