from duckduckgo_search import DDGS

def search_hotels(query: str):
    """Search hotels using DuckDuckGo."""
    full_query = f"{query} hotel options site:booking.com OR site:tripadvisor.com"
    with DDGS() as ddgs:
        return list(ddgs.text(full_query, max_results=5))
