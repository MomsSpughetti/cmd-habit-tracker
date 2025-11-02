from cmd_habit_tracker.config.settings import *

class ConfigFactory:
    """Factory for creating configuration objects"""

    @staticmethod
    def create_config(environment: str = None):
        """Create configuration based on environment"""
        env = environment or os.getenv('ENVIRONMENT', 'production')

        if env == 'test':
            return ConfigFactory._create_test_config()
        elif env == 'development':
            return ConfigFactory._create_dev_config()
        else:
            return AppConfig.create()
    


    
    @staticmethod
    def _create_test_config() -> AppConfig:
        """Create test configuration with sqlite in-memory database"""
        return AppConfig(
            database = DatabaseConfig(path=':memory:'),
            debug=True,
            logging=LoggingConfig.from_defaults(LogLevel.DEBUG)
        )
        

    @staticmethod
    def _create_dev_config() -> AppConfig:
        """Create development configuration"""
        config = AppConfig.create()
        config.debug = True
        config.logging.level = LogLevel.DEBUG
        return config