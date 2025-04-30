# agents/weather_tool.py
from langchain.agents import Tool
from pydantic import BaseModel, Field
from services.weather_service import get_weather_summary

# 🧠 Pydantic schema for structured input
class WeatherInputSchema(BaseModel):
    city: str = Field(description="City to get the current weather for.")

# 🌤️ LangChain Tool
live_weather = Tool(
    name="weather_summary",
    func=get_weather_summary,
    description="Returns a simple weather summary for any city using online search. Example: 'Weather in Berlin'",
    args_schema=WeatherInputSchema,
    return_direct=True
)
