import wrapper_functions as wf
from utils.data import Habits
from db.db_operations import get_habit_by_title

def test_habit_addition(monkeypatch):
    wf.initialize_for_testing()
    inputs = iter(['Drinking water', '90', '4', '2', 'Liters', '1.5', 'Please listen to your past self'])
    monkeypatch.setattr('builtins.input', lambda _=None: next(inputs))
    wf.add()
    result = get_habit_by_title('Drinking water')
    print(result)
    result = result.get_dict()

    expected_result = {
        Habits.TITLE:'Drinking water', 
        Habits.PERIOD: '90', 
        Habits.FREQUENCY_FORMAT:'3', 
        Habits.FREQUENCY_AMOUNT:'2', 
        Habits.TARGET_METRIC:'Liters', 
        Habits.TARGET_AMOUNT:'1.5',
        Habits.NOTE:'Please listen to your past self'
    }
    for k in expected_result.keys():
        assert expected_result[k] == str(result[k])
    