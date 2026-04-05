import streamlit as st
import requests
import time
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

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

def fetch_stock_chart(ticker, period):
    hist = yf.Ticker(ticker).history(period=period)
    return hist

def render_chart(ticker, period):
    with st.spinner("Loading chart..."):
        hist = fetch_stock_chart(ticker, period)

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

def render_metrics(ticker):
    info = yf.Ticker(ticker).info

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Price",
        f"${info.get('currentPrice', 'N/A')}",
        f"{info.get('regularMarketChangePercent', 0):.2f}%"
    )
    col2.metric(
        "Market Cap",
        f"${info.get('marketCap', 0)/1e9:.1f}B"
    )
    col3.metric(
        "P/E Ratio",
        f"{info.get('trailingPE', 'N/A')}"
    )
    col4.metric(
        "52W High",
        f"${info.get('fiftyTwoWeekHigh', 'N/A')}"
    )

def render_recommendation(result_text):
    action = "N/A"
    confidence = "N/A"

    if "BUY" in result_text:
        action = "BUY"
        color = "green"
    elif "SELL" in result_text:
        action = "SELL"
        color = "red"
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

    st.markdown("### Full Report")
    st.markdown(result_text)

def run_analysis(ticker):
    try:
        response = requests.post(f"{BACKEND_URL}/analyze/{ticker}", timeout=10)
        if response.status_code != 200:
            st.error(f"API error: {response.status_code}")
            return None
        return response.json()["job_id"]
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure uvicorn is running on port 8000.")
        return None

def poll_result(job_id):
    while True:
        response = requests.get(f"{BACKEND_URL}/report/{job_id}", timeout=10)
        data = response.json()

        if data["status"] == "completed":
            return data["result"]
        elif data["status"] == "failed":
            st.error(f"Analysis failed: {data['error']}")
            return None

        time.sleep(3)

st.subheader(f"Analysis for {ticker_input}")

render_metrics(ticker_input)
render_chart(ticker_input, period)

if analyze_btn:
    st.divider()
    st.subheader("AI Analysis")

    with st.status("Running AI crew analysis...", expanded=True) as status:
        st.write("Starting research agent...")
        job_id = run_analysis(ticker_input)

        if job_id:
            st.write(f"Job started: `{job_id}`")
            st.write("Agents working... this takes 60–90 seconds...")

            result = poll_result(job_id)

            if result:
                status.update(label="Analysis complete!", state="complete")
                st.divider()
                render_recommendation(result)