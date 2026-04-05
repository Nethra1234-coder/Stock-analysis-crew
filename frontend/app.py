import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
MODEL = st.secrets.get("MODEL", os.getenv("MODEL", "groq/llama-3.3-70b-versatile"))

USD_TO_INR = 84.0

st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Analyst")
st.caption("Powered by crewAI · For educational purposes only · Not financial advice")

st.sidebar.title("Settings")

currency = st.sidebar.radio("Currency", ["USD ($)", "INR (₹)"])
use_inr = currency == "INR (₹)"

ticker_input = st.sidebar.text_input(
    "Enter Stock Ticker",
    placeholder="AAPL, TSLA, NVDA, RELIANCE.NS...",
    max_chars=15
).upper()

period = st.sidebar.selectbox(
    "Chart Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=1
)

analyze_btn = st.sidebar.button("Analyze", type="primary", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("For Indian stocks add .NS — e.g. RELIANCE.NS, TCS.NS, INFY.NS")

if not ticker_input:
    st.info("Enter a stock ticker in the sidebar and click Analyze to begin.")
    st.stop()

def convert(value):
    try:
        if use_inr:
            return f"₹{float(value) * USD_TO_INR:,.2f}"
        return f"${float(value):,.2f}"
    except:
        return str(value)

def convert_large(value):
    try:
        v = float(value)
        if use_inr:
            v = v * USD_TO_INR
            if v >= 1e12:
                return f"₹{v/1e12:.1f}T"
            elif v >= 1e9:
                return f"₹{v/1e9:.1f}B"
            return f"₹{v:,.0f}"
        else:
            if v >= 1e12:
                return f"${v/1e12:.1f}T"
            elif v >= 1e9:
                return f"${v/1e9:.1f}B"
            return f"${v:,.0f}"
    except:
        return str(value)

def render_metrics(ticker):
    try:
        info = yf.Ticker(ticker).info
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Current Price",
            convert(info.get("currentPrice", 0)),
            f"{info.get('regularMarketChangePercent', 0):.2f}%"
        )
        col2.metric(
            "Market Cap",
            convert_large(info.get("marketCap", 0))
        )
        col3.metric(
            "P/E Ratio",
            f"{info.get('trailingPE', 'N/A')}"
        )
        col4.metric(
            "52W High",
            convert(info.get("fiftyTwoWeekHigh", 0))
        )
    except Exception as e:
        st.error(f"Could not load metrics: {e}")

def render_chart(ticker, period):
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            st.error("Could not load chart data.")
            return

        if use_inr:
            hist["Open"]  = hist["Open"]  * USD_TO_INR
            hist["High"]  = hist["High"]  * USD_TO_INR
            hist["Low"]   = hist["Low"]   * USD_TO_INR
            hist["Close"] = hist["Close"] * USD_TO_INR

        symbol = "₹" if use_inr else "$"

        fig = go.Figure(go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350"
        ))

        fig.update_layout(
            title=f"{ticker} Price Chart ({period}) — {symbol}",
            xaxis_title="Date",
            yaxis_title=f"Price ({symbol})",
            xaxis_rangeslider_visible=False,
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load chart: {e}")

def run_crew_analysis(ticker):
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
        os.environ["MODEL"] = MODEL
        from src.stock_analyst.crew import StockAnalystCrew
        crew = StockAnalystCrew(ticker)
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"Error running analysis: {str(e)}"

def render_recommendation(result_text):
    if "BUY" in result_text:
        action = "BUY"
    elif "SELL" in result_text:
        action = "SELL"
    else:
        action = "HOLD"

    if "High" in result_text:
        confidence = "High"
    elif "Medium" in result_text:
        confidence = "Medium"
    else:
        confidence = "Low"

    col1, col2 = st.columns(2)
    col1.metric("Recommendation", action)
    col2.metric("Confidence", confidence)

    st.markdown("### Full AI Report")
    st.markdown(result_text)

st.subheader(f"Analysis for {ticker_input}")
render_metrics(ticker_input)
render_chart(ticker_input, period)

if analyze_btn:
    st.divider()
    st.subheader("AI Analysis")
    with st.spinner("Running AI crew analysis... this takes 60–90 seconds..."):
        result = run_crew_analysis(ticker_input)
    if result:
        render_recommendation(result)