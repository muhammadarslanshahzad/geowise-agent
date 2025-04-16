# """
#     This module contains the implementation of the conversational agent for Streamlit use.
# """

# from langchain.agents import AgentExecutor
# from langchain_core.utils.function_calling import convert_to_openai_function
# from langchain.memory import ConversationBufferWindowMemory
# from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.agents.format_scratchpad import format_to_openai_functions

# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os

# from tools import currency_exchange, current_time, live_weather

# # Load environment variables from .env file
# load_dotenv()
# GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]  

# def create_conversational_agent():
#     tools = [currency_exchange, current_time, live_weather]

#     # Convert tools to OpenAI-compatible functions
#     functions = [convert_to_openai_function(tool) for tool in tools]

#     # Define model (Ollama)
#     model = ChatGoogleGenerativeAI(
#         api_key=GEMINI_API_KEY,
#         model="gemini-2.0-pro",
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#     )

#     # Prompt template
#     prompt = ChatPromptTemplate(
#         messages=[
#             (
#                 "system",
#                 "You are a helpful assistant. Always use the provided tools to answer user queries. "
#                 "Respond directly using the output from the tools only. Don't guess or invent answers.",
#             ),
#             MessagesPlaceholder(variable_name="chat_history"),
#             ("user", "{input}"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )

#     # Memory setup
#     memory = ConversationBufferWindowMemory(
#         return_messages=True,
#         memory_key="chat_history",
#         k=5
#     )

#     # Define agent chain
#     chain = (
#         RunnablePassthrough.assign(
#             agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
#         )
#         | prompt
#         | model
#         | OpenAIFunctionsAgentOutputParser()
#     )

#     # Agent Executor
#     agent_executor = AgentExecutor(
#         agent=chain,
#         tools=tools,
#         memory=memory,
#         verbose=False,  # Turn off verbose for UI use
#     )

#     return agent_executor



# def main():
#     """
#     Main function to run the conversational agent.
#     """
#     agent_executor = create_conversational_agent()

#     print("👋 Welcome to your AI agent. Type 'exit' or 'quit' to end the conversation.\n")

#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ["exit", "quit"]:
#             print("👋 Bye!")
#             break

#         try:
#             response = agent_executor.invoke({"input": user_input})
#             print("Agent:", response["output"])  # Clean, final output
#         except Exception as e:
#             print("❌ An error occurred:", str(e))
#             with open("error.log", "a") as log_file:
#                 log_file.write(f"Error: {str(e)}\n")


# if __name__ == "__main__":
#     main()
"""
Conversational Agent for Streamlit using Gemini + Tools
"""

from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]

# Tool imports
from tools import currency_exchange, current_time, live_weather

def create_conversational_agent():
    # Define tools
    tools = [currency_exchange, current_time, live_weather]

    # Define the model
    model = ChatGoogleGenerativeAI(
        api_key=GEMINI_API_KEY,
        model=os.environ.get("MODEL_NAME"),  # Use "pro" model for richer replies
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Define memory
    memory = ConversationBufferWindowMemory(
        return_messages=True,
        memory_key="chat_history",
        k=5,
    )

    # Agent setup using OpenAI Function-style tools + Gemini
    agent_executor = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=False,
        agent_kwargs={
            "system_message": (
                "You are a helpful, friendly assistant. "
                "Use tools when necessary, otherwise respond naturally and conversationally."
            ),
        }
    )

    return agent_executor


def main():
    """
    Run the Gemini conversational agent in CLI.
    """
    agent_executor = create_conversational_agent()

    print("👋 Welcome to your AI agent. Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        try:
            response = agent_executor.invoke({"input": user_input})
            print("Agent:", response["output"])
        except Exception as e:
            print("❌ Error:", str(e))
            with open("error.log", "a") as log_file:
                log_file.write(f"Error: {str(e)}\n")


if __name__ == "__main__":
    main()
