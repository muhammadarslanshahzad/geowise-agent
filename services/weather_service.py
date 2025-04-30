import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_summary(city: str) -> str:
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return f"⚠️ Could not get weather data for {city}."

    data = response.json()
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]

    return (
        f"🌤️ **Weather in {city.title()}**:\n"
        f"- Temperature: **{temp}°C**\n"
        f"- Condition: **{condition}**\n"
        f"- Humidity: **{humidity}%**"
    )
