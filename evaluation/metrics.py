from pymongo import MongoClient
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["tweets"]

# Fetch data
data = list(collection.find())

# Extract predicted labels
y_pred = [doc["sentiment"] for doc in data]

# Simulated ground truth (for demo)
def generate_true_label(text):
    if "hate" in text or "worst" in text or "loss" in text:
        return "negative"
    elif "happy" in text or "profit" in text or "growth" in text:
        return "positive"
    else:
        return "neutral"

y_true = [generate_true_label(doc["text"].lower()) for doc in data]

# Metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')

cm = confusion_matrix(y_true, y_pred)

# Print results
print("\n===== Evaluation Metrics =====")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\n===== Confusion Matrix =====")
print(cm)