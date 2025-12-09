
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    addFormClasses();
    setupRealTimeValidation();
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    });
    
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function addFormClasses() {
    const textInputs = document.querySelectorAll('input[type="text"], input[type="email"]');
    const selects = document.querySelectorAll('select');
    
    textInputs.forEach(input => {
        input.classList.add('form-control');
        
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
        
        if (select.options.length === 0 || select.options[0].value !== '') {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Seleccione...';
            select.insertBefore(defaultOption, select.firstChild);
        }
    });
}

function setupRealTimeValidation() {
    const cedulaInput = document.querySelector('input[name="cedula"]');
    if (cedulaInput) {
        cedulaInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '');
            
            if (this.value.length > 0 && this.value.length < 6) {
                this.setCustomValidity('La cédula debe tener al menos 6 dígitos');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
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

function validateForm() {
    let isValid = true;
    
    const firstName = document.querySelector('input[name="first_name"]');
    if (firstName && !firstName.value.trim()) {
        showError(firstName, 'El nombre es requerido');
        isValid = false;
    }

    const lastName = document.querySelector('input[name="last_name"]');
    if (lastName && !lastName.value.trim()) {
        showError(lastName, 'El apellido es requerido');
        isValid = false;
    }
    
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
    
    const rol = document.querySelector('select[name="rol"]');
    if (rol && !rol.value) {
        showError(rol, 'Debe seleccionar un rol');
        isValid = false;
    }
    
    return isValid;
}


function showError(field, message) {
    field.classList.add('is-invalid');
    
    let errorDiv = field.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.classList.add('invalid-feedback');
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    errorDiv.textContent = message;
}

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

const submitBtn = document.querySelector('button[type="submit"]');
if (submitBtn) {
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', function() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Registrando...';
    });
}