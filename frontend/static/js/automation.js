// SalesGenie AI - Automation & Real-time Integrations Module

window.showToast = function (message, type = "success") {
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
};
