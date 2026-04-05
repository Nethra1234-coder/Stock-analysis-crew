from crewai import Crew, Process
from dotenv import load_dotenv
import os
from .agents.researcher import create_researcher

load_dotenv()

from .agents.researcher import create_researcher
from .agents.analyst import create_analyst
from .agents.sentiment import create_sentiment_analyst
from .agents.advisor import create_advisor

from .tasks.research_task import create_research_task
from .tasks.analysis_task import create_analysis_task
from .tasks.sentiment_task import create_sentiment_task
from .tasks.recommendation_task import create_recommendation_task

class StockAnalystCrew:
    def __init__(self,ticker: str):
        self.ticker = ticker.upper()

    def kickoff(self):
        researcher = create_researcher()
        analyst    = create_analyst()
        sentiment  = create_sentiment_analyst()
        advisor    = create_advisor()

        research_task       = create_research_task(researcher, self.ticker)
        analysis_task       = create_analysis_task(analyst, self.ticker)
        sentiment_task      = create_sentiment_task(sentiment, self.ticker)
        recommendation_task = create_recommendation_task(
            advisor, self.ticker,
            context=[research_task, analysis_task, sentiment_task]
        )
        crew = Crew(
            agents=[researcher,analyst,sentiment,advisor],
            tasks=[research_task,analysis_task,sentiment_task,recommendation_task],
            process=Process.sequential,
            verbose=True
        )
        result = crew.kickoff()
        return result


