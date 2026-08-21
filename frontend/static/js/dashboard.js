// SalesGenie AI - Real-time Dashboard & KPI Metrics Module

document.addEventListener("DOMContentLoaded", function () {
    initDashboardKPIRefresh();
});

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
            if (kpiVal) kpiVal.textContent = `$${Number(data.pipeline_value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            if (kpiAvgScore) kpiAvgScore.textContent = `${data.average_score}%`;
            if (kpiCycle) kpiCycle.textContent = `${data.average_cycle_days}d`;
        }
    } catch (e) {
        // Silently skip if polling fails
    }
}

window.fetchAndUpdateKPIs = fetchAndUpdateKPIs;

function initDashboardKPIRefresh() {
    fetchAndUpdateKPIs();
}
