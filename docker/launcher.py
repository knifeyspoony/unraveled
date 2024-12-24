import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from unraveled.container.service import ChallengeRequest, ChallengeResponse

# Load environment variables
LOCAL_DIR = Path(__file__).parent
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH)


def main():
    parser = argparse.ArgumentParser(
        description="Launch CTF agent container with a challenge directory"
    )
    parser.add_argument(
        "--challenge-dir", "-c", type=str, help="Path to the challenge directory"
    )
    args = parser.parse_args()

    prev_dir = os.getcwd()

    try:
        # Resolve the challenge directory path
        challenge_dir = Path(args.challenge_dir).resolve()
        if not challenge_dir.exists():
            print(
                f"Error: Challenge directory '{challenge_dir}' does not exist",
                file=sys.stderr,
            )
            sys.exit(1)

        # Change to the local directory
        os.chdir(LOCAL_DIR)
        os.environ["CHALLENGE_DIR"] = str(challenge_dir)

        # Construct the docker compose command
        cmd = [
            "docker-compose",
            "up",
            "--build",  # Always build to ensure latest code
            "--detach",
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running docker compose: {e}", file=sys.stderr)
            sys.exit(1)

        # Wait for the container to be ready
        while True:
            try:
                response = requests.get("http://localhost:8000/health")
                if response.status_code == 200:
                    print("Container is ready!")
                    break
            except Exception:
                pass
            time.sleep(1)

        # Send a request to the API to solve the challenge
        response = requests.post(
            "http://localhost:8000/solve",
            json=ChallengeRequest(challenge_dir="/challenge").model_dump(),
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.text}")
        challenge_response = ChallengeResponse.model_validate(response.json())
        print(challenge_response.solution)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Shutting down...")
        subprocess.run(
            [
                "docker-compose",
                "down",
            ],
            check=True,
        )

        os.chdir(prev_dir)


if __name__ == "__main__":
    main()
