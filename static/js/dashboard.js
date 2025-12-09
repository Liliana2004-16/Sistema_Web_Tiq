document.addEventListener("DOMContentLoaded", function () {
    
    const toggleButtons = document.querySelectorAll(".toggle-btn");

    toggleButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const content = document.querySelector(targetId);

            if (content) {
                content.classList.toggle("show");

                this.classList.toggle("active");
                
                if (content.classList.contains("show")) {
                    this.textContent = "▲";
                } else {
                    this.textContent = "▼";
                }
            }
        });
    });

    const allContents = document.querySelectorAll(".block-content");
    allContents.forEach(content => {
        content.classList.add("show");
    });
    
    toggleButtons.forEach(btn => {
        btn.textContent = "▲";
        btn.classList.add("active");
    });

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
    const counterElements = document.querySelectorAll(".resumen-card h2");
    
    counterElements.forEach(el => {
        const text = el.textContent.trim();
        const numberMatch = text.match(/[\d,]+/);
        
        if (numberMatch) {
            const targetNumber = parseInt(numberMatch[0].replace(/,/g, ""));
            const hasDecimals = text.includes(".");
            const suffix = text.replace(/[\d,\.]/g, "").trim();

            const originalSuffix = suffix;
            
            if (!isNaN(targetNumber)) {
                el.textContent = "0";
                animateCounter(el, 0, targetNumber, 1500);
                
                setTimeout(() => {
                    if (originalSuffix) {
                        el.textContent = el.textContent + " " + originalSuffix;
                    }
                }, 1500);
            }
        }
    });

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

    const enableAutoRefresh = false; 
    const refreshInterval = 5 * 60 * 1000; 
    
    if (enableAutoRefresh) {
        setInterval(() => {
            console.log("Actualizando dashboard...");
           
        }, refreshInterval);
    }

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
    const checkAlerts = () => {
        const pendientesElement = document.querySelector("#inseminaciones .block-content p:last-of-type");
        
        if (pendientesElement) {
            const text = pendientesElement.textContent;
            const numberMatch = text.match(/\d+/);
            
            if (numberMatch && parseInt(numberMatch[0]) > 0) {
                showNotification("Tienes inseminaciones pendientes de confirmar", "warning");
            }
        }
    };
    
    function showNotification(message, type = "info") {
        if (typeof showToast === "function") {
            showToast(message, type);
        }
    }
    
    setTimeout(checkAlerts, 2000);

    const addPrintButton = () => {
        const printBtn = document.querySelector("#print-dashboard");
        
        if (printBtn) {
            printBtn.addEventListener("click", function () {
                window.print();
            });
        }
    };
    
    addPrintButton();

    console.log("Dashboard cargado correctamente");
    console.log("Bloques inicializados:", toggleButtons.length);
    console.log("Contadores animados:", counterElements.length);

});

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function updateCounter(elementId, newValue) {
    const element = document.querySelector(elementId);
    if (element) {
        element.textContent = formatNumber(newValue);
    }
}

window.dashboardUtils = {
    formatNumber,
    updateCounter
};