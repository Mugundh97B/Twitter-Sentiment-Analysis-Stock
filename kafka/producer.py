import json
import time
import random
from kafka import KafkaProducer

# Kafka configuration
KAFKA_TOPIC = "twitter_topic"
KAFKA_SERVER = "localhost:9092"

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Mock tweet data (simulate real tweets)
tweets = [
    "Stock market is booming today!",
    "I hate this market crash",
    "Tesla stock looks promising",
    "Bitcoin is falling badly",
    "Amazing growth in tech stocks",
    "This is the worst investment ever",
    "Profit is going high!",
    "Loss everywhere in market",
    "Investors are happy",
    "Market uncertainty is rising"
]

# Function to generate tweet JSON
def generate_tweet():
    return {
        "timestamp": time.time(),
        "user": f"user_{random.randint(1, 1000)}",
        "text": random.choice(tweets)
    }

# Continuous streaming
def stream_data():
    print("Starting Kafka Producer... ")
    while True:
        tweet = generate_tweet()
        producer.send(KAFKA_TOPIC, value=tweet)
        print(f"Sent: {tweet}")
        time.sleep(0.1)  # 1 tweet per second

if __name__ == "__main__":
    stream_data()