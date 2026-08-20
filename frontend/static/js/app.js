// SalesGenie AI - Core Frontend Application Architecture
// Modular Left Sidebar CRM & Asynchronous Operations

// ============================================================
// JWT LOGIN GUARD
// ============================================================
(function () {
    const publicPages = ["/login", "/register"];
    const currentPath = window.location.pathname;
    const token = localStorage.getItem("salesgenie_jwt_token");

    if (!publicPages.includes(currentPath) && !token) {
        window.location.replace("/login");
        return;
    }

   
})();
document.addEventListener("DOMContentLoaded", function () {
    initAuthFlow();
    initQuickAddLeadForm();
    initAIScoringModal();
});

/* ==========================================================================
   Toast Notification Helper
   ========================================================================== */
function showToast(message, type = "success") {
    const toastEl = document.getElementById("actionToast");
    if (!toastEl) return;

    const toastText = document.getElementById("toastText");
    const toastIcon = document.getElementById("toastIcon");

    if (toastText) toastText.textContent = message;

    if (toastIcon) {
        toastIcon.className = "fs-5 bi";
        if (type === "success") {
            toastIcon.classList.add("bi-check-circle-fill", "text-success");
        } else if (type === "warning") {
            toastIcon.classList.add("bi-exclamation-triangle-fill", "text-warning");
        } else if (type === "danger" || type === "error") {
            toastIcon.classList.add("bi-x-circle-fill", "text-danger");
        } else {
            toastIcon.classList.add("bi-info-circle-fill", "text-primary");
        }
    }

    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();
}
window.showToast = showToast;

/* ==========================================================================
   AI Lead Scoring Interactive Calculator & Modal
   ========================================================================== */
let currentScoringLeadId = null;

function initAIScoringModal() {
    const scoringModal = document.getElementById("aiScoringModal");
    if (!scoringModal) return;

    scoringModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) return;

        currentScoringLeadId = button.getAttribute("data-lead-id");
        const company = button.getAttribute("data-company") || "Selected Company";
        const currentScore = parseFloat(button.getAttribute("data-current-score") || 0);

        const modalCompany = document.getElementById("scoringModalCompany");
        const currentScoreEl = document.getElementById("scoringCurrentScore");
        if (modalCompany) modalCompany.textContent = company;
        if (currentScoreEl) currentScoreEl.textContent = `${currentScore}%`;
        
        // Reset interactive inputs
        const emailEl = document.getElementById("aiEmailOpens");
        const visitEl = document.getElementById("aiWebsiteVisits");
        const demoEl = document.getElementById("aiDemoRequested");

        if (emailEl) emailEl.value = 10;
        if (visitEl) visitEl.value = 15;
        if (demoEl) demoEl.checked = true;

        calculatePredictedScore();
    });

    const calcInputs = ["aiEmailOpens", "aiWebsiteVisits", "aiDemoRequested"];
    calcInputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener("input", calculatePredictedScore);
            el.addEventListener("change", calculatePredictedScore);
        }
    });

    const applyScoreBtn = document.getElementById("applyAIScoreBtn");
    if (applyScoreBtn) {
        applyScoreBtn.addEventListener("click", applyScoreToLead);
    }
}

function calculatePredictedScore() {
    const emails = parseInt(document.getElementById("aiEmailOpens")?.value || 0, 10);
    const visits = parseInt(document.getElementById("aiWebsiteVisits")?.value || 0, 10);
    const demo = document.getElementById("aiDemoRequested")?.checked ? 1 : 0;

    let rawScore = (emails * 2.8) + (visits * 1.6) + (demo * 38.0) + 10.0;
    if (rawScore > 98.5) rawScore = 98.5;
    if (rawScore < 5.0) rawScore = 5.0;
    const computedScore = parseFloat(rawScore.toFixed(1));

    const meter = document.getElementById("aiScoreMeter");
    const scoreVal = document.getElementById("aiPredictedScoreVal");
    const catBadge = document.getElementById("aiPredictedCategoryBadge");

    if (scoreVal) scoreVal.textContent = `${computedScore}%`;
    if (meter) {
        meter.style.width = `${computedScore}%`;
        meter.setAttribute("aria-valuenow", computedScore);

        meter.className = "progress-bar progress-bar-striped progress-bar-animated";
        if (computedScore >= 90) {
            meter.classList.add("bg-danger");
        } else if (computedScore >= 70) {
            meter.classList.add("bg-teal");
        } else if (computedScore >= 50) {
            meter.classList.add("bg-warning");
        } else {
            meter.classList.add("bg-secondary");
        }
    }

    if (catBadge) {
        if (computedScore >= 90) {
            catBadge.className = "category-badge category-hot";
            catBadge.innerHTML = `<span class="pulse-indicator"></span> Hot (≥90%)`;
        } else if (computedScore >= 70) {
            catBadge.className = "category-badge category-qualified";
            catBadge.innerHTML = `<i class="bi bi-check2-circle"></i> Qualified (70-89%)`;
        } else if (computedScore >= 50) {
            catBadge.className = "category-badge category-warm";
            catBadge.innerHTML = `<i class="bi bi-sun-fill"></i> Warm (50-69%)`;
        } else {
            catBadge.className = "category-badge category-cold";
            catBadge.innerHTML = `<i class="bi bi-snow"></i> Cold (<50%)`;
        }
    }
}

async function applyScoreToLead() {
    if (!currentScoringLeadId) return;

    const scoreValText = document.getElementById("aiPredictedScoreVal")?.textContent || "0";
    const scoreNum = parseFloat(scoreValText);

    const btn = document.getElementById("applyAIScoreBtn");
    const spinner = document.getElementById("aiScoreSpinner");

    try {
        if (btn) btn.disabled = true;
        if (spinner) spinner.classList.remove("d-none");

        const response = await fetch(`/update_score/${currentScoringLeadId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ score: scoreNum })
        });

        const result = await response.json();
        if (response.ok && result.success) {
            const updated = result.data;
            const row = document.getElementById(`lead-row-${currentScoringLeadId}`);
            if (row) {
                row.setAttribute("data-category", updated.category);
                
                const scorePill = row.querySelector(".lead-score-pill");
                if (scorePill) {
                    scorePill.textContent = `${updated.score}%`;
                }

                const catPill = row.querySelector(".lead-category-pill");
                if (catPill) {
                    const cLower = updated.category.toLowerCase();
                    catPill.className = `category-badge category-${cLower} lead-category-pill`;
                    if (cLower === "hot") {
                        catPill.innerHTML = `<span class="pulse-indicator"></span> Hot`;
                    } else if (cLower === "qualified") {
                        catPill.innerHTML = `<i class="bi bi-check2-circle"></i> Qualified`;
                    } else if (cLower === "warm") {
                        catPill.innerHTML = `<i class="bi bi-sun-fill"></i> Warm`;
                    } else {
                        catPill.innerHTML = `<i class="bi bi-snow"></i> Cold`;
                    }
                }

                const triggerBtn = row.querySelector(`[data-bs-target="#aiScoringModal"]`);
                if (triggerBtn) {
                    triggerBtn.setAttribute("data-current-score", updated.score);
                }
            }

            const modalEl = document.getElementById("aiScoringModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            showToast(`Lead score updated to ${updated.score}% (${updated.category})`, "success");
            if (window.refreshPipelineCharts) window.refreshPipelineCharts();
            if (window.fetchAndUpdateKPIs) window.fetchAndUpdateKPIs();
        } else {
            showToast(result.message || "Failed to update AI score", "danger");
        }
    } catch (err) {
        showToast("Network error updating score", "danger");
    } finally {
        if (btn) btn.disabled = false;
        if (spinner) spinner.classList.add("d-none");
    }
}

/* ==========================================================================
   Quick Add Lead Form Async Handler
   ========================================================================== */
function initQuickAddLeadForm() {
    const form = document.getElementById("quickAddLeadForm");
    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const submitBtn = document.getElementById("quickAddSubmitBtn");
        const spinner = document.getElementById("quickAddSpinner");
        const icon = document.getElementById("quickAddIcon");

        const payload = {
            company: document.getElementById("qa_company").value.trim(),
            contact: document.getElementById("qa_contact").value.trim(),
            designation: document.getElementById("qa_designation").value.trim(),
            industry: document.getElementById("qa_industry").value,
            revenue: parseFloat(document.getElementById("qa_revenue").value || 0),
            stage: document.getElementById("qa_stage").value,
            notes: document.getElementById("qa_notes").value.trim()
        };

        if (!payload.company || !payload.contact) {
            showToast("Company name and Contact person are required", "warning");
            return;
        }

        try {
            submitBtn.disabled = true;
            spinner.classList.remove("d-none");
            icon.classList.add("d-none");

            const response = await fetch("/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (response.ok && data.success) {
                form.reset();
                const modalEl = document.getElementById("quickAddLeadModal");
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();

                showToast(`Opportunity for "${payload.company}" created!`, "success");
                setTimeout(() => window.location.reload(), 500);
            } else {
                showToast(data.message || "Failed to create lead", "danger");
            }
        } catch (err) {
            showToast("Network error while creating lead", "danger");
        } finally {
            submitBtn.disabled = false;
            spinner.classList.add("d-none");
            icon.classList.remove("d-none");
        }
    });
}

/* ==========================================================================
   Agent Authentication (JWT Session Verification)
   ========================================================================== */
function initAuthFlow() {
    const token = localStorage.getItem("salesgenie_jwt_token");
    if (token) {
        verifyAgentSession(token);
    }
}

async function verifyAgentSession(token) {
    try {
        const res = await fetch("/auth/me", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            const user = data.data;

            // Update Header Auth Profile
            const headerContainer = document.getElementById("headerAuthContainer");
            if (headerContainer) {
                headerContainer.innerHTML = `
                    <div class="dropdown">
                        <button class="btn btn-outline-primary btn-sm rounded-pill dropdown-toggle d-flex align-items-center gap-2 px-3 shadow-none" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-person-check-fill text-success"></i>
                            <span class="fw-semibold">@${user.username}</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 rounded-3 text-sm">
                            <li class="px-3 py-2 border-bottom">
                                <div class="text-xs text-secondary">Signed in as</div>
                                <div class="fw-bold text-dark text-truncate" style="max-width: 180px;">${user.email}</div>
                            </li>
                            <li>
                                <a class="dropdown-item text-danger py-2 d-flex align-items-center gap-2 sign-out-action" href="#">
                                    <i class="bi bi-box-arrow-right"></i> Sign Out
                                </a>
                            </li>
                        </ul>
                    </div>
                `;
            }

            // Update Sidebar Auth Profile
            const sidebarArea = document.getElementById("sidebarAuthArea");
            if (sidebarArea) {
                sidebarArea.innerHTML = `
                    <div class="p-2 rounded-3 bg-light border d-flex align-items-center justify-content-between">
                        <div class="d-flex align-items-center gap-2 overflow-hidden">
                            <div class="p-1 rounded-circle bg-success-subtle text-success d-flex align-items-center justify-content-center" style="width: 28px; height: 28px;">
                                <i class="bi bi-person-fill fs-6"></i>
                            </div>
                            <div class="overflow-hidden">
                                <div class="fw-bold text-dark text-xs text-truncate">@${user.username}</div>
                                <div class="text-muted text-xs text-truncate" style="font-size: 10px;">${user.email}</div>
                            </div>
                        </div>
                        <button class="btn btn-link text-danger p-0 sign-out-action" title="Sign Out">
                            <i class="bi bi-box-arrow-right fs-6"></i>
                        </button>
                    </div>
                `;
            }

            // Attach Sign Out Handlers
            document.querySelectorAll(".sign-out-action").forEach(btn => {
                btn.addEventListener("click", function (e) {
                    e.preventDefault();
                    localStorage.removeItem("salesgenie_jwt_token");
                    showToast("Signed out successfully", "info");
                    setTimeout(() => window.location.reload(), 400);
                });
            });
        } else {
            localStorage.removeItem("salesgenie_jwt_token");
        }
    } catch (e) {
        // Silently continue on network errors
    }
}
