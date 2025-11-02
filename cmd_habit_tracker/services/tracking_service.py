from cmd_habit_tracker.services.habit_service import HabitService
from cmd_habit_tracker.db.operations import DatabaseOperations

class TrackingService:
    """Providing tracking service"""
    def __init__(self, db_ops : DatabaseOperations, habit_service : HabitService):
        self.db_ops = db_ops
        self.habit_service = habit_service



