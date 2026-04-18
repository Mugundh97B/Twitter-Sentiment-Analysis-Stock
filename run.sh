#!/bin/bash

echo " Starting Full Pipeline..."

PROJECT_DIR=$(pwd)
ENV_NAME="twitter_env"

# -------------------------
# JAVA FIX (VERY IMPORTANT)
# -------------------------
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

echo " Using Java:"
java -version

# -------------------------
# Activate Conda Env
# -------------------------
echo " Activating Conda Environment..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate $ENV_NAME

# -------------------------
# Start MongoDB
# -------------------------
echo " Starting MongoDB..."
sudo service mongod start

# -------------------------
# Start Kafka & Zookeeper
# -------------------------
KAFKA_DIR=~/kafka_2.13-3.6.1

echo " Starting Zookeeper..."
nohup $KAFKA_DIR/bin/zookeeper-server-start.sh $KAFKA_DIR/config/zookeeper.properties > $PROJECT_DIR/zookeeper.log 2>&1 &

sleep 5

echo " Starting Kafka Broker..."
nohup $KAFKA_DIR/bin/kafka-server-start.sh $KAFKA_DIR/config/server.properties > $PROJECT_DIR/kafka.log 2>&1 &

sleep 10

# -------------------------
# Create Topic (safe)
# -------------------------
echo " Creating Kafka Topic..."
$KAFKA_DIR/bin/kafka-topics.sh --create \
--topic twitter_topic \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1 2>/dev/null || true

# -------------------------
# Start Producer
# -------------------------
echo " Starting Producer..."
cd $PROJECT_DIR/kafka
nohup python producer.py > $PROJECT_DIR/producer.log 2>&1 &

## -------------------------
# Start Spark Streaming
# -------------------------
echo " Starting Spark..."

SPARK_HOME=/home/mugulinux/spark-3.5.0-bin-hadoop3
export SPARK_HOME
export PATH=$SPARK_HOME/bin:$PATH

cd $PROJECT_DIR/spark

nohup $SPARK_HOME/bin/spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
spark_stream.py > $PROJECT_DIR/spark.log 2>&1 &
# -------------------------
# Start Dashboard
# -------------------------
echo " Starting Dashboard..."
cd $PROJECT_DIR/dashboard
nohup streamlit run app.py > $PROJECT_DIR/dashboard.log 2>&1 &

# -------------------------
# Final Status
# -------------------------
echo ""
echo " ALL SERVICES STARTED (BACKGROUND MODE)"
echo " Open Dashboard: http://localhost:8501"
echo ""
echo " Logs:"
echo "tail -f zookeeper.log"
echo "tail -f kafka.log"
echo "tail -f producer.log"
echo "tail -f spark.log"
echo "tail -f dashboard.log"