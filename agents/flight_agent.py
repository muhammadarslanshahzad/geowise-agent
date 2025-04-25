from langchain.agents import Tool
import os
from dotenv import load_dotenv
from services.flight_service import search_flights

load_dotenv()

def get_flight_agent():
    def fetch_flights(query: str) -> str:
        if not query.strip():
            return "⚠️ No flight query provided."

        flight_results = search_flights(query)
        if not flight_results:
            return "❌ No flights found. Please try a different route."

        formatted = []
        for res in flight_results:
            title = res.get("title", "✈️ Flight Option")
            link = res.get("href", "")
            snippet = res.get("body", "")

            formatted.append(f"✈️ **{title}**\n{snippet}\n🔗 {link}")

        if not formatted:
            return "⚠️ No usable flight data found."

        return "\n\n".join(formatted)

    return Tool(
        name="flight_recommendation_tool",
        func=fetch_flights,
        description="Fetches flight search snippets from Google Flights using DuckDuckGo."
    )
