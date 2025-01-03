from db.tools import Errors, ERROR_MESSAGES

class DuplicateHabit(Exception):
    def __init__(self):
        super().__init__(ERROR_MESSAGES[Errors.DUPLICATE_HABIT])

class CorruptedHabit(Exception):
    def __init__(self):
        super().__init__(ERROR_MESSAGES[Errors.CORRUPTED_HABIT])

class HabitNotFound(Exception):
    def __init__(self, habit_title=""):
        super().__init__(ERROR_MESSAGES[Errors.HABIT_NOT_FOUND] + ": " + habit_title)

class CorruptedInput(Exception):
    def __init__(self, _input=""):
        super().__init__(ERROR_MESSAGES[Errors.CORRUPTED_INPUT] + ": " + _input)

