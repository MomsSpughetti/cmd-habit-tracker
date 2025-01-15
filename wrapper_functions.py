import db.db_operations as db
import c_logging.logger as log
from utils.aux import get_new_habit, set_test_mode, get_goal, get_question, get_date, to_sql_date_foramt, show_tracking_info, get_choice
from helper_functions import track_date
from db.models import Habit
import utils.data as data
import exceptions.exceptions as exceptions
from pandas import DataFrame
from ai.ai_methods import generate_single_habit, answer_question_for_app_use


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

def initialize():
    try:
        initialize_logger()
        initialize_db()
    except Exception as e:
        print(e)
        close_app()

def initialize_for_testing():
    try:
        set_test_mode()
        initialize_db()
        clear_storage()
        initialize_logger()
        initialize_db()
    except Exception as e:
        print(e)
        close_app()

################################ Commands wrappers ################################
def add():
    """a function to add a new habit"""
    # ask the user to insert values
    new_habit = get_new_habit()
    try:
        db.add_habit(new_habit)
    except exceptions.DuplicateHabit as e:
        print(e)
    except Exception as e:
        print(e)

def help():
    """Prints all the possible commands with their usage"""
    print()
    for command_usage in data.Commands.get_commands().values():
        print(command_usage + "\n")


def progress(month: int, year: int):
    """Prints the progress of all habits for the specified month"""
    pass

def habits():
    [print(habit) for habit in db.get_all_habits()]


def generate():
    generate_new = 1
    while generate_new:
        goal = get_goal()
        suggested_habit = generate_single_habit(goal)
        print(suggested_habit)
        print()
        print("Do you want to add this habit?")
        answer = input()
        if answer.strip().lower() in ['yes', 'y']:
            db.add_habit(Habit.get_habit_from_str(suggested_habit).get_dict_column_value())
            print("Habit was added. Run 'habits' to see it")
            generate_new = 0
        else:
            print("Habit was not added, do you want to suggest a new habit?")
            answer = input()
            if answer.strip().lower() in ['yes', 'y']:
                generate_new = 1
            else:
                generate_new = 0

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
    pass


def track():
    print("Choose an option:")
    choice = get_choice([
        "Insert tracking info for yesterday",
        "Insert tracking info for a specific date"
    ])
    date = get_date() if choice == 1 else data.Date.get_yesterday()
    if date.in_future():
        print("Please enter a valid date (Not in the future)")
    else:
        try:
            track_date(date=date)
        except Exception as e:
            print(e)
    
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

    return command

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
        pass
    elif command == data.Commands.HABITS.value:
        habits()
    elif command == data.Commands.HELP.value:
        help()
    elif command == data.Commands.PROGRESS.value:
        pass
    elif command == data.Commands.UPDATE.value:
        pass
    elif command == data.Commands.EXIT.value:
        close_app()
    elif command == data.Commands.GENERATE.value:
        generate()
    elif command == data.Commands.DOCS.value:
        docs()
    else:
        return
