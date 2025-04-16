import streamlit as st
from conversational_agent import create_conversational_agent
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="🧠 GeoWise Agent", page_icon="🌍")
st.title("🌍 GeoWise Chat Agent")

# Create the agent once
if "agent" not in st.session_state:
    st.session_state.agent = create_conversational_agent()

# Keep chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Ask me something like: 'What's the time in Tokyo?'")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.invoke({"input": user_input})
                reply = response["output"]
                st.session_state.chat_history.append(AIMessage(content=reply))
                st.markdown(reply, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# Optional: Display past history below
with st.expander("💬 Chat History", expanded=False):
    for msg in st.session_state.chat_history:
        role = "🧑‍💻 You" if isinstance(msg, HumanMessage) else "🤖 Agent"
        st.markdown(f"**{role}:** {msg.content}")
