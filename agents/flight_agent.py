from langchain.agents import Tool
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_flight_agent():
    model = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME")
    )

    def analyze_flight(data: str) -> str:
        prompt = f"""
        Analyze the following flight data and recommend the best option:

        {data}

        Provide reasoning based on price, duration, stops, and convenience.
        """
        return model.invoke(prompt)

    return Tool(
        name="flight_analyst",
        func=analyze_flight,
        description="Analyzes flight options and returns the best one."
    )
