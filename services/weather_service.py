from duckduckgo_search import DDGS

def get_weather_summary(city: str) -> str:
    query = f"current weather in {city}"
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=1)
        if not results:
            return f"⚠️ Could not find weather information for {city}."
        
        snippet = results[0]['body']
        return f"🌤️ Weather summary for **{city.title()}**:\n{snippet}"
