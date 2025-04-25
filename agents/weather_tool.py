from langchain.agents import Tool
from services.weather_service import get_weather_summary

live_weather = Tool(
    name="weather_summary",
    func=get_weather_summary,
    description="Returns a simple weather summary for any city using online search. Example: 'Weather in Berlin'"
)
