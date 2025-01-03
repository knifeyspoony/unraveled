import asyncio
import logging

from dotenv import load_dotenv
from floki import RoundRobinWorkflowService


async def main():
    logger = logging.getLogger("orchestrator-service")
    try:
        roundrobin_workflow_service = RoundRobinWorkflowService(
            name="Orchestrator",
            message_bus_name="messagepubsub",
            agents_state_store_name="agentstatestore",
            workflow_state_store_name="workflowstatestore",
            port=8001,
            daprGrpcPort=50001,
            max_iterations=10,
        )

        await roundrobin_workflow_service.start()
    except Exception:
        logger.exception("Error starting service.")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
