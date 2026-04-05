from crewai import Agent
import os

def create_sentiment_analyst() -> Agent:
    return Agent(
        role="Market Sentiment Analyst",
        goal=(
            "Analyse recent news, analyst ratings, and market "
            "sentiment around {ticker}. Score sentiment as "
            "Bullish / Neutral / Bearish with evidence."
        ),
        backstory=(
            "You are a behavioural finance specialist who reads "
            "hundreds of articles daily. You cut through media "
            "noise to find signal in sentiment data."
        ),
        tools=[],
        llm=os.getenv("MODEL", "groq/llama-3.1-70b-versatile"),
        verbose=True,
        max_iter=3
    )