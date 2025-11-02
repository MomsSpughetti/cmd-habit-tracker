
from exceptions.base import HabitTrackerError


class DomainError(HabitTrackerError):
    """Base class for domain-specific errors"""
    pass

class HabitError(DomainError):
    """Habit-related errors"""
    pass

class DuplicateHabitError(HabitError):
    """Raised when trying to create a habit that already exists"""
    pass

class HabitNotFoundError(HabitError):
    """Raised when habit cannot be found"""
    pass

class InvalidHabitDataError(HabitError):
    """Raised when habit data is invalid"""
    pass

class TrackingError(DomainError):
    """Tracking-related errors"""
    pass

class FutureDateError(TrackingError):
    """Raised when trying to track future dates"""
    pass

class InvalidAchievementError(TrackingError):
    """Raised when achievement value is invalid"""
    pass

