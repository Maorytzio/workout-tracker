import os
from datetime import datetime
import requests as requests
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

exercise_log = input("what exercises did you do + duration/distance?: ")

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
NU_response = requests.post(url=NU_endpoint, json=NU_params, headers=headers)

NU_data = NU_response.json()

date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

# print(f"Time:{time.split('.', 1)[0]}")
# print(f"Date:{date}")

post_endpoint = "https://api.sheety.co/33cf7bb2149a15daeb8c642346c5e378/myWorkouts/workouts"

header_sheety = {
    'Content-Type': 'application/json'
}

for exercise in NU_data["exercises"]:
    print(exercise)
    activity_name = exercise['name']
    duration = exercise['duration_min']
    calories = exercise['nf_calories']
    params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": activity_name,
            "duration": duration,
            "calories": calories,
        }
    }

    sheety_response = requests.post(url=post_endpoint, json=params, headers=header_sheety)
    sheety_response.raise_for_status()
    print(f"POST RESULT: {sheety_response.text}")
