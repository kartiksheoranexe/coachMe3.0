import requests

# Create your scripts here.
APP_KEY = "ee44e667d2bd6504b36f6abddcdccea6"
APP_ID = "217598f8"

def fetch_food_info(food_name):
    API_URL = f"https://api.edamam.com/api/food-database/v2/parser?app_id={APP_ID}&app_key={APP_KEY}&ingr={food_name}" 
    response = requests.get(API_URL)
    food_info = response.json()
    return food_info

def auto_complete(string):
    API_URL = f"https://api.edamam.com/auto-complete?app_id={APP_ID}&app_key={APP_KEY}&q={string}&limit=10"
    response = requests.get(API_URL)
    food_info = response.json()
    return food_info

def nutrition_info(data):
    API_URL = f"https://api.edamam.com/api/food-database/v2/nutrients?app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.post(API_URL, json=data)
    nutrition_information = response.json()
    return nutrition_information