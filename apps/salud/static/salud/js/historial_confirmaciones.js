document.addEventListener('DOMContentLoaded', function() {

    initializeFilters();
    initializeTable();
    addAnimations();
    
    function initializeFilters() {
        const filterForm = document.querySelector('.filter-form');
        const filterSelects = document.querySelectorAll('.filter-select');
        
        if (!filterForm) return;
        
        filterForm.style.opacity = '0';
        filterForm.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            filterForm.style.transition = 'all 0.5s ease';
            filterForm.style.opacity = '1';
            filterForm.style.transform = 'translateY(0)';
        }, 100);
        
        filterForm.addEventListener('submit', function(e) {
            const btnFilter = filterForm.querySelector('.btn-filter');
            
            btnFilter.innerHTML = '<span class="loading-spinner"></span> Filtrando...';
            btnFilter.disabled = true;
        });

        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                this.style.borderColor = '#4a7c2c';
                setTimeout(() => {
                    this.style.borderColor = '';
                }, 300);
            });
        });
    }
    
    function initializeTable() {
        const table = document.querySelector('.historial-table');
        if (!table) return;
        
        const rows = table.querySelectorAll('tbody tr');
        
        if (rows.length === 0) {
            showEmptyState();
            return;
        }
        
        rows.forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                row.style.transition = 'all 0.3s ease';
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, 50 * index);
        });
        
        formatResultCells();
        
        addTooltips();
    }
    
    function formatResultCells() {
        const table = document.querySelector('.historial-table');
        if (!table) return;
        
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            
            if (cells[4]) {
                const resultText = cells[4].textContent.trim().toLowerCase();
                const badge = document.createElement('span');
                badge.className = 'badge-resultado';
                
                if (resultText.includes('gestante') || resultText.includes('positiv')) {
                    badge.classList.add('badge-gestante');
                    badge.innerHTML = '✓ Gestante';
                } else if (resultText.includes('negativ') || resultText.includes('no gestante')) {
                    badge.classList.add('badge-negativa');
                    badge.innerHTML = '✗ No Gestante';
                } else {
                    badge.textContent = resultText;
                }
                
                cells[4].innerHTML = '';
                cells[4].appendChild(badge);
            }
            
            if (cells[3]) {
                const metodo = cells[3].textContent.trim();
                cells[3].innerHTML = `<span>🔬 ${metodo}</span>`;
            }
        });
    }
    
    function showEmptyState() {
        const tableWrapper = document.querySelector('.table-wrapper');
        if (!tableWrapper) return;
        
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = `
            <div class="empty-state-icon">📋</div>
            <p class="empty-state-text">No se encontraron confirmaciones con los filtros seleccionados</p>
        `;
        
        tableWrapper.appendChild(emptyState);
    }
    
    function addTooltips() {
        const observacionCells = document.querySelectorAll('.historial-table tbody td:last-child');
        
        observacionCells.forEach(cell => {
            const text = cell.textContent.trim();
            if (text && text.length > 30) {
                cell.title = text;
                cell.style.cursor = 'help';
            }
        });
    }
    
    function addAnimations() {
        const title = document.querySelector('.historial-title');
        
        if (title) {
            title.style.opacity = '0';
            title.style.transform = 'translateY(-30px)';
            
            setTimeout(() => {
                title.style.transition = 'all 0.6s ease';
                title.style.opacity = '1';
                title.style.transform = 'translateY(0)';
            }, 50);
        }
    }
    
    window.exportarHistorial = function() {
        const table = document.querySelector('.historial-table');
        if (!table) return;
        
        let csv = [];
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
            const cols = row.querySelectorAll('td, th');
            const rowData = Array.from(cols).map(col => {
                let text = col.textContent.trim();
                // Limpiar badges
                text = text.replace(/[✓✗]/g, '').trim();
                return `"${text}"`;
            });
            csv.push(rowData.join(','));
        });
        
        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `historial_confirmaciones_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
    };
    
    window.imprimirHistorial = function() {
        window.print();
    };
    
});

const printStyles = `
    @media print {
        .filter-form,
        .btn-filter,
        .sidebar,
        .navbar {
            display: none !important;
        }
        
        .historial-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .historial-table th,
        .historial-table td {
            border: 1px solid #333;
            padding: 8px;
        }
        
        .badge-resultado {
            border: 1px solid #333;
            padding: 2px 8px;
        }
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = printStyles;
document.head.appendChild(styleSheet);