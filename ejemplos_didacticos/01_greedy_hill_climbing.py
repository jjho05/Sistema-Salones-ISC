"""
EJEMPLO DIDÁCTICO: Greedy + Hill Climbing
==========================================

Este ejemplo muestra cómo funciona el algoritmo Greedy con Hill Climbing
en un problema de asignación de salones.

Problema: 10 clases, 4 salones, 4 profesores
Objetivo: Minimizar movimientos de profesores

Autor: Sistema de Asignación de Salones ISC
Fecha: Diciembre 2025
"""

import random
from typing import List, Dict, Tuple

# ============================================================================
# DATOS DEL PROBLEMA
# ============================================================================

# 10 Clases con sus atributos
clases = [
    {"id": "C1", "profesor": "P1", "dia": "Lunes", "hora": "08:00", "tipo": "T", "estudiantes": 25},
    {"id": "C2", "profesor": "P1", "dia": "Lunes", "hora": "10:00", "tipo": "T", "estudiantes": 30},
    {"id": "C3", "profesor": "P1", "dia": "Martes", "hora": "09:00", "tipo": "T", "estudiantes": 28},
    {"id": "C4", "profesor": "P2", "dia": "Lunes", "hora": "09:00", "tipo": "T", "estudiantes": 20},
    {"id": "C5", "profesor": "P2", "dia": "Martes", "hora": "11:00", "tipo": "L", "estudiantes": 15},
    {"id": "C6", "profesor": "P2", "dia": "Miércoles", "hora": "08:00", "tipo": "T", "estudiantes": 22},
    {"id": "C7", "profesor": "P3", "dia": "Martes", "hora": "08:00", "tipo": "T", "estudiantes": 18},
    {"id": "C8", "profesor": "P3", "dia": "Miércoles", "hora": "10:00", "tipo": "L", "estudiantes": 12},
    {"id": "C9", "profesor": "P4", "dia": "Jueves", "hora": "09:00", "tipo": "T", "estudiantes": 26},
    {"id": "C10", "profesor": "P4", "dia": "Viernes", "hora": "08:00", "tipo": "T", "estudiantes": 24},
]

# 4 Salones disponibles
salones = [
    {"id": "S1", "capacidad": 30, "tipo": "T", "piso": 0},
    {"id": "S2", "capacidad": 25, "tipo": "T", "piso": 0},
    {"id": "S3", "capacidad": 20, "tipo": "T", "piso": 1},
    {"id": "S4", "capacidad": 20, "tipo": "L", "piso": 1},
]

# ============================================================================
# FUNCIONES DE EVALUACIÓN
# ============================================================================

def calcular_movimientos(asignacion: Dict[str, str]) -> int:
    """Calcula el número de movimientos de profesores."""
    profesores_salones = {}
    
    for clase in clases:
        profesor = clase["profesor"]
        salon = asignacion[clase["id"]]
        
        if profesor not in profesores_salones:
            profesores_salones[profesor] = set()
        profesores_salones[profesor].add(salon)
    
    movimientos = 0
    for profesor, salones_usados in profesores_salones.items():
        movimientos += len(salones_usados) - 1
    
    return max(0, movimientos)


def energia(asignacion: Dict[str, str]) -> float:
    """Función objetivo: E = 10 * movimientos"""
    return 10 * calcular_movimientos(asignacion)


def es_factible(asignacion: Dict[str, str]) -> bool:
    """Verifica si una asignación es factible."""
    # Verificar capacidad y tipo
    for clase in clases:
        salon_id = asignacion[clase["id"]]
        salon = next(s for s in salones if s["id"] == salon_id)
        
        if clase["estudiantes"] > salon["capacidad"]:
            return False
        if clase["tipo"] != salon["tipo"]:
            return False
    
    # Verificar conflictos temporales
    for i, c1 in enumerate(clases):
        for c2 in clases[i+1:]:
            if c1["dia"] == c2["dia"] and c1["hora"] == c2["hora"]:
                if asignacion[c1["id"]] == asignacion[c2["id"]]:
                    return False
    
    return True


# ============================================================================
# ALGORITMO GREEDY
# ============================================================================

def greedy_construccion():
    """Construye una solución inicial (intencionalmente subóptima para demostración)."""
    asignacion = {}
    
    # Asignar de forma simple sin optimizar (para que Hill Climbing pueda mejorar)
    for i, clase in enumerate(clases):
        # Rotar entre salones compatibles (subóptimo)
        salones_compatibles = [s for s in salones if s["tipo"] == clase["tipo"] and s["capacidad"] >= clase["estudiantes"]]
        if salones_compatibles:
            # Usar módulo para rotar (crea solución subóptima)
            salon = salones_compatibles[i % len(salones_compatibles)]
            asignacion[clase["id"]] = salon["id"]
    
    return asignacion


# ============================================================================
# HILL CLIMBING
# ============================================================================

def generar_vecinos(asignacion: Dict[str, str]) -> List[Dict[str, str]]:
    """Genera vecinos intercambiando asignaciones."""
    vecinos = []
    
    for i, c1 in enumerate(clases):
        for c2 in clases[i+1:]:
            if c1["tipo"] == c2["tipo"]:
                vecino = asignacion.copy()
                vecino[c1["id"]], vecino[c2["id"]] = vecino[c2["id"]], vecino[c1["id"]]
                
                if es_factible(vecino):
                    vecinos.append(vecino)
    
    return vecinos


def hill_climbing(asignacion_inicial: Dict[str, str], max_iter: int = 100) -> Tuple[Dict[str, str], List[float]]:
    """Mejora la solución usando Hill Climbing."""
    actual = asignacion_inicial.copy()
    energia_actual = energia(actual)
    historial = [energia_actual]
    
    for iteracion in range(max_iter):
        vecinos = generar_vecinos(actual)
        
        if not vecinos:
            break
        
        mejor_vecino = None
        mejor_energia = energia_actual
        
        for vecino in vecinos:
            e = energia(vecino)
            if e < mejor_energia:
                mejor_energia = e
                mejor_vecino = vecino
        
        if mejor_vecino is None:
            break
        
        actual = mejor_vecino
        energia_actual = mejor_energia
        historial.append(energia_actual)
    
    return actual, historial


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("EJEMPLO DIDÁCTICO: Greedy + Hill Climbing")
    print("=" * 70)
    
    # Construcción Greedy
    solucion_inicial = greedy_construccion()
    energia_inicial = energia(solucion_inicial)
    
    print(f"\nSolución Inicial (Greedy):")
    for clase in clases:
        print(f"  {clase['id']} → {solucion_inicial[clase['id']]}")
    print(f"Energía: {energia_inicial}")
    
    # Hill Climbing
    solucion_final, historial = hill_climbing(solucion_inicial)
    energia_final = energia(solucion_final)
    
    print(f"\nSolución Final (Hill Climbing):")
    for clase in clases:
        print(f"  {clase['id']} → {solucion_final[clase['id']]}")
    print(f"Energía: {energia_final}")
    
    mejora = ((energia_inicial - energia_final) / energia_inicial) * 100 if energia_inicial > 0 else 0
    print(f"\nMejora: {mejora:.1f}%")
    print(f"Iteraciones: {len(historial)}")


if __name__ == "__main__":
    main()
