

import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StructType, StringType, DoubleType

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["tweets"]

# VADER
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    start = time.time()
    
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    latency = time.time() - start
    return sentiment, float(compound), float(latency)

def get_sentiment(text):
    return analyze_sentiment(text)[0]

def get_score(text):
    return analyze_sentiment(text)[1]

def get_latency(text):
    return analyze_sentiment(text)[2]

# Simulated ML
def nb_predict(text):
    start = time.time()
    
    text = text.lower()
    if "loss" in text or "worst" in text or "hate" in text:
        pred = 0.0
    elif "profit" in text or "growth" in text or "happy" in text:
        pred = 1.0
    else:
        pred = 2.0

    latency = time.time() - start
    return pred, float(latency)

def lr_predict(text):
    start = time.time()
    
    text = text.lower()
    if "loss" in text or "bad" in text:
        pred = 0.0
    elif "profit" in text or "good" in text:
        pred = 1.0
    else:
        pred = 2.0

    latency = time.time() - start
    return pred, float(latency)

# UDFs
sentiment_udf = udf(get_sentiment, StringType())
score_udf = udf(get_score, DoubleType())
latency_udf = udf(get_latency, DoubleType())

nb_udf = udf(lambda x: nb_predict(x)[0], DoubleType())
nb_latency_udf = udf(lambda x: nb_predict(x)[1], DoubleType())

lr_udf = udf(lambda x: lr_predict(x)[0], DoubleType())
lr_latency_udf = udf(lambda x: lr_predict(x)[1], DoubleType())

# Spark
spark = SparkSession.builder \
    .appName("TwitterKafkaStreaming") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Schema
schema = StructType() \
    .add("timestamp", DoubleType()) \
    .add("user", StringType()) \
    .add("text", StringType())

# Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "twitter_topic") \
    .option("startingOffsets", "latest") \
    .load()

df = df.selectExpr("CAST(value AS STRING)")

json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Add metrics
result_df = json_df \
    .withColumn("sentiment", sentiment_udf(col("text"))) \
    .withColumn("score", score_udf(col("text"))) \
    .withColumn("vader_latency", latency_udf(col("text"))) \
    .withColumn("nb_prediction", nb_udf(col("text"))) \
    .withColumn("nb_latency", nb_latency_udf(col("text"))) \
    .withColumn("lr_prediction", lr_udf(col("text"))) \
    .withColumn("lr_latency", lr_latency_udf(col("text")))

# Mongo write
def write_to_mongo(batch_df, epoch_id):
    rows = batch_df.collect()
    data = []

    for row in rows:
        data.append({
            "timestamp": row["timestamp"],
            "user": row["user"],
            "text": row["text"],
            "sentiment": row["sentiment"],
            "score": row["score"],
            "vader_latency": row["vader_latency"],
            "nb_prediction": row["nb_prediction"],
            "nb_latency": row["nb_latency"],
            "lr_prediction": row["lr_prediction"],
            "lr_latency": row["lr_latency"]
        })

    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} records with latency")

query = result_df.writeStream \
    .foreachBatch(write_to_mongo) \
    .outputMode("append") \
    .start()

query.awaitTermination()