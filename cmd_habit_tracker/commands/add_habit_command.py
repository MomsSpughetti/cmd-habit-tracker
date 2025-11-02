from cmd_habit_tracker.commands.base import BaseCommand
from typing import Dict, Any
from cmd_habit_tracker.services.habit_service import HabitService
from utils.input_validators import get_new_habit_input

class AddHabitCommand(BaseCommand):
    def __init__(self, habit_service: HabitService):
        self.habit_service = habit_service
    
    def execute(self, args: Dict[str, Any] = None) -> None:
        try:
            new_habit = get_new_habit_input()
            self.habit_service.create_habit(new_habit)
            print("Habit added successfully!")
        except Exception as e:
            print(f"Error adding habit: {e}")
    
    def get_help_text(self):
        return "Add a new habit to track"

