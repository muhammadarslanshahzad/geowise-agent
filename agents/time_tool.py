from langchain.agents import Tool
from services.time_service import TimeService

time_service = TimeService()

def get_local_time(city: str) -> str:
    result = time_service.get_local_time(city)

    if result["status"] == "error":
        return f"⚠️ {result['message']}"
    
    return (
        f"### 🕒 Time in {result['city']}\n"
        f"- The current time is **{result['local_time']}** ({result['timezone']})"
    )


current_time = Tool(
    name="current_time",
    func=get_local_time,
    description="Get the current local time in any city. Example: 'What time is it in Tokyo?'"
)
