import itertools as its
from collections import defaultdict
import os
from typing import List

from cmd_habit_tracker.db import operations as db
from cmd_habit_tracker.db.models import Habit, Record

from cmd_habit_tracker.utils import aux as aux_funcs
from cmd_habit_tracker.utils.aux import (
    get_new_habit,
    set_test_mode,
    get_goal,
    get_question,
    get_date,
    get_choice,
    get_year_and_month,
)
from cmd_habit_tracker.utils import data

from cmd_habit_tracker.exceptions import errors
from cmd_habit_tracker.ai.api import generate_single_habit, answer_question_for_app_use
from cmd_habit_tracker.clogging import config as log

from pandas import DataFrame
from tabulate import tabulate


def quick_test():
    # add()
    # print(db.get_habit_by_title('mama'))
    # generate_single_habit("I am suffering from bad sleeping, can you suggest me a habit to track so I can recover.")
    # reset()
    pass

################################ Main wrappers ################################

def welcome():
    print("Welcome to your personal habit tracker")

def initialize_logger():
    log.start_logger()
    log.set_level_debug()

def initialize_db():
    db.create_tables()

def close_app():
    exit(0)

def reset():
    """Removes database and initializes it again"""
    initialize()
    clear_storage()
    initialize()

def clear_storage():
    db.drop_db()

def refresh():
    db.refresh_tracker_table()

def initialize():
    try:
        # the following two lines are important in case the program was executed from a directory other than the one of the project
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        initialize_logger()
        initialize_db()
    except Exception as e:
        print(e)
        close_app()

def initialize_for_testing():
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        set_test_mode()
        initialize_db()
        clear_storage()
        initialize_logger()
        initialize_db()
    except Exception as e:
        print(e)
        close_app()



####################

######################################

def get_habits_for_date(date: data.Date):
    """
    Returns all the habits that make since to track for the given date based on habit.frequency
    Currently it returns all habits
    """
    return db.get_all_habits()

def get_habit_by_id(habit_id: int, habits: List[Habit]) -> Habit:
    for habit in habits:
        if habit.id == habit_id:
            return habit
    return Habit()

def make_table_by_range(habits : List[Habit], records : List[Record], min : int = 1, max : int = 31):
    table = {
        'Habit' : [h.title for h in habits],
    }
    for day in range(min, max+1):
        table[day] = []
        
    for date, recs in its.groupby(records, key=lambda r: r.date):
        day = date.split('-')[2]
        if int(day) > max or int(day) < min:
            continue
        recs = list(recs)
        recs.sort(key=lambda r: r.habit_id)
        for rec in recs:
                table[int(day)].append(rec.achieved)
    
    for column_name, values in table.items():
        if len(values) < len(habits):
            table[column_name] = table[column_name] + [0]*(len(habits)-len(values))
    
    table['Total'] = []
    table['Goal'] = []
    total = defaultdict(int)

    for rec in records:
        total[rec.habit_id] += rec.achieved
    
    for habit in habits:
        table['Total'].append(total[habit.id])
        target_metric = habit.target_metric if habit.target_metric else 'times'
        table['Goal'].append(str(habit.get_total_target(max)) + ' ' + target_metric)

    return table

def get_table_dict_of_records(records: List[Record], year, month):
    """
    returns two dicts
    first is from day 1-15
    second is from day 16-31
    """
    habits = db.get_all_habits()
    habits.sort(key=lambda h: h.id)
    max_day = data.Date.get_max_day(year=year, month=month)
    table = make_table_by_range(habits, records, max=max_day)

    table1 = {}
    table2 = {}

    for key, val in table.items():
        if key == 'Habit':
            table1[key] = val
            table2[key] = val
        elif key == 'Total' or key == 'Goal':
            table2[key] = val
        elif int(key) < 16:
            table1[key] = val
        else:
            table2[key] = val
    
    return table1, table2

############################ CLI UI

def get_tracking_info_for_unmeasurable_habit(habit: Habit, date: str):
    """Returns an object of class Record"""
    new_record = Record()
    print()
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
    print()
    print(f"Habit: {habit.title} - Date: {date}")
    question = f"How much have I completed out of {habit.target_amount} {habit.target_metric}?" if habit_is_measurable != None else f"Have I completed this habit at this date?"
    helper_strs = [f"out of {habit.target_amount}", "Yes/No"]
    print(question)
    answer = aux_funcs.get_float_bigger_than_from_input(0)
    explanation = ""
    if answer < habit.target_amount:
        print(f"Please provide an explanation of why you did not reach the target ({habit.target_amount} {habit.target_metric}):")
        explanation = aux_funcs.get_str_input()
    new_record.set_record_values((None, habit.id, date, answer, explanation))
    return new_record

def get_tracking_info_from_user_for_each_habit(habits: List[Habit], date: data.Date):
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

def show_tracking_info(date: data.Date):
    records_of_date = db.get_all_track_info_of_date(date.string_format())
    if len(records_of_date) == 0:
        return
    habits = db.get_all_habits()
    table = {'Habit':[], 'Target': [], 'Achieved':[]} # columns are keys
    for rec in records_of_date:
        habit = aux_funcs.get_habit_by_id(rec.habit_id, habits)
        table['Habit'].append(habit.title)
        table['Target'].append(' '.join([str(habit.get_target_amount()), habit.get_target_metric()]))
        table['Achieved'].append(rec.achieved)
    print(tabulate(DataFrame(table), headers = 'keys', tablefmt = 'psql') )

def track_date(date: data.Date):
    """Wrapper function that lets the user insert tracking information for a specific date"""
    # get date

    # show all tracking info from that date then show it
    show_tracking_info(date)

    # let the user choose
    print("\nPlease choose an option:")
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


################################ Commands wrappers ################################
def add():
    """a function to add a new habit"""
    # ask the user to insert values
    new_habit = get_new_habit()
    try:
        db.add_habit(new_habit)
    except errors.DuplicateHabit as e:
        print(e)
    except Exception as e:
        print(e)

def help():
    """Prints all the possible commands with their usage"""
    print()
    for command_usage in data.Commands.get_commands().values():
        print(command_usage + "\n")


def progress():
    """Prints the progress of all habits for the specified month"""
    year, month = get_year_and_month()
    print()
    table_dict1, table_dict2 = get_table_dict_of_records(records=db.get_tracked_info_by_month(year=year, month=month), year=year, month=month)
    print(tabulate(table_dict1, headers = 'keys', tablefmt = 'rounded_grid' ) )
    print(tabulate(table_dict2, headers = 'keys', tablefmt = 'rounded_grid' ) )

def habits():
    [print(habit) for habit in db.get_all_habits()]


import threading



def generate():
    generate_new = 1
    while generate_new:
        goal = get_goal()
        holder = data.Holder()
        t = threading.Thread(target=aux_funcs.animate, args=(holder,))
        t.start()
        suggested_habit_str = generate_single_habit(goal)
        holder.done = True 
        suggested_habit = Habit()
        suggested_habit.set_habit_from_str(suggested_habit_str)
        print(suggested_habit)
        print()
        print("Do you want to add this habit?")
        answer = input()
        if answer.strip().lower() in ['yes', 'y']:
            try:
                db.add_habit(suggested_habit.get_dict_column_value())
            except Exception as e:
                print(e)
                return
            print("Habit was added. Run 'habits' to see it")
            generate_new = 0
        else:
            print("Habit was not added, do you want to generate a new habit?")
            answer = input()
            if answer.strip().lower() in ['yes', 'y']:
                generate_new = 1
            else:
                generate_new = 0

def delete():
    """Deletes a habit"""
    available_habits = db.get_all_habits()
    print("Kindly choose the habit you want to delete:")
    options = [habit.title for habit in available_habits]+["Cancel"]
    choice = get_choice(options)
    if choice == len(options):
        print("No habits were deleted.")
        return
    db.delete_habit(available_habits[choice-1].id)
    print("Habit deleted successfully!")

def docs():
    question  = get_question()
    print(answer_question_for_app_use(question))

def command_not_found():
    print("Command not found. You can run `help` for more information.")
    print("")
    print("Do you have a specific question?")
    answer = input("Your answer (yes/no): ")
    if answer.strip().lower() in data.YES_ANSWERS:
        question  = input("\nWhat are you looking for?\nType here: ")
        print(answer_question_for_app_use(question))


def automatic_track():
    """Runs upon starting the program - let's user track todays info"""
    date=data.Date.get_yesterday()
    habits_count = len(db.get_all_habits())
    if habits_count == 0:
        print("Add habits to be tracked!\n")
    elif len(db.get_all_track_info_of_date(date.string_format())) != habits_count :
        track_date(date)
    else:
        print("Well done! Yesterday's tracking info were provided.\n")


def track():
    print("Choose an option:")
    choice = get_choice([
        "Insert tracking info for yesterday",
        "Insert tracking info for a specific date"
    ])
    date = get_date() if choice == 2 else data.Date.get_yesterday()
    if date.in_future():
        print("Please enter a valid date (Not in the future)")
    else:
        try:
            track_date(date=date)
        except Exception as e:
            print(e)

def clear():
    os.system("clear")

def info():
    print("Important files locations:")
    print(data.DATABASE)
    print(data.LOGFILE)
################################ Command handlers ################################

def get_command() -> str:
    """must be one of predefined commands, otherwise ask again"""
    command = input(">>> ").strip()
    while len(command) == 0:
        command = input("\n>>> ")
    main_command = command.split()[0]
    while main_command not in data.Commands.get_commands().keys():
        command_not_found()
        command = input(">>> ").strip()
        while len(command) == 0:
            command = input("\n>>> ")
        main_command = command.split()[0]

    return main_command

def execute_command(command: str):
    """
    parameters:
        command: a string containing the whole command
    """

    if command == data.Commands.ADD.value:
        add()
    elif command == data.Commands.TRACK.value:
        track()
    elif command == data.Commands.ARCHIVE.value:
        pass
    elif command == data.Commands.DELETE.value:
        delete()
    elif command == data.Commands.HABITS.value:
        habits()
    elif command == data.Commands.HELP.value:
        help()
    elif command == data.Commands.PROGRESS.value:
        progress()
    elif command == data.Commands.UPDATE.value:
        pass
    elif command == data.Commands.EXIT.value:
        close_app()
    elif command == data.Commands.GENERATE.value:
        generate()
    elif command == data.Commands.DOCS.value:
        docs()
    elif command == data.Commands.CLEAR.value:
        clear()
    elif command == data.Commands.INFO.value:
        info()
    else:
        return
