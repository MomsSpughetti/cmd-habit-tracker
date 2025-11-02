from functools import wraps
from exceptions.handler import ErrorHandler

def error_boundary(error_handler: ErrorHandler):
    """Decorator to create error boundaries around functions"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = error_handler.handle(e)
                print(f"Error: {error_message}")
                return None
        return wrapper
    return decorator