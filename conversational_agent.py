
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-pro")

# Import your tool objects from agents module
from agents import currency_exchange, current_time, live_weather

def create_conversational_agent():
    # 1. Tools
    tools = [currency_exchange, current_time, live_weather]

    # 2. LLM setup
    model = ChatGoogleGenerativeAI(
        api_key=GEMINI_API_KEY,
        model=MODEL_NAME,
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # 3. Memory (keeps last 5 messages for context)
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        k=5
    )

    # 4. Initialize Agent
    agent_executor = initialize_agent(
        tools=tools,
        llm=model,
        memory=memory,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": (
                "You are GeoWise, a smart, direct global travel assistant 🌍. "
                "You handle questions about time, weather, currency, destinations, and cultural travel tips. "
                "Always call the relevant tool **immediately** when available — don't ask for permission. "
                "Be brief, helpful, and format your response using **Markdown**: use headers, bullet points, and emojis. "
                "If you're unsure, ask for more details, but don’t stall — take action."
            )
        }
    )

    return agent_executor


def main():
    print("🌍 Initializing GeoWise Travel Assistant...\n")

    try:
        agent = create_conversational_agent()
        print("✅ GeoWise is ready! Ask anything about time, weather, or currency.")
        print("💡 Type 'exit' or 'quit' to end the conversation.\n")

        while True:
            user_input = input("👤 You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye! Safe travels ✈️")
                break

            try:
                response = agent.run(user_input)
                print(f"\n🤖 GeoWise:\n{response}\n")
            except Exception as e:
                print(f"⚠️ Error processing your request: {e}")

    except Exception as setup_error:
        print(f"❌ Failed to initialize agent: {setup_error}")


if __name__ == "__main__":
    main()