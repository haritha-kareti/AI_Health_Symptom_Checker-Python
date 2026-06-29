import requests
from config import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL

API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}


# ==========================================
# SAFE REQUEST HANDLER
# ==========================================

def call_hf(prompt, max_tokens=150, temp=0.5):

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temp
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        # Handle HTTP errors
        if response.status_code != 200:
            return None

        data = response.json()

        # Safe parsing
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return None

    except Exception:
        return None


# ==========================================
# OFFLINE FALLBACK (IMPORTANT)
# ==========================================

def offline_response(text):

    text = text.lower()

    if "fever" in text:
        return "Fever: Rest, drink fluids, monitor temperature."

    if "cough" in text:
        return "Cough: Drink warm water and rest."

    if "headache" in text:
        return "Headache: Reduce stress and stay hydrated."

    return "I am an offline health assistant. Please describe symptoms clearly."


# ==========================================
# AI RECOMMENDATION
# ==========================================

def ai_recommendation(disease, symptoms):

    prompt = f"""
Healthcare assistant.

Disease: {disease}
Symptoms: {', '.join(symptoms)}

1. Explanation
2. Home care
3. When to see doctor

No diagnosis.
Max 150 words.
"""

    result = call_hf(prompt, max_tokens=180, temp=0.4)

    if result:
        return result

    return offline_response(disease)


# ==========================================
# CHATBOT AI
# ==========================================

def chatbot_ai(user_message):

    prompt = f"""
You are a health assistant.

User: {user_message}

Reply safely in 100 words.
"""

    result = call_hf(prompt, max_tokens=150, temp=0.5)

    if result:
        return result

    return offline_response(user_message)


# ==========================================
# SUMMARY
# ==========================================

def summarize_report(report_text):

    prompt = f"""
Summarize in 3 points:

{report_text}
"""

    result = call_hf(prompt, max_tokens=120, temp=0.3)

    if result:
        return result

    return "Summary not available (offline mode)."


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("\nAI TEST\n")

    print(ai_recommendation("Flu", ["Fever", "Cough"]))

    print("\n--- CHATBOT ---\n")

    print(chatbot_ai("I have fever for 2 days"))