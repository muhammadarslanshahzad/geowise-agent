from duckduckgo_search import DDGS

def search_flights(query: str):
    """Search flights using DuckDuckGo."""
    full_query = f"{query} site:google.com/travel/flights"
    with DDGS() as ddgs:
        results = list(ddgs.text(full_query, max_results=5))
    return results
