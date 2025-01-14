
from utils.aux import get_habit_dictionary_str_keys, get_habit_dictionary, get_frequency_from_str, get_target_from_str, get_period, is_float
from exceptions.exceptions import CorruptedHabit, CorruptedRecord
from utils.data import Habits, FREQUENCY_DICT, Tracker
from collections import defaultdict

class Habit:
    def __init__(self):
        self.id = None
        self.title = None
        self.period = None
        self.start_date = None
        self.note = None
        self.frequency_format = None
        self.frequency_amount = None
        self.target_metric = None
        self.target_amount = None
    
    def is_habit_valid(self):
        return self.id and self.title and self.start_date and self.note and self.frequency_amount and self.frequency_format
    
    def get_dict(self):
        return get_habit_dictionary(
            id=self.id,
            title=self.title,
            start_date=self.start_date,
            period=self.period,
            note=self.note,
            freq_format=self.frequency_format,
            freq_amount=self.frequency_amount,
            target_metric=self.target_metric,
            target_amount=self.target_amount
        )
    
    def get_dict_column_value(self):
        return get_habit_dictionary_str_keys(
            id=self.id,
            title=self.title,
            start_date=self.start_date,
            period=self.period,
            note=self.note,
            freq_format=self.frequency_format,
            freq_amount=self.frequency_amount,
            target_metric=self.target_metric,
            target_amount=self.target_amount
        )
    
    def set_values_from_dict(self, habit_dict: defaultdict):
        """
        Parameters:
            A defaultdict(lambda: None) that have Enum:value pairs for habit table
        """
        self.id=habit_dict[Habits.ID]
        self.title = habit_dict[Habits.TITLE]
        self.start_date = habit_dict[Habits.START_DATE]
        self.period = habit_dict[Habits.PERIOD]
        self.note = habit_dict[Habits.NOTE]
        self.frequency_format = habit_dict[Habits.FREQUENCY_FORMAT]
        self.frequency_amount = habit_dict[Habits.FREQUENCY_AMOUNT]
        self.target_metric = habit_dict[Habits.TARGET_METRIC]
        self.target_amount = habit_dict[Habits.TARGET_AMOUNT]

    def set_habit_values(self, habit):
        """
        Parameters:
            habit - a tuple (id, title, start_date, period, note, freq_format, freq_amount, target_metric, target_amount)
        return value:
            a dict {<name1>:value1, ...}
        
            Note: This is a very sensitive function :) - its correctness is dependant on the order of columns in the definition of the habits' table - see queries.py
        """
        if habit == None or len(habit) < Habits.get_number_of_columns():
            raise CorruptedHabit()
        
        self.id=habit[0]
        self.title = habit[1]
        self.start_date = habit[2]
        self.period = habit[3]
        self.note = habit[4]
        self.frequency_format = habit[5]
        self.frequency_amount = int(habit[6])
        self.target_metric = habit[7]
        self.target_amount = float(habit[8]) if is_float(habit[8]) else None
    
    def get_habit_from_str(habit: str):
        """
        Parameters:
            habit - A string containing a habit in the following format:

                habit: ""
                frequency: every X [days|weeks|months|day|week|moth]
                period: Y days
                target per time: <amount> <metric>
                note: ""
        """
        habit_list = [line.split(':')[-1].strip() for line in habit.strip().split("\n")]
        habit_obj = Habit()
        frequency_amount, frequency_format = get_frequency_from_str(habit_list[1])
        target_amount, target_metric = get_target_from_str(habit_list[3])
        habit_dict = defaultdict(lambda: None)
        habit_to_partial_dict = get_habit_dictionary(
            title=habit_list[0],
            freq_amount=frequency_amount,
            freq_format=frequency_format,
            target_amount=target_amount,
            target_metric=target_metric,
            note=habit_list[-1],
            period=get_period(habit_list[2])
        )

        for key,value in habit_to_partial_dict.items():
            habit_dict[key] = value 

        habit_obj.set_values_from_dict(
            habit_dict
        )

        return habit_obj

    def __str__(self):
        """Returns a string representation of the Habit object in a human-readable format.

        Returns:
            str: A string representation of the Habit object.
        """

        return f"""
        - Title: {self.title}
        - Start Date (YYYY-MM-DD): {self.start_date}
        - Period: {self.period if self.period else "Not provided"}
        - Frequency: every{' '+str(self.frequency_amount)+' ' if self.frequency_amount > 1 else ' '}{FREQUENCY_DICT[self.frequency_format].split()[-1]}
        - Target: {str(self.target_amount) + " " + str(self.target_metric) if self.target_metric else "Not provided"}
        - Note: {self.note}
        """
    
class Record():
    def __init__(self):
        self.id = None
        self.habit_id = None
        self.date = None
        self.achieved = None
        self.explanation = None

    def set_record_values(self, record):
        """
        Parameters:
            record - a tuple (id, habit_id, date, achieved, explanation)
        return value:
            a dict {<name1>:value1, ...}
        
            Note: This is a very sensitive function :) - its correctness is dependant on the order of columns in the definition of the habits' table - see queries.py
        """
        if record == None or len(record) < Tracker.get_number_of_columns():
            raise CorruptedRecord()
        
        self.id=record[0]
        self.habit_id = record[1]
        self.date = record[2]
        self.achieved = record[3]
        self.explanation = record[4]
    
