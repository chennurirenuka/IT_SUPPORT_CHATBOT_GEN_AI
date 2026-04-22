import joblib
import numpy as np
from app.services.preprocess import clean_text

class IntentClassifier:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict_intent(self, text: str):
        cleaned = clean_text(text)
        vector = self.vectorizer.transform([cleaned])
        pred = self.model.predict(vector)[0]

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(vector)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.5

        return pred, confidence
