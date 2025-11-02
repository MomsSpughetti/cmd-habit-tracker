
class HabitTrackerError(Exception):
    """Base exception for all application errors"""

    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
    