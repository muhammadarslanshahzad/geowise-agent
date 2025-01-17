"""
    Time Tool
"""
from langchain.agents import tool

from services import TimeService

time_service = TimeService()

@tool
def current_time(city: str) -> str:
    """Fetches the current local time for a given timezone."""
    try:
        time_data = time_service.get_local_time(city)
        datetime = time_data.get('local_time', 'N/A')
        timezone = time_data.get('timezone', 'N/A')
        return f"The current time in {city} is {datetime}."
    except (ConnectionError, TimeoutError, ValueError) as e:
        return f"Error fetching weather: {str(e)}"
