import streamlit as st
import requests
import pandas as pd

# Replace with your actual API key
API_KEY = "your_openweathermap_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# MLB Ballparks and Cities
ballparks = {
    "Fenway Park": "Boston",
    "Yankee Stadium": "New York",
    "Wrigley Field": "Chicago",
    "Dodger Stadium": "Los Angeles",
    "Coors Field": "Denver"
}

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "City": city,
            "Temp (F)": data["main"]["temp"],
            "Conditions": data["weather"][0]["description"].title(),
            "Wind (mph)": data["wind"]["speed"]
        }
    else:
        return {"City": city, "Error": "Could not fetch weather"}

st.title("MLB Ballpark Weather Tracker")

weather_data = [get_weather(city) for city in ballparks.values()]
df = pd.DataFrame(weather_data)

st.dataframe(df)
