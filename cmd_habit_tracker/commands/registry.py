from typing import Dict, Type
from cmd_habit_tracker.commands.base import BaseCommand

class CommandRegistry:
    def __init__(self):
        self._commands: Dict[str, BaseCommand] = {}
    
    def register(self, name: str, command: BaseCommand) -> None:
        """Register a command with a name"""
        self._commands[name] = command
    
    def get_command(self, name: str) -> BaseCommand:
        """Get command by name"""
        if name not in self._commands:
            raise ValueError(f"Unknown command: {name}")
        return self._commands[name]
    
    def list_commands(self):
        """Return dict of command names and their help text"""
        return { name: cmd.get_help_text() for name, cmd in self._commands.items()}