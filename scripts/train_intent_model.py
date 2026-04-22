import os
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score
from app.services.preprocess import clean_text
from config.settings import settings

def train_model():
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment("it_support_intent_classifier")

    df = pd.read_csv("data/tickets.csv")
    df["clean_text"] = df["text"].apply(clean_text)

    X = df["clean_text"]
    y = df["intent"]

    intent_counts = y.value_counts()

    with mlflow.start_run():
        if (intent_counts < 2).any():
            print("Some classes have fewer than 2 samples. Running without stratify.")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train_vec, y_train)

        preds = model.predict(X_test_vec)

        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")

        print(classification_report(y_test, preds))

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("ngram_range", "(1,2)")
        mlflow.log_param("max_features", 5000)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("weighted_f1", f1)
        mlflow.sklearn.log_model(model, "intent_model")

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/intent_model.pkl")
        joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

        print("Training completed successfully.")

if __name__ == "__main__":
    train_model()