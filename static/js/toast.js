function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = "toast-message " + type;
    toast.style.cssText = `
        background: ${type === "success" ? "#4caf50" :
                     type === "error" ? "#f44336" :
                     type === "warning" ? "#ff9800" :
                     "#2196f3"};
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        margin-top: 10px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        opacity: 0;
        transform: translateX(20px);
        transition: all .4s ease;
    `;

    toast.innerText = message;
    container.appendChild(toast);

    // Aparición
    setTimeout(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateX(0)";
    }, 100);

    // Desaparición
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(20px)";
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

// Procesa los mensajes del backend
document.addEventListener("DOMContentLoaded", function () {
    const djangoMessages = document.querySelectorAll(".alert");

    djangoMessages.forEach(msg => {
        let tipo = "info";
        if (msg.classList.contains("alert-success")) tipo = "success";
        if (msg.classList.contains("alert-error")) tipo = "error";
        if (msg.classList.contains("alert-warning")) tipo = "warning";

        showToast(msg.innerText.trim(), tipo);
        msg.remove();
    });
});

function showToast(text, tipo = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.classList.add("toast", `toast-${tipo}`);
    toast.textContent = text;

    container.appendChild(toast);

    setTimeout(() => toast.remove(), 4000);
}

// Exportar función para uso global
window.showToast = showToast;
