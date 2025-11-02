import os
from dataclasses import dataclass
from typing import Optional
from platformdirs import user_data_dir, user_log_dir
from pathlib import Path
from enum import Enum

# Constants for defaults
APP_NAME = "cmd_habit_tracker"
DEFAULT_DB_NAME = "habit_tracker.db"
DEFAULT_LOG_NAME = "app.log"

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

DEFAULT_LOG_LEVEL = LogLevel.INFO

@dataclass
class DatabaseConfig:
    """Database configuration"""
    path: str

    @classmethod
    def from_defaults(cls):
        default_db_path = Path(user_data_dir(APP_NAME)) / DEFAULT_DB_NAME
        return cls(
            path=default_db_path
        )

@dataclass
class LoggingConfig:
    """Logging configuration"""
    path: str
    level: LogLevel

    @classmethod
    def from_defaults(cls, level: LogLevel = DEFAULT_LOG_LEVEL):
        default_log_file_path = Path(user_log_dir(APP_NAME)) / DEFAULT_LOG_NAME
        return cls(
            path=default_log_file_path,
            level=level
        )

@dataclass
class AIConfig:
    """AI service configuration"""
    hg_token: str
    generation_model_id: str = "deepseek-ai/DeepSeek-R1:fireworks-ai"
    qa_model_id: str = "deepset/roberta-base-squad2"
    generation_api_url: str = "https://router.huggingface.co/v1/chat/completions"
    qa_api_url: str = "https://api-inference.huggingface.co/models/"
    timeout_seconds = 60
    max_retries: int = 3

    @classmethod
    def from_env(cls):
        token = os.getenv('HUGGING_FACE_TOKEN')
        if not token:
            raise ValueError("HUGGING_FACE_TOKEN environment variable is required")
        
        return cls(
            hg_token=token
        )


@dataclass
class AppConfig:
    """Aplication general configuration"""
    # non-default (required) fields must appear first for dataclasses
    database: DatabaseConfig
    logging: LoggingConfig
    ai: AIConfig
    # fields with defaults go after
    app_name: str = "cmd_habit_tracker"
    debug: bool = False

    @classmethod
    def create(cls):
        return cls(
            database=DatabaseConfig.from_defaults(),
            logging=LoggingConfig.from_defaults(),
            ai=AIConfig.from_env(),
        )