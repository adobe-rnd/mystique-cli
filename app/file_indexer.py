import os
from concurrent.futures import ThreadPoolExecutor
import pathspec


class FileIndexer:
    def __init__(
        self, project_directory: str, llm_client, context_db, max_workers: int = 10
    ):
        self.project_directory = project_directory
        self.llm_client = llm_client
        self.context_db = context_db
        self.max_workers = max_workers
        self.ignore_spec = self._load_gitignore()

    def _load_gitignore(self):
        gitignore_path = os.path.join(self.project_directory, ".gitignore")
        if not os.path.exists(gitignore_path):
            return None

        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()
        return pathspec.PathSpec.from_lines(
            "gitwildmatch", gitignore_content.splitlines()
        )

    def _is_ignored(self, file_path):
        if self.ignore_spec is None:
            return False
        rel_path = os.path.relpath(file_path, self.project_directory)
        return self.ignore_spec.match_file(rel_path)

    def index_files(self):
        self.context_db.reset()
        files_to_index = []
        for root, _, files in os.walk(self.project_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_ignored(file_path):
                    continue  # Skip ignored files

                if file.endswith((".js", ".html", ".css")):
                    files_to_index.append(file_path)

        # Use ThreadPoolExecutor to parallelize the indexing process
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._process_file, files_to_index)

    def has_been_indexed(self) -> bool:
        return not self.context_db.is_empty()

    def _process_file(self, file_path: str):
        try:
            # Read the content of the file
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            # Generate a summary of the file content
            summary = self.llm_client.generate_completion(
                f"""
            We are indexing source code files in a project to enhance search and retrieval capabilities.
            
            Please provide a concise yet comprehensive summary of the file's content, purpose, and functionality. Focus on key elements such as:
            
            - Main functionality and purpose of the file.
            - Key classes, functions, and their roles.
            - Important logic, algorithms, or workflows implemented.
            - Any unique or notable aspects of the code, such as patterns, optimizations, or dependencies.
            
            The summary will be used to determine the file's relevance to user queries.
            
            File content:
            {file_content}
            
            Summary:
            """
            )

            self.context_db.store_file(file_path=file_path, content=summary)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    from llm_client import LlmClient
    from context_storage import ContextStorage

    llm_client = LlmClient()
    context_db = ContextStorage(llm_client)

    # Example usage
    indexer = FileIndexer(
        project_directory="../server/generation_pipelines/components",
        llm_client=llm_client,
        context_db=context_db,
    )
    indexer.index_files()

    prompt = "Add a card block to the home page"
    similar_files = context_db.get_similar_files(prompt)

    print(f"Similar files for prompt '{prompt}': {similar_files}")
