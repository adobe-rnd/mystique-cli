import sys  # Add this import for improved print handling
from typing import List, Dict, Optional
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.diff import DiffLexer
from unidiff import PatchSet, PatchedFile
import os
import time
from threading import Thread, Event

from app.context_storage import ContextStorage
from app.llm_client import LlmClient

TOP_N_SIMILAR_FILES = 5

FILE_MODIFICATION_SCHEMA: Dict = {
    "title": "FileModification",
    "description": "Modify the provided files to fulfill the user's request.",
    "type": "object",
    "properties": {
        "files": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string"
                    },
                    "new_content": {
                        "type": "string"
                    }
                },
                "required": ["file_path", "new_content"]
            }
        }
    },
    "required": ["files"]
}

class ChangeProcessor:
    def __init__(self, llm_client: LlmClient, context_db: ContextStorage, project_directory: str):
        self.llm_client = llm_client
        self.context_db = context_db
        self.project_directory = os.path.abspath(project_directory)

    def rotating_animation(self, message: str, stop_event: Event):
        """Displays a rotating progress animation in a separate thread."""
        symbols = "|/-\\"
        idx = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\r{message} {symbols[idx % len(symbols)]}")  # Use sys.stdout.write
            sys.stdout.flush()  # Flush the output to ensure it's printed immediately
            idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r")  # Clear the line after stopping the animation
        sys.stdout.flush()

    def compute_changes(self, prompt: str) -> Dict[str, any]:
        similar_files = self.context_db.get_similar_files(prompt, TOP_N_SIMILAR_FILES)
        file_contents = []

        for file_path in similar_files:
            full_path = file_path
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
                file_contents.append(f"### File: {file_path}\n{content}\n")
        print("Files pulled successfully (RAG)...")

        llm_prompt = f"""
        You have been provided with the content of the following files:
        {'\n\n'.join(file_contents)}
        
        And the user's request:
        {prompt}
        
        Your task is to:
        
        1. **Analyze** the provided files to understand their current functionality and determine the changes required to satisfy the user's request.
        2. **Modify** the files with precise and minimal changes necessary to fulfill the requirements specified.
        3. **Output** the modifications in a JSON format as specified below:
            {{
                "files": [
                    {{
                        "file_path": "path/to/file1",
                        "new_content": "modified content of file1"
                    }},
                    {{
                        "file_path": "path/to/file2",
                        "new_content": "modified content of file2"
                    }},
                    ...
                ]
            }}
        4. **Provide** the complete modified source code for each changed file in the 'new_content' field.
        
        Ensure your modifications are accurate, concise, and directly address the user's request.
        """

        # Start the animation in a separate thread
        stop_event = Event()
        anim_thread = Thread(target=self.rotating_animation, args=("Thinking...", stop_event))
        anim_thread.start()

        try:
            changes = self.llm_client.generate_completion(llm_prompt, json_schema=FILE_MODIFICATION_SCHEMA)
        finally:
            # Signal the animation thread to stop
            stop_event.set()
            anim_thread.join()
            print("LLM processing complete.")

        return changes

    def apply_changes(self, changes: Dict[str, any]) -> Dict[str, any]:
        previous_file_states = {
            "files": []
        }

        # Start the animation in a separate thread
        stop_event = Event()
        anim_thread = Thread(target=self.rotating_animation, args=("Applying changes...", stop_event))
        anim_thread.start()

        try:
            for file_change in changes["files"]:
                file_path = file_change["file_path"]
                new_content = file_change["new_content"]
                try:
                    if not os.path.exists(file_path):
                        print(f"Error: File not found - {file_path}")
                        continue

                    with open(file_path, 'r', encoding='utf-8') as file:
                        original_content = file.readlines()
                        previous_file_states["files"].append({
                            "file_path": file_path,
                            "new_content": original_content
                        })

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(new_content)

                    print(f"Applied changes to {file_path}")

                except Exception as e:
                    print(f"Failed to apply changes to {file_path}: {e}")
        finally:
            # Signal the animation thread to stop
            stop_event.set()
            anim_thread.join()
            print("Changes applied successfully.")

        return previous_file_states

    def rollback_changes(self, changes: Dict[str, any]):
        # Start the animation in a separate thread
        stop_event = Event()
        anim_thread = Thread(target=self.rotating_animation, args=("Rolling back changes...", stop_event))
        anim_thread.start()

        try:
            for file_change in changes["files"]:
                file_path = file_change["file_path"]
                new_content = file_change["new_content"]
                try:
                    if not os.path.exists(file_path):
                        print(f"Error: File not found - {file_path}")
                        continue

                    with open(file_path, 'r', encoding='utf-8') as file:
                        original_lines = file.readlines()

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(new_content)

                    print(f"Rolled back changes to {file_path}")

                except Exception as e:
                    print(f"Failed to rollback changes to {file_path}: {e}")
        finally:
            # Signal the animation thread to stop
            stop_event.set()
            anim_thread.join()
            print("Rollback complete.")
