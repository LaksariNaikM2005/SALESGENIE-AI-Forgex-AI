// SalesGenie AI - Lead Pipeline & Table Management

document.addEventListener("DOMContentLoaded", function () {
    initLeadSearchAndFilter();
    initLeadStageTransitions();
    initLeadDeletion();
});

function initLeadSearchAndFilter() {
    const searchInput = document.getElementById("tableSearchInput");
    const stageFilter = document.getElementById("stageFilterSelect");
    const categoryFilter = document.getElementById("categoryFilterSelect");
    const countBadge = document.getElementById("filteredCountBadge");

    if (!searchInput && !stageFilter && !categoryFilter) return;

    function filterRows() {
        const query = (searchInput ? searchInput.value : "").toLowerCase().trim();
        const selectedStage = (stageFilter ? stageFilter.value : "").toLowerCase();
        const selectedCategory = (categoryFilter ? categoryFilter.value : "").toLowerCase();

        const rows = document.querySelectorAll("#leadTableBody tr[data-lead-id]");
        let visible = 0;

        rows.forEach(row => {
            const company = (row.querySelector(".lead-company")?.textContent || "").toLowerCase();
            const contact = (row.querySelector(".lead-contact")?.textContent || "").toLowerCase();
            const industry = (row.querySelector(".lead-industry")?.textContent || "").toLowerCase();
            const notes = (row.getAttribute("data-notes") || "").toLowerCase();

            const rowStage = (row.getAttribute("data-stage") || "").toLowerCase();
            const rowCat = (row.getAttribute("data-category") || "").toLowerCase();

            const matchQuery = !query || company.includes(query) || contact.includes(query) || industry.includes(query) || notes.includes(query);
            const matchStage = !selectedStage || rowStage === selectedStage;
            const matchCat = !selectedCategory || rowCat === selectedCategory;

            if (matchQuery && matchStage && matchCat) {
                row.style.display = "";
                visible++;
            } else {
                row.style.display = "none";
            }
        });

        if (countBadge) {
            countBadge.textContent = `${visible} of ${rows.length} leads`;
        }

        const noResults = document.getElementById("tableNoResultsRow");
        if (noResults) {
            noResults.style.display = visible === 0 && rows.length > 0 ? "" : "none";
        }
    }

    if (searchInput) searchInput.addEventListener("input", filterRows);
    if (stageFilter) stageFilter.addEventListener("change", filterRows);
    if (categoryFilter) categoryFilter.addEventListener("change", filterRows);

    const resetBtn = document.getElementById("resetFiltersBtn");
    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (searchInput) searchInput.value = "";
            if (stageFilter) stageFilter.value = "";
            if (categoryFilter) categoryFilter.value = "";
            filterRows();
        });
    }
}

function initLeadStageTransitions() {
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
                }
                if (window.showToast) window.showToast(`Lead stage updated to "${newStage}"`, "success");
                if (window.refreshPipelineCharts) window.refreshPipelineCharts();
                if (window.fetchAndUpdateKPIs) window.fetchAndUpdateKPIs();
            } else {
                select.value = previousStage;
                if (window.showToast) window.showToast(data.message || "Failed to update stage", "danger");
            }
        } catch (err) {
            select.value = previousStage;
            if (window.showToast) window.showToast("Network error updating stage", "danger");
        } finally {
            select.disabled = false;
        }
    });
}

function initLeadDeletion() {
    let targetDeleteLeadId = null;
    const deleteModal = document.getElementById("deleteConfirmModal");

    if (deleteModal) {
        deleteModal.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;
            if (!button) return;
            targetDeleteLeadId = button.getAttribute("data-lead-id");
            const company = button.getAttribute("data-company") || "this lead";
            const nameSpan = document.getElementById("deleteModalLeadName");
            if (nameSpan) nameSpan.textContent = company;
        });
    }

    const confirmBtn = document.getElementById("confirmDeleteLeadBtn");
    if (confirmBtn) {
        confirmBtn.addEventListener("click", async function () {
            if (!targetDeleteLeadId) return;

            confirmBtn.disabled = true;
            try {
                const response = await fetch(`/delete/${targetDeleteLeadId}`, {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" }
                });

                const data = await response.json();
                if (response.ok && data.success) {
                    const row = document.getElementById(`lead-row-${targetDeleteLeadId}`);
                    if (row) {
                        row.classList.add("table-danger");
                        setTimeout(() => row.remove(), 250);
                    }

                    if (deleteModal) {
                        const modal = bootstrap.Modal.getInstance(deleteModal);
                        if (modal) modal.hide();
                    }

                    if (window.showToast) window.showToast("Lead successfully deleted", "success");
                    setTimeout(() => {
                        if (window.refreshPipelineCharts) window.refreshPipelineCharts();
                        if (window.fetchAndUpdateKPIs) window.fetchAndUpdateKPIs();
                    }, 300);
                } else {
                    if (window.showToast) window.showToast(data.message || "Failed to delete lead", "danger");
                }
            } catch (err) {
                if (window.showToast) window.showToast("Network error deleting lead", "danger");
            } finally {
                confirmBtn.disabled = false;
            }
        });
    }
}
