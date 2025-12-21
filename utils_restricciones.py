#!/usr/bin/env python3
"""
Utilidades para Restricciones - Sistema de Salones ISC
Funciones compartidas para manejar configuración de materias y preferencias de profesores
"""

import json
import os
from typing import Dict, Tuple, Optional

def cargar_configuraciones(script_dir: Optional[str] = None) -> Tuple[Dict, Dict]:
    """
    Carga configuración de materias y preferencias de profesores
    
    Returns:
        Tuple[Dict, Dict]: (config_materias, preferencias_profesores)
    """
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar configuración de materias
    config_materias_path = os.path.join(script_dir, "configuracion_materias.json")
    try:
        with open(config_materias_path, 'r', encoding='utf-8') as f:
            config_materias = json.load(f)
        print(f"✅ Configuración de materias cargada: {len(config_materias)} materias")
    except FileNotFoundError:
        print("⚠️  configuracion_materias.json no encontrado, usando valores por defecto")
        config_materias = {}
    
    # Cargar preferencias de profesores
    prefs_profesores_path = os.path.join(script_dir, "preferencias_profesores.json")
    try:
        with open(prefs_profesores_path, 'r', encoding='utf-8') as f:
            preferencias_profesores = json.load(f)
        print(f"✅ Preferencias de profesores cargadas: {len(preferencias_profesores)} profesores")
    except FileNotFoundError:
        print("⚠️  preferencias_profesores.json no encontrado, sin preferencias")
        preferencias_profesores = {}
    
    return config_materias, preferencias_profesores


def determinar_tipo_hora(materia: str, indice_hora: int, config_materias: Dict) -> str:
    """
    Determina si una hora específica debe ser teoría o laboratorio
    
    Args:
        materia: Nombre de la materia
        indice_hora: Índice de la hora (0-based) dentro de la semana
        config_materias: Configuración de materias
    
    Returns:
        str: 'Teoría' o 'Laboratorio'
    """
    if materia not in config_materias:
        # Si no está configurada, asumir teoría por defecto
        return 'Teoría'
    
    config = config_materias[materia]
    horas_teoria = config.get('horas_teoria', config.get('total_horas', 0))
    horas_lab = config.get('horas_lab', 0)
    
    # Distribuir: primeras N horas son teoría, resto son lab
    # Esto es una estrategia simple, se puede mejorar
    if indice_hora < horas_teoria:
        return 'Teoría'
    else:
        return 'Laboratorio'


def obtener_preferencia_profesor(profesor: str, tipo_salon: str, 
                                 preferencias_profesores: Dict) -> Optional[str]:
    """
    Obtiene la preferencia de salón para un profesor
    
    Args:
        profesor: Nombre del profesor
        tipo_salon: 'Teoría' o 'Laboratorio'
        preferencias_profesores: Diccionario de preferencias
    
    Returns:
        str: Nombre del salón preferido o None
    """
    if profesor not in preferencias_profesores:
        return None
    
    prefs = preferencias_profesores[profesor]
    
    if tipo_salon == 'Teoría':
        salon = prefs.get('salon_teoria', 'Sin preferencia')
    else:
        salon = prefs.get('salon_lab', 'Sin preferencia')
    
    if salon == 'Sin preferencia':
        return None
    
    return salon


def es_preferencia_prioritaria(profesor: str, tipo_salon: str,
                               preferencias_profesores: Dict) -> bool:
    """
    Verifica si la preferencia del profesor es prioritaria
    
    Args:
        profesor: Nombre del profesor
        tipo_salon: 'Teoría' o 'Laboratorio'
        preferencias_profesores: Diccionario de preferencias
    
    Returns:
        bool: True si es prioritaria
    """
    if profesor not in preferencias_profesores:
        return False
    
    prefs = preferencias_profesores[profesor]
    
    if tipo_salon == 'Teoría':
        prioridad = prefs.get('prioridad_teoria', 'Opcional')
    else:
        prioridad = prefs.get('prioridad_lab', 'Opcional')
    
    return prioridad == 'Prioritario'


def filtrar_salones_por_tipo(salones_disponibles: list, tipo_requerido: str,
                             salones_teoria: list = None, salones_lab: list = None) -> list:
    """
    Filtra salones por tipo (teoría o laboratorio)
    
    Args:
        salones_disponibles: Lista de salones disponibles
        tipo_requerido: 'Teoría' o 'Laboratorio'
        salones_teoria: Lista de salones de teoría (opcional)
        salones_lab: Lista de salones de laboratorio (opcional)
    
    Returns:
        list: Salones filtrados por tipo
    """
    # Definir salones por tipo si no se proporcionan
    if salones_teoria is None:
        salones_teoria = ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9',
                         'FFA', 'FFB', 'FFC', 'FFD']
    
    if salones_lab is None:
        salones_lab = ['LBD', 'LBD2', 'LCA', 'LCG1', 'LCG2', 'LIA', 'LR', 'LSO']
    
    if tipo_requerido == 'Teoría':
        return [s for s in salones_disponibles if s in salones_teoria]
    else:
        return [s for s in salones_disponibles if s in salones_lab]


def calcular_penalizacion_preferencias(asignaciones: Dict, preferencias_profesores: Dict,
                                       config_materias: Dict) -> Tuple[int, int]:
    """
    Calcula penalizaciones por violar preferencias de profesores
    
    Args:
        asignaciones: Dict con asignaciones {(grupo, dia, bloque): salon}
        preferencias_profesores: Preferencias de profesores
        config_materias: Configuración de materias
    
    Returns:
        Tuple[int, int]: (violaciones_prioritarias, violaciones_opcionales)
    """
    violaciones_prioritarias = 0
    violaciones_opcionales = 0
    
    # Esta función se implementará específicamente en cada optimizador
    # ya que la estructura de asignaciones puede variar
    
    return violaciones_prioritarias, violaciones_opcionales


def validar_distribucion_teoria_lab(df, config_materias: Dict) -> Dict:
    """
    Valida que la distribución de horas teoría/lab sea correcta
    
    Args:
        df: DataFrame con el horario
        config_materias: Configuración de materias
    
    Returns:
        Dict: Estadísticas de validación
    """
    stats = {
        'total_materias': 0,
        'correctas': 0,
        'incorrectas': 0,
        'detalles': []
    }
    
    # Agrupar por materia
    for materia in df['Materia'].unique():
        if materia not in config_materias:
            continue
        
        stats['total_materias'] += 1
        materia_df = df[df['Materia'] == materia]
        
        config = config_materias[materia]
        horas_teoria_esperadas = config['horas_teoria']
        horas_lab_esperadas = config['horas_lab']
        
        # Contar horas asignadas
        horas_teoria_asignadas = len(materia_df[materia_df['Tipo_Salon'] == 'Teoría'])
        horas_lab_asignadas = len(materia_df[materia_df['Tipo_Salon'] == 'Laboratorio'])
        
        if (horas_teoria_asignadas == horas_teoria_esperadas and 
            horas_lab_asignadas == horas_lab_esperadas):
            stats['correctas'] += 1
        else:
            stats['incorrectas'] += 1
            stats['detalles'].append({
                'materia': materia,
                'esperado': f"{horas_teoria_esperadas}T + {horas_lab_esperadas}L",
                'asignado': f"{horas_teoria_asignadas}T + {horas_lab_asignadas}L"
            })
    
    return stats


if __name__ == "__main__":
    # Prueba de las funciones
    print("🧪 Probando utilidades de restricciones...\n")
    
    config_materias, prefs_profesores = cargar_configuraciones()
    
    print(f"\n📊 Materias configuradas: {len(config_materias)}")
    print(f"👨‍🏫 Profesores con preferencias: {len(prefs_profesores)}")
    
    # Ejemplo de uso
    if config_materias:
        materia_ejemplo = list(config_materias.keys())[0]
        print(f"\n🔍 Ejemplo - {materia_ejemplo}:")
        print(f"   Configuración: {config_materias[materia_ejemplo]}")
        
        for i in range(config_materias[materia_ejemplo]['total_horas']):
            tipo = determinar_tipo_hora(materia_ejemplo, i, config_materias)
            print(f"   Hora {i+1}: {tipo}")
    
    if prefs_profesores:
        profesor_ejemplo = list(prefs_profesores.keys())[0]
        print(f"\n👨‍🏫 Ejemplo - {profesor_ejemplo}:")
        print(f"   Preferencias: {prefs_profesores[profesor_ejemplo]}")
        
        pref_teoria = obtener_preferencia_profesor(profesor_ejemplo, 'Teoría', prefs_profesores)
        es_prioritaria = es_preferencia_prioritaria(profesor_ejemplo, 'Teoría', prefs_profesores)
        print(f"   Salón teoría preferido: {pref_teoria} ({'Prioritario' if es_prioritaria else 'Opcional'})")
