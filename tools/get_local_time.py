"""
    This module contains a tool that gets the local time of a city.
"""
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper

@tool
def google_local_time(city: str) -> dict:
    """
    Search for a query on google and return the top 5 results.

    Args:
        query (str): The query to search for.

    Returns:
        list: The top 5 search results.
    """
    query = f"current time in {city}"
    serp_api_wrapper = SerpAPIWrapper()
    search_results = serp_api_wrapper.search(query)
    if "local_time" in search_results:
            return {"status": "success", "time": search_results["local_time"]}
    return {"status": "success", "data": search_results}

if __name__ == "__main__":
    print(google_local_time("New York"))