"""
Excel Detector - Detección inteligente de columnas
Usa fuzzy matching para detectar columnas automáticamente
"""

import pandas as pd
from fuzzywuzzy import fuzz
from typing import Dict, List, Tuple
import json
from pathlib import Path

class ExcelDetector:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None
        self.columns = []
        
        # Palabras clave para cada campo requerido
        self.keywords = {
            'Grupo': ['grupo', 'grp', 'class', 'clase'],
            'Materia': ['materia', 'asignatura', 'subject', 'curso', 'course'],
            'Dia': ['dia', 'day', 'fecha', 'date'],
            'Hora': ['hora', 'time', 'horario', 'bloque', 'block'],
            'Salon': ['salon', 'aula', 'room', 'classroom', 'salón'],
            'Profesor': ['profesor', 'teacher', 'docente', 'maestro', 'instructor'],
            'Tipo_Salon': ['tipo', 'type', 'categoria', 'category']
        }
        
        # Cargar mapeos previos si existen
        self.load_previous_mappings()
    
    def load_previous_mappings(self):
        """Carga mapeos guardados anteriormente"""
        mapping_file = Path(__file__).parent.parent / 'models' / 'column_mappings.json'
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                self.previous_mappings = json.load(f)
        else:
            self.previous_mappings = {}
    
    def detect_columns(self) -> Dict:
        """
        Detecta columnas automáticamente
        Retorna: {
            'columns': list,  # Columnas del Excel
            'mapping': dict,  # Mapeo detectado
            'confidence': dict,  # Confianza por campo
            'preview': list   # Preview de datos
        }
        """
        try:
            # Leer Excel
            self.df = pd.read_csv(self.filepath) if self.filepath.endswith('.csv') else pd.read_excel(self.filepath)
            self.columns = list(self.df.columns)
            
            # Detectar mapeo
            mapping = {}
            confidence = {}
            
            for required_field, keywords in self.keywords.items():
                best_match = None
                best_score = 0
                
                for col in self.columns:
                    # Calcular score con fuzzy matching
                    scores = [fuzz.ratio(col.lower(), kw.lower()) for kw in keywords]
                    max_score = max(scores)
                    
                    if max_score > best_score:
                        best_score = max_score
                        best_match = col
                
                if best_score >= 60:  # Umbral de confianza
                    mapping[required_field] = best_match
                    confidence[required_field] = best_score
                else:
                    mapping[required_field] = None
                    confidence[required_field] = 0
            
            # Calcular confianza general
            total_confidence = sum(confidence.values()) / len(confidence)
            
            # Preview de datos (primeras 5 filas)
            preview = self.df.head(5).to_dict('records')
            
            return {
                'columns': self.columns,
                'mapping': mapping,
                'confidence': confidence,
                'total_confidence': round(total_confidence, 1),
                'preview': preview,
                'total_rows': len(self.df)
            }
        
        except Exception as e:
            raise Exception(f"Error al detectar columnas: {str(e)}")
    
    def validate_mapping(self, mapping: Dict) -> Tuple[bool, List[str]]:
        """
        Valida que el mapeo sea correcto
        Retorna: (is_valid, errors)
        """
        errors = []
        required_fields = ['Grupo', 'Materia', 'Dia', 'Hora', 'Salon']
        
        for field in required_fields:
            if field not in mapping or mapping[field] is None:
                errors.append(f"Falta mapear campo requerido: {field}")
            elif mapping[field] not in self.columns:
                errors.append(f"Columna '{mapping[field]}' no existe en el Excel")
        
        return len(errors) == 0, errors
