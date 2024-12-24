from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from unraveled.ctf_bot.agents.ctf_agent import ctf_agent

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


def main():
    parser = ArgumentParser()
    parser.add_argument("--challenge_dir", type=str, required=True)
    args = parser.parse_args()

    challenge_dir = Path(args.challenge_dir)
    if not challenge_dir.exists():
        raise ValueError(f"Challenge directory {challenge_dir} does not exist")

    response = ctf_agent.run_sync(f"Please solve this challenge: {challenge_dir}")
    print(response.data)


if __name__ == "__main__":
    main()
