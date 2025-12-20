"""
Database - Gestión de historial con SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class Database:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / 'optimizations.db'
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de optimizaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                filename TEXT NOT NULL,
                method TEXT NOT NULL,
                metrics TEXT NOT NULL,
                input_path TEXT,
                output_path TEXT,
                elapsed_time REAL
            )
        ''')
        
        # Tabla de mapeos de columnas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS column_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename_pattern TEXT NOT NULL,
                mapping TEXT NOT NULL,
                usage_count INTEGER DEFAULT 1,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_optimization(self, filename: str, method: str, metrics: Dict, 
                         input_path: str, output_path: str, elapsed_time: float) -> int:
        """Guarda una optimización en el historial"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO optimizations (filename, method, metrics, input_path, output_path, elapsed_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, method, json.dumps(metrics), input_path, output_path, elapsed_time))
        
        opt_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return opt_id
    
    def get_all_optimizations(self, limit: int = 50) -> List[Dict]:
        """Obtiene todas las optimizaciones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, filename, method, metrics, elapsed_time
            FROM optimizations
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'filename': row[2],
                'method': row[3],
                'metrics': json.loads(row[4]),
                'elapsed_time': row[5]
            }
            for row in rows
        ]
    
    def get_optimization(self, opt_id: int) -> Optional[Dict]:
        """Obtiene una optimización específica"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, filename, method, metrics, input_path, output_path, elapsed_time
            FROM optimizations
            WHERE id = ?
        ''', (opt_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'timestamp': row[1],
            'filename': row[2],
            'method': row[3],
            'metrics': json.loads(row[4]),
            'input_path': row[5],
            'output_path': row[6],
            'elapsed_time': row[7]
        }
    
    def save_column_mapping(self, filename_pattern: str, mapping: Dict):
        """Guarda un mapeo de columnas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute('''
            SELECT id, usage_count FROM column_mappings
            WHERE filename_pattern = ?
        ''', (filename_pattern,))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar
            cursor.execute('''
                UPDATE column_mappings
                SET mapping = ?, usage_count = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (json.dumps(mapping), existing[1] + 1, existing[0]))
        else:
            # Insertar nuevo
            cursor.execute('''
                INSERT INTO column_mappings (filename_pattern, mapping)
                VALUES (?, ?)
            ''', (filename_pattern, json.dumps(mapping)))
        
        conn.commit()
        conn.close()
    
    def get_column_mapping(self, filename_pattern: str) -> Optional[Dict]:
        """Obtiene un mapeo de columnas guardado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mapping FROM column_mappings
            WHERE filename_pattern = ?
            ORDER BY usage_count DESC, last_used DESC
            LIMIT 1
        ''', (filename_pattern,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
