"""
=========================================
AI Health Symptom Checker
Voice Input Module
=========================================
"""

import speech_recognition as sr


# ==========================================
# Speech Recognizer
# ==========================================

recognizer = sr.Recognizer()


# ==========================================
# Listen From Microphone
# ==========================================

def listen():

    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )

    try:

        print("Recognizing...")

        text = recognizer.recognize_google(audio)

        print("You Said:", text)

        return text

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        return ""

    except Exception:

        return ""


# ==========================================
# Extract Symptoms
# ==========================================

def extract_symptoms(text):

    text = text.lower()

    symptom_dictionary = {

        "fever": "Fever",

        "cough": "Cough",

        "headache": "Headache",

        "fatigue": "Fatigue",

        "body pain": "Body_Pain",

        "pain": "Body_Pain",

        "runny nose": "Runny_Nose",

        "cold": "Runny_Nose",

        "sore throat": "Sore_Throat",

        "vomiting": "Vomiting",

        "vomit": "Vomiting",

        "nausea": "Nausea",

        "diarrhea": "Diarrhea",

        "breathing": "Breathing_Difficulty",

        "breath": "Breathing_Difficulty",

        "shortness of breath": "Breathing_Difficulty"

    }

    symptoms = []

    for keyword, symptom in symptom_dictionary.items():

        if keyword in text:

            if symptom not in symptoms:

                symptoms.append(symptom)

    return symptoms


# ==========================================
# Voice To Symptoms
# ==========================================

def voice_to_symptoms():

    text = listen()

    if text == "":

        return []

    return extract_symptoms(text)


# ==========================================
# Voice API
# ==========================================

def get_voice_input():

    symptoms = voice_to_symptoms()

    return {

        "status": "success",

        "symptoms": symptoms

    }


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    print("=" * 45)
    print("AI HEALTH VOICE INPUT")
    print("=" * 45)

    symptoms = voice_to_symptoms()

    if symptoms:

        print("\nDetected Symptoms\n")

        for symptom in symptoms:

            print("✔", symptom)

    else:

        print("\nNo Symptoms Detected.")