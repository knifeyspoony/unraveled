import os
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from unraveled.ctf_bot.agents.ctf_agent import CTFAgentDeps, ctf_agent

app = FastAPI()


class ChallengeRequest(BaseModel):
    challenge_dir: str


class ChallengeResponse(BaseModel):
    solution: str


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/solve")
async def solve_challenge(request: ChallengeRequest) -> ChallengeResponse:
    challenge_path = Path(request.challenge_dir).resolve()

    if not challenge_path.exists():
        raise HTTPException(status_code=404, detail="Challenge directory not found")

    # Change to the challenge directory
    os.chdir(challenge_path)

    async with httpx.AsyncClient() as client:
        deps = CTFAgentDeps(http_client=client)
        response = await ctf_agent.run(
            f"Please solve the challenge in the current directory: {challenge_path}",
            deps=deps,
        )
        return ChallengeResponse(solution=response.data)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
