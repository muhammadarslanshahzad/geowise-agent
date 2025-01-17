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
    base_currency: str
    target_currency: str

@tool
def currency_exchange(input: CurrencyExchangeInput) -> str:
    """Fetches the currency exchange rate between two currencies."""
    print(f"\n\n input_Currency: {input}\n type is {type(input)}\n\n")
    try:
        exchange_data = currency_service.get_exchange_rate(input.base_currency, input.target_currency)
        rate = exchange_data.get('conversion_rate', 'N/A')
        return f"The exchange rate from {input.base_currency} to {input.target_currency} is {rate}."
    except (ConnectionError, TimeoutError, ValueError) as e:
        return f"Error fetching exchange rate: {str(e)}"
