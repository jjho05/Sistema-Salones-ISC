"""
History route - Gestión de historial de optimizaciones
"""

from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Agregar path para importar modelos
sys.path.append(str(Path(__file__).parent.parent))
from models.database import Database

bp = Blueprint('history', __name__, url_prefix='/api')

@bp.route('/history', methods=['GET'])
def get_history():
    """Obtiene historial de optimizaciones"""
    try:
        db = Database()
        history = db.get_all_optimizations()
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history/<int:opt_id>', methods=['GET'])
def get_optimization(opt_id):
    """Obtiene una optimización específica"""
    try:
        db = Database()
        optimization = db.get_optimization(opt_id)
        
        if not optimization:
            return jsonify({'error': 'Optimización no encontrada'}), 404
        
        return jsonify({
            'success': True,
            'optimization': optimization
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
