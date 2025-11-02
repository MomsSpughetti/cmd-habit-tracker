from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseCommand(ABC):
    """Base class for all commands"""

    @abstractmethod
    def execute(self, args: Dict[str, Any] = None) -> None:
        """Executes the command with optional arguments"""
        pass

    @abstractmethod
    def get_help_text(self) -> str:
        """Return help text for this command"""
        pass

    def validate_args(self, args: Dict[str, Any]) -> bool:
        """Validate command args"""
        return True
    