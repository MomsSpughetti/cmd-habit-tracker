from enum import Enum
########################################## Data ##########################################

TEST_MODE = 0
DATABASE = "habit_tracker.db"

class Errors(Enum):
    DUPLICATE_HABIT = 0
    CORRUPTED_HABIT = 1
    HABIT_NOT_FOUND = 2
    CORRUPTED_INPUT = 3

ERROR_MESSAGES = {
    Errors.DUPLICATE_HABIT: "Habit was not added because it already exists",
    Errors.CORRUPTED_HABIT: "Habit info is corrupted",
    Errors.HABIT_NOT_FOUND: "Habit not found",
    Errors.CORRUPTED_INPUT: "An input was corrupted. The input was"
}


class Frequency(Enum):
    """Must stay the same - do not modify!"""
    EVERY_DAY = 0
    EVERY_WEEK = 1
    EVERY_MONTH = 2
    EVERY_Z_DAYS = 3
    EVERY_Z_WEEKS = 4
    EVERY_Z_MONTHS = 5

    def get_single_freq_amount():
        return [Frequency.EVERY_DAY.value, Frequency.EVERY_MONTH.value, Frequency.EVERY_WEEK.value]
    
    def get_freq_enum(freq: str):
        """Parameters: string containing one of day|week|month|days|weeks|months """
        freq_cleared = freq.strip().lower()
        if freq_cleared == 'day':
            return Frequency.EVERY_DAY.value
        elif freq_cleared == 'week':
            return Frequency.EVERY_WEEK.value
        elif freq_cleared == 'month':
            return Frequency.EVERY_MONTH.value
        elif freq_cleared == 'days':
            return Frequency.EVERY_Z_DAYS.value
        elif freq_cleared == 'weeks':
            return Frequency.EVERY_Z_WEEKS.value
        elif freq_cleared == 'moths':
            return Frequency.EVERY_Z_MONTHS.value





FREQUENCY_DICT = {
    Frequency.EVERY_Z_DAYS.value: "every Z days",
    Frequency.EVERY_DAY.value: "every day",
    Frequency.EVERY_Z_WEEKS.value: "every Z weeks",
    Frequency.EVERY_WEEK.value: "every week",
    Frequency.EVERY_Z_MONTHS.value: "every Z months",
    Frequency.EVERY_MONTH.value: "every month"
}

class Commands(Enum):
    #general
    HELP = "help"
    HABITS = "habits" # shows a list of all the habits
    PROGRESS = "progress" # shows the progress during a specific month
    EXIT = "exit"

    # for habits
    ADD = "add"
    ARCHIVE = "archive"
    DELETE = "delete"
    UPDATE = "update"
    GENERATE = "generate"
    DOCS = "docs"

    # for tracking
    TRACK = "track" # provide tracking info for a specific date

    def get_commands():
        """returns a dict(str, str) of all possible commands - command: <usage>"""
        return {
            Commands.ADD.value: "add - to add a new habit",
            # Commands.ARCHIVE.value: "Not available",
            # Commands.DELETE.value: "Not available",
            Commands.HABITS.value: "habits - see all your habits",
            Commands.HELP.value: "help - See possible commands",
            Commands.DOCS.value: "docs - ask the program what you need to do",
            Commands.PROGRESS.value: "progress <Year> <Month> - Shows the progress for a specific month",
            Commands.UPDATE.value: "Not available",
            Commands.TRACK.value: "Not available",
            Commands.EXIT.value: "exit",
            Commands.GENERATE.value: "generate - to make the AI suggest you a habit based on your goal"
        }



class Habits(Enum):
    """period should store an integer indicating the number of days that the app should track a habit"""
    ID = "id"
    TITLE = "title"
    START_DATE = "start_date"
    PERIOD = "period"
    NOTE = "note"
    FREQUENCY_FORMAT = "frequency_format"
    FREQUENCY_AMOUNT = "frequency_amount"
    TARGET_METRIC = "target_metric"
    TARGET_AMOUNT = "target_amount"

    def __str__(self):
        return self.value
    def get_number_of_columns():
        return 9


class Tracker(Enum):
    ID = "id"
    HABIT_ID = "habit_id"
    DATE = "date"
    COMPLETED = "completed"
    EXPLANATION = "explanation"

    def __str__(self):
        return self.value
    

class Tables(Enum):
    HABITS = "habits"
    TRACKER = "tracker"
    ARCHIVED_TRACKER = "archived_tracker"
    ARCHIVED_Habits = "archived_habits"
    def __str__(self):
        return self.value

DOCUMENTATION = """
**Habit Tracker with AI - FAQ**

**Q: What can I ask?** 
A: Ask about the tool, commands, features, troubleshooting, or limitations.

**Q: What is this tool?**
A: Command-line habit tracker.

**Q: What is this app?**
A: Command-line habit tracker app.

**Q: What can I do?** 
A: Track habits, get AI suggestions, customize tracking.

**Q: How do I add a habit?**
A: Use `add` or `generate`.

**Q: How do I view habits?**
A: Use `habits`.

**Q: How do I see progress?**
A: Use `progress <year> <month>`.

**Q: How do I get AI suggestions?**
A: Use `generate`.

**Q: What is a good feature?**
A: AI-powered habit suggestions.

**Q: Why is this app special?**
A: AI suggestions & user-friendly interface.

**Q: How do I tell my goals?**
A: Use `generate`.

**Q: How do I get help?**
A: Use `help`.

**Q: How do I exit?**
A: Use `exit`.

**Q: Are there any limitations?**
A: Some features may be under development.

**Q: Is this tool suitable for everyone?**
A: Consult a healthcare professional.

**Disclaimer:** 
For informational purposes only. 
"""

########################################## Functions ##########################################
