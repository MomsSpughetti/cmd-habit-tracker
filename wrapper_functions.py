import db.db_operations as db
import c_logging.logger as log
from db.tools import get_new_habit, Commands, set_test_mode
import db.tools as tools
import exceptions.exceptions as exceptions
from pandas import DataFrame
from ai.ai_methods import generate_habit


def quick_test():
    # add()
    # print(db.get_habit_by_title('mama'))
    generate_habit("I am suffering from bad sleeping, can you suggest me a habit to track so I can recover.")
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
        close_app()

def help():
    """Prints all the possible commands with their usage"""
    print()
    for command_usage in Commands.get_commands().values():
        print(command_usage + "\n")

def ask():
    """
    Will ask the user about each habit if he completed yesterday, 
    if he already answered those or there are no habits => tell the user
    """

    # get habits

    # if no habits print
    # get rows in the table named tracker with yesterday's date
    # if there are rows ? in the last query =? ask about the habkits that are not there
    try:
        print(DataFrame(db.get_all_habits()))
    except Exception as e:
        print(e)
        close_app()

def progress(month: int, year: int):
    """Prints the progress of all habits for the specified month"""
    pass

def habits():
    [print(habit) for habit in db.get_all_habits()]


def generate():
    generate_new = 1
    while generate_new:
        goal = tools.get_goal()
        suggested_habit = generate_habit(goal)
        print(suggested_habit)
        print()
        print("Do you want to add this habit?")
        answer = input()
        if answer.strip().lower() in ['yes', 'y']:
            db.add_habit(tools.get_habit_from_str(suggested_habit).get_dict_column_value())
            print("Habit was added. Run 'habits' to see it")
            generate_new = 0
        else:
            print("Habit was not added, do you want to suggest a new habit?")
            answer = input()
            if answer.strip().lower() in ['yes', 'y']:
                generate_new = 1


################################ Command handlers ################################

def get_command() -> str:
    """must be one of predefined commands, otherwise ask again"""
    command = input(">>> ").strip()
    while len(command) == 0:
        command = input("\n>>> ")
    main_command = command.split()[0]
    while main_command not in Commands.get_commands().keys():
        print("Command not found. Use the command 'help' to see possible Commands.\n")
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

    if command == Commands.ADD.value:
        add()
    elif command == Commands.TRACK.value:
        pass
    elif command == Commands.ARCHIVE.value:
        pass
    elif command == Commands.DELETE.value:
        pass
    elif command == Commands.HABITS.value:
        habits()
    elif command == Commands.HELP.value:
        help()
    elif command == Commands.PROGRESS.value:
        pass
    elif command == Commands.UPDATE.value:
        pass
    elif command == Commands.EXIT.value:
        close_app()
    else:
        return