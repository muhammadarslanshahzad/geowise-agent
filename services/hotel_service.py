from duckduckgo_search import DDGS

def search_hotels(query: str):
    """DuckDuckGo search to simulate hotel listings."""
    full_query = f"{query} hotel site:google.com/travel/hotels"
    with DDGS() as ddgs:
        results = list(ddgs.text(full_query, max_results=5))
    return results
