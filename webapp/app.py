#!/usr/bin/env python3
"""
Aplicación Web - Optimizador de Salones ISC
Servidor Flask principal
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Agregar path del proyecto para importar optimizadores
sys.path.append(str(Path(__file__).parent.parent))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SECRET_KEY'] = 'isc-salones-2024'

# Crear carpetas si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/mapper')
def mapper():
    """Interfaz de mapeo de columnas"""
    return render_template('mapper.html')

@app.route('/results')
def results():
    """Página de resultados"""
    return render_template('results.html')

# Importar rutas
from routes import upload, optimize, history

# Registrar blueprints
app.register_blueprint(upload.bp)
app.register_blueprint(optimize.bp)
app.register_blueprint(history.bp)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏫 Optimizador de Salones ISC - Aplicación Web")
    print("="*60)
    print("\n🌐 Servidor iniciado en: http://localhost:5001")
    print("📁 Carpeta de uploads:", app.config['UPLOAD_FOLDER'])
    print("📁 Carpeta de outputs:", app.config['OUTPUT_FOLDER'])
    print("\n✨ Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
