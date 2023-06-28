import os
from dotenv import load_dotenv
from datetime import datetime
import requests

load_dotenv()
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
BEARER = os.getenv("BEARER")


def get_nutrition_info():
    NU_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise/"

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "x-remote-user-id": "0",
    }
    NU_params = {
        "query": exercise_log,
        "gender": "male",
        "weight_kg": "72",
        "height_cm": "175",
        "age": "30",
    }
    return requests.post(url=NU_endpoint, json=NU_params, headers=headers).json()


def send_data_to_sheet(workout):
    sheety_post_endpoint = "https://api.sheety.co/33cf7bb2149a15daeb8c642346c5e378/myWorkouts/workouts"

    header_sheety = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {BEARER}"
    }

    activity_name = workout['name']
    duration = workout['duration_min']
    calories = workout['nf_calories']
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%X")

    params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": activity_name,
            "duration": duration,
            "calories": calories,
        }
    }

    sheety_response = requests.post(url=sheety_post_endpoint, json=params, headers=header_sheety)
    sheety_response.raise_for_status()


exercise_log = input("what exercises did you do + duration/distance?: ")

NU_data = get_nutrition_info()
exercises_data = NU_data["exercises"]

for exercise in exercises_data:
    send_data_to_sheet(exercise)
