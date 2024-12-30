"""
    This app is a conversational agent that can answer questions about countries and search the web.
"""
import streamlit as st
from conversational_agent import create_conversational_agent

def main():
    """
        Main function for the conversational agent.

    """
    st.title("GeoWise Agent (Ollama)")

    # Initialize the agent only once
    if "agent_executor" not in st.session_state:
        st.session_state["agent_executor"] = create_conversational_agent()

    # Display the conversation history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Text input for the user
    user_input = st.text_input("Ask something about countries or do a web search:")

    # When user presses Enter or clicks a button
    if st.button("Send") and user_input.strip():
        # Append user query to the conversation
        st.session_state["messages"].append(("user", user_input))

        # Run the agent
        response = st.session_state["agent_executor"].invoke({"input": user_input})

        # The agent returns a dictionary (depending on your agent config),
        # so adjust accordingly. If you see the final text under "output" key, do:
        agent_output = response.get("output", "")

        # Append agent's response to conversation
        st.session_state["messages"].append(("agent", agent_output))

    # Display the entire conversation
    for role, content in st.session_state["messages"]:
        if role == "user":
            st.markdown(f"**You**: {content}")
        else:
            st.markdown(f"**Agent**: {content}")

if __name__ == "__main__":
    main()
