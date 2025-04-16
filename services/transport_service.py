from duckduckgo_search import DDGS

def search_local_transport(destination: str):
    """
    Uses DuckDuckGo to search for local transport suggestions.
    Returns a list of text results.
    """
    query = (
        f"How to get around {destination} as a tourist site:tripadvisor.com OR "
        f"site:reddit.com OR site:lonelyplanet.com"
    )

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    return results
