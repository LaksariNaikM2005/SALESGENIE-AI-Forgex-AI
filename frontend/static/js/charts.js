// SalesGenie AI - Pipeline & Analytics Visualizations
// Teammate requested color hierarchy:
// New Lead -> Blue (#3b82f6), Qualified -> Teal (#0d9488), Proposal -> Purple (#8b5cf6), Negotiation -> Orange (#f97316), Closed Won -> Green (#10b981)

document.addEventListener("DOMContentLoaded", function () {
    initPipelineStageChart();
    initLeadCategoryChart();
});

let stageChartInstance = null;
let categoryChartInstance = null;

function initPipelineStageChart() {
    const ctx = document.getElementById("pipelineStageChart");
    if (!ctx) return;

    // Collect stage counts from the table rows or injected dataset
    const stageCounts = {
        "New Lead": 0,
        "Qualified": 0,
        "Proposal": 0,
        "Negotiation": 0,
        "Closed Won": 0
    };

    const rows = document.querySelectorAll("#leadTableBody tr[data-stage]");
    rows.forEach(row => {
        const stage = row.getAttribute("data-stage");
        if (stageCounts.hasOwnProperty(stage)) {
            stageCounts[stage]++;
        } else {
            stageCounts["New Lead"]++;
        }
    });

    const labels = ["New Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"];
    const data = labels.map(l => stageCounts[l] || 0);

    if (stageChartInstance) {
        stageChartInstance.destroy();
    }

    stageChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Leads in Stage",
                data: data,
                backgroundColor: [
                    "rgba(59, 130, 246, 0.85)",   // New Lead -> Blue
                    "rgba(13, 148, 136, 0.85)",   // Qualified -> Teal
                    "rgba(139, 92, 246, 0.85)",  // Proposal -> Purple
                    "rgba(249, 115, 22, 0.85)",   // Negotiation -> Orange
                    "rgba(16, 185, 129, 0.85)"   // Closed Won -> Green
                ],
                borderColor: [
                    "#3b82f6",
                    "#0d9488",
                    "#8b5cf6",
                    "#f97316",
                    "#10b981"
                ],
                borderWidth: 1.5,
                borderRadius: 8,
                barPercentage: 0.55
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: "#0f172a",
                    titleFont: { family: "Plus Jakarta Sans", weight: "bold" },
                    bodyFont: { family: "Plus Jakarta Sans" },
                    padding: 12,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: { family: "Plus Jakarta Sans", size: 11 },
                        color: "#64748b"
                    },
                    grid: {
                        color: "#f1f5f9"
                    }
                },
                x: {
                    ticks: {
                        font: { family: "Plus Jakarta Sans", size: 11, weight: "600" },
                        color: "#334155"
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function initLeadCategoryChart() {
    const ctx = document.getElementById("leadCategoryChart");
    if (!ctx) return;

    // Milestone 2 Category Definitions: 90-100 Hot, 70-89 Qualified, 50-69 Warm, <50 Cold
    const categoryCounts = {
        "Hot": 0,
        "Qualified": 0,
        "Warm": 0,
        "Cold": 0
    };

    const rows = document.querySelectorAll("#leadTableBody tr[data-category]");
    rows.forEach(row => {
        const cat = row.getAttribute("data-category");
        if (categoryCounts.hasOwnProperty(cat)) {
            categoryCounts[cat]++;
        } else {
            categoryCounts["Cold"]++;
        }
    });

    const total = categoryCounts.Hot + categoryCounts.Qualified + categoryCounts.Warm + categoryCounts.Cold;
    const labels = ["Hot (90-100%)", "Qualified (70-89%)", "Warm (50-69%)", "Cold (<50%)"];
    const data = total > 0
        ? [categoryCounts.Hot, categoryCounts.Qualified, categoryCounts.Warm, categoryCounts.Cold]
        : [0, 0, 0, 0];

    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    categoryChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels,
            datasets: [{
                data: total > 0 ? data : [1],
                backgroundColor: total > 0 ? [
                    "#ef4444", // Hot -> Red
                    "#0d9488", // Qualified -> Teal
                    "#f59e0b", // Warm -> Amber
                    "#64748b"  // Cold -> Slate
                ] : ["#e2e8f0"],
                borderWidth: 2,
                borderColor: "#ffffff",
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "68%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        boxWidth: 10,
                        font: { family: "Plus Jakarta Sans", size: 11, weight: "500" },
                        color: "#475569",
                        padding: 10
                    }
                },
                tooltip: {
                    enabled: total > 0,
                    backgroundColor: "#0f172a",
                    padding: 10,
                    cornerRadius: 8,
                    callbacks: {
                        label: function (context) {
                            const val = context.raw || 0;
                            const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
                            return ` ${context.label}: ${val} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Global hook for live refresh
window.refreshPipelineCharts = function () {
    initPipelineStageChart();
    initLeadCategoryChart();
};
