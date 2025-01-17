"""
    Weather tool
"""
import os
from dotenv import load_dotenv
from langchain.agents import tool

from services import WeatherService

load_dotenv()
weather_service = WeatherService(api_key=os.getenv('WEATHER_API_KEY'))

@tool
def live_weather(city: str) -> str:
    """
        Fetches the live weather of the given city
    """
    try:
        city = city.strip().strip("'\"")
        weather_data = weather_service.get_weather(city)
        description = weather_data.get('weather', [{}])[0].get('description', 'No description')
        temp = weather_data.get('main', {}).get('temp', 'N/A')
        if temp != 'N/A':
            temp = round(temp)
        return f"The current weather in {city} is {description} with a temperature of {temp}°C."
    except (ConnectionError, TimeoutError, ValueError) as e:
        return f"Error fetching weather: {str(e)}"
