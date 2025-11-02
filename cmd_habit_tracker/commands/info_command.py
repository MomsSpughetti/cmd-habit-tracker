from cmd_habit_tracker.commands.base import BaseCommand
from typing import Dict, Any
from cmd_habit_tracker.config.settings import AppConfig

class InfoCommand(BaseCommand):
    def __init__(self, config: AppConfig):
        self.db_location = config.database.path
        self.log_location = config.logging.path
    
    def execute(self, args: Dict[str, Any] = None) -> None:
        print("Database location: " + self.db_location)
        print("Log file location: " + self.log_location)
    
    def get_help_text(self):
        return "Prints general app info"

