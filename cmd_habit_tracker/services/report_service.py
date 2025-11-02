from cmd_habit_tracker.services.habit_service import HabitService
from cmd_habit_tracker.services.tracking_service import TrackingService

class ReportService:
    """Providing report services"""
    def __init__(self, habit_service : HabitService, tracking_service : TrackingService):
        self.habit_service = habit_service
        self.tracking_service = tracking_service
    


