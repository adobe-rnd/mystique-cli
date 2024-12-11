import os
import json
from typing import Optional, List
from pydantic import BaseModel, ValidationError
from humps import camel

BASE_DIR = os.path.join(os.getcwd(), ".coda")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.json")


def to_camel(string):
    return camel.case(string)


class ProjectSettings(BaseModel):
    api_provider: Optional[str] = None
    openai_api_key: Optional[str] = None
    azure_api_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    azure_completion_model: Optional[str] = None
    azure_embedding_model: Optional[str] = None
    log_level: Optional[str] = "ERROR"
    file_patterns: Optional[List[str]] = [
        ".js",
        ".html",
        ".css",
        ".py",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".ts",
        ".jsx",
        ".tsx",
        ".php",
        ".rb",
        ".go",
        ".rs",
        ".swift",
        ".kt",
        ".m",
        ".mm",
        ".sh",
        ".bat",
        ".pl",
        ".r",
        ".scala",
        ".lua",
        ".sql",
        ".xml",
        ".json",
        ".yaml",
        ".yml",
    ]

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True,
    }


settings: ProjectSettings = None


def load_project_settings():
    global settings
    if not os.path.exists(CONFIG_FILE_PATH):
        save_project_settings(ProjectSettings)
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            settings = ProjectSettings(**json.load(f))
    except json.JSONDecodeError:
        settings = ProjectSettings()


def save_project_settings(new_settings: ProjectSettings):
    global settings
    try:
        with open(CONFIG_FILE_PATH, "w") as f:
            f.write(new_settings.model_dump_json(indent=4))
        settings = new_settings
    except ValidationError as e:
        print(f"Validation error: {e}")


def get_project_settings() -> ProjectSettings:
    global settings
    if settings is None:
        load_project_settings()
    return settings
