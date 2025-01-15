import utils.aux as aux_funcs
from db.models import Habit, Record
import utils.data as data
import db.db_operations as db

def get_tracking_info_for_unmeasurable_habit(habit: Habit, date: str):
    """Returns an object of class Record"""
    new_record = Record()
    print(f"Habit: {habit.title} - Date: {date}")
    question = f"Have I completed this habit at this date?"
    print(question)
    print(f"Answer (Yes/No): ")
    answer = aux_funcs.get_yes_no_answer()
    achieved = 1 if answer else 0
    explanation = ""
    if not achieved:
        print("Please provide an explanation of why not:")
        explanation = aux_funcs.get_str_input()
    new_record.set_record_values((None, habit.id, date, achieved, explanation))
    return new_record

def get_tracking_info_for_measurable_habit(habit: Habit, date: str):
    """Returns an object of class Record"""
    new_record = Record()
    habit_is_measurable = habit.target_amount != None
    print(f"Habit: {habit.title} - Date: {date}")
    question = f"How much have I completed out of {habit.target_amount} {habit.target_metric}?" if habit_is_measurable != None else f"Have I completed this habit at this date?"
    helper_strs = [f"out of {habit.target_amount}", "Yes/No"]
    print(question)
    answer = aux_funcs.get_number_from_input(0, 9999)
    explanation = ""
    if answer < habit.target_amount:
        print(f"Please provide an explanation of why you did not reach the target ({habit.target_amount} {habit.target_metric}):")
        explanation = aux_funcs.get_str_input()
    new_record.set_record_values((None, habit.id, date, answer, explanation))
    return new_record

def get_tracking_info_from_user_for_each_habit(habits: list[Habit], date: data.Date):
    """
    Asks the user if he completed a habit for each habit in habits
    params:
            - habits - a list of Habit objects
            - date - an object of type Date
    return value:
            - list of dicts of pairs <column name>:<value> for the table `Tracker`
    """
    records = [Record()]
    records.clear()
    for habit in habits:
        if habit.target_amount == None:
            records.append(get_tracking_info_for_unmeasurable_habit(habit, date.string_format()))
        else:
            records.append(get_tracking_info_for_measurable_habit(habit, date.string_format()))
    return [record.get_dict_column_value() for record in records]
    
def get_habits_for_date(date: data.Date):
    """
    Returns all the habits that make since to track for the given date based on habit.frequency
    Currently it returns all habits
    """
    return db.get_all_habits()


def track_date(date: data.Date):
    """Wrapper function that lets the user insert tracking information for a specific date"""
    # get date

    # get all tracking info from that date then show it
    records_of_date = db.get_all_track_info_of_date(date.string_format())
    aux_funcs.show_tracking_info(records_of_date, date.string_format())

    # let the user choose
    option = aux_funcs.get_choice(data.Tracking_options.get_options())
    #   track all habits again at this date
    if option == data.Tracking_options.TRACK_ALL.value:
        habits = get_habits_for_date(date)
        db.insert_tracking_info_for_a_specific_date(get_tracking_info_from_user_for_each_habit(habits, date))

    elif option == data.Tracking_options.EXIT.value:
        print("Operation stopped!")
    else:
        #   track only the habits that were not tracked at this date
        #   track a specific habit
        print("Not supported yet!")