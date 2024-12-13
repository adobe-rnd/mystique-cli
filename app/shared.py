import logging
from dotenv import load_dotenv
from app.settings import get_project_settings, BASE_DIR
from threading import Event
import time
from colorama import Fore
import os

load_dotenv()


def configure_logging():
    settings = get_project_settings()
    log_level = settings.log_level.upper() if settings.log_level else "ERROR"
    log_file_path = os.path.join(BASE_DIR, "app.log")
    logging.basicConfig(
        level=getattr(logging, log_level, logging.ERROR),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path)],
    )


configure_logging()


def show_rotating_animation(message: str, stop_event: Event):
    """Displays a rotating progress animation in a separate thread."""
    symbols = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(Fore.YELLOW + f"\r{message} {symbols[idx % len(symbols)]}", end="")
        idx += 1
        time.sleep(0.1)
    print("\r", end="")  # Clear the line after stopping the animation
