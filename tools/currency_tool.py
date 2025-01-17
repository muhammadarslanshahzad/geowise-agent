"""
    Currency exchange tool
"""
import os

from dotenv import load_dotenv
from langchain.agents import tool
from pydantic import BaseModel

from services import CurrencyService

load_dotenv()
currency_service = CurrencyService(api_key=os.getenv('EXCHANGE_RATE_API_KEY'))


class CurrencyExchangeInput(BaseModel):
    """
        Input model for the currency exchange tool.
    """
    base_currency: str
    target_currency: str

@tool
def currency_exchange(exchange_input: CurrencyExchangeInput) -> str:
    """Fetches the currency exchange rate between two currencies."""
    print(f"\n\n input_Currency: {exchange_input}\n type is {type(exchange_input)}\n\n")
    try:
        exchange_data = currency_service.get_exchange_rate(
            exchange_input.base_currency,
            exchange_input.target_currency
        )
        rate = exchange_data.get('conversion_rate', 'N/A')
        return f"The exchange rate from {exchange_input.base_currency} \
            to {exchange_input.target_currency} is {rate}."
    except (ConnectionError, TimeoutError, ValueError) as e:
        return f"Error fetching exchange rate: {str(e)}"
