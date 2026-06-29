/*
==========================================
AI Health Symptom Checker
voice.js
Voice Recognition
==========================================
*/

"use strict";

// ==========================================
// Check Browser Support
// ==========================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (!SpeechRecognition) {

    console.warn("Speech Recognition is not supported.");

} else {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    // ==========================================
    // Voice Button
    // ==========================================

    document.addEventListener("DOMContentLoaded", () => {

        const voiceBtn =
            document.getElementById("voiceBtn");

        if (!voiceBtn) return;

        voiceBtn.addEventListener("click", () => {

            voiceBtn.disabled = true;

            voiceBtn.innerHTML =
                '<i class="fa-solid fa-microphone-lines"></i> Listening...';

            recognition.start();

        });

    });

    // ==========================================
    // Voice Result
    // ==========================================

    recognition.onresult = function (event) {

        const transcript =
            event.results[0][0].transcript.toLowerCase();

        console.log("Voice:", transcript);

        fillSymptoms(transcript);

        const voiceBtn =
            document.getElementById("voiceBtn");

        if (voiceBtn) {

            voiceBtn.disabled = false;

            voiceBtn.innerHTML =
                '🎤 Speak Symptoms';

        }

        if (typeof showToast === "function") {

            showToast("Voice recognized successfully.");

        }

    };

    // ==========================================
    // Recognition End
    // ==========================================

    recognition.onend = function () {

        const voiceBtn =
            document.getElementById("voiceBtn");

        if (voiceBtn) {

            voiceBtn.disabled = false;

            voiceBtn.innerHTML =
                '🎤 Speak Symptoms';

        }

    };

    // ==========================================
    // Recognition Error
    // ==========================================

    recognition.onerror = function (event) {

        console.error(event.error);

        const voiceBtn =
            document.getElementById("voiceBtn");

        if (voiceBtn) {

            voiceBtn.disabled = false;

            voiceBtn.innerHTML =
                '🎤 Speak Symptoms';

        }

        if (typeof showToast === "function") {

            showToast(
                "Voice recognition failed.",
                "danger"
            );

        }

    };

}

// ==========================================
// Symptom Dictionary
// ==========================================

const symptomMap = {

    "fever":"fever",

    "cough":"cough",

    "headache":"headache",

    "vomiting":"vomiting",

    "nausea":"nausea",

    "cold":"cold",

    "fatigue":"fatigue",

    "chest pain":"chest_pain",

    "dizziness":"dizziness",

    "sore throat":"sore_throat",

    "diarrhea":"diarrhea",

    "body pain":"body_pain",

    "muscle pain":"muscle_pain",

    "joint pain":"joint_pain",

    "breathing":"breathlessness",

    "breathlessness":"breathlessness",

    "loss of smell":"loss_of_smell",

    "loss of taste":"loss_of_taste",

    "rash":"skin_rash"

};

// ==========================================
// Auto Select Symptoms
// ==========================================

function fillSymptoms(sentence){

    Object.keys(symptomMap).forEach(key=>{

        if(sentence.includes(key)){

            const id = symptomMap[key];

            const checkbox =
                document.getElementById(id);

            if(checkbox){

                checkbox.checked = true;

            }

        }

    });

}

// ==========================================
// Clear Symptoms
// ==========================================

function clearSymptoms(){

    document
        .querySelectorAll(
            ".symptom-checkbox"
        )
        .forEach(box=>{

            box.checked = false;

        });

}

// ==========================================
// Get Selected Symptoms
// ==========================================

function getSelectedSymptoms(){

    let symptoms=[];

    document
        .querySelectorAll(
            ".symptom-checkbox:checked"
        )
        .forEach(box=>{

            symptoms.push(box.value);

        });

    return symptoms;

}

// ==========================================
// Speak Text
// ==========================================

function speakText(text){

    if(!window.speechSynthesis) return;

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang="en-US";

    speech.rate=1;

    speech.pitch=1;

    window.speechSynthesis.speak(speech);

}

// ==========================================
// Example Usage
// ==========================================

function speakRecommendation(){

    const recommendation =
        document.getElementById(
            "recommendation"
        );

    if(recommendation){

        speakText(
            recommendation.innerText
        );

    }

}

console.log("Voice Recognition Loaded");