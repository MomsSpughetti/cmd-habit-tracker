from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
from utils.data import DOCUMENTAION
# import os module
import os
from db.db_operations import add_habit
from db.models import Habit
from random import randint

# access environment variable
token = os.environ['HUGGING_FACE_TOKEN']

def answer_question_for_app_use(question: str):
    model_id = "deepset/roberta-base-squad2"
    model_id2 = "mistralai/Mistral-7B-Instruct-v0.2"
    API_URL = "https://api-inference.huggingface.co/models/" + model_id
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs" : {
            "question" : question,
            "context": DOCUMENTAION
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json())

def generate_single_habit(goal: str):
    # https://api-inference.huggingface.co/models/<MODEL_ID>

    model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    model_id2 = "mistralai/Mistral-7B-Instruct-v0.2"
    API_URL = "https://api-inference.huggingface.co/models/" + model_id2
    headers = {"Authorization": "Bearer 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"}
    payload = {
        
        "inputs": f"""
                    My goal: {goal}
                    Suggest me a habit to achieve the previous goal.
                    Write the habit with the following format: 
                    title: <>, 
                    frequency: <pick one from the following formats: every day, every week, every month, every z days, every z weeks, every z months>, 
                    period:<should represent number of days>, 
                    target per time: <in this format: <amount> <metric>>,
                    note: <A note to make the user more motivated>

                    For example, to make the structure clear, it should be something like this:
                    title: running 1 mile
                    frequency: every 3 days
                    period: 90 days
                    target per time: 1 miles
                    note: See your granpa, his health is bad, so do not be like him, play sports and keep healthy
                    Please just write the habit, not any other text, provide an output as the provided template
                    """,
        "parameters": {
            'seed': randint(1,100)
        }
    }


    response = requests.post(API_URL, headers=headers, json=payload)
    suggested_habit = response.json()[0]['generated_text'][len(payload['inputs']):]
    return suggested_habit