
import streamlit as st
from conversational_agent import create_conversational_agent
from langchain_core.messages import AIMessage, HumanMessage
from planner_flow import build_travel_planner
from services.prompt_utils import build_safe_prompt

# ----------------------------
# 🌍 Page Setup
# ----------------------------
st.set_page_config(page_title="🧠 GeoWise Agent", page_icon="🌍")
st.title("🌍 GeoWise Chat Agent")

# ----------------------------
# 🧠 Initialize Agent State
# ----------------------------
if "agent" not in st.session_state:
    st.session_state.agent = create_conversational_agent()

if "planner_agent" not in st.session_state:
    st.session_state.planner_agent, st.session_state.system_prompt = build_travel_planner()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# 🧭 Tabs Layout
# ----------------------------
tab1, tab2 = st.tabs(["🗣️ Chat Agent", "✈️ Travel Planner"])

# ----------------------------
# 🤖 TAB 1: Conversational Agent
# ----------------------------
with tab1:
    st.markdown(
        """
        <div style="
            padding: 1.5rem; 
            margin-top: 1.25rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 12px; 
            background-color: #111111;
        ">
            <h3 style="margin-bottom: 1.2rem; font-weight: 700; font-size: 1.5rem;">
                🧭 What can I help you with today?
            </h3>
            <ul style="list-style-type: none; padding-left: 0; line-height: 1.8;">
                <li>🌤️ <strong>Weather:</strong> <code>What's the weather in London?</code></li>
                <li>🕒 <strong>Time:</strong> <code>Current time in Tokyo?</code></li>
                <li>💱 <strong>Currency:</strong> <code>Convert 100 USD to PKR</code></li>
            </ul>
            <div style="margin-top: 1rem; font-size: 0.95rem;">
                Or switch to the <strong>✈️ Travel Planner</strong> tab to generate your custom trip!
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    user_input = st.chat_input("Ask me anything...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepend system prompt to user input
                    full_input = f"{st.session_state.system_prompt}\n\n{user_input}"
                    response = st.session_state.agent.invoke({"input": full_input})
                    reply = response.get("output", "⚠️ No reply received.")
                    st.session_state.chat_history.append(AIMessage(content=reply))
                    st.markdown(reply, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

    with st.expander("💬 Chat History", expanded=False):
        for msg in st.session_state.chat_history:
            role = "🧑‍💻 You" if isinstance(msg, HumanMessage) else "🤖 Agent"
            st.markdown(f"**{role}:** {msg.content}")

# ----------------------------
# 🧳 TAB 2: Travel Planner
# ----------------------------
with tab2:
    st.markdown("Plan a trip using our **Multi-Agent Travel Planner** powered by Gemini 🧠")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Starting Location", placeholder="e.g. Islamabad")
    with col2:
        destination = st.text_input("Destination", placeholder="e.g. Hunza Valley")
    days = st.slider("Number of days", 1, 10, 3)
    include_flights = st.checkbox("Include flights?", value=True)
    include_hotels = st.checkbox("Include hotel search?", value=True)
    include_transport = st.checkbox("Include local transport info?", value=True)

    if st.button("🧠 Generate Itinerary"):
        full_prompt = build_safe_prompt(origin, destination, days, include_flights, include_hotels, include_transport)

        if not full_prompt:
            st.error("⚠️ Please enter a valid destination.")
        else:
            with st.spinner("🛫 Planning your trip..."):
                try:
                    # Prepend system prompt to full prompt
                    full_input = f"{st.session_state.system_prompt}\n\n{full_prompt}"
                    response = st.session_state.planner_agent.invoke({"input": full_input})
                    trip_plan = response.get("output", "⚠️ No itinerary generated.")
                    st.success("✅ Here's your personalized itinerary:")
                    st.markdown(trip_plan, unsafe_allow_html=True)

                    # Optional: Debugging / Dev Output
                    with st.expander("🧪 Raw Agent Response", expanded=False):
                        st.json(response)

                except Exception as e:
                    st.error(f"⚠️ Planner Agent Error: {e}")
