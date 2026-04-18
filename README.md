# Twitter Sentiment Analysis using Kafka, Spark & MongoDB

## Overview

This project implements a **data pipeline** that simulates Twitter streaming, processes data using **Apache Spark Streaming**, performs **sentiment analysis**, and visualizes insights through an interactive **Streamlit dashboard**.

The system demonstrates how modern data engineering tools can be combined to build scalable, real-time analytics pipelines.

---

##  Objectives

- Simulate real-time tweet streaming using Kafka
- Perform sentiment analysis using NLP techniques
- Process streaming data using Apache Spark
- Store processed data in MongoDB
- Visualize insights through a real-time dashboard
- Compare latency across multiple models

---

##  Architecture

Producer → Kafka → Spark Streaming → MongoDB → Streamlit Dashboard

---


###  Flow Explanation

1. **Producer**
   - Simulates live tweets and pushes data into Kafka

2. **Kafka**
   - Acts as a distributed messaging system

3. **Spark Streaming**
   - Consumes data from Kafka
   - Performs:
     - Sentiment Analysis (VADER)
     - ML Predictions (Naive Bayes, Logistic Regression)
     - Latency calculation

4. **MongoDB**
   - Stores processed results

5. **Streamlit Dashboard**
   - Displays:
     - Sentiment distribution
     - Latest tweets
     - Model latency comparison

---

##  Project Structure

MLDB_project/
│

├── kafka/ # Kafka Producer
│ └── producer.py

│
├── spark/ # Spark Streaming Job

│ └── spark_stream.py

│
├── dashboard/ # Streamlit Dashboard
│ └── app.py

│
├── ml/ # Trained ML Models
│ ├── logistic_model/
│ └── naive_bayes_model/

│
├── evaluation/ # Evaluation Metrics
│ └── metrics.py

│
├── stock/ # (Optional) Stock module
│ └── stock_fetcher.py

│
├── run.sh # Run full pipeline

├── requirements.txt

└── README.md


---

## Stack

- **Python**
- **Apache Kafka**
- **Apache Spark (PySpark)**
- **MongoDB**
- **Streamlit**
- **NLTK (VADER)**
- **Scikit-learn (ML models)**

---

##  Models Used

### 1. VADER (Rule-Based)
- Fast
- Works well for social media text
- Provides sentiment score (-1 to +1)

### 2. Naive Bayes
- Probabilistic classifier
- Efficient for text classification

### 3. Logistic Regression
- Linear model
- Good baseline for classification

---

##  Evaluation Metrics

Accuracy : 0.6988

Precision : 0.8046

Recall : 0.6988

F1 Score : 0.6407

### Confusion Matrix
---

[[55686 0 0]

[37362 18563 18651]

[ 0 0 55730]]

---


---

## How to Run the Project

## Prerequisites

Before running this project, ensure the following are installed on your system:

- Python (>= 3.9)
- Anaconda / Miniconda
- Java (OpenJDK 11 recommended)
- Apache Kafka (with Zookeeper)
- MongoDB (running locally)
- Git

---

##  Environment Setup

### 1️ Clone the Repository

```bash
1 git clone https://github.com/Mugundh97B/Twitter-Sentiment-Analysis-Stock.git

cd MLDB_project


2️ Create Conda Environment
conda create -n twitter_env python=3.9 -y

3️ Activate Environment
conda activate twitter_env

4️ Install Dependencies
pip install -r requirements.txt

5️ Download NLTK Data
python -c "import nltk; nltk.download('vader_lexicon')"

```

--- 

### Run the Project


Once everything is set up, run the entire pipeline using:

./run.sh


After execution, open your browser and go to:

http://localhost:8501
---


## Troubleshooting
If ports are already in use, stop previous processes:
pkill -f kafka

pkill -f zookeeper

pkill -f spark
pkill -f streamlit

pkill -f producer

If dashboard does not load, check logs:

tail -f spark.log

tail -f kafka.log

---

## Contributors


- Mugundhan B - spark/, kafka/,  run.sh
- Kakarla Sai Swaroop - ml/,  evaluation/

- Abhinav Tote - stock/, dashboard/
---
