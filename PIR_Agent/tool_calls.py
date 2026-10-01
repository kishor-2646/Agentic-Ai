from langchain_core.tools import tool
from rag import ingest_data
import yfinance as yf
from typing import Union
from dotenv import load_dotenv
import os
import requests

load_dotenv()

print("All libraries imported")

# Tool 1 : Financial document retriever tool 
@tool
def get_financial_data(query: str) -> str:
    """ Retrieve chunks of the company's
    annual report via similarity search """
    vector_store = ingest_data()
    response = vector_store.similarity_search(query)
    return response



# Tool 2 : Live stock price
@tool
def get_stock_price(ticker: str) -> str:
    """Fetches the latest stock price using Alpha Vantage."""

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return "Error: ALPHA_VANTAGE_API_KEY not set in .env file."

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_INTRADAY&symbol={ticker}"
        f"&interval=5min&apikey={api_key}"
    )
    response = requests.get(url)
    return response.json()

# Tool 3 (NEW) : Deterministic P/E classifier — genuine Python logic, not the LLM guessing
@tool
def classify_pe_ratio(pe_ratio: Union[float, str]) -> str:
    """Classifies a P/E ratio as LOW, FAIR, or HIGH using fixed benchmark thresholds.
    Always call this instead of judging a P/E number yourself — it's a fixed
    calculation, not a guess. Pass the numeric P/E value returned by get_stock_price.

    Thresholds: below 15 = LOW, 15-25 = FAIR, above 25 = HIGH.
    """

    try:
        pe = float(pe_ratio)
    except (TypeError, ValueError):
        return f"Invalid P/E ratio '{pe_ratio}'; expected a number."

    if pe < 15:
        band = "LOW (potentially undervalued or slow-growth)"
    elif pe <= 25:
        band = "FAIR (typical for a stable, established company)"
    else:
        band = "HIGH (usually only justified by strong expected growth)"
    return f"P/E of {pe:.2f} is {band}. Not personalized advice."

if __name__ == "__main__":

    # tool 1 invoke
    #print(get_financial_data.invoke({"query": "Q2 revenue"})[0])

    # tool 2 invoke
     response = get_stock_price.invoke({"ticker": "AAPL"})
     print(response)

    # tool 3 invoke
   #
   #  print(classify_pe_ratio.invoke({"pe_ratio": 22.5}))
