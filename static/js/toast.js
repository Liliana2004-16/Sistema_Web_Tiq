
/**
 * @param {string} text 
 * @param {string} tipo 
 */
function showToast(text, tipo = "info") {
    const container = document.getElementById("toast-container");
    if (!container) {
        console.error("toast-container no encontrado en el DOM");
        return;
    }

    const toast = document.createElement("div");
    toast.classList.add("toast", `toast-${tipo}`);
    toast.textContent = text;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 4000);
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Sistema de toasts inicializado");
    
    const djangoMessages = document.querySelectorAll(".alert");

    djangoMessages.forEach(msg => {
        let tipo = "info";
        
        if (msg.classList.contains("alert-success")) tipo = "success";
        if (msg.classList.contains("alert-error") || msg.classList.contains("alert-danger")) tipo = "error";
        if (msg.classList.contains("alert-warning")) tipo = "warning";

        showToast(msg.innerText.trim(), tipo);
        msg.remove();
    });
});

window.showToast = showToast;