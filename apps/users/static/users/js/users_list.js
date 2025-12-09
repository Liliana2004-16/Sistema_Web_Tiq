// users_list.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initSearch();
    initFilters();
    initCheckboxes();
    initEditModal();
    initToggleStatus();
    autoHideAlerts();
    
    // Actualizar contador inicial
    updateCounter();
});

/**
 * Búsqueda en tiempo real
 */
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterTable();
        });
    }
}

/**
 * Filtros de rol y estado
 */
function initFilters() {
    const filterRol = document.getElementById('filterRol');
    const filterEstado = document.getElementById('filterEstado');
    
    if (filterRol) {
        filterRol.addEventListener('change', filterTable);
    }
    
    if (filterEstado) {
        filterEstado.addEventListener('change', filterTable);
    }
}

/**
 * Filtrar tabla según búsqueda y filtros
 */
function filterTable() {
    const searchValue = document.getElementById('searchInput').value.toLowerCase();
    const rolValue = document.getElementById('filterRol').value;
    const estadoValue = document.getElementById('filterEstado').value;
    
    const rows = document.querySelectorAll('#usersTable tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        // Saltar fila de "no hay datos"
        if (row.cells.length === 1) return;
        
        const nombre = row.dataset.nombre.toLowerCase();
        const cedula = row.dataset.cedula.toLowerCase();
        const correo = row.dataset.correo.toLowerCase();
        const rol = row.dataset.rol;
        const estado = row.dataset.estado;
        
        // Verificar búsqueda
        const matchSearch = nombre.includes(searchValue) || 
                          cedula.includes(searchValue) || 
                          correo.includes(searchValue);
        
        // Verificar filtros
        const matchRol = !rolValue || rol === rolValue;
        const matchEstado = !estadoValue || estado === estadoValue;
        
        // Mostrar u ocultar fila
        if (matchSearch && matchRol && matchEstado) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Actualizar contador
    document.getElementById('showingCount').textContent = visibleCount;
    
    // Mostrar mensaje si no hay resultados
    showNoResults(visibleCount === 0);
}

/**
 * Mostrar mensaje de "sin resultados"
 */
function showNoResults(show) {
    let noResultsRow = document.querySelector('.no-results-row');
    
    if (show) {
        if (!noResultsRow) {
            const tbody = document.querySelector('#usersTable tbody');
            noResultsRow = document.createElement('tr');
            noResultsRow.classList.add('no-results-row');
            noResultsRow.innerHTML = `
                <td colspan="8" class="text-center py-4 text-muted">
                    <i class="bi bi-search fs-1 d-block mb-2"></i>
                    No se encontraron resultados
                </td>
            `;
            tbody.appendChild(noResultsRow);
        }
    } else {
        if (noResultsRow) {
            noResultsRow.remove();
        }
    }
}

/**
 * Manejo de checkboxes
 */
function initCheckboxes() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.user-checkbox');
    const btnActualizarMasivo = document.getElementById('btnActualizarMasivo');
    
    // Seleccionar/deseleccionar todos
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(checkbox => {
                if (checkbox.closest('tr').style.display !== 'none') {
                    checkbox.checked = this.checked;
                }
            });
            updateBulkActions();
        });
    }
    
    // Actualizar estado del botón masivo
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActions();
            
            // Actualizar "seleccionar todos"
            const visibleCheckboxes = Array.from(checkboxes).filter(
                cb => cb.closest('tr').style.display !== 'none'
            );
            const checkedCount = visibleCheckboxes.filter(cb => cb.checked).length;
            selectAll.checked = checkedCount === visibleCheckboxes.length && visibleCheckboxes.length > 0;
        });
    });
}

/**
 * Actualizar acciones masivas
 */
function updateBulkActions() {
    const checkboxes = document.querySelectorAll('.user-checkbox:checked');
    const btnActualizarMasivo = document.getElementById('btnActualizarMasivo');
    
    if (btnActualizarMasivo) {
        if (checkboxes.length > 0) {
            btnActualizarMasivo.style.display = 'inline-block';
            btnActualizarMasivo.textContent = `Actualizar (${checkboxes.length})`;
        } else {
            btnActualizarMasivo.style.display = 'none';
        }
    }
}

/**
 * Modal de edición de rol
 */
function initEditModal() {
    const editModal = document.getElementById('editModal');
    
    if (editModal) {
        editModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const userId = button.getAttribute('data-user-id');
            const userName = button.getAttribute('data-user-name');
            const userRol = button.getAttribute('data-user-rol');
            
            // Actualizar contenido del modal
            document.getElementById('editUserId').value = userId;
            document.getElementById('editUserName').textContent = userName;
            document.getElementById('editUserRol').value = userRol;
        });
    }
}

/**
 * Toggle de estado con confirmación
 */
function initToggleStatus() {
    const forms = document.querySelectorAll('.toggle-status-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const btn = this.querySelector('button');
            const currentStatus = btn.textContent.trim();
            const newStatus = currentStatus === 'Activo' ? 'Inactivo' : 'Activo';
            
            const message = `¿Está seguro de cambiar el estado a "${newStatus}"?`;
            
            if (confirm(message)) {
                // Mostrar indicador de carga
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
                
                // Enviar formulario
                this.submit();
            }
        });
    });
}

/**
 * Ver detalles del usuario
 */
function viewUserDetails(userId) {
    const row = document.querySelector(`tr[data-user-id="${userId}"]`);
    
    if (row) {
        const nombre = row.dataset.nombre;
        const cedula = row.dataset.cedula;
        const correo = row.dataset.correo;
        const empresa = row.querySelector('td:nth-child(5)').textContent;
        const rol = row.dataset.rol;
        const estado = row.dataset.estado;
        
        const details = `
            <strong>Nombre:</strong> ${nombre}<br>
            <strong>Cédula:</strong> ${cedula}<br>
            <strong>Correo:</strong> ${correo}<br>
            <strong>Empresa:</strong> ${empresa}<br>
            <strong>Rol:</strong> ${rol}<br>
            <strong>Estado:</strong> ${estado}
        `;
        
        // Crear modal de detalles
        const modal = new bootstrap.Modal(document.createElement('div'));
        const modalHtml = `
            <div class="modal fade" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header bg-info text-white">
                            <h5 class="modal-title">
                                <i class="bi bi-person-circle me-2"></i>Detalles del Usuario
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${details}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modalElement = document.body.lastElementChild;
        const bsModal = new bootstrap.Modal(modalElement);
        bsModal.show();
        
        // Eliminar modal del DOM al cerrarse
        modalElement.addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
}

/**
 * Actualizar contador de usuarios
 */
function updateCounter() {
    const rows = document.querySelectorAll('#usersTable tbody tr');
    const validRows = Array.from(rows).filter(row => row.cells.length > 1);
    document.getElementById('totalCount').textContent = validRows.length;
    document.getElementById('showingCount').textContent = validRows.length;
}

/**
 * Auto-ocultar alertas
 */
function autoHideAlerts() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

/**
 * Exportar tabla a CSV (funcionalidad adicional)
 */
function exportToCSV() {
    const table = document.getElementById('usersTable');
    const rows = table.querySelectorAll('tr:not([style*="display: none"])');
    
    let csv = [];
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach((col, index) => {
            // Saltar columna de checkbox y acciones
            if (index !== 0 && index !== cols.length - 1) {
                rowData.push(col.textContent.trim());
            }
        });
        
        if (rowData.length > 0) {
            csv.push(rowData.join(','));
        }
    });
    
    // Descargar CSV
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'usuarios_' + new Date().toISOString().split('T')[0] + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * Imprimir tabla
 */
function printTable() {
    window.print();
}

// Exponer funciones globalmente para uso en HTML
window.viewUserDetails = viewUserDetails;
window.exportToCSV = exportToCSV;
window.printTable = printTable;