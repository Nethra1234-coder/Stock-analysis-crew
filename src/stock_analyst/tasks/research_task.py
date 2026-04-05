from crewai import Task

def create_research_task(agent, ticker: str) -> Task:
    return Task(
        description=f"""
        Research {ticker} stock thoroughly. Collect:
        1. Current price, market cap, 52-week high/low
        2. P/E ratio, EPS, revenue (last 4 quarters)
        3. Dividend yield (if any)
        4. Top 3 recent news headlines with dates
        5. Analyst consensus rating and average price target

        Format your output as a clean structured report.
        Use only factual data — no opinions at this stage.
        """,
        expected_output=(
            f"A structured data report on {ticker} covering "
            "fundamentals, key metrics, and recent news headlines."
        ),
        agent=agent
    )