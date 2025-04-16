from langchain.agents import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_itinerary_agent():
    model = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME")
    )

    def generate_itinerary(query: str) -> str:
        return model.invoke(f"""
            You are an expert AI travel planner. Your task is to generate a structured, visually clear 3-day itinerary based on the following user request:

            **User Input**:
            {query}

            ---

            ## 🧠 OUTPUT STRUCTURE INSTRUCTIONS:

            Return your entire response in **Markdown format** with the following structure:

            ### 🏔️ Title
            A short, bold title like "3-Day Hunza Valley Travel Itinerary"

            ---

            ### 🚕 Local Transport Summary
            - List main transport methods (jeep, car hire, walking)
            - Include rough cost suggestions if possible
            - Use bullet points only

            ---

            ### 🏨 Recommended Hotels Table
            Provide a table like this:

            | Hotel | Vibe | Notes |
            |-------|------|-------|
            | Serena Inn | Premium | Scenic views, full service |
            | Eagle's Nest | Rustic/Scenic | Best sunrise spot |

            ---

            ### 📅 Day-by-Day Plan

            Each day should follow this structure:

            #### 🗓️ Day X – Title of the Day (e.g. Culture & Forts)

            - 🕗 Morning: bullet list of activities
            - 🍽️ Lunch: recommended spot
            - 🏞️ Afternoon: sites or activities
            - 🌄 Evening: sunset/dinner rec
            - 🚗 Transport: hired/local/etc

            Repeat this for 3 days.

            ---

            ### 🧠 Travel Tips (Table or Bullets)

            - 💨 Acclimatize slowly
            - 💵 Carry cash (PKR)
            - 📶 Network best with SCOM
            - 👕 Dress modestly
            - 🧕 Ask before taking photos

            ---

            ### 💡 Additional Rules

            - Use emojis for context: 🏨 🚌 🍽️ 📸 🧳 etc
            - **No excessive fluff** – be concise, actionable, and structured
            - No repeating "as described above" or vague generalities
            - Assume the traveler is new to the area
            - Keep tone practical, friendly, but not chatty
            - DO NOT include Thought, Action, or Observation. Just give the final itinerary in markdown only.

            Generate your response now.

                """)

    return Tool(
        name="itinerary_generator",
        func=generate_itinerary,
        description="Creates a day-by-day markdown trip itinerary using Gemini."
    )
