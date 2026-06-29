/*
==========================================
AI Health Symptom Checker
darkmode.js
Dark Mode Toggle
==========================================
*/

"use strict";

document.addEventListener("DOMContentLoaded", () => {

    initializeDarkMode();

});

// =====================================
// Initialize Theme
// =====================================

function initializeDarkMode() {

    let darkCSS =
        document.getElementById("dark-theme");

    if (!darkCSS) {

        darkCSS = document.createElement("link");

        darkCSS.rel = "stylesheet";

        darkCSS.href = "/static/css/dark.css";

        darkCSS.id = "dark-theme";

        darkCSS.disabled = true;

        document.head.appendChild(darkCSS);

    }

    let toggle =
        document.getElementById("darkModeToggle");

    // Create Toggle Button Automatically
    if (!toggle) {

        toggle = document.createElement("button");

        toggle.id = "darkModeToggle";

        toggle.className =
            "btn btn-dark rounded-circle";

        toggle.style.position = "fixed";
        toggle.style.bottom = "25px";
        toggle.style.left = "25px";
        toggle.style.zIndex = "9999";
        toggle.style.width = "55px";
        toggle.style.height = "55px";

        document.body.appendChild(toggle);

    }

    // Load Saved Theme
    const savedTheme =
        localStorage.getItem("theme");

    if (savedTheme === "dark") {

        enableDarkMode();

    } else {

        disableDarkMode();

    }

    toggle.addEventListener("click", () => {

        if (darkCSS.disabled) {

            enableDarkMode();

        } else {

            disableDarkMode();

        }

    });

}

// =====================================
// Enable Dark Mode
// =====================================

function enableDarkMode() {

    const darkCSS =
        document.getElementById("dark-theme");

    const toggle =
        document.getElementById("darkModeToggle");

    darkCSS.disabled = false;

    localStorage.setItem("theme", "dark");

    toggle.innerHTML =
        '<i class="fa-solid fa-sun"></i>';

    toggle.classList.remove("btn-dark");

    toggle.classList.add("btn-warning");

}

// =====================================
// Disable Dark Mode
// =====================================

function disableDarkMode() {

    const darkCSS =
        document.getElementById("dark-theme");

    const toggle =
        document.getElementById("darkModeToggle");

    darkCSS.disabled = true;

    localStorage.setItem("theme", "light");

    toggle.innerHTML =
        '<i class="fa-solid fa-moon"></i>';

    toggle.classList.remove("btn-warning");

    toggle.classList.add("btn-dark");

}

// =====================================
// Optional Functions
// =====================================

function isDarkMode() {

    return localStorage.getItem("theme") === "dark";

}

function toggleTheme() {

    if (isDarkMode()) {

        disableDarkMode();

    } else {

        enableDarkMode();

    }

}

console.log("Dark Mode Loaded Successfully");