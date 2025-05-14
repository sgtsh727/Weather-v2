
import streamlit as st
import requests
import pandas as pd
import math
import json

# Load ballpark data
with open("ballparks_data.json", "r") as f:
    ballparks = json.load(f)

API_KEY = "8f0513552fb991ad098623e6d79f8426"

def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def wind_relative_direction(wind_deg, park_orientation):
    angle = (wind_deg - park_orientation + 360) % 360
    if angle <= 45 or angle >= 315:
        return "Out"
    elif 135 <= angle <= 225:
        return "In"
    elif 45 < angle < 135:
        return "To RF"
    else:
        return "To LF"

def wind_arrow(angle):
    arrows = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']
    return arrows[round(angle % 360 / 45) % 8]

st.set_page_config(page_title="MLB Ballpark Weather", layout="wide")
st.title("MLB Ballpark Weather Tracker - Chart View")

# Gather weather data
rows = []
for park, data in ballparks.items():
    weather = fetch_weather(*data["coords"])
    if not weather:
        continue
    row = {
        "Ballpark": park,
        "Indoor": "Yes" if data["indoor"] else "No",
        "Temp (F)": weather["main"]["temp"] if not data["indoor"] else None,
        "Humidity (%)": weather["main"]["humidity"] if not data["indoor"] else None,
        "Wind (mph)": weather["wind"]["speed"] if not data["indoor"] else None,
        "Wind Dir": None,
        "Wind Arrow": None,
        "Logo": f"![]({data['logo']})"
    }
    if not data["indoor"]:
        wind_deg = weather["wind"]["deg"]
        row["Wind Dir"] = wind_relative_direction(wind_deg, data["orientation"])
        row["Wind Arrow"] = wind_arrow((wind_deg - data["orientation"]) % 360)
    rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Reorder and display
df = df[["Ballpark", "Indoor", "Temp (F)", "Humidity (%)", "Wind (mph)", "Wind Arrow", "Wind Dir"]]
st.dataframe(df, use_container_width=True)
