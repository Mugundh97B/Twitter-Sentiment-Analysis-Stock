import streamlit as st
from pymongo import MongoClient
import pandas as pd
import requests

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["tweets"]

st.set_page_config(page_title="Real-Time Sentiment Dashboard", layout="wide")

st.title("Real-Time Twitter Sentiment Analysis")

# -----------------------------
# Fetch latest data
# -----------------------------
data = list(collection.find().sort("_id", -1).limit(200))

if len(data) == 0:
    st.warning("No data available yet...")
    st.stop()

df = pd.DataFrame(data)

# =============================
# 🔹 SENTIMENT COUNTS
# =============================
st.subheader("🔹 Sentiment Distribution")

sentiment_counts = df["sentiment"].value_counts()

col1, col2, col3 = st.columns(3)

col1.metric("Positive", sentiment_counts.get("positive", 0))
col2.metric("Negative", sentiment_counts.get("negative", 0))
col3.metric("Neutral", sentiment_counts.get("neutral", 0))

# =============================
# 🔹 LATEST TWEETS
# =============================
st.subheader("🔹 Latest Tweets")

st.dataframe(df[["user", "text", "sentiment", "score"]].head(10))

# =============================
# 🔹 LATENCY COMPARISON
# =============================
st.subheader("⚡ Latency Comparison")

latency_df = pd.DataFrame({
    "Model": ["VADER", "Naive Bayes", "Logistic Regression"],
    "Latency": [
        df["vader_latency"].mean(),
        df["nb_latency"].mean(),
        df["lr_latency"].mean()
    ]
})

st.bar_chart(latency_df.set_index("Model"))

# =============================
# 🔹 STOCK ANALYSIS (AlphaVantage)
# =============================
st.subheader("📈 Stock vs Sentiment")

stock_symbol = st.selectbox(
    "Select Stock",
    ["TSLA", "AAPL", "AMZN", "GOOGL"]
)

API_KEY = "VBSZ3TKFRRG13O0D"

latest_price = None
chart_data = pd.DataFrame()

try:
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    time_series = data.get("Time Series (5min)", {})

    if time_series:
        df_stock = pd.DataFrame.from_dict(time_series, orient='index')

        df_stock = df_stock.rename(columns={
            "4. close": "Close"
        })

        df_stock.index = pd.to_datetime(df_stock.index)
        df_stock = df_stock.sort_index()

        df_stock["Close"] = df_stock["Close"].astype(float)

        latest_price = df_stock["Close"].iloc[-1]
        chart_data = df_stock

    else:
        st.warning("⚠️ API limit reached (wait 1 min)")

except Exception as e:
    st.error("Stock API failed")

# =============================
# DISPLAY
# =============================
avg_sentiment = df["score"].mean()

col1, col2 = st.columns(2)

if latest_price is not None:
    col1.metric("Stock Price", f"{latest_price:.2f}")
else:
    col1.metric("Stock Price", "N/A")

col2.metric("Avg Sentiment", f"{avg_sentiment:.2f}")

# =============================
# INTERPRETATION
# =============================
if avg_sentiment > 0:
    st.success("📈 Market likely bullish")
else:
    st.error("📉 Market likely bearish")

# =============================
# CHART
# =============================
if not chart_data.empty:
    st.line_chart(chart_data["Close"])
else:
    st.info("Stock chart unavailable")

# =============================
# FOOTER
# =============================
st.caption("Refresh manually or press R")