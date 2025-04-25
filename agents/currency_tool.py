
from langchain.agents import Tool
from services.currency_service import get_currency_summary
from langchain_core.messages import AIMessage

def get_currency_conversion(query: str) -> AIMessage:
    summary = get_currency_summary(query)

    if not summary or not isinstance(summary, str) or summary.strip() == "":
        return AIMessage(
            content="### 💱 Currency Conversion Summary\n- ⚠️ Sorry, I couldn’t fetch a conversion for that. Please try something like `100 USD to GBP`."
        )
    cleaned_summary = summary.replace("```", "").strip()
    return AIMessage(content=f"### 💱 Currency Conversion Summary\n- {cleaned_summary}")

currency_exchange = Tool(
    name="currency_summary",
    func=get_currency_conversion,
    description="Returns a summary of currency conversion using online search. Example: '100 USD to EUR'"
)
