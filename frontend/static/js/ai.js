// SalesGenie AI - AI Intelligence & Outreach Generation Module

document.addEventListener("DOMContentLoaded", function () {
    initAISimulator();
    initAIEmailGenerator();
});

/* ==========================================================================
   AI Lead Intelligence Simulator & Scoring
   ========================================================================== */
function initAISimulator() {
    const emailRange = document.getElementById("intelEmailOpens");
    const visitRange = document.getElementById("intelWebsiteVisits");
    const growthSelect = document.getElementById("intelCompanyGrowth");
    const icpSelect = document.getElementById("intelIndustryMatch");
    const demoToggle = document.getElementById("intelDemoRequest");
    const recalcBtn = document.getElementById("recalculateIntelBtn");

    if (!emailRange || !visitRange) return;

    function updateLabelsAndCompute() {
        const emails = parseInt(emailRange.value, 10);
        const visits = parseInt(visitRange.value, 10);
        const growth = growthSelect ? growthSelect.value : "high";
        const icp = icpSelect ? icpSelect.value : "exact";
        const demo = demoToggle && demoToggle.checked ? 1 : 0;

        const emailLabel = document.getElementById("emailValLabel");
        const visitLabel = document.getElementById("visitValLabel");
        if (emailLabel) emailLabel.textContent = emails;
        if (visitLabel) visitLabel.textContent = visits;

        // Random Forest feature weights matching Milestone 2
        let score = (emails * 1.6) + (visits * 0.9) + (demo * 35.0);
        if (growth === "high") score += 15;
        else if (growth === "moderate") score += 8;

        if (icp === "exact") score += 20;
        else if (icp === "secondary") score += 10;

        if (score > 98) score = 98;
        if (score < 15) score = 15;
        score = Math.round(score);

        // Milestone 2 Category: 90-100 Hot, 70-89 Qualified, 50-69 Warm, <50 Cold
        let category = "Cold";
        let catClass = "category-cold";
        let catHtml = '<i class="bi bi-snow"></i> COLD LEAD';
        let convProb = Math.min(Math.round(score * 0.92), 95);
        let nextAction = "Nurture via automated monthly newsletter";
        let actionPriority = "Low Priority";
        let actionReason = "Low direct engagement signals. Keep lead in automated drip campaign.";

        if (score >= 90) {
            category = "Hot";
            catClass = "category-hot";
            catHtml = '<span class="pulse-indicator"></span> HOT LEAD';
            nextAction = "Next Best Action: Schedule Product Demo with Executive Sponsor";
            actionPriority = "High Priority";
            actionReason = "Lead exhibits peak engagement signals and high ICP alignment. Recommended action is direct executive presentation within 24 hours.";
        } else if (score >= 70) {
            category = "Qualified";
            catClass = "category-qualified";
            catHtml = '<i class="bi bi-check2-circle"></i> QUALIFIED LEAD';
            nextAction = "Next Best Action: Deliver Tailored Proposal & ROI Benchmark";
            actionPriority = "Medium Priority";
            actionReason = "Solid ICP fit with active discovery. Send formal proposal addressing primary pain points.";
        } else if (score >= 50) {
            category = "Warm";
            catClass = "category-warm";
            catHtml = '<i class="bi bi-sun-fill"></i> WARM LEAD';
            nextAction = "Next Best Action: Share Industry Case Study on LinkedIn & Email";
            actionPriority = "Medium Priority";
            actionReason = "Moderate interest detected. Share relevant customer success stories to build confidence.";
        }

        const scoreDisplay = document.getElementById("intelScoreDisplay");
        const statusBadge = document.getElementById("intelStatusBadge");
        const convProbDisplay = document.getElementById("intelConvProbDisplay");
        const progressBar = document.getElementById("intelProgressBar");
        const actionTitle = document.getElementById("intelNextActionTitle");
        const actionReasonEl = document.getElementById("intelActionReason");

        if (scoreDisplay) scoreDisplay.textContent = `${score} / 100`;
        if (statusBadge) {
            statusBadge.className = `category-badge ${catClass}`;
            statusBadge.innerHTML = catHtml;
        }
        if (convProbDisplay) convProbDisplay.textContent = `${convProb}%`;
        if (progressBar) {
            progressBar.style.width = `${score}%`;
            progressBar.className = `progress-bar ${score >= 90 ? 'bg-danger' : score >= 70 ? 'bg-teal' : score >= 50 ? 'bg-warning' : 'bg-secondary'}`;
        }
        if (actionTitle) actionTitle.textContent = nextAction;
        if (actionReasonEl) actionReasonEl.textContent = actionReason;
    }

    [emailRange, visitRange, growthSelect, icpSelect, demoToggle].forEach(el => {
        if (el) {
            el.addEventListener("input", updateLabelsAndCompute);
            el.addEventListener("change", updateLabelsAndCompute);
        }
    });

    if (recalcBtn) {
        recalcBtn.addEventListener("click", function () {
            updateLabelsAndCompute();
            if (window.showToast) window.showToast("AI Intelligence Model recalculated successfully!", "success");
        });
    }
}

/* ==========================================================================
   AI Outreach & Cold Email Generator
   ========================================================================== */
function initAIEmailGenerator() {
    const form = document.getElementById("aiEmailGenForm");
    const subjectInput = document.getElementById("generatedEmailSubject");
    const bodyArea = document.getElementById("generatedEmailBody");
    const copyBtn = document.getElementById("copyEmailBtn");
    const regenBtn = document.getElementById("regenerateEmailBtn");
    const clearBtn = document.getElementById("clearEmailBtn");

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            generateColdEmail();
        });
    }

    function generateColdEmail() {
        const prospect = document.getElementById("outreachProspectName")?.value || "Prospect";
        const company = document.getElementById("outreachCompany")?.value || "Your Company";
        const title = document.getElementById("outreachJobTitle")?.value || "Leader";
        const industry = document.getElementById("outreachIndustry")?.value || "Software";
        const event = document.getElementById("outreachEvent")?.value || "recent growth";
        const painPoint = document.getElementById("outreachPainPoint")?.value || "scaling pipeline velocity";

        const spinner = document.getElementById("genEmailSpinner");
        const icon = document.getElementById("genEmailIcon");
        const btn = document.getElementById("generateEmailBtn");

        if (spinner) spinner.classList.remove("d-none");
        if (icon) icon.classList.add("d-none");
        if (btn) btn.disabled = true;

        setTimeout(() => {
            if (subjectInput) {
                subjectInput.value = `Scaling ${company}'s enterprise revenue with automated AI lead qualification`;
            }
            if (bodyArea) {
                bodyArea.value = `Hi ${prospect},

Noticed ${company}'s recent milestone regarding ${event}—congratulations on the great momentum!

As sales operations scale in the ${industry} space, ${painPoint.toLowerCase()} often creates severe friction for closing enterprise deals. With SalesGenie AI, revenue teams automate behavioral lead scoring and surface high-converting opportunities in real-time.

Given your role as ${title}, would you be open to a brief 15-minute conversation next Tuesday to see how peer teams in ${industry} are reducing sales cycles by 35%?

Best regards,

Enterprise Sales Intelligence Team
SalesGenie AI`;
            }

            if (spinner) spinner.classList.add("d-none");
            if (icon) icon.classList.remove("d-none");
            if (btn) btn.disabled = false;

            if (window.showToast) window.showToast("Personalized cold email generated!", "success");
        }, 350);
    }

    if (copyBtn && bodyArea) {
        copyBtn.addEventListener("click", function () {
            const fullText = `Subject: ${subjectInput ? subjectInput.value : ''}

${bodyArea.value}`;
            navigator.clipboard.writeText(fullText).then(() => {
                if (window.showToast) window.showToast("Email content copied to clipboard!", "success");
            });
        });
    }

    if (regenBtn) {
        regenBtn.addEventListener("click", function () {
            generateColdEmail();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            if (subjectInput) subjectInput.value = "";
            if (bodyArea) bodyArea.value = "";
            if (window.showToast) window.showToast("Email content cleared", "info");
        });
    }
}
