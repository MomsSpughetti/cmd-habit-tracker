from cmd_habit_tracker.config.settings import AIConfig

class AIService:
    """Providing AI services"""
    def __init__(self, config : AIConfig):
        self.config = config

