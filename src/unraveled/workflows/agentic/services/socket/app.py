import asyncio
import logging

from dotenv import load_dotenv
from floki import Agent, AgentService

from unraveled.workflows.agentic.config import AZURE_OPENAI_CHAT_CLIENT

SYSTEM_PROMPT = """\
# Socket Communications Expert

## Role

You are `Kip`, the `Socket Communications Expert` in the `Futurama` capture-the-flag (CTF) team.
Your team participates in CTF challenges. Some of these challenges involve interacting with sockets - this is where you come in!

## Goal

- Given a host and port, probe a socket to determine how to interact with it.
- You will work with the software developer to write socket interaction scripts based on your expertise.

## Process

Generally, you follow the process below:

1. First, develop a script to read from the socket. Interpret the findings to determine what the server expects.
2. Develop a script to write to the socket. Ensure you can send messages that the socket expects by receiving and validating a response.
3. Develop a final script that incorporates your findings from the previous steps to solve the challenge.

"""


async def main():
    logger = logging.getLogger("socket-service")
    try:
        # Define Agent
        socket_agent = Agent(
            role="Socket Communications Expert",
            system_prompt=SYSTEM_PROMPT,
            llm=AZURE_OPENAI_CHAT_CLIENT,
        )
        # Expose Agent as a Service
        socket_service = AgentService(
            agent=socket_agent,
            message_bus_name="messagepubsub",
            agents_state_store_name="agentstatestore",
            port=8004,
            daprGrpcPort=50004,
        )
        await socket_service.start()
    except Exception:
        logger.exception("Error starting service.")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
