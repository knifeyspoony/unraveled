import asyncio
import logging

from dotenv import load_dotenv
from floki import Agent, AgentService

from unraveled.tools.code import execute_python_script
from unraveled.workflows.agentic.config import AZURE_OPENAI_CHAT_CLIENT

SYSTEM_PROMPT = """\
# Software Developer

## Role

You are `Dr. Zoidberg`, the `Software Developer` in the `Futurama` capture-the-flag (CTF) team.
Your team participates in CTF challenges. Many of these challenges require you to develop code to solve them - this is where you come in!
Working with your teammates to understand the requirements, you will develop code to solve challenges.

## Goal

- Develop code to solve challenges.

## Process

1. Write your code in python.
2. Test your code to ensure it works.

"""


async def main():
    logger = logging.getLogger("coder-service")
    try:
        # Define Agent
        coder_agent = Agent(
            role="Software Developer",
            tools=[execute_python_script],
            llm=AZURE_OPENAI_CHAT_CLIENT,
            system_prompt=SYSTEM_PROMPT,
        )
        # Expose Agent as a Service
        coder_service = AgentService(
            agent=coder_agent,
            message_bus_name="messagepubsub",
            agents_state_store_name="agentstatestore",
            port=8003,
            daprGrpcPort=50003,
        )
        await coder_service.start()
    except Exception:
        logger.exception("Error starting service.")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
