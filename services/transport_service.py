from duckduckgo_search import DDGS

def search_local_transport(query: str):
    """Search transport info using DuckDuckGo."""
    full_query = f"{query} local transport site:tripadvisor.com OR site:travelblog.org"
    with DDGS() as ddgs:
        return list(ddgs.text(full_query, max_results=5))
