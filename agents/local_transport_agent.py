from services.transport_service import search_local_transport
from langchain.agents import Tool

def get_local_transport_agent():
    def fetch_local_transport(query: str) -> str:
        if not query.strip():
            return "⚠️ No destination provided."

        results = search_local_transport(query)
        if not results:
            return f"❌ No local transport data found for '{query}'."

        formatted = []
        for res in results:
            method = res.get("title", "🚍 Local Option")
            tips = res.get("body", "")
            link = res.get("href", "")

            formatted.append(
                f"🚍 **{method}**\n💡 {tips}\n🔗 {link}"
            )

        return "\n\n".join(formatted) if formatted else "⚠️ No useful transport info found."

    return Tool(
        name="local_transport_planner",
        func=fetch_local_transport,
        description="Returns local transport options for a given destination."
    )
