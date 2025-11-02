from container import Container
from config.factory import ConfigFactory
from commands.factory import CommandFactory
from cli_controller import CLIController
from cmd_habit_tracker.services.habit_service import HabitService
from cmd_habit_tracker.services.tracking_service import TrackingService
from cmd_habit_tracker.services.ai_service import AIService
from cmd_habit_tracker.services.report_service import ReportService
from cmd_habit_tracker.db.operations import DatabaseOperations

class Application:
    """Main application class that bootstraps everything"""

    def __init__(self, environment: str = None):
        self.config = ConfigFactory.create_config(environment)
        self.container = Container(self.config)
        self.ci_controller = self._setup_cli()
    
    def _setup_cli(self) -> CLIController:
        """Setup CLI with all dependencies"""
        habit_service = self.container.get(HabitService)
        tracking_service = self.container.get(TrackingService)
        ai_service = self.container.get(AIService)
        report_service = self.container.get(ReportService)

        command_registry = CommandFactory.create_registry(
            habit_service, tracking_service, ai_service, report_service, self.config
        )

        return CLIController(command_registry)
    
    def run(self):
        """Run the application"""
        try:
            self._initialize()
            self._welcome()
            self._main_loop()
        except KeyboardInterrupt:
            print("\nGoodbye!")
        except Exception as e:
            print(f"Application error: {e}")
            if self.config.debug:
                raise
    
    def _initialize(self):
        """Initialize application components"""
        db_ops: DatabaseOperations = self.container.get(DatabaseOperations)
        db_ops.create_tables()
    
    def _welcome(self):
        """Show welcome message"""
        print("Welcome to your personal habit tracker")

    def _main_loop(self):
        """Main application loop"""
        while True:
            try:
                command_name = input(">>> ").strip()
                if command_name:
                    self.ci_controller.execute_command(command_name)
            except EOFError:
                break



