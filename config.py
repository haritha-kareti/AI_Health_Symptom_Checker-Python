"""
=========================================
AI Health Symptom Checker
Configuration File
=========================================
"""

import os

# ==========================================
# Flask Configuration
# ==========================================

SECRET_KEY = "AI_HEALTH_SECRET_KEY_2026"

# ==========================================
# Database
# ==========================================

DATABASE = "database/users.db"

# ==========================================
# Dataset
# ==========================================

DATASET_PATH = "dataset.csv"

# ==========================================
# Machine Learning Model
# ==========================================

MODEL_DIR = "models"

MODEL_NAME = "trained_model.pkl"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    MODEL_NAME
)

# ==========================================
# Reports
# ==========================================

REPORT_DIR = "reports"

TEXT_REPORT = os.path.join(
    REPORT_DIR,
    "health_report.txt"
)

PDF_REPORT = os.path.join(
    REPORT_DIR,
    "health_report.pdf"
)


# ==========================================
# Hugging Face
# ==========================================

# Replace this with your own Hugging Face API key
HUGGINGFACE_API_KEY = "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"

# Example medical model (can be changed)
HUGGINGFACE_MODEL = "google/flan-t5-base"

# ==========================================
# Application
# ==========================================

APP_NAME = "AI Health Symptom Checker"

VERSION = "2.0"

AUTHOR = "Your Name"

# ==========================================
# Available Symptoms
# ==========================================

SYMPTOMS = [

    "fever",
    "cough",
    "headache",
    "body_pain",
    "fatigue",
    "sore_throat",
    "breathlessness",
    "nausea",
    "vomiting",
    "diarrhea",
    "loss_of_smell",
    "loss_of_taste",
    "chest_pain",
    "dizziness",
    "skin_rash"

]

# ==========================================
# Directories
# ==========================================

os.makedirs(MODEL_DIR, exist_ok=True)

os.makedirs(REPORT_DIR, exist_ok=True)

os.makedirs("database", exist_ok=True)