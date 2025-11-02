import logging
from typing import Dict, Type, Callable
from cmd_habit_tracker.exceptions.base import HabitTrackerError
from cmd_habit_tracker.exceptions.domain_errors import *
from cmd_habit_tracker.exceptions.infrastructure_errors import *

class ErrorHandler:
    """Centralized error handling"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._handlers: Dict[Type[Exception], Callable] = {}
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup error handlers for different exception types"""
        # Habit errors
        self._handlers[DuplicateHabitError] = self._handle_duplicate_habit
        self._handlers[HabitNotFoundError] = self._handle_habit_not_found
        self._handlers[InvalidHabitDataError] = self._handle_invalid_habit_data
        # Tracking errors
        self._handlers[FutureDateError] = self._handle_future_date
        self._handlers[InvalidAchievementError] = self._handle_invalid_achievement
        # Infra errors
        self._handlers[AIServiceError] = self._handle_ai_service_error
        self._handlers[DatabaseError] = self._handle_database_error
        self._handlers[ConfigurationError] = self._handle_config_error

    
    def handle(self, error: Exception):
        """Handle an error and return user-friendly message"""
        # Log the error
        self.logger.error(f"Error occured: {error}", exc_info=True)

        # Find appropriate handler
        for error_type, handler in self._handlers.items():
            if isinstance(error, error_type):
                return handler(error)
        
        # Default handler for unknown errors
        return self._handle_unknown_error(error)

    def _handle_duplicate_habit(self, error: DuplicateHabitError):
        return f"A habit with that name already exists. Please choose a different name"
    
    def _handle_habit_not_found(self, error: HabitNotFoundError):
        return f"The requested habit was not found. It may have been deleted"
    
    def _handle_invalid_habit_data(self, error: InvalidHabitDataError):
        return f"The data provided to create the habit is corrupted."
    
    def _handle_future_date(self, error: FutureDateError):
        return f"Cannot track habits for future dates. Please select today or a past date"
    
    def _handle_invalid_achievement(self, error: InvalidAchievementError):
        return f"Invalid achievement."
    
    def _handle_ai_service_error(self, error:AIServiceError ):
        return f"AI service is currently unavailable. Please try again later or continue without AI features"
    
    def _handle_database_error(self, error: DatabaseError):
        return f"A database error occured. Please try again or contact support if the problem persists"
    
    def _handle_config_error(self, error: ConfigurationError):
        return f"Configuration error: {error.message}."
    
    def _handle_unknown_error(self, error: Exception):
        return "An unexpected error occurred. Please try again or contact support."