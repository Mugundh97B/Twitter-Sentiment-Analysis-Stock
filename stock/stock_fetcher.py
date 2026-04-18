import yfinance as yf
from pymongo import MongoClient

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
tweets = db["tweets"]

# Fetch stock data (Tesla example)
stock = yf.Ticker("TSLA")
hist = stock.history(period="1d", interval="1m")

# Get latest price
latest_price = hist["Close"].iloc[-1]

# Get average sentiment
data = list(tweets.find().sort("_id", -1).limit(50))

sentiment_score = sum([d["score"] for d in data]) / len(data)

print("\n===== STOCK vs SENTIMENT =====")
print(f"Stock Price: {latest_price}")
print(f"Avg Sentiment: {sentiment_score}")

# Simple correlation logic
if sentiment_score > 0:
    print(" Positive sentiment → Market likely bullish")
else:
    print(" Negative sentiment → Market likely bearish")