// register.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    
    // Agregar clases de Bootstrap a los campos del formulario
    addFormClasses();
    
    // Validación en tiempo real
    setupRealTimeValidation();
    
    // Validación al enviar el formulario
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
    
    // Auto-desaparecer alertas después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * Agregar clases de Bootstrap a los campos del formulario
 */
function addFormClasses() {
    const textInputs = document.querySelectorAll('input[type="text"], input[type="email"]');
    const selects = document.querySelectorAll('select');
    
    textInputs.forEach(input => {
        input.classList.add('form-control');
        
        // Placeholder según el tipo de campo
        if (input.name.includes('cedula')) {
            input.setAttribute('placeholder', 'Ingrese número de cédula');
        } else if (input.name.includes('email')) {
            input.setAttribute('placeholder', 'ejemplo@correo.com');
        } else if (input.name.includes('first_name')) {
            input.setAttribute('placeholder', 'Ingrese el nombre');
        } else if (input.name.includes('last_name')) {
            input.setAttribute('placeholder', 'Ingrese el apellido');
        }
    });
    
    selects.forEach(select => {
        select.classList.add('form-select');
        
        // Agregar opción por defecto si no existe
        if (select.options.length === 0 || select.options[0].value !== '') {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Seleccione...';
            select.insertBefore(defaultOption, select.firstChild);
        }
    });
}

/**
 * Configurar validación en tiempo real
 */
function setupRealTimeValidation() {
    // Validación de cédula
    const cedulaInput = document.querySelector('input[name="cedula"]');
    if (cedulaInput) {
        cedulaInput.addEventListener('input', function(e) {
            // Solo permitir números
            this.value = this.value.replace(/\D/g, '');
            
            if (this.value.length > 0 && this.value.length < 6) {
                this.setCustomValidity('La cédula debe tener al menos 6 dígitos');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Validación de email
    const emailInput = document.querySelector('input[name="email"]');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.value && !emailRegex.test(this.value)) {
                this.setCustomValidity('Ingrese un correo electrónico válido');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Validación de campos requeridos
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
        
        field.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
}

/**
 * Validar todo el formulario
 */
function validateForm() {
    let isValid = true;
    
    // Validar nombre
    const firstName = document.querySelector('input[name="first_name"]');
    if (firstName && !firstName.value.trim()) {
        showError(firstName, 'El nombre es requerido');
        isValid = false;
    }
    
    // Validar apellido
    const lastName = document.querySelector('input[name="last_name"]');
    if (lastName && !lastName.value.trim()) {
        showError(lastName, 'El apellido es requerido');
        isValid = false;
    }
    
    // Validar cédula
    const cedula = document.querySelector('input[name="cedula"]');
    if (cedula) {
        if (!cedula.value.trim()) {
            showError(cedula, 'La cédula es requerida');
            isValid = false;
        } else if (!/^\d+$/.test(cedula.value)) {
            showError(cedula, 'La cédula solo debe contener números');
            isValid = false;
        } else if (cedula.value.length < 6) {
            showError(cedula, 'La cédula debe tener al menos 6 dígitos');
            isValid = false;
        }
    }
    
    // Validar email
    const email = document.querySelector('input[name="email"]');
    if (email) {
        if (!email.value.trim()) {
            showError(email, 'El correo electrónico es requerido');
            isValid = false;
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            showError(email, 'Ingrese un correo electrónico válido');
            isValid = false;
        }
    }
    
    // Validar rol
    const rol = document.querySelector('select[name="rol"]');
    if (rol && !rol.value) {
        showError(rol, 'Debe seleccionar un rol');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Mostrar mensaje de error en un campo
 */
function showError(field, message) {
    field.classList.add('is-invalid');
    
    // Buscar o crear div de error
    let errorDiv = field.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.classList.add('invalid-feedback');
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    errorDiv.textContent = message;
}

/**
 * Confirmar antes de cancelar si hay cambios
 */
const cancelBtn = document.querySelector('a[href*="users_list"]');
if (cancelBtn) {
    cancelBtn.addEventListener('click', function(e) {
        const form = document.getElementById('registerForm');
        const formData = new FormData(form);
        let hasData = false;
        
        for (let [key, value] of formData.entries()) {
            if (key !== 'csrfmiddlewaretoken' && value.trim()) {
                hasData = true;
                break;
            }
        }
        
        if (hasData) {
            if (!confirm('¿Está seguro de cancelar? Los datos ingresados se perderán.')) {
                e.preventDefault();
            }
        }
    });
}

/**
 * Mostrar indicador de carga al enviar
 */
const submitBtn = document.querySelector('button[type="submit"]');
if (submitBtn) {
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', function() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Registrando...';
    });
}