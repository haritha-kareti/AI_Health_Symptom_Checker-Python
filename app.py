from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, send_file
)

import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# IMPORTS
# =========================
from symptom_checker import (
    predict_disease,
    train_model,
    load_model,
    get_recommendation
)

from report_generator import generate_report
from pdf_generator import generate_pdf
from visualizations import generate_charts

from huggingface_ai import ai_recommendation
from chatbot import chatbot_response


# =========================
# FLASK SETUP
# =========================
app = Flask(__name__)
app.secret_key = "AI_HEALTH_SECRET_KEY"

DATABASE = "database/users.db"


# =========================
# DATABASE INIT
# =========================
def create_database():
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================
# LOAD MODEL (IMPORTANT)
# =========================
model = load_model()


# =========================
# GLOBAL FEATURES (IMPORTANT FIX)
# =========================
FEATURES = [
    "fever","cough","headache","body_pain","fatigue",
    "sore_throat","breathlessness","nausea","vomiting",
    "diarrhea","loss_of_smell","loss_of_taste",
    "chest_pain","dizziness","skin_rash"
]


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )
            conn.commit()
            flash("Registration Successful!", "success")
            return redirect(url_for("login"))

        except:
            flash("Email already exists.", "danger")

        conn.close()

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = user[1]
            flash("Login Successful", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["user"],
        symptoms=FEATURES,
        symptom_chart=None,
        confidence_chart=None
    )


# =========================
# PREDICT (FIXED)
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    selected_symptoms = request.form.getlist("symptoms")

    feature_vector = [
        1 if s in selected_symptoms else 0
        for s in FEATURES
    ]

    # ML PREDICTION
    disease, confidence = predict_disease(feature_vector, model)

    recommendation = get_recommendation(disease)
    ai_result = ai_recommendation(disease, selected_symptoms)

    # ✅ CREATE REAL IMAGE FILES
    symptom_chart_path, confidence_chart_path = generate_charts(
        selected_symptoms,
        confidence * 100,   # IMPORTANT FIX
        disease
    )

    # Convert to URL PATH for HTML
    symptom_chart_url = "/" + symptom_chart_path.split("static")[-1].replace("\\", "/")
    confidence_chart_url = "/" + confidence_chart_path.split("static")[-1].replace("\\", "/")

    # REPORTS
    generate_report(
        selected_symptoms,
        disease,
        confidence,
        recommendation
    )

    pdf_path = generate_pdf(
        selected_symptoms,
        disease,
        confidence,
        recommendation,
        username=session["user"]
    )

    return render_template(
        "result.html",
        disease=disease,
        confidence=round(confidence * 100, 2),
        recommendation=recommendation,
        ai_result=ai_result,
        symptoms=selected_symptoms,
        symptom_chart=symptom_chart_url,
        confidence_chart=confidence_chart_url,
        pdf_path=pdf_path
    )


# =========================
# API PREDICT
# =========================
@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()
    selected = data.get("symptoms", [])

    vector = [1 if s in selected else 0 for s in FEATURES]

    disease, confidence = predict_disease(vector, model)

    recommendation = get_recommendation(disease)

    return jsonify({
        "disease": disease,
        "confidence": round(confidence, 2),
        "recommendation": recommendation
    })


# =========================
# CHATBOT
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data.get("message")

    reply = chatbot_response(message)

    return jsonify({"reply": reply})


# =========================
# REPORT DOWNLOAD
# =========================
@app.route("/download-report")
def download_report():

    pdf_file = os.path.join("reports", "health_report.pdf")
    return send_file(pdf_file, as_attachment=True)


# =========================
# REPORT VIEW
# =========================
@app.route("/report")
def report():

    report_file = os.path.join("reports", "health_report.txt")

    if os.path.exists(report_file):
        with open(report_file, "r", encoding="utf-8") as file:
            content = file.read()
    else:
        content = "No Report Found"

    return render_template("report.html", report=content)


# =========================
# VOICE API
# =========================
@app.route("/voice", methods=["POST"])
def voice():

    data = request.get_json()

    return jsonify({
        "text": data.get("voice", ""),
        "status": "success"
    })


# =========================
# CHATBOT PAGE
# =========================
@app.route("/chatbot")
def chatbot():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chatbot.html")


# =========================
# ERROR HANDLING
# =========================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# =========================
# TRAIN MODEL
# =========================
if not os.path.exists("models/trained_model.pkl"):
    print("Training Model...")
    train_model()
    print("Model Ready")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)