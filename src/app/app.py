import os
import sys
import time
from typing import Dict
from threading import Thread, Event

from colorama import init, Fore
from InquirerPy import inquirer

from app.change_processor import ChangeProcessor
from app.context_storage import ContextStorage
from app.file_indexer import FileIndexer
from app.llm_client import LlmClient

init(autoreset=True)

changes_made = []

project_directory = os.getcwd()
print(Fore.GREEN + f"Current project directory: {project_directory}")

# Initialize clients and databases
llm_client = LlmClient()
context_db = ContextStorage(llm_client=llm_client)
change_processor = ChangeProcessor(
    llm_client=llm_client, context_db=context_db, project_directory=project_directory
)
file_indexer = FileIndexer(
    project_directory=project_directory, llm_client=llm_client, context_db=context_db
)


def rotating_animation(message: str, stop_event: Event):
    """Displays a rotating progress animation in a separate thread."""
    symbols = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(Fore.YELLOW + f"\r{message} {symbols[idx % len(symbols)]}", end="")
        idx += 1
        time.sleep(0.1)
    print("\r", end="")  # Clear the line after stopping the animation


def run_indexing():
    print(Fore.YELLOW + "Indexing (RAG) in progress... This might take a few moments.")

    # Start the animation in a separate thread
    stop_event = Event()
    anim_thread = Thread(
        target=rotating_animation, args=("Indexing (RAG) in progress...", stop_event)
    )
    anim_thread.start()

    try:
        file_indexer.index_files()
    finally:
        # Signal the animation thread to stop
        stop_event.set()
        anim_thread.join()
        print(Fore.GREEN + "\nIndexing is complete.")


def make_changes():
    prompt = inquirer.text(message="Please enter the prompt for changes: ").execute()
    changes = change_processor.compute_changes(prompt)

    if not changes:
        print(Fore.RED + "No changes were made.")
        return

    print(Fore.GREEN + "The following files were changed:")
    for file_change in changes["files"]:
        file_path = file_change["file_path"]
        print(Fore.YELLOW + f"File: {file_path}")

    accept_or_reject_changes(changes)


def accept_or_reject_changes(changes: Dict[str, any]):
    decision = inquirer.select(
        message="What would you like to do with these changes?",
        choices=[
            {"name": "Accept the changes", "value": "accept"},
            {"name": "Reject the changes", "value": "reject"},
        ],
    ).execute()

    if decision == "accept":
        previous_file_states = change_processor.apply_changes(changes)
        changes_made.append(previous_file_states)
        print(Fore.GREEN + "Changes have been accepted.")
    elif decision == "reject":
        print(Fore.RED + "Changes have been rejected.")


def rollback_changes():
    if changes_made:
        last_change = changes_made.pop()
        for file_change in last_change["files"]:
            file_path = file_change["file_path"]
            print(
                Fore.YELLOW + f"Rolling back the last change to the file: {file_path}"
            )
        change_processor.rollback_changes(last_change)
        print(Fore.GREEN + "Rollback complete.")
    else:
        print(Fore.RED + "No changes are available to rollback.")


def main_menu():
    while True:
        choices = [
            {"name": "Modify files based on a prompt", "value": "1"},
        ]

        if changes_made:
            choices.append({"name": "Undo the last set of changes", "value": "2"})
        else:
            choices.append(
                {
                    "name": "Undo changes (no changes to undo)",
                    "value": "2",
                    "disabled": True,
                }
            )

        choices.extend(
            [
                {"name": "Reindex project files", "value": "3"},
                {"name": "Exit application", "value": "4"},
            ]
        )

        choice = inquirer.select(
            message="Choose an action:", choices=choices, max_height=10
        ).execute()

        if choice == "1":
            make_changes()
        elif choice == "2":
            rollback_changes()
        elif choice == "3":
            run_indexing()
        elif choice == "4":
            print(Fore.GREEN + "Exiting the application.")
            sys.exit(0)


def cli_app():
    print(
        Fore.GREEN
        + r"""
    
  __  __              _    _                     
 |  \/  |            | |  (_)                    
 | \  / | _   _  ___ | |_  _   __ _  _   _   ___ 
 | |\/| || | | |/ __|| __|| | / _` || | | | / _ \
 | |  | || |_| |\__ \| |_ | || (_| || |_| ||  __/
 |_|  |_| \__, ||___/ \__||_| \__, | \__,_| \___|
           __/ |                 | |             
          |___/                  |_|             
          """
    )

    if not file_indexer.has_been_indexed():
        user_input = inquirer.confirm(
            message="No indexing found. Would you like to start indexing?"
        ).execute()
        if user_input:
            run_indexing()
        else:
            print(Fore.RED + "Exiting the application...")
            sys.exit(0)

    main_menu()


def main():
    cli_app()
