import os
import logging
from typing import Union, Dict, Any
from app.settings import BASE_DIR, get_project_settings

from langchain_openai import (
    AzureChatOpenAI,
    ChatOpenAI,
    AzureOpenAIEmbeddings,
    OpenAIEmbeddings,
)
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

ENV_PREFIX = "CODA_"

DEFAULT_API_PROVIDER = "openai"


class LlmClient:
    def __init__(self):
        settings = get_project_settings()
        api_provider = settings.api_provider

        if api_provider == "azure":
            azure_api_key = settings.azure_api_key
            azure_endpoint = settings.azure_endpoint
            azure_completion_model = settings.azure_completion_model
            azure_embedding_model = settings.azure_embedding_model

            if not azure_endpoint or not azure_api_key:
                raise ValueError(
                    "Azure API key and endpoint must be provided for Azure OpenAI."
                )

            self.llm = AzureChatOpenAI(
                openai_api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                deployment_name=azure_completion_model,
                api_version="2024-07-01-preview",
                max_tokens=4096,
            )

            self.embeddings = AzureOpenAIEmbeddings(
                api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                deployment=azure_embedding_model,
                api_version="2024-07-01-preview",
            )

            logger.info("Azure OpenAI initialized.")

        elif api_provider == "openai":
            api_key = settings.openai_api_key
            self.llm = ChatOpenAI(api_key=api_key)

            self.embeddings = OpenAIEmbeddings(api_key=api_key)

            logger.info("OpenAI initialized.")

        else:
            raise ValueError(
                f"Invalid API provider: {api_provider}. Please specify 'azure' or 'openai'."
            )

    def generate_completion(
        self, prompt: str, json_schema: Dict[str, any] = None
    ) -> Union[str, Dict[str, Any]]:
        if json_schema:
            return self.llm.with_structured_output(json_schema).invoke(prompt)
        return self.llm.invoke(prompt).content

    def generate_embedding(self, text: str) -> list[float]:
        # Generate embeddings using the configured provider
        embedding_values = self.embeddings.embed_query(text)
        return embedding_values


if __name__ == "__main__":
    llm_client = LlmClient()
    completion = llm_client.generate_completion(
        "Explain quantum computing in simple terms. Return JSON output."
    )
    print("Completion:", completion)
    embedding = llm_client.generate_embedding("Quantum computing")
    print("Embedding:", embedding)
