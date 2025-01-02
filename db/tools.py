from enum import Enum
import math

DATABASE = "habit_tracker.db"

class Errors(Enum):
    DUPLICATE_HABIT = 0

ERROR_MESSAGES = {
    Errors.DUPLICATE_HABIT: "Habit was not added because it already exists"
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

    # for tracking
    TRACK = "track" # provide tracking info for a specific date

    def get_commands():
        """returns a dict(str, str) of all possible commands - command: <usage>"""
        return {
            Commands.ADD.value: "add - to add a new habit",
            Commands.ARCHIVE.value: "Not available",
            Commands.DELETE.value: "Not available",
            Commands.HABITS.value: "Not available",
            Commands.HELP.value: "Not available",
            Commands.PROGRESS.value: "progress <Year> <Month> - Shows the progress for a specific month",
            Commands.UPDATE.value: "Not available",
            Commands.TRACK.value: "Not available",
            Commands.EXIT.value: "exit"
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


def get_habit_dictionary(title: str, period: int, note: str, freq_format: int, freq_amout, target_metric: str, target_amount: int):

    return {
        Habits.TITLE.value: title.strip(),
        Habits.PERIOD.value: period,
        Habits.NOTE.value: note.strip(),
        Habits.FREQUENCY_FORMAT.value: freq_format,
        Habits.FREQUENCY_AMOUNT.value: freq_amout,
        Habits.TARGET_METRIC.value: target_metric.strip(),
        Habits.TARGET_AMOUNT.value: target_amount
    }

def get_number_from_input(min=1, max=math.inf):
    num = input().strip()
    while not num.isdigit() or int(num) < min or int(num) > max:
        num = input(f"Please provide a number between {min} and {max}\n")
    return int(num)

def get_frequency_amount(freq_format: int):
    if freq_format in Frequency.get_single_freq_amount():
        return 1
    every_z_amount_of_what = FREQUENCY_DICT[freq_format].split()[2] # days / weeks / months
    print(f"You have chosen to do this habit every certain amount of {every_z_amount_of_what}")
    print("Please insert the desired amount:")

    if freq_format == Frequency.EVERY_Z_DAYS.value:
        return get_number_from_input(min=1, max=6)
    elif freq_format == Frequency.EVERY_WEEK:
        return get_number_from_input(min=1, max=3)
    else: # freq_format = Frequency.EVERY_MONTH
        return get_number_from_input(min=1, max=12)
    

def get_frequency():
    """return value: (freq_format, freq_amount) - see Frequency.py to understand"""
    print("What is the frequency of this habit?")
    max_freq_enum_val = max(FREQUENCY_DICT.keys())
    options = [str(idx+1)+". "+FREQUENCY_DICT[idx] for idx in range(0, max_freq_enum_val+1)]
    for option in options:
        print(option)
    print("Please insert the number of the desired option:")
    freq_format = get_number_from_input(min=1, max=max_freq_enum_val+1)-1
    freq_amount = get_frequency_amount(freq_format)
    return (freq_format, freq_amount)
    

def get_target():
    """Return value: (target_metric, target_amount) - e.g, (hours, 10)"""
    print("(Optional) What is the metric for this habit? (e.g, pages, mins, hours, miles, person)")
    print("Press Enter to skip")
    metric = input().strip()
    if len(metric) == 0:
        return (None, None)
    print(f"Please insert the target amount of this habit (in {metric}):")
    target = get_number_from_input(min=1)
    return (metric, target)


def get_new_habit():
    # get title
    print("Describe the habit in a few words:")
    title = input()
    # get period
    print("How many days you want to do this habit? If not sure skip by pressing Enter")
    period = input().strip()

    while len(period) > 0 and not period.isdigit():
        period = input("Please provide a valid number of days. If not sure skip by pressing Enter\n").strip()
    
    period_converted = int(period) if len(period) > 0 else None

    # get frequency
    frequency_format, frequency_amount = get_frequency()

    # get target
    target_metric, target_amount = get_target()

    # get note
    print("If you have a note for your future self, please provide it, otherwise press enter")
    note = input()

    return get_habit_dictionary(title=title, 
                                period=period_converted, 
                                note=note, 
                                freq_format=frequency_format, 
                                freq_amout=frequency_amount, 
                                target_metric=target_metric, 
                                target_amount=target_amount)
