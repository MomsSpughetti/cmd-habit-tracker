
import pandas as pd
import sqlite3
from faker import Faker
import db.tools as tools
import os
import db.queries as queries
import c_logging.logger as log
import exceptions.exceptions as exceptions
import db.models as models


def execute_query(query, params=''):
    """
    Execute a query on the db
    
    Parmeters:
        query: a string containing the query in sql format
        params: a dictionary of values {<name>: value}, in the query string, value will be
                added where there is :<name> in the query
    """
    result = None
    try:
        with sqlite3.connect(tools.DATABASE) as connection:
            connection.set_trace_callback(log.logger().info)
            cursor = connection.cursor()
            cursor.execute(query, (params))
            result = cursor.fetchall()
            connection.commit()
    except Exception as e:
         connection.rollback()
         log.logger().error(f"Error executing the following query: \n {query} \n Error message: {e}")
         raise Exception("An error occured - see log file")
    
    return result

def executemany_query(query, params=''):
    """
    Execute a query on the db
    
    Parmeters:
        query: a string containing the query in sql format
        params: a list of dictionaries of values {<name>: value}, in the query string, value will be
                added where there is :<name> in the query
        note that the query will be ran once on every elemnt of the list.
    """
    result = None
    try:
        with sqlite3.connect(tools.DATABASE) as connection:
            connection.set_trace_callback(log.logger().info)
            cursor = connection.cursor()
            cursor.executemany(query, tuple(params))
            result = cursor.fetchall()
            connection.commit() 
    except Exception as e:
         connection.rollback()
         log.logger().error(f"Error executing the following query: \n {query} \n Error message: {e}")
         raise Exception("An error occured - see log file")
    
    return result


def create_tables():
        execute_query(queries.habits_table_creation_query())
        execute_query(queries.tracker_table_creation_query())
        execute_query(queries.archived_habits_table_creation_query())
    
        
def drop_db():
    if os.path.exists(tools.DATABASE):
         os.remove(tools.DATABASE)


def drop_tables():
    execute_query(queries.drop_tables_query())




# basic operations for table 'habits'

def get_habit(id: int):
    """
    @Parameters:
        id -> the id of the target habit
    
    @ return value:
        ????? 
    """
    return execute_query(queries.get_habit_query(), {'id': id})

def get_habit_by_title(habit_title: str) -> models.Habit:
    """
    return value:
        an object of models.Habit class
    """
    results = execute_query(queries.get_habit_by_title_query(), {f'{tools.Habits.TITLE.value}': habit_title})
    if len(results) == 0:
        raise exceptions.HabitNotFound(habit_title=habit_title)
    
    habit = models.Habit()
    habit.set_habit_values(results[0])
    return habit

def get_all_habits():
    """
    Returns a list of models.Habit objects
    """
    results = execute_query(queries.get_all_habits())
    habits = [models.Habit() for _ in results]
    [habit.set_habit_values(res) for habit, res in zip(habits, results)]
    return habits


def add_habit(habit):
    """
     add a new habit to the database
     Parameters:
            habit -> a dictionary of column:value
    you can get column names using tools.habits
    """
    # check if habit of the same title existd
    if(len(execute_query(queries.get_habits_by_title(), (habit))) > 0):
        raise exceptions.DuplicateHabit()

    execute_query(queries.add_habit_query(), habit)



# Basic operations for table 'tracker'





