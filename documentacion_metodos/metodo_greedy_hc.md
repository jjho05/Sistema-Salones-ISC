# Método de Optimización: Greedy + Hill Climbing

## Problema ISC: Asignación de Salones
**680 asignaciones, 21 salones válidos, 51 inválidos iniciales**

---

## Introducción

**Greedy + Hill Climbing** combina construcción voraz con búsqueda local para obtener soluciones de alta calidad en **tiempo muy corto** (< 30 segundos).

### Ventajas

- ✅ **Muy rápido**: Segundos vs minutos de otros métodos
- ✅ **Efectivo**: Resultados comparables a métodos complejos
- ✅ **Simple**: Fácil de entender y modificar
- ✅ **Determinista**: Resultados reproducibles

---

## Algoritmo en Dos Fases

### Fase 1: Construcción Greedy (Voraz)

Construye solución inicial priorizando restricciones:

```python
def construccion_greedy(asignaciones):
    solucion = {}
    
    # 1. Ordenar por prioridad
    prioridades = ordenar_asignaciones(asignaciones)
    # Orden: 1er semestre > Labs > Teoría
    
    # 2. Asignar vorazmente
    for asig in prioridades:
        mejor_salon = None
        mejor_score = -inf
        
        for salon in salones_validos(asig):
            if disponible(salon, asig.hora):
                score = evaluar_asignacion(asig, salon)
                if score > mejor_score:
                    mejor_score = score
                    mejor_salon = salon
        
        solucion[asig] = mejor_salon
    
    return solucion
```

**Criterios de Evaluación**:
1. Minimizar movimientos del profesor
2. Preferir salones cercanos a clases anteriores
3. Balancear uso de salones

### Fase 2: Hill Climbing (Mejora Local)

Mejora la solución mediante swaps locales:

```python
def hill_climbing(solucion, max_iter=100):
    mejor_solucion = solucion
    mejor_energia = calcular_energia(solucion)
    
    for _ in range(max_iter):
        mejoro = False
        
        # Probar swaps de pares de asignaciones
        for asig1, asig2 in generar_pares(solucion):
            vecino = swap(solucion, asig1, asig2)
            energia = calcular_energia(vecino)
            
            if energia < mejor_energia:
                mejor_solucion = vecino
                mejor_energia = energia
                mejoro = True
                break
        
        if not mejoro:
            break  # Óptimo local alcanzado
    
    return mejor_solucion
```

---

## Función de Energía

```python
def calcular_energia(solucion):
    # HARD constraints (peso alto)
    invalidos = contar_invalidos(solucion) * 10000
    conflictos = contar_conflictos(solucion) * 5000
    
    # SOFT constraints
    movimientos = contar_movimientos(solucion) * 10
    distancia = calcular_distancia(solucion) * 1
    
    return invalidos + conflictos + movimientos + distancia
```

---

## Optimizaciones de Velocidad

1. **Caché de evaluaciones**: Guardar scores calculados
2. **Evaluación incremental**: Solo recalcular lo que cambió
3. **Early stopping**: Parar si no mejora en N iteraciones
4. **Pares inteligentes**: Solo swaps que puedan mejorar

---

## Parámetros (ISC)

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **max_iter_hill** | 100 | Suficiente para converger |
| **early_stop** | 10 | Parar si no mejora |
| **n_swaps_por_iter** | 50 | Balance velocidad/calidad |

---

## Resultados Esperados

| Métrica | Inicial | Esperado | Tiempo |
|---------|---------|----------|--------|
| **Inválidos** | 51 | 0 | - |
| **Movimientos** | 357 | ~250 | - |
| **Distancia** | 2847 | ~2000 | - |
| **Ejecución** | - | - | **< 30s** ⚡ |

---

## Comparación

| Método | Velocidad | Calidad | Complejidad |
|--------|-----------|---------|-------------|
| **Greedy+HC** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Genético | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| ML | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Tabu | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**Conclusión**: Mejor relación velocidad/calidad para este problema.
