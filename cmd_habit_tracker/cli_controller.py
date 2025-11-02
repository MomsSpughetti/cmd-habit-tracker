from cmd_habit_tracker.commands.registry import CommandRegistry
from typing import Dict, Any

class CLIController:
    def __init__(self, command_registry: CommandRegistry):
        self.command_registry = command_registry

    def execute_command(self, command_name: str, args: Dict[str, Any] = None):
        try:
            command = self.command_registry.get_command(command_name)
            if command.validate_args(args or {}):
                command.execute(args)
            else:
                print("Invalid arguments for command")
        except ValueError as e:
            print(f"Error: {e}")
            self.show_available_commands()
    
    def show_available_commands(self):
        commands = self.command_registry.list_commands()
        print("Available commands:")
        for name, help_text in commands.items():
            print(f"  {name} - {help_text}")
