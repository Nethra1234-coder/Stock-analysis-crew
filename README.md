<<<<<<< HEAD
# stock-analysis-crew
=======
# AI Stock Analyst Crew

Multi-agent AI system that analyses stocks and gives BUY/HOLD/SELL recommendations.

## Tech Stack
- crewAI — multi-agent orchestration
- FastAPI — REST API backend
- Streamlit — dashboard frontend
- yfinance — free stock data
- Groq — free LLM (Llama 3.3 70B)

## How it works
4 AI agents work in sequence:
1. Research Agent — fetches live stock data
2. Technical Analyst — calculates RSI, MACD, moving averages
3. Sentiment Analyst — scores market sentiment
4. Investment Advisor — gives final BUY/HOLD/SELL recommendation

## Setup
1. Clone the repo
2. Create virtual environment
3. pip install -r requirements.txt
4. Add your API keys to .env
5. Run: uvicorn api.main:app --reload
6. Run: streamlit run frontend/app.py

## Disclaimer
For educational purposes only. Not financial advice.
>>>>>>> 8b5bd036aeb8b1f03d2a357015838d9fcd14bb3a
