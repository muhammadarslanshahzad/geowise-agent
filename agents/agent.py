"""
    This is the main file where you can define your agent and tools.
"""
from langchain.agents import initialize_agent, Tool
from langchain_ollama.llms import OllamaLLM

from tools import live_weather, current_time

# Define tools
tools = [
    Tool(name="Live Weather", func=live_weather, description=(
        "Use this to get live weather info of a city."
        "Input must be city name only. one city name at a time."
        )),
    Tool(name="Current Time", func=current_time, description=(
        "Use this to  the local time in a location."
        "Input must be city name only. one city name at a time.")),
    # Tool(name="Currency Exchange", func=currency_exchange, description=
    #      ("Get the exchange rate between two currencies."
    #       "Input should be a dictionary with 'base_currency' and 'target_currency'.")),
]


# Initialize your LLM with the desired model
llm = OllamaLLM(
        # model="llama3.1", temperature=0)
        base_url="http://localhost:11434",
        model="llama3",
        temperature=0.5,
    )

# Initialize the agent with tools
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
    )

response = agent.run("You can use your tools only once, \
                     and you need to Plan a 3-day trip to Pakistan, \
                     covering Karachi, Lahore, and Islamabad. \
                     The trip should include places to visit.")
print(response)
