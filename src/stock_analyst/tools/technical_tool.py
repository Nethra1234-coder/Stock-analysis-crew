from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf

class TechnicalInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol e.g. AAPL")

class TechnicalAnalysisTool(BaseTool):
    name: str = "Technical Analysis Calculator"
    description: str = (
        "Calculates technical indicators: SMA20, SMA50, RSI, "
        "MACD for a given stock ticker."
    )
    args_schema: type[BaseModel] = TechnicalInput

    def _run(self, ticker: str) -> str:
        try:
            df    = yf.Ticker(ticker).history(period="3mo")
            close = df["Close"]

            sma20 = close.rolling(20).mean().iloc[-1]
            sma50 = close.rolling(50).mean().iloc[-1]

            delta = close.diff()
            gain  = delta.clip(lower=0).rolling(14).mean()
            loss  = (-delta.clip(upper=0)).rolling(14).mean()
            rs    = gain / loss
            rsi   = (100 - 100 / (1 + rs)).iloc[-1]

            ema12  = close.ewm(span=12).mean()
            ema26  = close.ewm(span=26).mean()
            macd   = (ema12 - ema26).iloc[-1]
            signal = (ema12 - ema26).ewm(span=9).mean().iloc[-1]

            current = close.iloc[-1]
            trend = (
                "Uptrend"   if current > sma20 > sma50 else
                "Downtrend" if current < sma20 < sma50 else
                "Sideways"
            )

            return f"""
Technical Indicators for {ticker.upper()}:
Current Price : ${current:.2f}
SMA 20        : ${sma20:.2f} ({'Bullish' if current > sma20 else 'Bearish'})
SMA 50        : ${sma50:.2f} ({'Bullish' if current > sma50 else 'Bearish'})
RSI (14)      : {rsi:.1f} ({'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'})
MACD          : {macd:.4f}
MACD Signal   : {signal:.4f} ({'Bullish' if macd > signal else 'Bearish'})
Trend         : {trend}
"""
        except Exception as e:
            return f"Error: {str(e)}"