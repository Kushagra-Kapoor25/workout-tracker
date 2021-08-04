import os
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
BEARER_AUTH_KEY = os.getenv("BEARER_AUTH_KEY")

headers_for_nutritionix = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_params = {
    "query": input("Tell me which exercise you did:"),
    "gender": os.getenv("GENDER"),
    "weight_kg": int(os.getenv("WEIGHT")),
    "height_cm": int(os.getenv("HEIGHT")),
    "age": int(os.getenv("AGE")),
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers_for_nutritionix)
data = response.json()["exercises"]

today = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%H:%M:%S")


workout_sheet_endpoint = "https://api.sheety.co/22271f0b672b0caa44a563f53e425469/workoutTracking/workouts"

headers_for_sheet = {
    "Authorization":BEARER_AUTH_KEY
}

for exercise in data:
    sheet_params = {
        "workout": {
            "date": today,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=workout_sheet_endpoint, json=sheet_params, headers=headers_for_sheet)
    print(sheet_response.text)