import chromadb
from chromadb.config import Settings
from typing import List
import logging
import os

from app.llm_client import LlmClient
from app.settings import BASE_DIR

logger = logging.getLogger(__name__)


class ContextStorage:
    def __init__(
        self,
        llm_client: LlmClient,
        persist_directory=os.path.join(BASE_DIR, "db"),
    ):
        self.llm_client = llm_client
        self.client = chromadb.PersistentClient(
            path=persist_directory, settings=Settings(allow_reset=True)
        )
        self.files_collection = self.client.get_or_create_collection(
            name="files_collection"
        )

    def store_file(self, file_path: str, content: str) -> None:
        vector = self.llm_client.generate_embedding(content)
        self.files_collection.add(
            documents=[file_path],
            embeddings=[vector],
            metadatas=[{"file_path": file_path}],
            ids=[file_path],
        )

    def get_similar_files(self, prompt: str, n: int = 5) -> List[str]:
        prompt_vector = self.llm_client.generate_embedding(prompt)
        results = self.files_collection.query(
            query_embeddings=[prompt_vector], n_results=n
        )
        return [metadata["file_path"] for metadata in results["metadatas"][0]]

    def is_empty(self) -> bool:
        return self.files_collection.count() == 0

    def reset(self) -> None:
        self.client.delete_collection(name="files_collection")
        self.files_collection = self.client.get_or_create_collection(
            name="files_collection"
        )


if __name__ == "__main__":
    llm_client = LlmClient()
    context_db = ContextStorage(llm_client=llm_client)

    context_db.store_file(
        file_path="example.txt", content="This is an example content."
    )

    similar_files = context_db.get_similar_files(prompt="example prompt")
    logger.info(similar_files)

    logger.info(f"Is the database empty? {context_db.is_empty()}")
