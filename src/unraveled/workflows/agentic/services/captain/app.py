import asyncio
import logging

from dotenv import load_dotenv
from floki import Agent, AgentService

from unraveled.workflows.agentic.config import AZURE_OPENAI_CHAT_CLIENT

SYSTEM_PROMPT = """\
# CTF Team Captain

## Role

You are `Zap Brannigan`, the `Team Captain` in the `Futurama` capture-the-flag (CTF) team.

## Goal

Lead your team to victory by solving the CTF challenge.

## Process

1. Based on the challenge instructions, work with your team to develop a strategy and solve the challenge!

## Team Members

- `Zap Brannigan (this is you!)` - Team Captain
- `Kip` - Socket Communications Expert
- `Dr. Zoidberg` - Software Developer

"""


async def main():
    logger = logging.getLogger("captain-service")
    try:
        # Define Agent
        captain_agent = Agent(
            role="Team Captain",
            system_prompt=SYSTEM_PROMPT,
            llm=AZURE_OPENAI_CHAT_CLIENT,
        )
        print(f"Role: {captain_agent.role}\nName: {captain_agent.name}")
        # Expose Agent as a Service
        captain_service = AgentService(
            agent=captain_agent,
            message_bus_name="messagepubsub",
            agents_state_store_name="agentstatestore",
            port=8002,
            daprGrpcPort=50002,
        )
        await captain_service.start()
    except Exception:
        logger.exception("Error starting service.")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
