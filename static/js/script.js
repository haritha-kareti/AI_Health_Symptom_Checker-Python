/*
==========================================
AI Health Symptom Checker
script.js
Main JavaScript
==========================================
*/

"use strict";

// ==========================================
// Run After Page Loads
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    autoCloseAlerts();

    animateProgressBars();

    initializeTooltips();

    initializeScrollTop();

    initializeLoadingButtons();

});

// ==========================================
// Auto Close Alerts
// ==========================================

function autoCloseAlerts() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        setTimeout(() => {

            alert.classList.remove("show");

            setTimeout(() => {

                alert.remove();

            }, 300);

        }, 5000);

    });

}

// ==========================================
// Progress Bar Animation
// ==========================================

function animateProgressBars() {

    const bars = document.querySelectorAll(".progress-bar");

    bars.forEach(bar => {

        const value = bar.style.width;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.width = value;

        }, 300);

    });

}

// ==========================================
// Bootstrap Tooltips
// ==========================================

function initializeTooltips() {

    if (typeof bootstrap === "undefined") return;

    const tooltipTriggerList =
        [].slice.call(
            document.querySelectorAll(
                '[data-bs-toggle="tooltip"]'
            )
        );

    tooltipTriggerList.map(function (element) {

        return new bootstrap.Tooltip(element);

    });

}

// ==========================================
// Scroll To Top Button
// ==========================================

function initializeScrollTop() {

    let button = document.getElementById("scrollTopBtn");

    if (!button) {

        button = document.createElement("button");

        button.id = "scrollTopBtn";

        button.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';

        button.className =
            "btn btn-primary rounded-circle";

        button.style.position = "fixed";
        button.style.bottom = "20px";
        button.style.right = "20px";
        button.style.display = "none";
        button.style.zIndex = "9999";

        document.body.appendChild(button);

    }

    window.addEventListener("scroll", () => {

        button.style.display =
            window.scrollY > 200 ? "block" : "none";

    });

    button.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}

// ==========================================
// Loading Buttons
// ==========================================

function initializeLoadingButtons() {

    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", () => {

            const button =
                form.querySelector(
                    "button[type='submit']"
                );

            if (!button) return;

            button.disabled = true;

            button.dataset.original =
                button.innerHTML;

            button.innerHTML =
                '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

        });

    });

}

// ==========================================
// Toast Notification
// ==========================================

function showToast(message, type = "success") {

    const toast = document.createElement("div");

    toast.className =
        `alert alert-${type} position-fixed`;

    toast.style.top = "20px";
    toast.style.right = "20px";
    toast.style.zIndex = "9999";
    toast.style.minWidth = "250px";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.remove();

    }, 4000);

}

// ==========================================
// Copy Text
// ==========================================

function copyText(text) {

    navigator.clipboard.writeText(text)
        .then(() => {

            showToast("Copied to clipboard.");

        })
        .catch(() => {

            showToast("Copy failed.", "danger");

        });

}

// ==========================================
// Print Page
// ==========================================

function printPage() {

    window.print();

}

// ==========================================
// Confirm Delete
// ==========================================

function confirmDelete(message = "Are you sure?") {

    return confirm(message);

}

// ==========================================
// Format Date
// ==========================================

function formatDate(date) {

    return new Date(date).toLocaleDateString();

}

// ==========================================
// Character Counter
// ==========================================

function characterCounter(inputId, counterId) {

    const input = document.getElementById(inputId);

    const counter =
        document.getElementById(counterId);

    if (!input || !counter) return;

    input.addEventListener("input", () => {

        counter.innerHTML =
            input.value.length + " characters";

    });

}

// ==========================================
// Search Filter
// ==========================================

function filterList(inputId, listClass) {

    const input =
        document.getElementById(inputId);

    if (!input) return;

    input.addEventListener("keyup", function () {

        const value =
            this.value.toLowerCase();

        document.querySelectorAll(listClass)
            .forEach(item => {

                item.style.display =
                    item.textContent
                        .toLowerCase()
                        .includes(value)
                        ? ""
                        : "none";

            });

    });

}

// ==========================================
// Loading Overlay
// ==========================================

function showLoading() {

    let overlay =
        document.getElementById("loadingOverlay");

    if (!overlay) {

        overlay = document.createElement("div");

        overlay.id = "loadingOverlay";

        overlay.style.position = "fixed";
        overlay.style.left = 0;
        overlay.style.top = 0;
        overlay.style.width = "100%";
        overlay.style.height = "100%";
        overlay.style.background =
            "rgba(255,255,255,0.7)";
        overlay.style.display = "flex";
        overlay.style.justifyContent = "center";
        overlay.style.alignItems = "center";
        overlay.style.zIndex = "10000";

        overlay.innerHTML = `
            <div class="spinner-border text-primary"
                 style="width:4rem;height:4rem;">
            </div>
        `;

        document.body.appendChild(overlay);

    }

}

function hideLoading() {

    const overlay =
        document.getElementById("loadingOverlay");

    if (overlay) {

        overlay.remove();

    }

}

// ==========================================
// Console
// ==========================================

console.log(
    "AI Health Symptom Checker Loaded Successfully"
);