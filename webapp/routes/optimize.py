"""
Optimize route - Ejecuta optimización de horarios
"""

from flask import Blueprint, request, jsonify, current_app
import sys
from pathlib import Path

# Agregar path para importar servicios
sys.path.append(str(Path(__file__).parent.parent))
from services.optimizer_service import OptimizerService

bp = Blueprint('optimize', __name__, url_prefix='/api')

@bp.route('/optimize', methods=['POST'])
def optimize():
    """
    Endpoint para optimizar horario
    Body: {
        filepath: str,
        method: 'greedy'|'ml'|'genetic',
        column_mapping: dict
    }
    """
    try:
        data = request.get_json()
        
        filepath = data.get('filepath')
        method = data.get('method', 'greedy')
        column_mapping = data.get('column_mapping', {})
        
        if not filepath:
            return jsonify({'error': 'Falta filepath'}), 400
        
        # Ejecutar optimización
        optimizer = OptimizerService(filepath, column_mapping)
        result = optimizer.optimize(method)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
