from enum import Enum
from datetime import date
from calendar import monthrange
from datetime import timedelta

import os
from platformdirs import user_data_dir, user_log_dir
########################################## Data ##########################################

TEST_MODE = 0
APP_NAME = "cmd_habit_tracker"

class Errors(Enum):
    DUPLICATE_HABIT = 0
    CORRUPTED_HABIT = 1
    HABIT_NOT_FOUND = 2
    CORRUPTED_INPUT = 3
    CORRUPTED_RECORD = 4

ERROR_MESSAGES = {
    Errors.DUPLICATE_HABIT: "Habit was not added because it already exists",
    Errors.CORRUPTED_HABIT: "Habit info is corrupted",
    Errors.HABIT_NOT_FOUND: "Habit not found",
    Errors.CORRUPTED_INPUT: "An input was corrupted. The input was",
    Errors.CORRUPTED_RECORD: "Record info is corrupted"
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
    
    def frequency_to_days(freq_format: int, freq_amount: int):
        Z = 1
        if freq_format in [1, 4]:
            Z = 7
        elif freq_format in [2, 5]:
            Z = 30
        return Z*freq_amount



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
    INFO = "info"

    # for tracking
    TRACK = "track" # provide tracking info for a specific date

    # other
    CLEAR = "clear"

    def get_commands():
        """returns a dict(str, str) of all possible commands - command: <usage>"""
        return {
            Commands.ADD.value: "add - to add a new habit",
            Commands.DELETE.value: "delete - to delete a habit",
            # Commands.ARCHIVE.value: "Not available",
            Commands.HABITS.value: "habits - see all your habits",
            Commands.HELP.value: "help - See possible commands",
            Commands.DOCS.value: "docs - ask the program what you need to do",
            Commands.PROGRESS.value: "progress <Year> <Month> - Shows the progress for a specific month",
            Commands.UPDATE.value: "Not available",
            Commands.TRACK.value: "track - run to insert tracking info for a specific habit",
            Commands.EXIT.value: "exit",
            Commands.GENERATE.value: "generate - to make the AI suggest you a habit based on your goal",
            Commands.CLEAR.value: "clear - clears previous text",
            Commands.INFO.value: "info - show general info"
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
    ACHIEVED = "achieved"
    EXPLANATION = "explanation"

    def __str__(self):
        return self.value
    def get_number_of_columns():
        return 5
    

class Holder(object):
    done = False

class Tables(Enum):
    HABITS = "habits"
    TRACKER = "tracker"
    ARCHIVED_TRACKER = "archived_tracker"
    ARCHIVED_Habits = "archived_habits"
    def __str__(self):
        return self.value

class Tracking_options(Enum):
    TRACK_ALL = 1
    TRACK_UNTRACKED = 2
    TRACK_SINGLE = 3
    EXIT = 4

    def get_options():
        return [
            "Track all habits - will erase previous info",
            "Track only the habits that are not tracked",
            "Track a specific habit",
            "Exit"
            ]

YES_ANSWERS = ["yes", "y", "yeah", "ye", "yess", "yea", "yup", "es", "si"]
NO_ANSWERS = ["n", "nah", "no", "noo", "nooo", "nooo", "o", "nno"]


class Date():
    def __init__(self, year: int = None, month: int = None, day: int = None):
        self.year = int(year) if type(year) is int else 1
        self.month = int(month) if type(month) is int else 1
        self.day = int(day) if type(day) is int else 1

    def set_date(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def get_year_in_Y_format(year: int):
        year_str = str(year)
        zeros_to_be_added = 4 - len(year_str)
        for _ in range(zeros_to_be_added):
            year_str = "0" + year_str
        return year_str
    
    def get_month_in_M_format(month: int):
        return str(month) if month >= 10 else '0'+str(month)
    
    def get_day_in_D_format(day: int):
        return str(day) if day >= 10 else '0'+str(day)
    
    def is_year_valid(self):
        return self.year <= date.today().year or self.year >= 1
    
    def is_month_valid(self):
        return self.month >= 1 or self.month <= 12
    
    def get_max_day(year: int, month: int):
        return monthrange(year, month)[1]
    
    def is_day_valid(self):
        if not (self.day < 1 or self.day > 31 or not self.is_month_valid() or not self.is_year_valid()):
            max_day = monthrange(year=self.year, month=self.month)[1]
            return self.day <= max_day
        return False
    
    def is_date_valid(self):
        return self.is_year_valid() and self.is_month_valid() and self.is_day_valid()
    
    def string_format(self):
        YYYY = Date.get_year_in_Y_format(self.year)
        MM = Date.get_month_in_M_format(self.month)
        DD = Date.get_day_in_D_format(self.day)
        return f"{YYYY}-{MM}-{DD}"
    
    def __str__(self):
        return self.string_format()
    
    def get_yesterday():
        # Get today's date
        today = date.today()        
        # Yesterday date
        yesterday = today - timedelta(days = 1)
        new_date = Date()
        new_date.set_date(yesterday.year, yesterday.month, yesterday.day)
        return new_date
    
    def get_today():
        # Get today's date
        today = date.today()        
        today_date = Date()
        today_date.set_date(today.year, today.month, today.day)
        return today_date
    
    def in_future(self):
        return False

    def get_first_date_of_month(year: int, month: int):
        date = Date()
        date.set_date(year=year, month=month, day=1)
        return date.string_format()
    
    def get_last_date_of_month(year: int, month: int):
        date = Date()
        date.set_date(year=year, month=month, day=Date.get_max_day(year, month))
        return date.string_format()
          
DOCUMENTATION = """
You can ask about the tool, commands, features, troubleshooting, or limitations.
This tool is a Command-line habit tracker.
This app is a Command-line habit tracker app.
You can Track habits, get AI suggestions, customize tracking.
Some good commands are: `help`, `docs`, `generate`, `add`, `habits`, `track`
You can add a habit by running `add` or `generate`.
You can view your own habits by running `habits`.
To view your progress, you can run `progress <year> <month>`.
You can get an AI suggestions by running `generate`.
One of the best features of this app is the AI-powered habit suggestions. You can use this feature by running `generate`
This app is special and unique for many reasons. It offers AI suggestions & user-friendly interface.
In order to tell the problem your goal run `generate`.
To get help run `help`.
To exit this app you should run `exit`.
To exit this program you should run `exit`.
There are some limitations of this app, since some features may be under development.
This tool is designed and suitable for people that want to achieve their goals.
To clear the previous text run `clear`
"""

########################################## Functions ##########################################

def db_location():

    db_dir = user_data_dir(APP_NAME)
    os.makedirs(db_dir, exist_ok=True)  # Ensure directory exists
    return os.path.join(db_dir, "habit_tracker.db")

DATABASE = db_location()

def log_location():
    log_dir = user_log_dir(APP_NAME)
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "habit_tracker.log")

LOGFILE = log_location()