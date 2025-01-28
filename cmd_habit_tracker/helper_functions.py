from typing import List
import cmd_habit_tracker.utils.aux as aux_funcs
from cmd_habit_tracker.db.models import Habit, Record
import cmd_habit_tracker.utils.data as data
import cmd_habit_tracker.db.db_operations as db
from pandas import DataFrame
from tabulate import tabulate
import itertools as its
from collections import defaultdict

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

def show_tracking_info(date: data.Date):
    records_of_date = db.get_all_track_info_of_date(date.string_format())
    if len(records_of_date) == 0:
        return
    habits = db.get_all_habits()
    table = {'Habit':[], 'Target': [], 'Achieved':[]} # columns are keys
    for rec in records_of_date:
        habit = get_habit_by_id(rec.habit_id, habits)
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




    
    
        

    