// SalesGenie AI - Pipeline & Analytics Visualizations
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

    const labels = Object.keys(stageCounts);
    const data = Object.values(stageCounts);

    if (stageChartInstance) {
        stageChartInstance.destroy();
    }

    stageChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Number of Leads",
                data: data,
                backgroundColor: [
                    "rgba(100, 116, 139, 0.75)", // New Lead (Slate)
                    "rgba(59, 130, 246, 0.75)",  // Qualified (Blue)
                    "rgba(139, 92, 246, 0.75)",  // Proposal (Purple)
                    "rgba(245, 158, 11, 0.75)",  // Negotiation (Amber)
                    "rgba(16, 185, 129, 0.75)"   // Closed Won (Emerald)
                ],
                borderColor: [
                    "#64748b",
                    "#3b82f6",
                    "#8b5cf6",
                    "#f59e0b",
                    "#10b981"
                ],
                borderWidth: 1.5,
                borderRadius: 6,
                barPercentage: 0.6
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
                    padding: 10,
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
                        font: { family: "Plus Jakarta Sans", size: 11, weight: "500" },
                        color: "#475569"
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

    const categoryCounts = {
        "Hot": 0,
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

    const total = categoryCounts.Hot + categoryCounts.Warm + categoryCounts.Cold;
    const labels = ["Hot (Score >= 70)", "Warm (Score 40-69)", "Cold (Score < 40)"];
    const data = total > 0 ? [categoryCounts.Hot, categoryCounts.Warm, categoryCounts.Cold] : [0, 0, 0];

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
                    "#ef4444", // Hot (Red)
                    "#f59e0b", // Warm (Amber)
                    "#94a3b8"  // Cold (Slate)
                ] : ["#e2e8f0"],
                borderWidth: 2,
                borderColor: "#ffffff",
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "70%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        boxWidth: 12,
                        font: { family: "Plus Jakarta Sans", size: 11, weight: "500" },
                        color: "#475569",
                        padding: 12
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

// Global hook for live refresh without full reload
window.refreshPipelineCharts = function () {
    initPipelineStageChart();
    initLeadCategoryChart();
};
