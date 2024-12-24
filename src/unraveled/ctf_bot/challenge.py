from argparse import ArgumentParser
from pathlib import Path

import httpx
from dotenv import load_dotenv

from unraveled.ctf_bot.agents.ctf_agent import CTFAgentDeps, ctf_agent

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


async def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--challenge_dir",
        type=str,
        required=True,
        help="The directory containing the challenge.",
    )
    args = parser.parse_args()

    challenge_dir = Path(args.challenge_location)
    if not challenge_dir.exists():
        raise FileNotFoundError(f"Challenge location {challenge_dir} does not exist")

    async with httpx.AsyncClient() as client:
        deps = CTFAgentDeps(http_client=client)
        response = await ctf_agent.run(
            f"Please solve this challenge: {challenge_dir}", deps=deps
        )
        print(response.data)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
