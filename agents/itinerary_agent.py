from langchain.agents import Tool

def get_itinerary_agent():
    def fetch_itinerary_request(query: str) -> str:
        if not query.strip():
            return "⚠️ No travel destination or preferences provided."

        # Simply return user's request so that agent+LLM will use it with the system prompt
        return f"🧳 Travel Itinerary Request: {query}"

    return Tool(
        name="itinerary_generator",
        func=fetch_itinerary_request,
        description="Takes user travel preferences and returns a basic request for the agent to build a detailed itinerary."
    )
