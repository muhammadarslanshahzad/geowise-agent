"""
    This module contains the implementation of the conversational agent.
"""

from langchain.agents import AgentExecutor
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from tools import (
    google_search,
    get_countries_by_name,
    get_weather,
    get_local_time)


# def create_conversational_agent():
#     """
#     Create the conversational agent with tools, prompt, memory, and execution chain.
#     """
#     tools = [
#         google_search,
#         get_countries_by_name,
#         get_local_time,
#         get_weather
#         ]

#     # Convert tools into OpenAI-compatible functions
#     functions = [convert_to_openai_function(tool) for tool in tools]

#     # Define the model
#     model = ChatOllama(
#         base_url="http://localhost:11434",
#         model="llama3",
#         temperature=0.0,
#     )

#     # Define the system prompt
#     prompt = ChatPromptTemplate(
#         [
#             (
#                 "system",
#                 "You are a helpful assistant that answers user questions by directly using the tools provided. "
#                 "Your response must directly include the output from the tools. Do not add any extra information unless explicitly asked.",
#             ),
#             MessagesPlaceholder(variable_name="chat_history"),
#             ("user", "{input}"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )

#     # Define memory for conversational context
#     memory = ConversationBufferWindowMemory(
#         return_messages=True,
#         memory_key="chat_history",
#         k=5  # Adjust context length as needed
#     )

#     # Define the execution chain
#     chain = (
#         RunnablePassthrough.assign(
#             agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
#         )
#         | prompt
#         | model
#         | OpenAIFunctionsAgentOutputParser()
#     )

#     # Wrap the chain into an agent executor
#     agent_executor = AgentExecutor(
#         agent=chain,
#         tools=tools,
#         memory=memory,
#         verbose=True,  # Enable verbose for debugging
#     )

#     return agent_executor

def create_conversational_agent():
    tools = [
        google_search,
        get_countries_by_name,
        get_local_time,
        get_weather,
    ]

    # Debugging tools
    print("Loading tools...")
    for tool in tools:
        if hasattr(tool, 'name'):
            print(f"Tool: {tool.name}")
        else:
            print(f"Tool: {tool}")

    functions = []
    for tool in tools:
        try:
            functions.append(convert_to_openai_function(tool))
        except Exception as e:
            print(f"Error converting tool '{tool.__name__}': {e}")

    # Define the model
    model = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3",
        temperature=0.0,
    )

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are a helpful assistant. Always use the provided tools to answer user queries, and directly include their output in your response. "
                "Do not provide an example or a pre-trained answer; always call the relevant tool to get the actual output."
                "local_time tools returns a json object with keys 'status', 'city', 'timezone', 'local_time'."
                "your response must directly include the output from the tools. Do not add any extra information unless explicitly asked.",
          
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    memory = ConversationBufferWindowMemory(
        return_messages=True,
        memory_key="chat_history",
        k=5
    )

    chain = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
        )
        | prompt
        | model
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=chain,
        tools=tools,
        memory=memory,
        verbose=True,  # Enables detailed logging
    )

    return agent_executor


def main():
    """
    Main function to run the conversational agent.
    """
    agent_executor = create_conversational_agent()

    print("Type 'exit' or 'quit' to end the conversation.\n")

    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Bye!")
            break

        try:
            # Execute the agent with user input
            response = agent_executor.invoke({"input": user_input})
            
            # Extract the tool output directly
            tool_output = response.get("observation", None)  # Look for the tool output
            if tool_output:
                print("Agent:", tool_output)
            else:
                print("Agent:", response.get("output", "I couldn't find the information you requested."))
        except Exception as e:
            print("An error occurred:", str(e))
            # Optionally log errors to a file for debugging
            with open("error.log", "a") as log_file:
                log_file.write(f"Error: {str(e)}\n")


if __name__ == "__main__":
    main()
