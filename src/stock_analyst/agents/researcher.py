from crewai import Agent
from ..tools.yahoo_tool import YahooFinanceTool
import os

def create_researcher() -> Agent:
    return Agent(
        role="Senior Stock Research Analyst",
        goal=(
            "Gather comprehensive data for {ticker}: "
            "current price, 52-week range, P/E ratio, "
            "revenue, earnings, and recent news headlines."
        ),
        backstory=(
            "You are a meticulous financial researcher with 15 years "
            "at Goldman Sachs. You always verify data from multiple "
            "sources and present facts clearly and accurately."
        ),
        tools=[YahooFinanceTool()],
        llm=os.getenv("MODEL", "groq/llama-3.1-70b-versatile"),
        verbose=True,
        max_iter=3
    )