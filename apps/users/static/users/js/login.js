

document.addEventListener("DOMContentLoaded", function () {
    const inputCedula = document.querySelector("#id_username");
    const inputPassword = document.querySelector("#id_password");
    const form = document.querySelector("#loginForm");

    // Validación en tiempo real: permitir solo números en cédula
    if (inputCedula) {
        inputCedula.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9]/g, "");
            
            // Remover clase de error si empieza a escribir correctamente
            if (this.value.length > 0 && /^[0-9]+$/.test(this.value)) {
                this.classList.remove("is-invalid");
            }
        });

        // Validar al salir del campo
        inputCedula.addEventListener("blur", function () {
            if (this.value.length === 0) {
                this.classList.add("is-invalid");
            }
        });
    }

    // Validación del formulario antes de enviar
    if (form) {
        form.addEventListener("submit", function (e) {
            let isValid = true;

            // Validar cédula
            if (!inputCedula.value || !/^[0-9]+$/.test(inputCedula.value)) {
                e.preventDefault();
                inputCedula.classList.add("is-invalid");
                showToast("La cédula solo debe contener números", "error");
                isValid = false;
            } else {
                inputCedula.classList.remove("is-invalid");
            }

            // Validar contraseña
            if (!inputPassword.value || inputPassword.value.trim() === "") {
                e.preventDefault();
                inputPassword.classList.add("is-invalid");
                if (isValid) {
                    showToast("Debe ingresar su contraseña", "error");
                }
                isValid = false;
            } else {
                inputPassword.classList.remove("is-invalid");
            }
        });
    }

    // Procesar mensajes de Django y mostrarlos como toast
    const djangoMessages = document.querySelectorAll(".django-message");
    djangoMessages.forEach(function (msgDiv) {
        const type = msgDiv.getAttribute("data-type");
        const text = msgDiv.textContent.trim();
        
        if (text) {
            // Mapear tipos de Django a tipos de toast
            let toastType = "info";
            if (type === "error" || type === "danger") {
                toastType = "error";
            } else if (type === "success") {
                toastType = "success";
            } else if (type === "warning") {
                toastType = "warning";
            }
            
            showToast(text, toastType);
        }
    });
});

// Función para mostrar toast (debe estar definida en toast.js o aquí)
function showToast(message, type = "info") {
    // Si ya existe la función en toast.js, usar esa
    // Si no, implementar una versión básica
    if (typeof window.showToast === "function") {
        window.showToast(message, type);
        return;
    }

    // Implementación básica si no existe toast.js
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type === "error" ? "danger" : type === "success" ? "success" : "info"} border-0`;
    toast.setAttribute("role", "alert");
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    container.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 4000 });
    bsToast.show();

    toast.addEventListener("hidden.bs.toast", function () {
        toast.remove();
    });
}
