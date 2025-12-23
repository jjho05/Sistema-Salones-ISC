"""
EJEMPLO DIDÁCTICO: Algoritmo Genético
======================================

Problema: 10 clases, 4 salones, 4 profesores
Enfoque: Evolución con selección, cruce y mutación

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

def crear_individuo():
    """Crea individuo aleatorio."""
    individuo = []
    for clase in clases:
        compatibles = [i for i, s in enumerate(salones) 
                      if s["tipo"] == clase["tipo"]]
        individuo.append(random.choice(compatibles) if compatibles else 0)
    return individuo

def fitness(individuo):
    """Calcula fitness (mayor es mejor)."""
    # Contar movimientos
    prof_salones = {}
    for i, clase in enumerate(clases):
        prof = clase["profesor"]
        if prof not in prof_salones:
            prof_salones[prof] = set()
        prof_salones[prof].add(individuo[i])
    
    movimientos = sum(len(s) - 1 for s in prof_salones.values())
    return 1.0 / (1.0 + movimientos * 10)

def cruce(p1, p2):
    """Cruce de un punto."""
    punto = len(p1) // 2
    return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]

def mutacion(ind, prob=0.1):
    """Mutación aleatoria."""
    mutado = ind.copy()
    for i in range(len(mutado)):
        if random.random() < prob:
            compatibles = [j for j, s in enumerate(salones) 
                          if s["tipo"] == clases[i]["tipo"]]
            if compatibles:
                mutado[i] = random.choice(compatibles)
    return mutado

def algoritmo_genetico(tam_pob=20, generaciones=30):
    """Ejecuta AG."""
    poblacion = [crear_individuo() for _ in range(tam_pob)]
    historial = []
    
    for gen in range(generaciones):
        # Evaluar
        fits = [fitness(ind) for ind in poblacion]
        historial.append(max(fits))
        
        if gen % 10 == 0:
            print(f"Gen {gen}: Fitness = {max(fits):.4f}")
        
        # Elitismo
        elite_idx = fits.index(max(fits))
        elite = poblacion[elite_idx].copy()
        
        # Nueva población
        nueva_pob = [elite]
        
        while len(nueva_pob) < tam_pob:
            # Selección torneo
            torneo = random.sample(list(zip(poblacion, fits)), 3)
            p1 = max(torneo, key=lambda x: x[1])[0]
            torneo = random.sample(list(zip(poblacion, fits)), 3)
            p2 = max(torneo, key=lambda x: x[1])[0]
            
            # Cruce y mutación
            h1, h2 = cruce(p1, p2)
            h1 = mutacion(h1)
            h2 = mutacion(h2)
            
            nueva_pob.extend([h1, h2])
        
        poblacion = nueva_pob[:tam_pob]
    
    # Mejor individuo
    fits_final = [fitness(ind) for ind in poblacion]
    mejor = poblacion[fits_final.index(max(fits_final))]
    
    return mejor, historial

def main():
    print("=" * 60)
    print("EJEMPLO: Algoritmo Genético")
    print("=" * 60)
    
    random.seed(42)
    
    # Crear solución aleatoria inicial para comparar
    print("\n🎲 Solución aleatoria inicial:")
    inicial_random = crear_individuo()
    fitness_random = fitness(inicial_random)
    print(f"Fitness aleatorio: {fitness_random:.4f}")
    
    # Ejecutar AG con más generaciones
    print("\n🧬 Ejecutando Algoritmo Genético...")
    mejor, historial = algoritmo_genetico(tam_pob=30, generaciones=100)
    
    print("\n🏆 Mejor solución encontrada:")
    for i, clase in enumerate(clases):
        print(f"  {clase['id']} → {salones[mejor[i]]['id']}")
    
    fitness_final = fitness(mejor)
    print(f"\nFitness final: {fitness_final:.4f}")
    print(f"Fitness inicial (aleatorio): {fitness_random:.4f}")
    
    mejora = ((fitness_final - fitness_random) / fitness_random * 100) if fitness_random > 0 else 0
    print(f"Mejora sobre aleatorio: {mejora:.1f}%")
    
    # Mostrar evolución
    print(f"\n📈 Evolución:")
    print(f"  Generación 0: {historial[0]:.4f}")
    print(f"  Generación 50: {historial[50]:.4f}")
    print(f"  Generación 99: {historial[-1]:.4f}")
    
    print("\n✅ Completado!")

if __name__ == "__main__":
    main()
