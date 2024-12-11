import os
import sys
import time
import logging
from typing import Dict
from threading import Thread, Event

from colorama import init, Fore
from InquirerPy import inquirer
from dotenv import load_dotenv

from app.change_processor import ChangeProcessor
from app.context_storage import ContextStorage
from app.file_indexer import FileIndexer
from app.llm_client import LlmClient
from app.settings import (
    BASE_DIR,
    get_project_settings,
    save_project_settings,
)
from app.shared import show_rotating_animation

logger = logging.getLogger(__name__)

changes_made = []

project_directory = os.getcwd()
logger.info(f"Current project directory: {project_directory}")

project_settings = get_project_settings()


def check_essential_config_values():
    settings = get_project_settings()
    essential_keys = ["api_provider"]

    if settings.api_provider == "openai":
        essential_keys.extend(["openai_api_key"])
    elif settings.api_provider == "azure":
        essential_keys.extend(
            [
                "azure_api_key",
                "azure_endpoint",
                "azure_completion_model",
                "azure_embedding_model",
            ]
        )

    missing_keys = [key for key in essential_keys if not getattr(settings, key)]

    if missing_keys:
        api_provider = inquirer.select(
            message="Choose your API provider:",
            choices=[
                {"name": "OpenAI", "value": "openai"},
                {"name": "Azure OpenAI", "value": "azure"},
            ],
        ).execute()

        settings.api_provider = api_provider

        if api_provider == "openai":
            openai_api_key = inquirer.secret(
                message="Please enter your OpenAI API key: "
            ).execute()
            settings.openai_api_key = openai_api_key
        elif api_provider == "azure":
            azure_api_key = inquirer.secret(
                message="Please enter your Azure API key: "
            ).execute()
            azure_endpoint = inquirer.text(
                message="Please enter your Azure endpoint: "
            ).execute()
            azure_completion_model = inquirer.text(
                message="Please enter your Azure completion model: "
            ).execute()
            azure_embedding_model = inquirer.text(
                message="Please enter your Azure embedding model: "
            ).execute()
            settings.azure_api_key = azure_api_key
            settings.azure_endpoint = azure_endpoint
            settings.azure_completion_model = azure_completion_model
            settings.azure_embedding_model = azure_embedding_model

        save_project_settings(settings)


def perform_indexing(file_indexer):
    logger.info("Indexing (RAG) in progress... This might take a few moments.")

    try:
        files_to_index = file_indexer.get_files_to_index()
        file_count = len(files_to_index)
        user_input = inquirer.confirm(
            message=f"{file_count} files found. Do you want to proceed with indexing?"
        ).execute()
        if not user_input:
            logger.info("Indexing aborted by the user.")
            return

        # Start the animation in a separate thread
        stop_event = Event()
        anim_thread = Thread(
            target=show_rotating_animation,
            args=("Indexing in progress...", stop_event),
        )
        anim_thread.start()

        indexed_file_count = file_indexer.index_files(files_to_index)
    finally:
        # Signal the animation thread to stop
        stop_event.set()
        anim_thread.join()
        print(
            Fore.GREEN + f"\nIndexing is complete. {indexed_file_count} files indexed."
        )


def handle_process_changes(change_processor):
    prompt = inquirer.text(message="Please enter the prompt for changes: ").execute()
    changes = change_processor.compute_changes(prompt)

    if not changes:
        logger.error("No changes were made.")
        return

    logger.info("The following files were changed:")
    for file_change in changes["files"]:
        file_path = file_change["file_path"]
        print(Fore.YELLOW + f"File: {file_path}")

    confirm_or_reject_changes(changes, change_processor)


def confirm_or_reject_changes(changes: Dict[str, any], change_processor):
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
        logger.info("Changes have been accepted.")
    elif decision == "reject":
        logger.error("Changes have been rejected.")


def revert_changes(change_processor):
    if changes_made:
        last_change = changes_made.pop()
        for file_change in last_change["files"]:
            file_path = file_change["file_path"]
            print(
                Fore.YELLOW + f"Rolling back the last change to the file: {file_path}"
            )
        change_processor.rollback_changes(last_change)
        logger.info("Rollback complete.")
    else:
        logger.error("No changes are available to rollback.")


def update_api_secrets():
    api_provider = inquirer.select(
        message="Choose your API provider:",
        choices=[
            {"name": "OpenAI", "value": "openai"},
            {"name": "Azure OpenAI", "value": "azure"},
        ],
    ).execute()

    project_settings.api_provider = api_provider

    if api_provider == "openai":
        openai_api_key = inquirer.secret(
            message="Enter your OpenAI API key: "
        ).execute()
        project_settings.openai_api_key = openai_api_key
    elif api_provider == "azure":
        azure_api_key = inquirer.secret(message="Enter your Azure API key: ").execute()
        azure_endpoint = inquirer.text(message="Enter your Azure endpoint: ").execute()
        azure_completion_model = inquirer.text(
            message="Enter your Azure completion model: "
        ).execute()
        azure_embedding_model = inquirer.text(
            message="Enter your Azure embedding model: "
        ).execute()
        project_settings.azure_api_key = azure_api_key
        project_settings.azure_endpoint = azure_endpoint
        project_settings.azure_completion_model = azure_completion_model
        project_settings.azure_embedding_model = azure_embedding_model

    save_project_settings(project_settings)
    logger.info("Secrets have been updated and stored in the config.")


def handle_update_api_secrets():
    update_api_secrets()
    print(
        Fore.YELLOW
        + "\nSettings updated. Please restart the application to apply the new settings.\n"
    )
    sys.exit(0)


def handle_revert_changes(change_processor):
    revert_changes(change_processor)


def handle_perform_indexing(file_indexer):
    perform_indexing(file_indexer)


def handle_exit_app():
    save_project_settings(project_settings)  # Ensure it's a dictionary
    print(Fore.BLUE + "\nThank you for using the application. Goodbye!\n")
    sys.exit(0)


def handle_edit_file_patterns():
    current_patterns = project_settings.file_patterns
    print(Fore.CYAN + f"Current file patterns: {', '.join(current_patterns)}")

    new_patterns = inquirer.text(
        message="Enter new file patterns (comma-separated): "
    ).execute()

    project_settings.file_patterns = [
        pattern.strip() for pattern in new_patterns.split(",")
    ]
    save_project_settings(project_settings)
    print(Fore.GREEN + "File patterns updated successfully.")
    print(
        Fore.YELLOW
        + "\nSettings updated. Please restart the application to apply the new settings.\n"
    )
    sys.exit(0)


def display_settings_menu():
    while True:
        choice = inquirer.select(
            message="Settings Menu:",
            choices=[
                {"name": "Update API keys and secrets", "value": "1"},
                {"name": "Edit file patterns for indexing", "value": "2"},
                {"name": "Back to main menu", "value": "3"},
            ],
        ).execute()

        if choice == "1":
            handle_update_api_secrets()
        elif choice == "2":
            handle_edit_file_patterns()
        elif choice == "3":
            break


def display_main_menu(change_processor, file_indexer):
    while True:
        choices = [
            {"name": "Modify files using a prompt", "value": "1"},
            {"name": "Reindex project files", "value": "2"},
            {"name": "Change settings", "value": "3"},
            {"name": "Exit", "value": "4"},
        ]

        if changes_made:
            choices.insert(1, {"name": "Undo the last set of changes", "value": "5"})

        choice = inquirer.select(
            message="Choose an action:", choices=choices, max_height=10
        ).execute()

        if choice == "1":
            handle_process_changes(change_processor)
        elif choice == "2":
            handle_perform_indexing(file_indexer)
        elif choice == "3":
            display_settings_menu()
        elif choice == "4":
            handle_exit_app()
        elif choice == "5":
            handle_revert_changes(change_processor)


def display_startup_info():
    print(Fore.CYAN + f"Configuration folder: {BASE_DIR}")
    print(Fore.CYAN + f"Project directory: {project_directory}")

    api_provider = (
        project_settings.api_provider if project_settings.api_provider else "None"
    )

    if api_provider.lower() == "openai":
        api_provider = "OpenAI"
    elif api_provider.lower() == "azure openai":
        api_provider = "Azure OpenAI"

    print(Fore.CYAN + f"API Provider: {api_provider}\n")


def run():
    init(autoreset=True)
    load_dotenv()

    # flake8: noqa
    print(
        Fore.GREEN
        + r"""
_________     _________       
__  ____/___________  /_____ _
_  /    _  __ \  __  /_  __ `/
/ /___  / /_/ / /_/ / / /_/ / 
\____/  \____/\__,_/  \__,_/  
          """
    )

    display_startup_info()

    check_essential_config_values()

    llm_client = LlmClient()
    context_db = ContextStorage(llm_client=llm_client)
    change_processor = ChangeProcessor(
        llm_client=llm_client,
        context_db=context_db,
        project_directory=project_directory,
    )
    file_indexer = FileIndexer(
        project_directory=project_directory,
        llm_client=llm_client,
        context_db=context_db,
    )

    if not file_indexer.has_been_indexed():
        user_input = inquirer.confirm(
            message="No indexing found. Would you like to start indexing?"
        ).execute()
        if user_input:
            perform_indexing(file_indexer)
        else:
            print(
                Fore.RED
                + "\nIndexing is required to proceed. Exiting the application...\n"
            )
            sys.exit(0)

    display_main_menu(change_processor, file_indexer)


if __name__ == "__main__":
    run()
