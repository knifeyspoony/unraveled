import os

from dotenv import load_dotenv
from floki.llm import OpenAIChatClient

load_dotenv()

AZURE_OPENAI_CHAT_CLIENT = OpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment="gpt-4o-mini",
    api_version="2024-10-01-preview",
)

__all__ = ["AZURE_OPENAI_CHAT_CLIENT"]
