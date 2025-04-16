from langchain.agents import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from services.hotel_service import search_hotels  # optional, but cool for realism

def get_hotel_agent():
    model = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME")
    )

    def analyze_hotels(query: str) -> str:
        # Step 1: Run a live search (optional, or you can pass query directly)
        search_results = search_hotels(query)
        formatted_results = []
        for result in search_results:
            title = result.get("title", "No title")
            snippet = result.get("body", "")
            link = result.get("href", "")
            formatted_results.append(f"🏨 {title}\n{snippet}\n🔗 {link}")
        combined_text = "\n\n".join(formatted_results)

        # Step 2: Ask Gemini to analyze and recommend
        prompt = f"""
            You are a Hotel Recommendation Expert.

            Analyze the following hotel options for: "{query}"

            {combined_text}

            Recommend the best hotel based on:
            - 🏷️ Price
            - 🌟 Rating
            - 📍 Location
            - 🛏️ Amenities
            - 🧼 Cleanliness
            - 👥 User reviews (if mentioned)

            Return your result in well-formatted markdown with:
            - Hotel name
            - Justification for recommendation
            - Emoji bullets for key features
            - Approximate pricing if available
        """

        return model.invoke(prompt)

    return Tool(
        name="hotel_recomendation_tool",
        func=analyze_hotels,
        description="Analyzes and suggests the best hotel using Gemini LLM.",
    )
