from crewai import Task
from typing import List

def create_recommendation_task(agent, ticker: str,
                                context: List[Task]) -> Task:
    return Task(
        description=f"""
        Based on ALL previous research, technical analysis, and
        sentiment data for {ticker}, provide a final recommendation:

        1. Action: BUY / HOLD / SELL (pick one)
        2. Confidence: Low / Medium / High
        3. Price target (12-month estimate)
        4. Top 3 reasons supporting your recommendation
        5. Top 3 risks that could invalidate this view
        6. Risk rating: Conservative / Moderate / Aggressive

        End with: "This is for educational purposes only.
        Not financial advice."
        """,
        expected_output=(
            f"Investment recommendation for {ticker} with action, "
            "confidence, price target, reasons, and risks."
        ),
        agent=agent,
        context=context
    )

