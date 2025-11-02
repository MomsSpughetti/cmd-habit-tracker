from cmd_habit_tracker.commands.registry import CommandRegistry
from cmd_habit_tracker.commands.add_habit_command import AddHabitCommand
from cmd_habit_tracker.commands.info_command import InfoCommand
from cmd_habit_tracker.config.settings import AppConfig

class CommandFactory:
    @staticmethod
    def create_registry(habit_service, tracking_service, ai_service, report_service, config: AppConfig):
        registry = CommandRegistry()

        registry.register("info", InfoCommand(config))
        registry.register("add", AddHabitCommand(habit_service))
        ### Add more commands
    
        return registry

