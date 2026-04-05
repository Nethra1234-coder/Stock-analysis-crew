# 📈 AI Stock Analyst Crew

A multi-agent AI system that autonomously researches, analyses, and generates 
BUY/HOLD/SELL investment recommendations for any stock ticker.

Live Demo: https://stock-analysis-crew-m6fhw8stbgyxakpcj7dcdf.streamlit.app

> For educational purposes only. Not financial advice.

---

## How It Works

4 AI agents work in sequence, each passing their output to the next:

1. **Research Agent** — fetches live price, market cap, P/E ratio, EPS, revenue
2. **Technical Analyst** — calculates RSI, MACD, SMA20, SMA50, trend direction
3. **Sentiment Analyst** — scores market sentiment as Bullish/Neutral/Bearish
4. **Investment Advisor** — synthesises everything into a BUY/HOLD/SELL recommendation

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Multi-agent AI | crewAI |
| LLM | Groq (Llama 3.3 70B) — free |
| Stock Data | yfinance — free |
| Backend API | FastAPI + uvicorn |
| Frontend | Streamlit |
| Charts | Plotly |

## Features

- Real-time candlestick charts
- Live stock metrics (price, market cap, P/E, 52W high)
- USD / INR currency toggle
- Indian stock support (e.g. RELIANCE.NS, TCS.NS, INFY.NS)
- Full AI analysis report with price target and risk rating
- Saves reports to local files

## Local Setup
```bash
# 1. Clone the repo
git clone https://github.com/Nethra1234-coder/Stock-analysis-crew.git
cd Stock-analysis-crew

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run backend
uvicorn api.main:app --reload --port 8000

# 6. Run frontend (new terminal)
streamlit run frontend/app.py
```

## Project Structure
```
stock-analyst-crew/
├── src/stock_analyst/
│   ├── agents/          # 4 specialist AI agents
│   ├── tasks/           # task definitions
│   ├── tools/           # yfinance + technical tools
│   └── crew.py          # orchestrates the crew
├── api/                 # FastAPI backend
├── frontend/            # Streamlit dashboard
└── reports/             # saved analysis outputs
```

## What I Learned

- Designing multi-agent AI systems with crewAI
- Building custom tools for AI agents using yfinance
- Prompt engineering for structured outputs
- FastAPI background tasks for long-running jobs
- Deploying AI applications to the cloud

## Disclaimer

This project is for educational purposes only.
All analysis is AI-generated and should not be used for real investment decisions.
