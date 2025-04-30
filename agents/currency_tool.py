# agents/currency_tool.py

from langchain.agents import Tool
from pydantic import BaseModel, Field
from services.currency_service import get_currency_summary

# ✅ Input schema
class CurrencyQueryInput(BaseModel):
    query: str = Field(description="Currency conversion query like '100 USD to EUR'")

# ✅ Simple string output (no AIMessage)
def get_currency_conversion(query: str) -> str:
    summary = get_currency_summary(query)

    if not summary or not isinstance(summary, str) or summary.strip() == "":
        return (
            "### 💱 Currency Conversion Summary\n"
            "- ⚠️ Sorry, I couldn’t fetch a conversion for that. Please try something like `100 USD to GBP`."
        )

    cleaned_summary = summary.replace("```", "").strip()
    return f"### 💱 Currency Conversion Summary\n- {cleaned_summary}"

# ✅ Tool definition with args_schema and return_direct
currency_exchange = Tool(
    name="currency_summary",
    func=get_currency_conversion,
    description="Returns a summary of currency conversion using online search. Example: '100 USD to EUR'",
    args_schema=CurrencyQueryInput,
    return_direct=True
)


