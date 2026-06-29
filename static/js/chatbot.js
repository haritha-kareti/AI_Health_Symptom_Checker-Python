/*
==========================================
AI Health Symptom Checker
chatbot.js
==========================================
*/

"use strict";

// ======================================
// Elements
// ======================================

const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userMessage");
const sendButton = document.getElementById("sendBtn");

// ======================================
// Conversation History
// ======================================

let chatHistory = [];

// ======================================
// Enter Key
// ======================================

if (userInput) {

    userInput.addEventListener("keypress", function (e) {

        if (e.key === "Enter") {

            e.preventDefault();

            sendMessage();

        }

    });

}

// ======================================
// Send Button
// ======================================

if (sendButton) {

    sendButton.addEventListener("click", sendMessage);

}

// ======================================
// Main Function
// ======================================

async function sendMessage() {

    if (!userInput) return;

    const message = userInput.value.trim();

    if (message === "") return;

    addUserMessage(message);

    userInput.value = "";

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message,

                history: chatHistory

            })

        });

        const data = await response.json();

        removeTyping();

        if (data.reply) {

            addBotMessage(data.reply);

        }

        else {

            addBotMessage("No response received.");

        }

    }

    catch (error) {

        console.error(error);

        removeTyping();

        addBotMessage(

            "Unable to connect to AI server."

        );

    }

}

// ======================================
// User Message
// ======================================

function addUserMessage(text) {

    chatHistory.push({

        role: "user",

        content: text

    });

    appendMessage(

        text,

        "user"

    );

}

// ======================================
// Bot Message
// ======================================

function addBotMessage(text) {

    chatHistory.push({

        role: "assistant",

        content: text

    });

    appendMessage(

        text,

        "bot"

    );

}

// ======================================
// Append HTML
// ======================================

function appendMessage(text, sender) {

    if (!chatBox) return;

    const wrapper =

        document.createElement("div");

    wrapper.className =

        "message " + sender;

    const bubble =

        document.createElement("div");

    bubble.className =

        "bubble";

    bubble.innerHTML =

        formatMessage(text);

    wrapper.appendChild(bubble);

    chatBox.appendChild(wrapper);

    scrollBottom();

}

// ======================================
// Typing
// ======================================

function showTyping() {

    if (!chatBox) return;

    const typing =

        document.createElement("div");

    typing.id = "typingIndicator";

    typing.className = "message bot";

    typing.innerHTML =

        `<div class="bubble">

            <span class="spinner-border spinner-border-sm"></span>

            AI is typing...

        </div>`;

    chatBox.appendChild(typing);

    scrollBottom();

}

function removeTyping() {

    const typing =

        document.getElementById(

            "typingIndicator"

        );

    if (typing) {

        typing.remove();

    }

}

// ======================================
// Scroll
// ======================================

function scrollBottom() {

    if (!chatBox) return;

    chatBox.scrollTop =

        chatBox.scrollHeight;

}

// ======================================
// Quick Questions
// ======================================

function quickQuestion(question) {

    if (!userInput) return;

    userInput.value = question;

    sendMessage();

}

// ======================================
// Clear Chat
// ======================================

function clearChat() {

    if (!chatBox) return;

    chatBox.innerHTML = "";

    chatHistory = [];

}

// ======================================
// Export Chat
// ======================================

function exportChat() {

    let text = "";

    chatHistory.forEach(msg => {

        text +=

            msg.role.toUpperCase()

            + ": "

            + msg.content

            + "\n\n";

    });

    const blob =

        new Blob(

            [text],

            {

                type: "text/plain"

            }

        );

    const url =

        URL.createObjectURL(blob);

    const a =

        document.createElement("a");

    a.href = url;

    a.download =

        "chat_history.txt";

    a.click();

    URL.revokeObjectURL(url);

}

// ======================================
// Copy
// ======================================

function copyLastMessage() {

    if (chatHistory.length === 0)

        return;

    navigator.clipboard.writeText(

        chatHistory[

            chatHistory.length - 1

        ].content

    );

    if (typeof showToast === "function") {

        showToast(

            "Copied."

        );

    }

}

// ======================================
// Format
// ======================================

function formatMessage(text) {

    text = text.replace(

        /\n/g,

        "<br>"

    );

    text = text.replace(

        /\*\*(.*?)\*\*/g,

        "<strong>$1</strong>"

    );

    return text;

}

// ======================================
// Welcome
// ======================================

window.addEventListener(

    "load",

    function () {

        addBotMessage(

            "👋 Hello! I am your AI Health Assistant.\n\nDescribe your symptoms or ask any health-related question."

        );

    }

);

console.log(

    "Chatbot Loaded Successfully"

);