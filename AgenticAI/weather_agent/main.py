from google.genai import Client
from dotenv import load_dotenv
import os
import requests
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = Client(api_key=api_key)


def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format = %C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong!!"

def main():
    user_query = input(">_ ")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_query
    )

    print(f"🤖: {response.text}")

print(get_weather("Satara"))
