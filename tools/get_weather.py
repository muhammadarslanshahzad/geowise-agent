"""
    This tool fetches the current weather for a city using OpenStreetMap's 
    Nominatim and Open-Meteo APIs.
"""
import requests
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a city using OpenStreetMap's Nominatim and Open-Meteo APIs.
    """
    try:
        headers = {
            "User-Agent": "WeatherApp/1.0 (email@example.com)"  
        }

        # 1) Fetch coordinates from Nominatim
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        geocode_response = requests.get(geocode_url, headers=headers, timeout= 10)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if not geocode_data:
            return f"Could not find coordinates for '{city}'. Please check the city name."

        # Extract latitude and longitude
        lat = geocode_data[0]["lat"]
        lon = geocode_data[0]["lon"]

        # 2) Fetch weather data from Open-Meteo
        weather_url = (f"https://api.open-meteo.com/v1/forecast?"
                       f"latitude={lat}&longitude={lon}&current_weather=true")
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Extract weather details
        current_weather = weather_data["current_weather"]
        temperature = current_weather["temperature"]
        wind_speed = current_weather["windspeed"]

        return (
            f"The current weather in {city} is {temperature}°C"
            f"with a wind speed of {wind_speed} km/h."
        )

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
