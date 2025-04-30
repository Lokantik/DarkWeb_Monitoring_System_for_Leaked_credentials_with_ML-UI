import joblib
import os
from .preprocess import clean_text

# Load pre-trained model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_leak(text):
    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]  # Probability of class '1' (leaked)
    return int(prediction), round(probability * 100, 2)  # Return prediction and confidence in %

