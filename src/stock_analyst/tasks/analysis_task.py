from crewai import Task

def create_analysis_task(agent, ticker: str) -> Task:
    return Task(
        description=f"""
        Perform technical analysis on {ticker}. Calculate:
        1. 20-day and 50-day Simple Moving Averages
        2. RSI (14-period) — overbought >70, oversold <30
        3. MACD line and signal line
        4. Key support and resistance price levels
        5. Current trend: Uptrend / Downtrend / Sideways

        State clearly if each indicator is Bullish / Bearish / Neutral.
        """,
        expected_output=(
            f"Technical analysis report for {ticker} with "
            "indicator values and their bullish/bearish interpretation."
        ),
        agent=agent
    )