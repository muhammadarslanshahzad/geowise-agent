"""
    This module contains the implementation of the conversational agent.
"""

from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder



def create_conversational_agent():
    """
    Create the conversational agent.
    """
    # Create the memory
    memory = ConversationBufferWindowMemory()

    # Create the agent executor
    agent_executor = AgentExecutor(memory)

    # Create the chat prompt template
    chat_prompt_template = ChatPromptTemplate(
        "Chat with the conversational agent",
        MessagesPlaceholder("Enter your message here")
    )

    return agent_executor, chat_prompt_template