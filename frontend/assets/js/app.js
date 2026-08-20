// SalesGenie AI - Core Frontend Application Architecture

document.addEventListener("DOMContentLoaded", function () {
    initSearchAndFilters();
    initStageChangeHandlers();
    initQuickAddLeadForm();
    initAIScoringModal();
    initDeleteModal();
    initAuthFlow();
    fetchAndUpdateKPIs();
});

/* ==========================================================================
   Toast Notification Helper
   ========================================================================== */
function showToast(message, type = "success") {
    const toastEl = document.getElementById("actionToast");
    if (!toastEl) return;

    const toastText = document.getElementById("toastText");
    const toastIcon = document.getElementById("toastIcon");

    toastText.textContent = message;

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

    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();
}

/* ==========================================================================
   Live Search and Multi-Filtering System
   ========================================================================== */
function initSearchAndFilters() {
    const searchInput = document.getElementById("tableSearchInput");
    const stageFilter = document.getElementById("stageFilterSelect");
    const categoryFilter = document.getElementById("categoryFilterSelect");
    const counterEl = document.getElementById("filteredCountBadge");

    if (!searchInput && !stageFilter && !categoryFilter) return;

    function applyFilters() {
        const query = (searchInput ? searchInput.value : "").toLowerCase().trim();
        const selectedStage = stageFilter ? stageFilter.value : "";
        const selectedCategory = categoryFilter ? categoryFilter.value : "";

        const rows = document.querySelectorAll("#leadTableBody tr[data-lead-id]");
        let visibleCount = 0;

        rows.forEach(row => {
            const company = (row.querySelector(".lead-company")?.textContent || "").toLowerCase();
            const contact = (row.querySelector(".lead-contact")?.textContent || "").toLowerCase();
            const industry = (row.querySelector(".lead-industry")?.textContent || "").toLowerCase();
            const notes = (row.getAttribute("data-notes") || "").toLowerCase();

            const rowStage = row.getAttribute("data-stage") || "";
            const rowCategory = row.getAttribute("data-category") || "";

            const matchesQuery = !query || company.includes(query) || contact.includes(query) || industry.includes(query) || notes.includes(query);
            const matchesStage = !selectedStage || rowStage.toLowerCase() === selectedStage.toLowerCase();
            const matchesCategory = !selectedCategory || rowCategory.toLowerCase() === selectedCategory.toLowerCase();

            if (matchesQuery && matchesStage && matchesCategory) {
                row.style.display = "";
                visibleCount++;
            } else {
                row.style.display = "none";
            }
        });

        if (counterEl) {
            counterEl.textContent = `${visibleCount} of ${rows.length} leads`;
        }

        const emptyState = document.getElementById("tableNoResultsRow");
        if (emptyState) {
            emptyState.style.display = visibleCount === 0 && rows.length > 0 ? "" : "none";
        }
    }

    if (searchInput) searchInput.addEventListener("input", applyFilters);
    if (stageFilter) stageFilter.addEventListener("change", applyFilters);
    if (categoryFilter) categoryFilter.addEventListener("change", applyFilters);

    // Reset button
    const resetBtn = document.getElementById("resetFiltersBtn");
    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (searchInput) searchInput.value = "";
            if (stageFilter) stageFilter.value = "";
            if (categoryFilter) categoryFilter.value = "";
            applyFilters();
        });
    }
}

/* ==========================================================================
   Inline Pipeline Stage Change Handler
   ========================================================================== */
function initStageChangeHandlers() {
    document.addEventListener("change", async function (e) {
        if (!e.target.classList.contains("stage-select-dropdown")) return;

        const select = e.target;
        const leadId = select.getAttribute("data-lead-id");
        const newStage = select.value;
        const previousStage = select.getAttribute("data-current-stage");

        try {
            select.disabled = true;
            const response = await fetch(`/update_stage/${leadId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ stage: newStage })
            });

            const data = await response.json();
            if (response.ok && data.success) {
                select.setAttribute("data-current-stage", newStage);
                const row = document.getElementById(`lead-row-${leadId}`);
                if (row) {
                    row.setAttribute("data-stage", newStage);
                    updateStageBadgeInRow(row, newStage);
                }
                showToast(`Lead stage transitioned to "${newStage}"`, "success");
                if (window.refreshPipelineCharts) window.refreshPipelineCharts();
                fetchAndUpdateKPIs();
            } else {
                select.value = previousStage;
                showToast(data.message || "Failed to update stage", "danger");
            }
        } catch (err) {
            select.value = previousStage;
            showToast("Network error updating lead stage", "danger");
        } finally {
            select.disabled = false;
        }
    });
}

function updateStageBadgeInRow(row, stage) {
    const badge = row.querySelector(".lead-stage-badge");
    if (!badge) return;

    badge.className = "stage-badge lead-stage-badge";
    const stageKey = stage.toLowerCase().replace(/\s+/g, "-");
    badge.classList.add(`stage-${stageKey}`);
    badge.innerHTML = `<i class="bi bi-diagram-3-fill"></i> ${stage}`;
}

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

        document.getElementById("scoringModalCompany").textContent = company;
        document.getElementById("scoringCurrentScore").textContent = `${currentScore}%`;
        
        // Reset interactive inputs
        document.getElementById("aiEmailOpens").value = 10;
        document.getElementById("aiWebsiteVisits").value = 15;
        document.getElementById("aiDemoRequested").checked = true;

        // Perform initial calculation
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

async function calculatePredictedScore() {
    const emails = parseInt(document.getElementById("aiEmailOpens")?.value || 0, 10);
    const visits = parseInt(document.getElementById("aiWebsiteVisits")?.value || 0, 10);
    const demo = document.getElementById("aiDemoRequested")?.checked ? 1 : 0;

    const meter = document.getElementById("aiScoreMeter");
    const scoreVal = document.getElementById("aiPredictedScoreVal");
    const catBadge = document.getElementById("aiPredictedCategoryBadge");

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ emails, visits, demo })
        });
        const result = await response.json();
        if (response.ok && result.success) {
            const computedScore = result.score;

            if (scoreVal) scoreVal.textContent = `${computedScore}%`;
            if (meter) {
                meter.style.width = `${computedScore}%`;
                meter.setAttribute("aria-valuenow", computedScore);

                meter.className = "progress-bar progress-bar-striped progress-bar-animated";
                if (computedScore >= 70) {
                    meter.classList.add("bg-danger");
                } else if (computedScore >= 40) {
                    meter.classList.add("bg-warning");
                } else {
                    meter.classList.add("bg-secondary");
                }
            }

            if (catBadge) {
                if (computedScore >= 70) {
                    catBadge.className = "category-badge category-hot";
                    catBadge.innerHTML = `<span class="pulse-indicator"></span> Hot (High Conversion)`;
                } else if (computedScore >= 40) {
                    catBadge.className = "category-badge category-warm";
                    catBadge.innerHTML = `<i class="bi bi-sun-fill"></i> Warm (Nurture)`;
                } else {
                    catBadge.className = "category-badge category-cold";
                    catBadge.innerHTML = `<i class="bi bi-snow"></i> Cold (Low Engagement)`;
                }
            }
        }
    } catch (e) {
        console.error("Error predicting score:", e);
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
                
                // Update score column
                const scorePill = row.querySelector(".lead-score-pill");
                if (scorePill) {
                    scorePill.textContent = `${updated.score}%`;
                }

                // Update category column
                const catPill = row.querySelector(".lead-category-pill");
                if (catPill) {
                    const cLower = updated.category.toLowerCase();
                    catPill.className = `category-badge category-${cLower} lead-category-pill`;
                    if (cLower === "hot") {
                        catPill.innerHTML = `<span class="pulse-indicator"></span> Hot`;
                    } else if (cLower === "warm") {
                        catPill.innerHTML = `<i class="bi bi-sun-fill"></i> Warm`;
                    } else {
                        catPill.innerHTML = `<i class="bi bi-snow"></i> Cold`;
                    }
                }

                // Update trigger button attribute
                const triggerBtn = row.querySelector(`[data-bs-target="#aiScoringModal"]`);
                if (triggerBtn) {
                    triggerBtn.setAttribute("data-current-score", updated.score);
                }
            }

            // Close modal
            const modalEl = document.getElementById("aiScoringModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            showToast(`Lead score updated to ${updated.score}% (${updated.category})`, "success");
            if (window.refreshPipelineCharts) window.refreshPipelineCharts();
            fetchAndUpdateKPIs();
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
   Delete Confirmation Modal & Action
   ========================================================================== */
let pendingDeleteLeadId = null;

function initDeleteModal() {
    const deleteModal = document.getElementById("deleteConfirmModal");
    if (!deleteModal) return;

    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) return;

        pendingDeleteLeadId = button.getAttribute("data-lead-id");
        const company = button.getAttribute("data-company") || "this lead";
        document.getElementById("deleteModalLeadName").textContent = company;
    });

    const confirmBtn = document.getElementById("confirmDeleteLeadBtn");
    if (confirmBtn) {
        confirmBtn.addEventListener("click", async function () {
            if (!pendingDeleteLeadId) return;

            confirmBtn.disabled = true;
            try {
                const response = await fetch(`/delete/${pendingDeleteLeadId}`, {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" }
                });

                const result = await response.json();
                if (response.ok && result.success) {
                    const row = document.getElementById(`lead-row-${pendingDeleteLeadId}`);
                    if (row) {
                        row.classList.add("table-danger");
                        setTimeout(() => row.remove(), 250);
                    }

                    const modal = bootstrap.Modal.getInstance(deleteModal);
                    if (modal) modal.hide();

                    showToast("Lead successfully deleted from pipeline", "success");
                    setTimeout(() => {
                        if (window.refreshPipelineCharts) window.refreshPipelineCharts();
                        fetchAndUpdateKPIs();
                    }, 300);
                } else {
                    showToast(result.message || "Could not delete lead", "danger");
                }
            } catch (err) {
                showToast("Network error during delete", "danger");
            } finally {
                confirmBtn.disabled = false;
            }
        });
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
                setTimeout(() => window.location.reload(), 600);
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
   Real-Time KPI Poller & Metric Refresh
   ========================================================================== */
async function fetchAndUpdateKPIs() {
    try {
        const response = await fetch("/api/kpis");
        if (!response.ok) return;

        const result = await response.json();
        if (result.success && result.data) {
            const data = result.data;
            const kpiTotal = document.getElementById("kpi_total_leads");
            const kpiConv = document.getElementById("kpi_conversion_rate");
            const kpiVal = document.getElementById("kpi_pipeline_value");
            const kpiAvgScore = document.getElementById("kpi_avg_score");
            const kpiCycle = document.getElementById("kpi_avg_cycle");

            if (kpiTotal) kpiTotal.textContent = data.total_leads;
            if (kpiConv) kpiConv.textContent = `${data.conversion_rate}%`;
            if (kpiVal) kpiVal.textContent = `$${Number(data.pipeline_value).toLocaleString()}`;
            if (kpiAvgScore) kpiAvgScore.textContent = `${data.average_score}%`;
            if (kpiCycle) kpiCycle.textContent = `${data.average_cycle_days}d`;
        }
    } catch (e) {
        // Silently skip if polling fails
    }
}

/* ==========================================================================
   Agent Authentication (JWT)
   ========================================================================== */
function initAuthFlow() {
    const token = localStorage.getItem("salesgenie_jwt_token");
    if (token) {
        verifyAgentSession(token);
    }

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const identifier = document.getElementById("loginIdentifier").value.trim();
            const password = document.getElementById("loginPassword").value;
            const alertBox = document.getElementById("loginAlert");
            const spinner = document.getElementById("loginSpinner");
            const submitBtn = document.getElementById("loginSubmitBtn");

            try {
                submitBtn.disabled = true;
                spinner.classList.remove("d-none");
                alertBox.classList.add("d-none");

                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username_or_email: identifier, password: password })
                });

                const res = await response.json();
                if (response.ok && res.success) {
                    const token = res.data.access_token;
                    localStorage.setItem("salesgenie_jwt_token", token);
                    showToast("Authentication successful! Welcome agent.", "success");
                    
                    const modalEl = document.getElementById("authModal");
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    if (modal) modal.hide();

                    verifyAgentSession(token);
                } else {
                    alertBox.textContent = res.message || "Invalid credentials";
                    alertBox.classList.remove("d-none");
                }
            } catch (err) {
                alertBox.textContent = "Network error during authentication";
                alertBox.classList.remove("d-none");
            } finally {
                submitBtn.disabled = false;
                spinner.classList.add("d-none");
            }
        });
    }

    const regForm = document.getElementById("registerForm");
    if (regForm) {
        regForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const username = document.getElementById("regUsername").value.trim();
            const email = document.getElementById("regEmail").value.trim();
            const password = document.getElementById("regPassword").value;
            const alertBox = document.getElementById("registerAlert");
            const spinner = document.getElementById("registerSpinner");
            const submitBtn = document.getElementById("registerSubmitBtn");

            try {
                submitBtn.disabled = true;
                spinner.classList.remove("d-none");
                alertBox.classList.add("d-none");

                const response = await fetch("/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password })
                });

                const res = await response.json();
                if (response.ok && res.success) {
                    showToast("Registration complete! Please sign in.", "success");
                    document.getElementById("login-tab")?.click();
                    document.getElementById("loginIdentifier").value = username;
                } else {
                    alertBox.textContent = res.message || "Registration failed";
                    alertBox.classList.remove("d-none");
                }
            } catch (err) {
                alertBox.textContent = "Network error during registration";
                alertBox.classList.remove("d-none");
            } finally {
                submitBtn.disabled = false;
                spinner.classList.add("d-none");
            }
        });
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
            const container = document.getElementById("authContainer");
            if (container) {
                container.innerHTML = `
                    <div class="dropdown">
                        <button class="btn btn-outline-primary btn-sm rounded-pill dropdown-toggle d-flex align-items-center gap-2 px-3 shadow-sm" type="button" data-bs-toggle="dropdown">
                            <i class="bi bi-person-check-fill text-success"></i>
                            <span class="fw-semibold">@${user.username}</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3">
                            <li class="px-3 py-2 border-bottom">
                                <div class="text-xs text-secondary">Signed in as</div>
                                <div class="fw-bold text-dark text-sm text-truncate" style="max-width: 180px;">${user.email}</div>
                            </li>
                            <li>
                                <a class="dropdown-item text-danger py-2 d-flex align-items-center gap-2" href="#" id="signOutBtn">
                                    <i class="bi bi-box-arrow-right"></i> Sign Out
                                </a>
                            </li>
                        </ul>
                    </div>
                `;
                document.getElementById("signOutBtn")?.addEventListener("click", function (e) {
                    e.preventDefault();
                    localStorage.removeItem("salesgenie_jwt_token");
                    showToast("Signed out successfully", "info");
                    setTimeout(() => window.location.reload(), 400);
                });
            }
        } else {
            localStorage.removeItem("salesgenie_jwt_token");
        }
    } catch (e) {
        // Skip on network errors
    }
}
