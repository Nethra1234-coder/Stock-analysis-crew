import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Analyst")
st.caption("Powered by crewAI · For educational purposes only · Not financial advice")

st.sidebar.title("Settings")
ticker_input = st.sidebar.text_input(
    "Enter Stock Ticker",
    placeholder="AAPL, TSLA, NVDA...",
    max_chars=10
).upper()

period = st.sidebar.selectbox(
    "Chart Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=1
)

analyze_btn = st.sidebar.button("Analyze", type="primary", use_container_width=True)

if not ticker_input:
    st.info("Enter a stock ticker in the sidebar and click Analyze to begin.")
    st.stop()

def render_metrics(ticker):
    try:
        info = yf.Ticker(ticker).info
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        col2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
        col3.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
        col4.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
    except Exception as e:
        st.error(f"Could not load metrics: {e}")

def render_chart(ticker, period):
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            st.error("Could not load chart data.")
            return
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
            title=f"{ticker} Price Chart ({period})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
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
        from src.stock_analyst.crew import StockAnalystCrew
        crew = StockAnalystCrew(ticker)
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"Error running analysis: {str(e)}"

def render_recommendation(result_text):
    if "BUY" in result_text:
        action = "BUY"
        color = "green"
    elif "SELL" in result_text:
        action = "SELL"
        color = "orange"
    else:
        action = "HOLD"
        color = "orange"

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
    with st.spinner("Running AI crew analysis... this takes 60-90 seconds..."):
        result = run_crew_analysis(ticker_input)
    if result:
        render_recommendation(result)