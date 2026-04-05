from crewai import Task

def create_sentiment_task(agent, ticker: str) -> Task:
    return Task(
        description=f"""
        Analyse market sentiment for {ticker}:
        1. Search for latest news (last 7 days)
        2. Note any earnings surprises or guidance changes
        3. Check if institutional investors are buying or selling
        4. Look for any insider trading activity
        5. Overall sentiment score: Bullish / Neutral / Bearish

        Provide 2-3 specific examples that support your sentiment score.
        """,
        expected_output=(
            f"Sentiment report for {ticker} with an overall "
            "Bullish/Neutral/Bearish rating and supporting evidence."
        ),
        agent=agent
    )