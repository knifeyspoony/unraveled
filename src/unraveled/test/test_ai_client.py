import os

import openai
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion

load_dotenv()


def test_ai_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    assert api_key, "API key is required."

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    assert azure_endpoint, "Azure endpoint is required."

    client = openai.AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        azure_deployment="gpt-4o-mini",
        api_version="2024-10-01-preview",
    )
    response: ChatCompletion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a comedian."},
            {"role": "user", "content": "Tell me a joke."},
        ],
        model="gpt-4o-mini",
    )
    assert response, "Response is required."
    assert response.choices, "Choices are required."
    assert response.choices[0].message, "Text is required."
