/* ============================================
   DASHBOARD.JS - Agrotiquiza
   Ubicación: static/js/dashboard.js
   ============================================ */

document.addEventListener("DOMContentLoaded", function () {
    
    // ================================================
    // 1. FUNCIONALIDAD DE TOGGLE (EXPANDIR/COLAPSAR)
    // ================================================
    const toggleButtons = document.querySelectorAll(".toggle-btn");

    toggleButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const content = document.querySelector(targetId);

            if (content) {
                // Toggle de la clase 'show'
                content.classList.toggle("show");
                
                // Rotar el botón
                this.classList.toggle("active");
                
                // Cambiar el icono del botón
                if (content.classList.contains("show")) {
                    this.textContent = "▲";
                } else {
                    this.textContent = "▼";
                }
            }
        });
    });

    // ================================================
    // 2. ABRIR TODOS LOS BLOQUES POR DEFECTO
    // ================================================
    // Si deseas que todos los bloques estén abiertos al cargar la página
    const allContents = document.querySelectorAll(".block-content");
    allContents.forEach(content => {
        content.classList.add("show");
    });
    
    toggleButtons.forEach(btn => {
        btn.textContent = "▲";
        btn.classList.add("active");
    });

    // ================================================
    // 3. ANIMACIÓN DE CONTADORES (NÚMEROS)
    // ================================================
    function animateCounter(element, start, end, duration) {
        let startTime = null;
        
        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                element.textContent = end;
            }
        };
        
        window.requestAnimationFrame(step);
    }

    // Animar los números de las tarjetas de resumen
    const counterElements = document.querySelectorAll(".resumen-card h2");
    
    counterElements.forEach(el => {
        const text = el.textContent.trim();
        // Extraer solo números (por si hay "L" u otros caracteres)
        const numberMatch = text.match(/[\d,]+/);
        
        if (numberMatch) {
            const targetNumber = parseInt(numberMatch[0].replace(/,/g, ""));
            const hasDecimals = text.includes(".");
            const suffix = text.replace(/[\d,\.]/g, "").trim();
            
            // Guardar el sufijo original
            const originalSuffix = suffix;
            
            if (!isNaN(targetNumber)) {
                el.textContent = "0";
                animateCounter(el, 0, targetNumber, 1500);
                
                // Agregar el sufijo después de la animación
                setTimeout(() => {
                    if (originalSuffix) {
                        el.textContent = el.textContent + " " + originalSuffix;
                    }
                }, 1500);
            }
        }
    });

    // ================================================
    // 4. EFECTO PARALLAX EN IMÁGENES (OPCIONAL)
    // ================================================
    const dashboardImages = document.querySelectorAll(".dashboard-img");
    
    if (dashboardImages.length > 0) {
        window.addEventListener("scroll", function () {
            const scrolled = window.pageYOffset;
            
            dashboardImages.forEach((img, index) => {
                const speed = 0.2 + (index * 0.1);
                const yPos = -(scrolled * speed);
                img.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // ================================================
    // 5. TOOLTIP INFORMATIVO (OPCIONAL)
    // ================================================
    // Si quieres agregar tooltips a elementos específicos
    const addTooltips = () => {
        const tooltipElements = document.querySelectorAll("[data-tooltip]");
        
        tooltipElements.forEach(el => {
            el.addEventListener("mouseenter", function () {
                const tooltipText = this.getAttribute("data-tooltip");
                
                const tooltip = document.createElement("div");
                tooltip.className = "custom-tooltip";
                tooltip.textContent = tooltipText;
                tooltip.style.position = "absolute";
                tooltip.style.background = "#333";
                tooltip.style.color = "white";
                tooltip.style.padding = "8px 12px";
                tooltip.style.borderRadius = "6px";
                tooltip.style.fontSize = "13px";
                tooltip.style.zIndex = "9999";
                tooltip.style.whiteSpace = "nowrap";
                tooltip.style.pointerEvents = "none";
                
                document.body.appendChild(tooltip);
                
                const rect = this.getBoundingClientRect();
                tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + "px";
                tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + "px";
                
                this._tooltip = tooltip;
            });
            
            el.addEventListener("mouseleave", function () {
                if (this._tooltip) {
                    this._tooltip.remove();
                    this._tooltip = null;
                }
            });
        });
    };
    
    addTooltips();

    // ================================================
    // 6. ACTUALIZACIÓN AUTOMÁTICA (OPCIONAL)
    // ================================================
    // Si quieres que el dashboard se actualice automáticamente cada X minutos
    const enableAutoRefresh = false; // Cambiar a true para activar
    const refreshInterval = 5 * 60 * 1000; // 5 minutos
    
    if (enableAutoRefresh) {
        setInterval(() => {
            console.log("Actualizando dashboard...");
            // Aquí puedes hacer una petición AJAX para actualizar los datos
            // sin recargar la página completa
            // location.reload(); // Opción simple: recargar toda la página
        }, refreshInterval);
    }

    // ================================================
    // 7. BÚSQUEDA RÁPIDA EN BLOQUES (OPCIONAL)
    // ================================================
    const addSearchFunctionality = () => {
        const searchInput = document.querySelector("#dashboard-search");
        
        if (searchInput) {
            searchInput.addEventListener("input", function () {
                const searchTerm = this.value.toLowerCase();
                const blocks = document.querySelectorAll(".block-card");
                
                blocks.forEach(block => {
                    const text = block.textContent.toLowerCase();
                    
                    if (text.includes(searchTerm)) {
                        block.style.display = "block";
                        block.style.opacity = "1";
                    } else {
                        block.style.opacity = "0.3";
                    }
                });
            });
        }
    };
    
    addSearchFunctionality();

    // ================================================
    // 8. NOTIFICACIONES/ALERTAS
    // ================================================
    const checkAlerts = () => {
        // Ejemplo: verificar si hay animales con eventos pendientes
        const pendientesElement = document.querySelector("#inseminaciones .block-content p:last-of-type");
        
        if (pendientesElement) {
            const text = pendientesElement.textContent;
            const numberMatch = text.match(/\d+/);
            
            if (numberMatch && parseInt(numberMatch[0]) > 0) {
                // Mostrar una notificación
                showNotification("Tienes inseminaciones pendientes de confirmar", "warning");
            }
        }
    };
    
    // Función auxiliar para mostrar notificaciones
    function showNotification(message, type = "info") {
        // Esta función se integra con el sistema de toast existente
        if (typeof showToast === "function") {
            showToast(message, type);
        }
    }
    
    // Verificar alertas al cargar
    setTimeout(checkAlerts, 2000);

    // ================================================
    // 9. IMPRIMIR REPORTE
    // ================================================
    const addPrintButton = () => {
        const printBtn = document.querySelector("#print-dashboard");
        
        if (printBtn) {
            printBtn.addEventListener("click", function () {
                window.print();
            });
        }
    };
    
    addPrintButton();

    // ================================================
    // 10. LOG DE ACTIVIDAD (DESARROLLO)
    // ================================================
    console.log("Dashboard cargado correctamente");
    console.log("Bloques inicializados:", toggleButtons.length);
    console.log("Contadores animados:", counterElements.length);

});

// ================================================
// FUNCIONES GLOBALES AUXILIARES
// ================================================

// Función para formatear números
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Función para actualizar un contador específico
function updateCounter(elementId, newValue) {
    const element = document.querySelector(elementId);
    if (element) {
        element.textContent = formatNumber(newValue);
    }
}

// Exportar funciones si se necesita usar en otros scripts
window.dashboardUtils = {
    formatNumber,
    updateCounter
};