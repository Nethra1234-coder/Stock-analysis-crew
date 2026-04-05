from crewai import Agent
import os

def create_advisor() -> Agent:
    return Agent(
        role="Chief Investment Advisor",
        goal=(
            "Synthesise all research, technical, and sentiment "
            "data for {ticker} into a clear BUY / HOLD / SELL "
            "recommendation with a price target and risk rating."
        ),
        backstory=(
            "You are a senior portfolio manager with a fiduciary "
            "duty to clients. You weigh evidence carefully, "
            "acknowledge uncertainty, and always add a risk disclaimer."
        ),
        tools=[],
        llm=os.getenv("MODEL", "groq/llama-3.1-70b-versatile"),
        verbose=True,
        max_iter=2
    )