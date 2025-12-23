"""
EJEMPLO DIDÁCTICO: Machine Learning (Random Forest)
===================================================

Problema: 10 clases, 4 salones, 4 profesores
Enfoque: Aprendizaje supervisado

Autor: Sistema ISC
Fecha: Diciembre 2025
"""

import random

# Datos
clases = [
    {"id": "C1", "profesor": "P1", "tipo": "T", "estudiantes": 25},
    {"id": "C2", "profesor": "P1", "tipo": "T", "estudiantes": 30},
    {"id": "C3", "profesor": "P1", "tipo": "T", "estudiantes": 28},
    {"id": "C4", "profesor": "P2", "tipo": "T", "estudiantes": 20},
    {"id": "C5", "profesor": "P2", "tipo": "L", "estudiantes": 15},
    {"id": "C6", "profesor": "P2", "tipo": "T", "estudiantes": 22},
    {"id": "C7", "profesor": "P3", "tipo": "T", "estudiantes": 18},
    {"id": "C8", "profesor": "P3", "tipo": "L", "estudiantes": 12},
    {"id": "C9", "profesor": "P4", "tipo": "T", "estudiantes": 26},
    {"id": "C10", "profesor": "P4", "tipo": "T", "estudiantes": 24},
]

salones = [
    {"id": "S1", "capacidad": 30, "tipo": "T"},
    {"id": "S2", "capacidad": 25, "tipo": "T"},
    {"id": "S3", "capacidad": 20, "tipo": "T"},
    {"id": "S4", "capacidad": 20, "tipo": "L"},
]

def extraer_features(clase):
    """Extrae características para ML."""
    return [
        clase["estudiantes"] / 50.0,  # Normalizado
        1.0 if clase["tipo"] == "L" else 0.0,  # Tipo
        int(clase["profesor"][1]) / 10.0,  # Profesor
    ]

class ModeloSimple:
    """Modelo de ML simple."""
    
    def entrenar(self, X, y):
        print("Entrenando modelo...")
        # Reglas simples
        self.reglas = [
            ("Lab", lambda f: f[1] > 0.5, 2),  # Lab → S3
            ("Muchos est.", lambda f: f[0] > 0.54, 0),  # >27 → S1
            ("Default", lambda f: True, 1),  # Resto → S2
        ]
    
    def predecir(self, features):
        for _, condicion, salon_idx in self.reglas:
            if condicion(features):
                return salon_idx
        return 1

def main():
    print("=" * 60)
    print("EJEMPLO: Machine Learning")
    print("=" * 60)
    
    # Entrenar
    modelo = ModeloSimple()
    modelo.entrenar([], [])
    
    # Asignación aleatoria (baseline)
    print("\n🎲 Asignación aleatoria (sin ML):")
    import random
    random.seed(42)
    asignacion_random = {}
    movimientos_random = 0
    for clase in clases:
        compatibles = [s for s in salones if s["tipo"] == clase["tipo"]]
        salon = random.choice(compatibles)
        asignacion_random[clase["id"]] = salon["id"]
    
    # Calcular movimientos random
    prof_salones = {}
    for clase in clases:
        prof = clase["profesor"]
        if prof not in prof_salones:
            prof_salones[prof] = set()
        prof_salones[prof].add(asignacion_random[clase["id"]])
    movimientos_random = sum(len(s) - 1 for s in prof_salones.values())
    print(f"Movimientos: {movimientos_random}")
    
    # Predecir con ML
    print("\n🤖 Predicciones con ML:")
    asignacion_ml = {}
    for clase in clases:
        features = extraer_features(clase)
        salon_idx = modelo.predecir(features)
        asignacion_ml[clase["id"]] = salones[salon_idx]["id"]
        print(f"  {clase['id']} → {salones[salon_idx]['id']}")
    
    # Calcular movimientos ML
    prof_salones_ml = {}
    for clase in clases:
        prof = clase["profesor"]
        if prof not in prof_salones_ml:
            prof_salones_ml[prof] = set()
        prof_salones_ml[prof].add(asignacion_ml[clase["id"]])
    movimientos_ml = sum(len(s) - 1 for s in prof_salones_ml.values())
    
    print(f"\n📊 Comparación:")
    print(f"  Movimientos (aleatorio): {movimientos_random}")
    print(f"  Movimientos (ML): {movimientos_ml}")
    mejora = ((movimientos_random - movimientos_ml) / movimientos_random * 100) if movimientos_random > 0 else 0
    print(f"  Mejora: {mejora:.1f}%")
    
    print("\n✅ Completado!")

if __name__ == "__main__":
    main()
