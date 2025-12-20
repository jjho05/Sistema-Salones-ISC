// App.js - Main JavaScript Logic

let currentFile = null;
let currentMapping = null;
let selectedMethod = 'greedy';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupDropZone();
    setupFileInput();
    loadHistory();
});

// Drop Zone Setup
function setupDropZone() {
    const dropZone = document.getElementById('dropZone');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        }, false);
    });
    
    dropZone.addEventListener('drop', handleDrop, false);
    dropZone.addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Input Setup
function setupFileInput() {
    document.getElementById('fileInput').addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

// Handle File Upload
async function handleFile(file) {
    // Validate file
    if (!file.name.match(/\.(xlsx|xls)$/)) {
        alert('Por favor selecciona un archivo Excel (.xlsx o .xls)');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('El archivo es demasiado grande (máximo 10MB)');
        return;
    }
    
    currentFile = file;
    
    // Show file info
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    document.getElementById('fileInfo').classList.remove('d-none');
    
    // Upload file
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await axios.post('/api/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        if (response.data.success) {
            showDetectionResult(response.data.detection);
            currentMapping = response.data.detection.mapping;
        }
    } catch (error) {
        alert('Error al subir archivo: ' + (error.response?.data?.error || error.message));
    }
}

// Show Detection Result
function showDetectionResult(detection) {
    const confidence = detection.total_confidence;
    
    // Update confidence bar
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    
    confidenceBar.style.width = confidence + '%';
    confidenceText.textContent = confidence + '% confianza';
    
    if (confidence >= 80) {
        confidenceBar.className = 'progress-bar bg-success';
    } else if (confidence >= 60) {
        confidenceBar.className = 'progress-bar bg-warning';
    } else {
        confidenceBar.className = 'progress-bar bg-danger';
    }
    
    // Show mapping table
    let html = '<table class="table table-sm"><thead><tr><th>Campo Requerido</th><th>Columna Detectada</th><th>Confianza</th></tr></thead><tbody>';
    
    for (const [field, column] of Object.entries(detection.mapping)) {
        const conf = detection.confidence[field];
        const badge = conf >= 80 ? 'success' : conf >= 60 ? 'warning' : 'danger';
        
        html += `<tr>
            <td><strong>${field}</strong></td>
            <td>${column || '<span class="text-danger">No detectado</span>'}</td>
            <td><span class="badge bg-${badge}">${conf}%</span></td>
        </tr>`;
    }
    
    html += '</tbody></table>';
    document.getElementById('mappingPreview').innerHTML = html;
    
    // Show detection result
    document.getElementById('detectionResult').classList.remove('d-none');
    document.getElementById('detectionResult').classList.add('fade-in');
}

// Proceed to Optimize
function proceedToOptimize() {
    document.getElementById('optimizationSection').classList.remove('d-none');
    document.getElementById('optimizationSection').scrollIntoView({ behavior: 'smooth' });
}

// Select Method
function selectMethod(method) {
    selectedMethod = method;
    
    // Update UI
    document.querySelectorAll('.method-card').forEach(card => {
        card.classList.remove('active');
    });
    
    document.querySelector(`.method-card[data-method="${method}"]`).classList.add('active');
}

// Start Optimization
async function startOptimization() {
    if (!currentMapping) {
        alert('Por favor sube un archivo primero');
        return;
    }
    
    // Show progress
    document.getElementById('optimizeBtn').disabled = true;
    document.getElementById('optimizationProgress').classList.remove('d-none');
    
    try {
        const response = await axios.post('/api/optimize', {
            filepath: currentFile.name,
            method: selectedMethod,
            column_mapping: currentMapping
        });
        
        if (response.data.success) {
            // Redirect to results
            window.location.href = '/results?id=' + response.data.result.id;
        }
    } catch (error) {
        alert('Error en optimización: ' + (error.response?.data?.error || error.message));
        document.getElementById('optimizeBtn').disabled = false;
        document.getElementById('optimizationProgress').classList.add('d-none');
    }
}

// Load History
async function loadHistory() {
    try {
        const response = await axios.get('/api/history');
        
        if (response.data.success && response.data.history.length > 0) {
            let html = '';
            
            response.data.history.slice(0, 5).forEach(opt => {
                const date = new Date(opt.timestamp).toLocaleDateString('es-MX');
                const mejora = opt.metrics.distancia.mejora_pct;
                
                html += `
                    <div class="history-item" onclick="window.location.href='/results?id=${opt.id}'">
                        <div class="d-flex justify-content-between">
                            <strong>${opt.filename}</strong>
                            <span class="badge bg-success">${mejora}% ↓</span>
                        </div>
                        <small class="text-muted">${date} - ${opt.method}</small>
                    </div>
                `;
            });
            
            document.getElementById('historyList').innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function showMapper() {
    window.location.href = '/mapper';
}
