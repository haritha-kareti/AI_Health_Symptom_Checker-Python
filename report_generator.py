import os
from datetime import datetime

REPORT_DIR = "reports"
REPORT_FILE = os.path.join(
    REPORT_DIR,
    "health_report.txt"
)


def generate_report(
        symptoms,
        disease,
        confidence,
        recommendation):

    os.makedirs(REPORT_DIR, exist_ok=True)

    report = f"""
==========================================
        AI HEALTH REPORT
==========================================

Date:
{datetime.now().strftime('%d-%m-%Y')}

Time:
{datetime.now().strftime('%I:%M %p')}

------------------------------------------

Symptoms

{', '.join(symptoms)}

------------------------------------------

Predicted Disease

{disease}

------------------------------------------

Confidence Score

{confidence:.2f}%

------------------------------------------

AI Recommendation

{recommendation}

------------------------------------------

DISCLAIMER

This prediction is generated using
Machine Learning.

It is NOT a medical diagnosis.

Consult a healthcare professional for
proper diagnosis and treatment.

==========================================
"""

    with open(
            REPORT_FILE,
            "w",
            encoding="utf-8") as file:

        file.write(report)

    return REPORT_FILE