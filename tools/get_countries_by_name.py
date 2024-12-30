"""
    This tool is responsible for getting countries by name. 
    It is useful when we need to answer questions about the countries.
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


class Params(BaseModel):
    """
    The request parameters.
    """
    fields: Optional[conlist(str, min_length=1, max_length=27)] = Field(
        default=None, description="The fields to filter the return of the requests.",
        examples=[
            "name", "topLevelDomain", "alpha2Code", "alpha3Code", "currencies",
            "capital", "callingCodes","altSpellings", "region", "subregion", "population", 
            "latlng", "demonym", "area", "gini","timezones","borders", "nativeName", 
            "numericCode", "languages", "flag", "regionalBlocs", "cioc"
        ])

class PathParams(BaseModel):
    """
    The path parameters.
    """
    name: str = Field(..., description="The name of the country.")

class RequestModel(BaseModel):
    """
        The request model.
    """
    params : Optional[Params] = None
    path_params: PathParams

@tool(args_schema=RequestModel)
def get_countries_by_name(path_params: PathParams, params: Optional[Params] = None) -> dict:
    """
    Get countries by name. Useful when we need to answer questions about the countries.

    Args:
        path_params (PathParams): The path parameters.
        params (Params, optional): The request parameters. Defaults to None.
        
    Returns:
        dict: The response of the request.
    """
    base_url = f"https://restcountries.com/v3.1/name/{path_params.name}"

    effective_params = {"fields": ",".join(params.fields)} if params and params.fields else None

    req = prepare_and_log_request(base_url, effective_params)

    response = requests.get(req.url, timeout=10)

    response.raise_for_status()

    return response.json()
