"""
=========================================
AI Health Symptom Checker
Chatbot Module (Upgraded Version)
=========================================
"""

from huggingface_ai import chatbot_ai


# ==========================================
# Common Symptoms (Expanded + Cleaned)
# ==========================================

SYMPTOM_KEYWORDS = {
    "fever": "Fever",
    "high temperature": "Fever",
    "body heat": "Fever",

    "cough": "Cough",
    "dry cough": "Cough",
    "wet cough": "Cough",

    "headache": "Headache",
    "migraine": "Headache",

    "fatigue": "Fatigue",
    "tired": "Fatigue",
    "weakness": "Fatigue",
    "low energy": "Fatigue",

    "body pain": "Body Pain",
    "muscle pain": "Body Pain",
    "joint pain": "Body Pain",

    "runny nose": "Runny Nose",
    "cold": "Cold",
    "sneezing": "Cold",

    "sore throat": "Sore Throat",
    "throat pain": "Sore Throat",

    "vomiting": "Vomiting",
    "throwing up": "Vomiting",

    "diarrhea": "Diarrhea",
    "loose motion": "Diarrhea",

    "nausea": "Nausea",
    "feeling sick": "Nausea",

    "breathing difficulty": "Breathing Difficulty",
    "shortness of breath": "Breathing Difficulty",

    "chest pain": "Chest Pain",

    "dizziness": "Dizziness",
    "vertigo": "Dizziness",

    "stomach pain": "Stomach Pain",
    "abdominal pain": "Stomach Pain",
    "gas pain": "Stomach Pain"
}


# ==========================================
# Welcome Message
# ==========================================

WELCOME_MESSAGE = """
👋 Welcome to the AI Health Assistant.

You can ask questions like:

• I have fever and cough
• I feel stomach pain and dizziness
• What are dengue symptoms?
• I feel weak and tired

⚠ This chatbot provides educational information only.
It is not a substitute for professional medical advice.
"""


# ==========================================
# Detect Symptoms (Hybrid AI + Keyword)
# ==========================================

def detect_symptoms(message):

    message_lower = message.lower()
    detected = set()

    # 1. Keyword matching
    for keyword, symptom in SYMPTOM_KEYWORDS.items():
        if keyword in message_lower:
            detected.add(symptom)

    # 2. AI fallback if nothing detected
    if not detected:
        try:
            ai_prompt = f"""
Extract only medical symptoms from this text:

"{message}"

Rules:
- Return only comma-separated symptoms
- If no symptoms, return "None"
"""
            result = chatbot_ai(ai_prompt).strip()

            if result and "none" not in result.lower():
                detected = set([s.strip() for s in result.split(",") if s.strip()])

        except Exception:
            pass

    return list(detected)


# ==========================================
# Basic Rule-Based Responses
# ==========================================

def basic_response(message):

    text = message.lower()

    if any(greet in text for greet in ["hello", "hi", "hey"]):
        return "Hello! How can I help you with your health today?"

    if "thank" in text:
        return "You're welcome! Stay healthy and take care."
     
    if "fever" in text:
        return "You may have fever-related infection. Take rest, drink fluids, and monitor temperature."

    if "cough" in text:
        return "Cough may be due to cold or infection. Drink warm water and avoid cold food."

    if "vomiting" in text:
        return "Vomiting may be due to infection or food issues. Stay hydrated and take light food."

    if "chest pain" in text:
        return "Chest pain can be serious. If severe or persistent, seek medical attention immediately."

    if "dengue" in text:
        return "Dengue symptoms include fever, body pain, and weakness. Consult a doctor for testing."

    if "headache" in text:
        return "Headache may be due to stress or dehydration. Rest and drink water."

    if "sore throat" in text:
        return (
            "Sore throat is usually caused by viral infection or irritation. "
            "Gargle with warm salt water, drink warm fluids, and avoid cold drinks. "
            "See a doctor if pain or fever persists."
        )

    return None


# ==========================================
# Main Chatbot Function
# ==========================================

def chatbot_response(message):

    if not message or not message.strip():
        return "Please enter a valid message."

    # 1. Rule-based response first
    rule_reply = basic_response(message)
    if rule_reply:
        return rule_reply

    # 2. Detect symptoms
    symptoms = detect_symptoms(message)

    # 3. If symptoms found → medical explanation AI
    if symptoms:

        symptom_text = ", ".join(symptoms)

        ai_prompt = f"""
User Symptoms:
{symptom_text}

User Message:
{message}

Instructions:
1. Explain possible general causes
2. Give self-care advice
3. Mention when to consult doctor
4. Keep it simple and safe
5. Do NOT give exact diagnosis or medicine prescriptions
"""

        return chatbot_ai(ai_prompt)

    # 4. General fallback AI response
    try:
        return chatbot_ai(
            f"Act as a safe medical assistant and respond clearly:\n{message}"
        )
    except Exception:
        return "Sorry, I am unable to process your request right now."


# ==========================================
# Run Test Chatbot
# ==========================================

if __name__ == "__main__":

    print(WELCOME_MESSAGE)

    while True:

        user = input("\nYou: ")

        if user.lower() in ["exit", "quit"]:

            print("Bot: Goodbye! Stay healthy.")

            break

        reply = chatbot_response(user)

        print("\nBot:", reply)