"""
    
"""

from typing import Optional
from loguru import logger
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field, conlist
from requests import PreparedRequest

def prepare_and_log_request(base_url: str, params: Optional[dict] = None) -> PreparedRequest:
    """
    Prepare a request.

    Args:
        base_url (str): The base url.
        params (dict, optional): The request parameters. Defaults to None.

    Returns:
        PreparedRequest: The prepared request.
    """
    request = PreparedRequest()
    request.prepare_url(base_url, params)
    logger.info(f"\033[92mRequest URL: {request.url}\033[0m")
    return request
    