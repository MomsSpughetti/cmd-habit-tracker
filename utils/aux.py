import math
from collections import defaultdict
from exceptions.exceptions import CorruptedInput
from utils.data import Habits, FREQUENCY_DICT, Frequency, YES_ANSWERS, Tracker, Date
from datetime import date
from calendar import monthrange
from pandas import DataFrame

def set_test_mode():
    global TEST_MODE
    TEST_MODE = 1
    global DATABASE
    DATABASE = "habit_tracker_test.db"

def get_habit_dictionary(title: str, period: int, note: str, freq_format: int, freq_amount, target_metric: str, target_amount: int, id=None, start_date=None) -> dict:
    """Returns a dictionary where the keys are Enums"""
    return {
        Habits.ID: id,
        Habits.TITLE: title,
        Habits.START_DATE: start_date,
        Habits.PERIOD: period,
        Habits.NOTE: note,
        Habits.FREQUENCY_FORMAT: freq_format,
        Habits.FREQUENCY_AMOUNT: freq_amount,
        Habits.TARGET_METRIC: target_metric,
        Habits.TARGET_AMOUNT: target_amount
    }

def get_habit_dictionary_str_keys(title: str, period: int, note: str, freq_format: int, freq_amount, target_metric: str, target_amount: int, id=None, start_date=None):
    """Returns a dictionary where the keys are string - names of columns"""
    return {
        Habits.ID.value: id,
        Habits.TITLE.value: title,
        Habits.START_DATE.value: start_date,
        Habits.PERIOD.value: period,
        Habits.NOTE.value: note,
        Habits.FREQUENCY_FORMAT.value: freq_format,
        Habits.FREQUENCY_AMOUNT.value: freq_amount,
        Habits.TARGET_METRIC.value: target_metric,
        Habits.TARGET_AMOUNT.value: target_amount
    }

def get_record_dictionary_str_keys(habit_id: int, date: str, achieved: int, explanation: str, id=None):
    return {
        Tracker.ID.value: id,
        Tracker.HABIT_ID: habit_id,
        Tracker.DATE: date,
        Tracker.ACHIEVED: achieved,
        Tracker.EXPLANATION: explanation
    }

def get_number_from_input(min=1, max=math.inf):
    num = input().strip()
    while not num.isdigit() or int(num) < min or int(num) > max:
        num = input(f"Please provide a number >= {min} {"" if max == math.inf else "and <="+max}\n")
    return int(num)

def is_float(num):
    try:
        float(num)
    except Exception as e:
        return False
    return True

def get_float_bigger_than_from_input(min=1):
    num = input().strip()
    while not is_float(num) or float(num) < min:
        num = input(f"Please provide a number >= {min}\n")
    return float(num)

def get_frequency_amount(freq_format: int):
    if freq_format in Frequency.get_single_freq_amount():
        return 1
    every_z_amount_of_what = FREQUENCY_DICT[freq_format].split()[-1] # days / weeks / months
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
    target = get_float_bigger_than_from_input(min=0) # if someone want to quit smoking - he can set to smoke 0 cigarettes :)
    return (metric, target)

def get_title():
    print("Describe the habit in a few words:")
    title = input().strip()
    while len(title) == 0:
        input("Please provide a valid title:\n")
    return title

def get_new_habit():
    # get title
    title = get_title()

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

    return get_habit_dictionary_str_keys(title=title, 
                                period=period_converted, 
                                note=note, 
                                freq_format=frequency_format, 
                                freq_amount=frequency_amount, 
                                target_metric=target_metric, 
                                target_amount=target_amount)


def get_frequency_from_str(freq: str):
    """
    frequency: every X [days|weeks|months|day|week|moth]
    Return value:
        (amount, frequency_enum_value)
    """
    frequency_parts = freq.split()
    if len(frequency_parts) == 2:
        return (1, Frequency.get_freq_enum(frequency_parts[1]))
    if len(frequency_parts) != 3 or not frequency_parts[1].isdigit():
        raise CorruptedInput(freq)
    return (int(frequency_parts[1]), Frequency.get_freq_enum(frequency_parts[2]))
    
def get_target_from_str(target: str):
    """
    format of target: amount metric
    Return value: 
        (target_amount, target_metric)
    """
    target_parts = target.strip().split()
    if len(target_parts) != 2 or not is_float(target_parts[0]):
        return CorruptedInput(target)
    return (float(target_parts[0]), target_parts[1])

def get_period_from_str(period: str):
    """
    Parameters: a string of the format X days
    Return value: an int representing the amount of days
    """
    period_parts = period.strip().split()
    if len(period_parts) != 2:
        return CorruptedInput(period)
    if not period_parts[0].isdigit():
        return CorruptedInput
    return int(period_parts[0])


def get_goal():
    print("Please describe your goal (e.g, sleeping well)")
    goal = input().strip()
    return goal

def get_question():
    print("Here you can ask a question to know more about how to use this app.")
    print("In order to get better results, please ask in a question format, and be as detailed as possible.")
    question = input("My question: ")
    return question.strip()

def get_period(period: str):
    """Parameters:
        period - a string containg a number as the first word after calling split()
        if second word exists and days, then will return None
    
        Return value:
            an int representing the period in days
    """
    period_parts = period.split()
    if not period_parts[0].isdigit():
        return None
    elif len(period_parts) > 1 and period_parts[1] != 'days':
        return None
    else:
        return period_parts[0]

def get_year():
    print("Year:")
    year = input().strip()
    current_date = date.today()
    while not year.isdigit() or int(year) < 2024 or int(year) > current_date.year:
        print("Please enter a valid year (not in the future):\n")
        year = input().strip()
    
    return int(year)

def get_month(year: int):
    print("Month:")
    month = input().strip()
    while not month.isdigit() or int(month) > 12 or int(month) < 1:
        print("Please enter a valid month:\n")
        month = input().strip()
    
    return int(month)

def get_day(year: int, month: int):
    """params: valid year and month - gets a valid day for that specific month-year"""
    print("Month:")
    day = input().strip()
    max_day = monthrange(year=year, month=month)[1]
    while not day.isdigit() or int(day) > max_day or int(day) < 1:
        print(f"Please enter a valid day: (1 - {max_day})\n")
        day = input().strip()
    
    return int(day)

def get_date():
    """returns a tuple (year, month, day)"""
    print("Enter the date:")
    year = get_year()
    month = get_month()
    day = get_day(year, month)
    date = Date()
    date.set_date(year, month, day)
    return date

def to_sql_date_foramt(year, month, day) -> str:
    """YYYY-MM-DD"""
    day_formated = str(day)
    if day < 10:
        day_formated = '0'+day_formated

    month_formated = str(month)
    if month < 10:
        month_formated = '0'+month_formated

    return year+'-'+month_formated+'-'+day_formated


def show_tracking_info(info: list, date):
    # show the info (if exists)
    print(f"Tracking info from {date}:\n")
    if len(info) > 0:
        print(DataFrame(info))
    else:
        print("There is no tracking info for this date!")

def get_choice(options: list[str]):
    options_dict = {}
    for idx, option in enumerate(1, options):
        options_dict[idx] = option
    [print(f"{idx} {option}" for idx, option in options_dict.items())]
    choice = get_number_from_input(1, len(options))
    return choice

def get_yes_no_answer():
    """Returns a boolean that corresponds to the user input"""
    answer = input()
    if answer.strip().lower() in YES_ANSWERS:
        return True
    return False

def get_str_input():
    return input().strip().lower()