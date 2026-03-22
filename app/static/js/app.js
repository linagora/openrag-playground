// Copyright 2026 LINAGORA
// SPDX-License-Identifier: AGPL-3.0-only
/* OpenRAG Playground — minimal client-side JS */

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Lucide icons
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

    // Re-initialize icons after HTMX swaps
    document.body.addEventListener("htmx:afterSwap", function () {
        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    });

    // --- Theme toggle ---
    var html = document.documentElement;
    var stored = localStorage.getItem("theme");
    if (stored) {
        html.setAttribute("data-theme", stored);
    }
    updateThemeIcon();

    document.body.addEventListener("click", function (e) {
        var toggle = e.target.closest("#theme-toggle");
        if (!toggle) return;
        var next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        updateThemeIcon();
    });

    function updateThemeIcon() {
        var toggle = document.getElementById("theme-toggle");
        if (!toggle) return;
        var isDark = html.getAttribute("data-theme") === "dark";
        toggle.innerHTML = isDark
            ? '<i data-lucide="sun" class="w-4 h-4"></i>'
            : '<i data-lucide="moon" class="w-4 h-4"></i>';
        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }

    // --- Language selector ---
    document.body.addEventListener("change", function (e) {
        if (e.target.id !== "lang-select") return;
        var form = new FormData();
        form.append("lang", e.target.value);
        fetch("/set-language", { method: "POST", body: form })
            .then(function () { window.location.reload(); });
    });

    // --- Reusable confirm modal ---
    window.showConfirmModal = function (msg, onConfirm) {
        var overlay = document.createElement("div");
        overlay.className = "confirm-overlay";
        overlay.innerHTML =
            '<div class="confirm-box">' +
            '  <h3>' + msg + '</h3>' +
            '  <div class="confirm-actions">' +
            '    <button class="confirm-cancel" data-action="cancel">Cancel</button>' +
            '    <button class="confirm-delete" data-action="delete">Delete</button>' +
            '  </div>' +
            '</div>';
        document.body.appendChild(overlay);
        overlay.addEventListener("click", function (ev) {
            var action = ev.target.getAttribute("data-action");
            if (action === "delete") onConfirm();
            if (action === "cancel" || action === "delete" || ev.target === overlay) {
                overlay.remove();
            }
        });
    };

    // Custom confirm modal for hx-confirm attributes
    document.body.addEventListener("htmx:confirm", function (e) {
        var msg = e.detail.question;
        if (!msg) return;
        e.preventDefault();
        showConfirmModal(msg, function () { e.detail.issueRequest(true); });
    });

    // --- Random user button (event delegation, survives HTMX swaps) ---
    document.body.addEventListener("click", function (e) {
        var btn = e.target.closest(".js-random-user");
        if (!btn) return;
        fetch("/admin/users/random")
            .then(function (r) { return r.json(); })
            .then(function (d) {
                var form = document.getElementById("user-form");
                if (!form) return;
                var f = function (sel) { return form.querySelector(sel); };
                if (f('[data-field="user-name"]')) f('[data-field="user-name"]').value = d.name;
                if (f('[data-field="user-title"]')) f('[data-field="user-title"]').value = d.title;
                if (f('[data-field="user-email"]')) f('[data-field="user-email"]').value = d.email;
                if (f('[data-field="user-genre"]')) f('[data-field="user-genre"]').value = d.genre;
                if (f('[data-field="user-color"]')) f('[data-field="user-color"]').value = d.avatar_color;
            });
    });
});
