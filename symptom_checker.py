import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = os.path.join("models", "trained_model.pkl")
DATA_PATH = "dataset.csv"

symptoms = [
    "fever","cough","headache","body_pain","fatigue",
    "sore_throat","breathlessness","nausea","vomiting",
    "diarrhea","loss_of_smell","loss_of_taste",
    "chest_pain","dizziness","skin_rash"
]

def train_model():
    os.makedirs("models", exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower()

    X = df[symptoms]
    y = df["disease"]

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("✅ Model trained and saved at:", MODEL_PATH)


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠ Model not found. Training now...")
        train_model()

    return joblib.load(MODEL_PATH)


def predict_disease(features_vector, model):
    prediction = model.predict([features_vector])[0]

    prob = max(model.predict_proba([features_vector])[0])

    return prediction, prob


def get_recommendation(disease):
    return f"Suggested care for {disease}: Rest, hydration, and consult doctor if symptoms persist."