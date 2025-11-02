
from exceptions.base import HabitTrackerError


class InfrastructureError(HabitTrackerError):
    """Base class for infrastructure errors"""
    pass

class DatabaseError(InfrastructureError):
    """Database-related errors"""
    pass

class AIServiceError(InfrastructureError):
    """AI service-related errors"""
    pass

class ConfigurationError(InfrastructureError):
    """Configuration-related errors"""
    pass