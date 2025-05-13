import streamlit as st
import requests
import pandas as pd

API_KEY = "8f0513552fb991ad098623e6d79f8426"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

ballparks = {'Fenway Park': (42.3467, -71.0972), 'Yankee Stadium': (40.8296, -73.9262), 'Rogers Centre': (43.6414, -79.3894), 'Camden Yards': (39.2839, -76.6217), 'Tropicana Field (Steinbrenner Field)': (27.9762, -82.5035), 'Progressive Field': (41.4965, -81.6852), 'Comerica Park': (42.339, -83.0485), 'Kauffman Stadium': (39.0517, -94.4803), 'Target Field': (44.9817, -93.2782), 'Guaranteed Rate Field': (41.8299, -87.6338), 'Minute Maid Park': (29.7573, -95.3555), 'Globe Life Field': (32.7513, -97.0822), 'T-Mobile Park': (47.5914, -122.3325), 'Angel Stadium': (33.8003, -117.8827), 'Oakland Athletics (Sutter Health Park)': (38.5803, -121.5136), 'Oracle Park': (37.7786, -122.3893), 'Dodger Stadium': (34.0739, -118.24), 'Petco Park': (32.7076, -117.1566), 'Chase Field': (33.4455, -112.0667), 'Coors Field': (39.756, -104.9942), 'Wrigley Field': (41.9484, -87.6553), 'Great American Ball Park': (39.0979, -84.5064), 'Miller Park': (43.028, -87.9712), 'PNC Park': (40.4469, -80.0057), 'Busch Stadium': (38.6226, -90.1928), 'Truist Park': (33.8908, -84.4679), 'LoanDepot Park': (25.7781, -80.2195), 'Citi Field': (40.7571, -73.8458), 'Nationals Park': (38.873, -77.0075), 'Citizens Bank Park': (39.9057, -75.1665)}

def get_weather(lat, lon):
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "imperial"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "Location": data.get("name", ""),
            "Temp (F)": data["main"]["temp"],
            "Conditions": data["weather"][0]["description"].title(),
            "Wind (mph)": data["wind"]["speed"]
        }
    else:
        return {
            "Location": f"Lat: {lat}, Lon: {lon}",
            "Error": "Could not fetch weather"
        }

st.title("MLB Ballpark Weather Tracker")

weather_data = []
for park, (lat, lon) in ballparks.items():
    weather = get_weather(lat, lon)
    weather["Ballpark"] = park
    weather_data.append(weather)

df = pd.DataFrame(weather_data)
st.dataframe(df)
