from db.tools import Errors, ERROR_MESSAGES

class DuplicateHabit(Exception):
    def __init__(self):
        super().__init__(ERROR_MESSAGES[Errors.DUPLICATE_HABIT])
