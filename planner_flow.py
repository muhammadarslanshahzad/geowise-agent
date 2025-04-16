from agents import get_flight_agent,get_hotel_agent,get_itinerary_agent, get_local_transport_agent
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def build_travel_planner():
    tools = [
        get_flight_agent(),
        get_hotel_agent(),
        get_itinerary_agent(),
    ]

    model = ChatGoogleGenerativeAI(
        api_key=os.environ.get("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME"),
        temperature=0.4
    )

    return initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
    )

def main():
    print("✈️ Welcome to the Gemini AI Travel Planner CLI!")
    print("Type your travel query or type 'exit' to quit.\n")

    agent = build_travel_planner()

    while True:
        user_input = input("🧳 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        try:
            response = agent.run(user_input)
            print("\n🧠 Travel Planner:\n")
            print(response)
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()