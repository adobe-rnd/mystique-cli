import os
from typing import Union, List, Dict, Any

from langchain_openai import (
    AzureChatOpenAI,
    ChatOpenAI,
    AzureOpenAIEmbeddings,
    OpenAIEmbeddings,
)
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

ENV_PREFIX = "MYSTIQUE_"

DEFAULT_API_PROVIDER = "openai"


def get_env_var(var_name: str, default_value: str = None) -> str:
    prefixed_var_name = f"{ENV_PREFIX}{var_name}"
    return os.getenv(prefixed_var_name) or os.getenv(var_name, default_value)


api_key = get_env_var("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key must be provided.")


class LlmClient:
    def __init__(self):
        api_provider = get_env_var("AZURE_OR_OPENAI", DEFAULT_API_PROVIDER).lower()

        if api_provider == "azure":
            azure_api_key = get_env_var("AZURE_API_KEY")
            azure_endpoint = get_env_var("AZURE_ENDPOINT")
            azure_completion_deployment = get_env_var("AZURE_COMPLETION_DEPLOYMENT")
            azure_embedding_deployment = get_env_var("AZURE_EMBEDDING_DEPLOYMENT")

            if not azure_endpoint or not azure_api_key:
                raise ValueError(
                    "Azure API key and endpoint must be provided for Azure OpenAI."
                )

            self.llm = AzureChatOpenAI(
                openai_api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                deployment_name=azure_completion_deployment,
                api_version="2024-07-01-preview",
                max_tokens=4096,
            )

            self.embeddings = AzureOpenAIEmbeddings(
                api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                deployment=azure_embedding_deployment,
                api_version="2024-07-01-preview",
            )

            print("Azure OpenAI initialized.")

        elif api_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            self.llm = ChatOpenAI(api_key=api_key)

            self.embeddings = OpenAIEmbeddings(api_key=api_key)

            print("OpenAI initialized.")

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
