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

from tools import google_search, get_countries_by_name, get_local_time

def create_conversational_agent():
    """
    Create the conversational agent.
    """
    tools = [google_search, get_countries_by_name, get_local_time]

    # functions = [convert_to_openai_function(f) for f in tools]

    model = ChatOllama(
        base_url="http://localhost:11434",
        model = "llama3",
        temperature = 0.0,
    )

    prompt = ChatPromptTemplate(
        [
            ("system", "You are a helpful assistant that can answer questions about countries and search the web. Use the tools provided to you to answer users questions."),
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
            agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
        )
        | prompt
        | model
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(
        agent = chain,
        tools = tools,
        memory = memory,
        verbose = True,
    )

    return agent_executor


def main():
    """
    Main function.
    """
    agent_executor = create_conversational_agent()

    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bye!")
            break

        response = agent_executor.invoke({"input": user_input})
        print("Agent:", response)

if __name__ == "__main__":
    main()
