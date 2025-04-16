# from langchain.agents import Tool
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# def get_local_transport_agent():
#     model = ChatGoogleGenerativeAI(
#         api_key=os.getenv("GOOGLE_API_KEY"),
#         model="gemini-2.0-pro",
#     )

#     def local_travel_suggestions(query: str) -> str:
#         return model.invoke(f"""
#         You are a travel assistant who helps users navigate local transport options.

#         Based on this trip: "{query}", provide:
#         - Local transportation suggestions (e.g., bus, rental car, ride-share, walking)
#         - Prices (approximate)
#         - Pickup points or how to access transport
#         - Tips for tourists using public transport

#         Give it in a markdown format, structured by day or destination segment.
#         """)

#     return Tool(
#         name="Local Transport Planner",
#         func=local_travel_suggestions,
#         description="Suggests how to move around the city, using public/local transport.",
#     )

from services.transport_service import search_local_transport
from langchain.agents import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_local_transport_agent():
    model = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model=os.environ.get("MODEL_NAME")
    )

    def local_transport_analysis(query: str) -> str:
        city = query.strip().split("to")[-1].strip()
        raw_data = search_local_transport(city)
        context = "\n\n".join(raw_data)

        return model.invoke(f"""
        Based on the following search results, summarize how a tourist can move around in {city}:

        {context}

        Output format:
        - List transport options (bus, taxi, rickshaw, etc)
        - Approximate pricing if mentioned
        - Safety or practical tips
        - Structured in markdown
        """)

    return Tool(
        name="local_transport_planner",
        func=local_transport_analysis,
        description="Provides local transportation advice based on live web search."
    )
