"""
    Currency service module
"""
import requests

class CurrencyService:
    """
        Currency service class
    """
    def __init__(self, api_key: str) -> None:
        """
            Currency service constructor
        """
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def get_exchange_rate(self, base_currency: str, target_currency: str) -> dict:
        """
            Get exchange rate between two currencies
        """
        url = f"{self.base_url}/{self.api_key}/pair/{base_currency}/{target_currency}"
        response = requests.get(url, timeout=300)
        response.raise_for_status()
        return response.json()
