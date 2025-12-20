"""
Upload route - Manejo de subida de archivos Excel
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Agregar path para importar servicios
sys.path.append(str(Path(__file__).parent.parent))
from services.excel_detector import ExcelDetector

bp = Blueprint('upload', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para subir archivo Excel
    Retorna: detección automática de columnas
    """
    try:
        # Verificar que hay archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Formato no permitido. Use .xlsx o .xls'}), 400
        
        # Guardar archivo
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detectar columnas automáticamente
        detector = ExcelDetector(filepath)
        detection_result = detector.detect_columns()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'detection': detection_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
