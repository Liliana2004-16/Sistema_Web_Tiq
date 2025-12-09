document.addEventListener('DOMContentLoaded', function() {
    
    initializeForm();
    setupAnimalSearch();
    setupFormValidation();
    addAnimations();
    
    function initializeForm() {
        const form = document.querySelector('.evento-form');
        if (!form) return;
        
        const fechaInput = document.querySelector('input[name="fecha"], input[type="date"]');
        if (fechaInput && !fechaInput.value) {
            const today = new Date().toISOString().split('T')[0];
            fechaInput.value = today;
        }
        
        const firstInput = form.querySelector('input[type="text"]');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 300);
        }
    }
    
    function setupAnimalSearch() {
        const btnBuscar = document.getElementById('buscar');
        const areteInput = document.getElementById('arete');
        
        if (!btnBuscar || !areteInput) return;
        
        btnBuscar.addEventListener('click', function(e) {
            e.preventDefault();
            buscarAnimal();
        });
        
        areteInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarAnimal();
            }
        });
        
        areteInput.addEventListener('input', function() {
            limpiarInfoAnimal();
        });
    }
    
    function buscarAnimal() {
        const areteInput = document.getElementById('arete');
        const btnBuscar = document.getElementById('buscar');
        const arete = areteInput.value.trim();
        
        if (!arete) {
            mostrarAlerta('Por favor ingrese un número de arete', 'warning');
            areteInput.focus();
            return;
        }

        const originalText = btnBuscar.innerHTML;
        btnBuscar.innerHTML = '<span class="loading-spinner"></span> Buscando...';
        btnBuscar.disabled = true;
        
        fetch(`/salud/buscar-animal/?arete=${encodeURIComponent(arete)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la búsqueda');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    mostrarAlerta('Animal no encontrado. Verifique el número de arete.', 'error');
                    limpiarInfoAnimal();
                } else {
                    mostrarInfoAnimal(data);
                    mostrarAlerta('Animal encontrado exitosamente', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                mostrarAlerta('Error al buscar el animal. Intente nuevamente.', 'error');
                limpiarInfoAnimal();
            })
            .finally(() => {
                btnBuscar.innerHTML = originalText;
                btnBuscar.disabled = false;
            });
    }
    
    function mostrarInfoAnimal(data) {
        document.getElementById('nombre').value = data.nombre || 'Sin nombre';
        document.getElementById('edad').value = data.edad ? `${data.edad} días` : 'No disponible';
        document.getElementById('id_animal').value = data.id;
        
        const campos = ['nombre', 'edad'];
        campos.forEach((campo, index) => {
            const input = document.getElementById(campo);
            if (input) {
                input.style.background = '#e8f5e9';
                setTimeout(() => {
                    input.style.transition = 'background 0.5s ease';
                    input.style.background = '#f5f5f5';
                }, 300 * (index + 1));
            }
        });
    }
    
    function limpiarInfoAnimal() {
        document.getElementById('nombre').value = '';
        document.getElementById('edad').value = '';
        document.getElementById('id_animal').value = '';
    }
    
    function setupFormValidation() {
        const form = document.querySelector('.evento-form');
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
    
            const animalId = document.getElementById('id_animal').value;
            const diagnostico = document.querySelector('[name="diagnostico"]');
            const tratamiento = document.querySelector('[name="tratamiento"]');
            
            if (!animalId) {
                mostrarAlerta('Debe buscar y seleccionar un animal antes de guardar', 'error');
                document.getElementById('arete').focus();
                return false;
            }
            
            if (diagnostico && !diagnostico.value.trim()) {
                mostrarAlerta('El diagnóstico es obligatorio', 'error');
                diagnostico.focus();
                return false;
            }
            
            if (tratamiento && !tratamiento.value.trim()) {
                mostrarAlerta('El tratamiento es obligatorio', 'error');
                tratamiento.focus();
                return false;
            }
            
            const btnSubmit = form.querySelector('.btn-primary');
            if (btnSubmit) {
                btnSubmit.innerHTML = '<span class="loading-spinner"></span> Guardando...';
                btnSubmit.disabled = true;
            }
            
            form.submit();
        });
    }

    function mostrarAlerta(mensaje, tipo = 'info') {
        const alertaAnterior = document.querySelector('.alert');
        if (alertaAnterior) {
            alertaAnterior.remove();
        }
        
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo}`;
        
        const icono = tipo === 'success' ? '✓' : 
                     tipo === 'error' ? '✗' : 
                     tipo === 'warning' ? '⚠' : 'ℹ';
        
        alerta.innerHTML = `
            <span style="font-size: 1.2rem;">${icono}</span>
            <span>${mensaje}</span>
        `;
        
        const container = document.querySelector('.evento-container');
        if (container) {
            container.insertBefore(alerta, container.firstChild);
            
            alerta.style.opacity = '0';
            alerta.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alerta.style.transition = 'all 0.3s ease';
                alerta.style.opacity = '1';
                alerta.style.transform = 'translateY(0)';
            }, 10);
            
            if (tipo === 'success') {
                setTimeout(() => {
                    alerta.style.opacity = '0';
                    setTimeout(() => alerta.remove(), 300);
                }, 5000);
            }
        }
    }

    function addAnimations() {
        const container = document.querySelector('.evento-container');
        if (!container) return;
        
        container.style.opacity = '0';
        container.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            container.style.transition = 'all 0.6s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
        
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach((group, index) => {
            group.style.opacity = '0';
            group.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                group.style.transition = 'all 0.4s ease';
                group.style.opacity = '1';
                group.style.transform = 'translateX(0)';
            }, 150 + (index * 50));
        });
    }

    window.autocompletarCampos = function(diagnostico, tratamiento) {
        const diagnosticoInput = document.querySelector('[name="diagnostico"]');
        const tratamientoInput = document.querySelector('[name="tratamiento"]');
        
        if (diagnosticoInput) diagnosticoInput.value = diagnostico;
        if (tratamientoInput) tratamientoInput.value = tratamiento;
        
        mostrarAlerta('Campos autocompletados', 'success');
    };
    
    function calcularEdadDias(fechaNacimiento) {
        const hoy = new Date();
        const nacimiento = new Date(fechaNacimiento);
        const diferencia = hoy - nacimiento;
        return Math.floor(diferencia / (1000 * 60 * 60 * 24));
    }
    
});

const spinnerStyles = `
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 0.6s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = spinnerStyles;
document.head.appendChild(styleSheet);