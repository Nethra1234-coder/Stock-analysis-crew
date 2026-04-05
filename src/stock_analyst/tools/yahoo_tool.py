from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf

class YahooInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol e.g. AAPL")

class YahooFinanceTool(BaseTool):
    name: str = "Yahoo Finance Data Fetcher"
    description: str = (
        "Fetches real-time stock data including price, market cap, "
        "P/E ratio, EPS, 52-week range, and revenue from Yahoo Finance."
    )
    args_schema: type[BaseModel] = YahooInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info  = stock.info

            data = {
                "ticker":         ticker.upper(),
                "current_price":  info.get("currentPrice", "N/A"),
                "market_cap":     info.get("marketCap", "N/A"),
                "pe_ratio":       info.get("trailingPE", "N/A"),
                "eps":            info.get("trailingEps", "N/A"),
                "52w_high":       info.get("fiftyTwoWeekHigh", "N/A"),
                "52w_low":        info.get("fiftyTwoWeekLow", "N/A"),
                "revenue":        info.get("totalRevenue", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "analyst_target": info.get("targetMeanPrice", "N/A"),
                "recommendation": info.get("recommendationKey", "N/A"),
            }

            return "\n".join(f"{k}: {v}" for k, v in data.items())

        except Exception as e:
            return f"Error fetching {ticker}: {str(e)}"