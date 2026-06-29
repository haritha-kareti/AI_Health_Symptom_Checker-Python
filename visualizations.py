import os
import matplotlib.pyplot as plt

# ALWAYS correct static path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, "static", "graphs")

os.makedirs(STATIC_FOLDER, exist_ok=True)


# =========================
# SYMPTOM CHART
# =========================
def generate_symptom_bar(symptoms):

    if not symptoms:
        symptoms = ["None"]

    plt.figure(figsize=(6, 3))
    plt.bar(symptoms, [1] * len(symptoms))

    plt.title("Selected Symptoms")
    plt.xticks(rotation=45, ha="right")

    path = os.path.join(STATIC_FOLDER, "symptom_bar.png")

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path


# =========================
# CONFIDENCE CHART
# =========================
def generate_confidence_bar(disease, confidence):

    plt.figure(figsize=(4, 3))
    plt.bar([disease], [float(confidence)])

    plt.title("Prediction Confidence")
    plt.ylabel("Confidence (%)")

    path = os.path.join(STATIC_FOLDER, "confidence_bar.png")

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path


# =========================
# MAIN
# =========================
def generate_charts(symptoms, confidence, disease="Prediction"):
    symptom_chart = generate_symptom_bar(symptoms)
    confidence_chart = generate_confidence_bar(disease, confidence)

    return symptom_chart, confidence_chart