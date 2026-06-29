from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os


def generate_pdf(symptoms, disease, confidence, recommendation, username="User"):

    os.makedirs("reports", exist_ok=True)

    file_path = "reports/health_report.pdf"

    # 🔥 FORCE SMALLER PAGE CONTENT (A4)
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    # 🔥 SMALLER CUSTOM STYLE (IMPORTANT FOR SINGLE PAGE)
    small_title = ParagraphStyle(
        "small_title",
        parent=styles["Title"],
        fontSize=14,
        leading=16
    )

    small_text = ParagraphStyle(
        "small_text",
        parent=styles["Normal"],
        fontSize=9,
        leading=11
    )

    content = []

    # =========================
    # TITLE
    # =========================
    content.append(Paragraph("AI Health Report", small_title))
    content.append(Spacer(1, 5))

    # =========================
    # USER INFO
    # =========================
    content.append(Paragraph(f"Patient: {username}", small_text))
    content.append(Spacer(1, 5))

    # =========================
    # DISEASE
    # =========================
    content.append(Paragraph(f"Disease: <b>{disease}</b>", small_text))
    content.append(Spacer(1, 5))

    # =========================
    # CONFIDENCE
    # =========================
    content.append(Paragraph(f"Confidence: {confidence * 100:.2f}%", small_text))
    content.append(Spacer(1, 5))

    # =========================
    # SYMPTOMS (INLINE)
    # =========================
    symptom_text = ", ".join(symptoms) if symptoms else "None"
    content.append(Paragraph(f"Symptoms: {symptom_text}", small_text))
    content.append(Spacer(1, 5))

    # =========================
    # RECOMMENDATION
    # =========================
    content.append(Paragraph("Recommendation:", small_text))
    content.append(Paragraph(recommendation[:300], small_text))  # LIMIT TEXT
    content.append(Spacer(1, 8))

    # =========================
    # CHART IMAGES (SMALL SIZE)
    # =========================

    symptom_img = "static/graphs/symptom_bar.png"
    confidence_img = "static/graphs/confidence_bar.png"

    if os.path.exists(symptom_img):
        content.append(Image(symptom_img, width=220, height=90))
        content.append(Spacer(1, 5))

    if os.path.exists(confidence_img):
        content.append(Image(confidence_img, width=220, height=90))
        content.append(Spacer(1, 5))

    # =========================
    # BUILD PDF
    # =========================
    doc.build(content)

    return file_path