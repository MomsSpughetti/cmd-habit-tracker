import requests
from cmd_habit_tracker.utils.data import DOCUMENTATION
# import os module
import os
from cmd_habit_tracker.clogging.config import logger

# access environment variable
token = os.environ['HUGGING_FACE_TOKEN']

def answer_question_for_app_use(question: str):
    model_id = "deepset/roberta-base-squad2"
    API_URL = "https://api-inference.huggingface.co/models/" + model_id
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs" : {
            "question" : question,
            "context": DOCUMENTATION
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()['answer'] if 'answer' in response.json() else ""


def remove_thinking(s):
    key = "</think>"

    # find index of </think>
    idx = s.find(key)
    if idx != -1:  # make sure it exists
        result = s[idx + len(key):]
    else:
        result = s
    return result

def valid_response_structure(response):
    choices = response.get("choices")
    if choices == None:
        return False
    
    if len(choices) == 0:
        return False
    
    message = choices[0].get("message")

    if message == None:
        return False
    
    if message.get('content') == None:
        return False
    
    return True

def generate_single_habit(goal: str):
    model_id = "deepseek-ai/DeepSeek-R1:fireworks-ai"

    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {token}"}

    def query(payload):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger().error(e)
            print("Error: See log (run info command to get log location)")
        return response.json()
    
    question = f"""
                My goal: {goal}
                Suggest me only a single habit to achieve the previous goal.
                Write the habit with the following format, you must generate the habit with exact same format: 
                title: <>, 
                frequency: <pick one from the following formats: every day, every week, every month, every z days, every z weeks, every z months>, 
                period:<should represent number of days - must be included - and must be a number>, 
                target: <in this format: <amount - must be a single word> <metric - must be a single word>>,
                note: <A short note to make the user more motivated>

                An example of a well-formated habit (you should suggest the habit with the exact same format):
                title: Exercise
                frequency: every day
                period: 30 days
                target: 60 minutes
                note: Prioritize your physical and mental well-being.
                """
    response = query({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "model": model_id
    })

    if not valid_response_structure(response):
        logger().error("[generate_single_habit]: Error in response format. The response is \n")
        logger().error(response)
        return ""
    suggested_habit = remove_thinking(response["choices"][0]["message"]['content'])
    logger().info(suggested_habit)
    return suggested_habit