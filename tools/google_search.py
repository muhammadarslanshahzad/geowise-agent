"""
This module is used to search for a query on google and return the top 5 results.
"""
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper

@tool
def google_search(query: str):
    """
    Search for a query on google and return the top 5 results.

    Args:
        query (str): The query to search for.

    Returns:
        list: The top 5 search results.
    """
    serp_api_wrapper = SerpAPIWrapper()
    search_results = serp_api_wrapper.search(query)
    return search_results[:5]
