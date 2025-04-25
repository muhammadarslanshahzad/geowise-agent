from langchain.agents import Tool
from services.hotel_service import search_hotels  # assumed DDG-based

def get_hotel_agent():
    def fetch_hotels(query: str) -> str:
        if not query.strip():
            return "⚠️ No hotel query provided."

        hotel_results = search_hotels(query)
        if not hotel_results:
            return "❌ No hotels found for this destination."

        formatted = []
        for res in hotel_results:
            title = res.get("title", "🏨 Hotel")
            desc = res.get("body", "")
            link = res.get("href", "")

            formatted.append(f"🏨 **{title}**\n{desc}\n🔗 {link}")

        return "\n\n".join(formatted) if formatted else "⚠️ No detailed hotel info available."

    return Tool(
        name="hotel_recommendation_tool",
        func=fetch_hotels,
        description="Fetches hotel options and descriptions for a given destination using DuckDuckGo."
    )
