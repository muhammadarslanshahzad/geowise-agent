import streamlit as st
from conversational_agent import create_conversational_agent
from langchain_core.messages import AIMessage, HumanMessage
from planner_flow import build_travel_planner  # ✅ FIXED: no dot-relative import



# Page settings
st.set_page_config(page_title="🧠 GeoWise Agent", page_icon="🌍")
st.title("🌍 GeoWise Chat Agent")



# Initialize agents
if "agent" not in st.session_state:
    st.session_state.agent = create_conversational_agent()

if "planner_agent" not in st.session_state:
    st.session_state.planner_agent = build_travel_planner()

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Layout: Tabs for Normal Chat vs Travel Planner
tab1, tab2 = st.tabs(["🗣️ Chat Agent", "✈️ Travel Planner"])

# ----------------------------
# 🤖 TAB 1: Conversational Agent
# ----------------------------
with tab1:
    user_input = st.chat_input("Ask me anything...")

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

    # Optional: Display past chat
    with st.expander("💬 Chat History", expanded=False):
        for msg in st.session_state.chat_history:
            role = "🧑‍💻 You" if isinstance(msg, HumanMessage) else "🤖 Agent"
            st.markdown(f"**{role}:** {msg.content}")

# ----------------------------
# 🧳 TAB 2: Travel Planner
# ----------------------------
with tab2:
    st.markdown("Plan a trip using our **Multi-Agent Travel Planner** powered by Gemini 🧠")

    destination = st.text_input("Destination", placeholder="e.g. Hunza Valley")
    days = st.slider("Number of days", 1, 10, 3)
    include_flights = st.checkbox("Include flights?", value=True)
    include_hotels = st.checkbox("Include hotel search?", value=True)
    include_transport = st.checkbox("Include local transport info?", value=True)

    if st.button("🧠 Generate Itinerary"):
        full_prompt = f"Plan a {days}-day trip to {destination}."
        if include_flights:
            full_prompt += " Include best flights."
        if include_hotels:
            full_prompt += " Include hotel options."
        if include_transport:
            full_prompt += " Include local transport suggestions."
        full_prompt += " Format the output in markdown with emojis and clear structure."

        with st.spinner("🛫 Planning your trip..."):
            try:
                trip_plan = st.session_state.planner_agent.run(full_prompt)
                st.markdown(trip_plan, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Planner Agent Error: {e}")
