from typing import Callable, TypeVar, Type, Any, Dict

from cmd_habit_tracker.config.settings import AppConfig
from cmd_habit_tracker.db.operations import DatabaseOperations
from cmd_habit_tracker.services.habit_service import HabitService
from cmd_habit_tracker.services.tracking_service import TrackingService
from cmd_habit_tracker.services.ai_service import AIService
from cmd_habit_tracker.services.report_service import ReportService

T = TypeVar('T')

class Container:
    """Dependency injection container"""

    def __init__(self, config: AppConfig):
        self.config = config
        self._instances: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._setup_factories()

    def _setup_factories(self):
        """Setup factory methods for services"""
        self._factories[DatabaseOperations] = lambda: DatabaseOperations(self.config.database)
        self._factories[HabitService] = lambda: HabitService(self.get(DatabaseOperations))
        self._factories[TrackingService] = lambda: TrackingService(
            self.get(DatabaseOperations), 
            self.get(HabitService)
        )
        self._factories[AIService] = lambda: AIService(self.config.ai)
        self._factories[ReportService] = lambda: ReportService(
            self.get(HabitService),
            self.get(TrackingService)
        )
    
    def get(self, serivce_type: Type[T]):
        """Get service instance (singleton pattern)"""
        if serivce_type not in self._instances:
            if serivce_type not in self._factories:
                raise ValueError(F"No factory registered for {serivce_type}")
            self._instances[serivce_type] = self._factories[serivce_type]() # check later
        return self._instances[serivce_type]
    
    def register(self, service_type: Type[T], instance: T):
        """Register a specific instance"""
        self._instances[service_type] = instance
    


