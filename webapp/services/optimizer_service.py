"""
Optimizer Service - Integración con optimizadores
"""

import pandas as pd
import sys
from pathlib import Path
from typing import Dict
import time
import json

# Agregar path para importar optimizadores
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from optimizador_greedy import OptimizadorGreedyHC
from optimizador_ml import OptimizadorML
from optimizador_genetico import OptimizadorGenetico
from analizar_movimientos import AnalizadorMovimientos

class OptimizerService:
    def __init__(self, filepath: str, column_mapping: Dict):
        self.filepath = filepath
        self.column_mapping = column_mapping
        self.df = None
        self.df_optimizado = None
    
    def normalize_data(self) -> pd.DataFrame:
        """
        Normaliza datos del Excel al formato estándar
        """
        # Leer Excel
        df = pd.read_csv(self.filepath) if self.filepath.endswith('.csv') else pd.read_excel(self.filepath)
        
        # Renombrar columnas según mapeo
        rename_dict = {v: k for k, v in self.column_mapping.items() if v is not None}
        df = df.rename(columns=rename_dict)
        
        # Asegurar columnas requeridas
        required_cols = ['Grupo', 'Materia', 'Dia', 'Hora', 'Salon']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Falta columna requerida: {col}")
        
        # Agregar columnas opcionales si no existen
        if 'Profesor' not in df.columns:
            df['Profesor'] = 'Sin Asignar'
        
        if 'Tipo_Salon' not in df.columns:
            # Inferir tipo de salón
            df['Tipo_Salon'] = df['Salon'].apply(self._inferir_tipo_salon)
        
        if 'Es_Invalido' not in df.columns:
            df['Es_Invalido'] = 0
        
        # Normalizar bloques horarios si es necesario
        if 'Bloque_Horario' not in df.columns:
            df['Bloque_Horario'] = df['Hora']
        
        self.df = df
        return df
    
    def _inferir_tipo_salon(self, salon: str) -> str:
        """Infiere el tipo de salón basado en el nombre"""
        salon_upper = str(salon).upper()
        
        if any(lab in salon_upper for lab in ['L', 'LAB']):
            return 'Laboratorio'
        elif any(inv in salon_upper for inv in ['AV', 'E11']):
            return 'INVÁLIDO'
        else:
            return 'Teoría'
    
    def optimize(self, method: str = 'greedy') -> Dict:
        """
        Ejecuta optimización con el método seleccionado
        
        Args:
            method: 'greedy', 'ml', 'genetic'
        
        Returns:
            Dict con resultados
        """
        try:
            # Normalizar datos
            df_inicial = self.normalize_data()
            
            # Guardar temporalmente
            temp_path = Path(self.filepath).parent / 'temp_normalized.csv'
            df_inicial.to_csv(temp_path, index=False)
            
            # Medir tiempo
            start_time = time.time()
            
            # Ejecutar optimización según método
            if method == 'greedy':
                optimizador = OptimizadorGreedyHC(max_iter_hc=100, verbose=False)
                mejor_solucion, _ = optimizador.optimizar(df_inicial)
                
                # Aplicar solución
                df_optimizado = df_inicial.copy()
                df_optimizado['Salon'] = df_optimizado.index.map(mejor_solucion)
                
                # Actualizar columnas
                for idx in df_optimizado.index:
                    salon = df_optimizado.loc[idx, 'Salon']
                    df_optimizado.loc[idx, 'Es_Invalido'] = 1 if salon in optimizador.salones_invalidos else 0
                    if salon in optimizador.laboratorios:
                        df_optimizado.loc[idx, 'Tipo_Salon'] = 'Laboratorio'
                    elif salon in optimizador.salones_teoria:
                        df_optimizado.loc[idx, 'Tipo_Salon'] = 'Teoría'
            
            elif method == 'ml':
                optimizador = OptimizadorML(verbose=False)
                df_optimizado = optimizador.optimizar(str(temp_path))
            
            elif method == 'genetic':
                optimizador = OptimizadorGenetico(verbose=False)
                df_optimizado = optimizador.optimizar(str(temp_path))
            
            else:
                raise ValueError(f"Método desconocido: {method}")
            
            elapsed_time = time.time() - start_time
            
            # Calcular métricas
            metricas = self._calcular_metricas(df_inicial, df_optimizado)
            
            # Guardar resultado
            output_path = Path(self.filepath).parent.parent / 'outputs' / f'optimizado_{method}_{int(time.time())}.csv'
            df_optimizado.to_csv(output_path, index=False)
            
            # Limpiar temporal
            if temp_path.exists():
                temp_path.unlink()
            
            self.df_optimizado = df_optimizado
            
            return {
                'method': method,
                'elapsed_time': round(elapsed_time, 2),
                'metrics': metricas,
                'output_path': str(output_path),
                'total_rows': len(df_optimizado)
            }
        
        except Exception as e:
            raise Exception(f"Error en optimización: {str(e)}")
    
    def _calcular_metricas(self, df_inicial: pd.DataFrame, df_optimizado: pd.DataFrame) -> Dict:
        """Calcula métricas de mejora"""
        analizador = AnalizadorMovimientos()
        
        metricas_inicial = analizador.analizar_todos_profesores(df_inicial)
        metricas_optimizado = analizador.analizar_todos_profesores(df_optimizado)
        
        invalidos_inicial = df_inicial['Es_Invalido'].sum()
        invalidos_optimizado = df_optimizado['Es_Invalido'].sum()
        
        return {
            'invalidos': {
                'inicial': int(invalidos_inicial),
                'optimizado': int(invalidos_optimizado),
                'mejora': int(invalidos_inicial - invalidos_optimizado),
                'mejora_pct': round((invalidos_inicial - invalidos_optimizado) / invalidos_inicial * 100, 1) if invalidos_inicial > 0 else 0
            },
            'movimientos': {
                'inicial': metricas_inicial['agregado']['total_movimientos'],
                'optimizado': metricas_optimizado['agregado']['total_movimientos'],
                'mejora': metricas_inicial['agregado']['total_movimientos'] - metricas_optimizado['agregado']['total_movimientos'],
                'mejora_pct': round((metricas_inicial['agregado']['total_movimientos'] - metricas_optimizado['agregado']['total_movimientos']) / metricas_inicial['agregado']['total_movimientos'] * 100, 1)
            },
            'cambios_piso': {
                'inicial': metricas_inicial['agregado']['total_cambios_piso'],
                'optimizado': metricas_optimizado['agregado']['total_cambios_piso'],
                'mejora': metricas_inicial['agregado']['total_cambios_piso'] - metricas_optimizado['agregado']['total_cambios_piso'],
                'mejora_pct': round((metricas_inicial['agregado']['total_cambios_piso'] - metricas_optimizado['agregado']['total_cambios_piso']) / metricas_inicial['agregado']['total_cambios_piso'] * 100, 1)
            },
            'distancia': {
                'inicial': round(metricas_inicial['agregado']['total_distancia'], 0),
                'optimizado': round(metricas_optimizado['agregado']['total_distancia'], 0),
                'mejora': round(metricas_inicial['agregado']['total_distancia'] - metricas_optimizado['agregado']['total_distancia'], 0),
                'mejora_pct': round((metricas_inicial['agregado']['total_distancia'] - metricas_optimizado['agregado']['total_distancia']) / metricas_inicial['agregado']['total_distancia'] * 100, 1)
            }
        }
