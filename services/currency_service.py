# services/currency_service.py

from duckduckgo_search import DDGS

def get_currency_summary(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(f"{query} site:x-rates.com", max_results=3)
            for result in results:
                if "equals" in result["body"].lower() or "=" in result["body"]:
                    return f"💱 {result['body']}"
        return f"⚠️ Couldn’t find conversion info for '{query}'. Try rephrasing."
    except Exception as e:
        return f"❌ Error fetching currency info: {str(e)}"
