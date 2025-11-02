from typing import List, Optional

from cmd_habit_tracker.db.operations import DatabaseOperations
from cmd_habit_tracker.db.models import Habit
from cmd_habit_tracker.exceptions.domain_errors import DuplicateHabitError, HabitNotFoundError

class HabitService:
    def __init__(self, db_ops: DatabaseOperations):
        self.db_ops = db_ops
    
    def create_habit(self, habit_data: dict) -> Habit:
        """Create new habit with validation"""
        if self._habit_exists(habit_data['title']):
            raise DuplicateHabitError(f"Habit '{habit_data['title']}' already exists")
        
        # Create habit object
        habit = Habit()
        habit.set_habit_from_dict(habit_data)

        # Validate business rules
        self._validate_habit_rules(habit)

        # Save to database
        return self.db_ops.add_habit(habit)
    
    def get_all_habits(self) -> List[Habit]:
        """Get all habits"""
        return self.db_ops.get_all_habits()
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """Get habit by ID"""
        habit = self.db_ops.get_habit_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError(f"Habit with ID {habit_id} not found")
        return habit
    
    def delete_habit(self, habit_id: int) -> bool:
        """Delete habit and related records"""
        self.get_habit_by_id(habit_id) # Validate existence
        return self.db_ops.delete_habit(habit_id)

    def _habit_exists(self, title: str) -> bool:
        """Check if habit with title exists"""
        return self.db_ops.get_habit_by_title(title) is not None
    
    def _validate_habit_rules(self, habit: Habit) -> None:
        """Validate bussiness rules for habits"""
        if habit.frequency_amount <= 0:
            raise ValueError("Frequency amount must be positive")
        
        if habit.target_amount and habit.target_amount <= 0:
            raise ValueError("Target amount must be positive")
        
    
