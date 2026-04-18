from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF
from pyspark.ml.classification import NaiveBayes, LogisticRegression
from pyspark.ml import Pipeline

# Create Spark session
spark = SparkSession.builder.appName("TrainModels").getOrCreate()

# Sample training data (since no labeled dataset)
data = [
    ("I love this market", "positive"),
    ("This is terrible loss", "negative"),
    ("Stock is okay", "neutral"),
    ("Huge profit today", "positive"),
    ("Worst investment ever", "negative"),
    ("Market is stable", "neutral")
]

df = spark.createDataFrame(data, ["text", "label"])

# Convert labels to numeric
from pyspark.ml.feature import StringIndexer
label_indexer = StringIndexer(inputCol="label", outputCol="labelIndex")

# Text processing
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol="words", outputCol="features")
idf = IDF(inputCol="features", outputCol="final_features")

# Models
nb = NaiveBayes(featuresCol="final_features", labelCol="labelIndex")
lr = LogisticRegression(featuresCol="final_features", labelCol="labelIndex")

# Pipelines
nb_pipeline = Pipeline(stages=[label_indexer, tokenizer, hashingTF, idf, nb])
lr_pipeline = Pipeline(stages=[label_indexer, tokenizer, hashingTF, idf, lr])

# Train models
nb_model = nb_pipeline.fit(df)
lr_model = lr_pipeline.fit(df)

# Save models
nb_model.save("naive_bayes_model")
lr_model.save("logistic_model")

print("Models trained and saved successfully")