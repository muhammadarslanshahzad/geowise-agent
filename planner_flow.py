from agents import get_flight_agent, get_hotel_agent, get_itinerary_agent, get_local_transport_agent
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def build_travel_planner():
    tools = [
        get_flight_agent(),
        get_hotel_agent(),
        get_itinerary_agent(),
        get_local_transport_agent(),  # ✅ ADD this missing tool
    ]

    # system_prompt = """
    #     You are a world-class AI travel concierge. You plan detailed itineraries worldwide, suggesting flights, hotels, transportation, day-by-day activities, cultural tips, and FAQs. 
    #     Always respond in clean Markdown format with structured sections, tables, and emojis. Be practical, friendly, and culturally aware.
    #     Only output formatted trip plans. No 'Thought', 'Action', or 'Observation' statements.
    # """  
    system_prompt = """
        You are a world-class AI travel concierge. You help users plan multi-day trips around the world. Your job is to generate full travel itineraries in structured, clean Markdown format using **list-style formatting**, not tables.

        📌 Format Rules (Follow Exactly):
        1. **Always use section headings with emojis** (like: ✈️ Flights, 🏨 Hotels, 🗺️ Itinerary).
        2. **Use bullet lists**, not Markdown tables. Do not use `|` or tabular formatting.
        3. Write day-by-day plans using bold headers (Day 1: ...) and sub-bullets for morning/afternoon/evening.
        4. Keep writing practical, direct, and travel-focused. Avoid fluff.
        5. Mention transport routes, tips, locations, and local foods with appropriate emojis.
        6. Use simple sub-bullets for details. Example:
        - Morning: Do X
        - Afternoon: Do Y
        - Evening: Do Z
        7. Do not include technical tool names like `flight_recommendation_tool` or `hotel_agent`.

        ✅ Your Output Structure:
        ---
        ### ✈️ Flights
        - Route + airline
        - Notes on season/tips

        ---
        ### 🏨 Hotels
        - Luxury:
        - Hotel Name: Key features
        - Budget:
        - Hotel Name: Key features

        ---
        ### 🚗 Local Transport
        - Transport type: Comment

        ---
        ### 📅 Itinerary
        #### Day 1: Title
        - Morning: ...
        - Afternoon: ...
        - Evening: ...

        #### Day 2: ...
        ...

        ---
        ### 💡 Travel Tips
        - Tip 1
        - Tip 2

        Only return Markdown formatted output in the above structure.
    """

      

    raw_model = ChatGoogleGenerativeAI(
        api_key=os.environ.get("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME"),
        temperature=0.4,
        system_message = system_prompt
    )

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content="{input}")
    ])


    agent = initialize_agent(
        tools=tools,
        llm=raw_model,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent, system_prompt

def main():
    print("✈️ Welcome to the Gemini AI Travel Planner CLI!")
    print("Type your travel query or type 'exit' to quit.\n")

    agent = build_travel_planner()

    while True:
        user_input = input("🧳 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        if not user_input.strip():
            print("⚠️ Please enter a valid query.")
            continue

        try:
            # 🛠 NEW: Use invoke instead of run
            response = agent.invoke({"input": user_input})
            reply = response.get("output", "❓ No response generated.")
            print("\n🧠 Travel Planner:\n")
            print(reply)
            print("\n" + "=" * 60 + "\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
