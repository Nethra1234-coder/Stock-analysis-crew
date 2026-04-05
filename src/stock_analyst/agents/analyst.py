from crewai import Agent
from ..tools.technical_tool import TechnicalAnalysisTool
import os

def create_analyst() -> Agent:
    return Agent(
        role="Technical Analysis Expert",
        goal=(
            "Analyse price patterns, moving averages, RSI, "
            "and MACD for {ticker}. Identify support/resistance "
            "levels and trend direction."
        ),
        backstory=(
            "You are a CFA charterholder specialising in technical "
            "analysis. You use data-driven signals, never gut feelings. "
            "You explain indicators clearly for non-experts."
        ),
        tools=[TechnicalAnalysisTool()],
        llm=os.getenv("MODEL", "groq/llama-3.1-70b-versatile"),
        verbose=True,
        max_iter=3
    )