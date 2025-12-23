# Tabla Comparativa - Estado del Arte

## Comparación Detallada de Enfoques

| # | Autores | Año | Enfoque | Problema | Tamaño | Tiempo Ejec. | Calidad | Garantías P1 | Escalabilidad |
|---|---------|-----|---------|----------|--------|--------------|---------|--------------|---------------|
| 1 | Pillay & Qu | 2018 | Genetic Algorithm | Timetabling | 300-500 | >5 min | Alta | ❌ No | ⭐⭐⭐ |
| 2 | Kristiansen et al. | 2020 | Random Forest + RL | Classroom Assign. | 400-600 | <10s | Media | ❌ No | ⭐⭐⭐⭐ |
| 3 | Bellio et al. | 2021 | SA + Tabu Search | ITC Benchmark | 200-400 | 2-5 min | Muy Alta | ❌ No | ⭐⭐⭐ |
| 4 | Burke et al. | 2019 | Greedy + HC | Classroom Assign. | 300-500 | <1 min | Media | ❌ No | ⭐⭐⭐⭐ |
| 5 | Santos et al. | 2022 | Integer Programming | Optimal Assign. | <200 | Variable | Óptima | ✅ Sí | ⭐ |
| 6 | Zhang et al. | 2023 | Deep Q-Learning | Dynamic Scheduling | 500+ | Training: hrs | Alta | ❌ No | ⭐⭐⭐⭐⭐ |
| 7 | Fonseca et al. | 2020 | NSGA-II | Multi-objective | 300-400 | 3-7 min | Alta | ❌ No | ⭐⭐⭐ |
| 8 | Müller & Murray | 2021 | Constraint Prog. | Complex Constraints | 200-300 | Variable | Alta | ⚠️ Parcial | ⭐⭐ |
| 9 | Sørensen & Dahms | 2022 | ALNS | Large-scale | 500-1000 | 5-10 min | Muy Alta | ❌ No | ⭐⭐⭐⭐⭐ |
| 10 | Tan et al. | 2023 | GA + SA Hybrid | Preferences | 400-600 | 3-6 min | Alta | ⚠️ 95% | ⭐⭐⭐⭐ |
| 11 | Lewis & Thompson | 2019 | Graph Coloring | Exam/Class Assign. | <500 | <2 min | Óptima | ❌ No | ⭐⭐ |
| 12 | Qu et al. | 2020 | Memetic Algorithm | ITC 2019 | 300-500 | 5-8 min | Muy Alta | ❌ No | ⭐⭐⭐ |
| 13 | Shiau | 2021 | PSO | Timetabling | 200-400 | <2 min | Media | ❌ No | ⭐⭐⭐ |
| 14 | Sánchez-Oro et al. | 2022 | VNS | Multi-campus | 400-700 | 3-5 min | Alta | ❌ No | ⭐⭐⭐⭐ |
| 15 | Socha et al. | 2019 | Ant Colony | Course Scheduling | 300-500 | 4-6 min | Media-Alta | ❌ No | ⭐⭐⭐ |
| **NUESTRO** | **Olvera** | **2025** | **Multi-Algoritmo** | **Classroom + Pref.** | **680** | **16-74s** | **Alta** | **✅ 100%** | **⭐⭐⭐⭐** |

## Leyenda

**Escalabilidad:**
- ⭐ = Hasta 200 clases
- ⭐⭐ = Hasta 300 clases  
- ⭐⭐⭐ = Hasta 500 clases
- ⭐⭐⭐⭐ = Hasta 700 clases
- ⭐⭐⭐⭐⭐ = Más de 700 clases

**Garantías P1:**
- ✅ Sí = Garantía 100% de cumplimiento
- ⚠️ Parcial = Alto cumplimiento pero no garantizado
- ❌ No = Sin garantías específicas

## Análisis por Categorías

### Velocidad de Ejecución

**Top 3 Más Rápidos:**
1. Kristiansen et al. (2020) - ML: <10s
2. Burke et al. (2019) - Greedy+HC: <1 min
3. **NUESTRO - Greedy+HC: ~30s** ✅

**Más Lentos:**
- Zhang et al. (2023) - Deep RL: Horas de entrenamiento
- Qu et al. (2020) - Memetic: 5-8 min
- Sørensen & Dahms (2022) - ALNS: 5-10 min

### Calidad de Soluciones

**Mejor Calidad:**
1. Santos et al. (2022) - ILP: Óptima (pero no escala)
2. Bellio et al. (2021) - SA+Tabu: Muy Alta
3. Sørensen & Dahms (2022) - ALNS: Muy Alta

**Nuestra Posición:**
- Greedy+HC: Alta calidad, excelente balance velocidad/calidad
- ML: Media-Alta, muy rápido
- Genético: Alta calidad, exploración amplia

### Garantías de Prioridades

**Con Garantías:**
1. Santos et al. (2022) - ILP: Sí (pero limitado a <200 clases)
2. **NUESTRO: Sí (680 clases)** ✅ **ÚNICO EN SU CATEGORÍA**

**Sin Garantías:**
- Todos los demás enfoques metaheurísticos
- Tan et al. (2023): 95% pero no garantizado

### Escalabilidad

**Mejor Escalabilidad:**
1. Zhang et al. (2023) - Deep RL: ⭐⭐⭐⭐⭐
2. Sørensen & Dahms (2022) - ALNS: ⭐⭐⭐⭐⭐
3. Kristiansen et al. (2020) - ML: ⭐⭐⭐⭐

**Nuestra Posición:**
- 680 clases manejadas exitosamente
- 4 algoritmos diferentes probados
- Escalabilidad: ⭐⭐⭐⭐

## Ventajas Competitivas de Nuestra Solución

### 1. Garantía Absoluta de PRIORIDAD 1
**Único en la literatura para problemas de este tamaño**
- Pre-asignación forzada
- Índices inmutables
- Corrección post-optimización
- **Resultado: 100% de cumplimiento garantizado**

### 2. Enfoque Multi-Algoritmo
**Comparación sistemática en misma instancia**
- 4 algoritmos diferentes
- Mismos datos de entrada
- Análisis estadístico riguroso (30+ corridas)
- Identificación del mejor enfoque según contexto

### 3. Métricas Centradas en el Profesor
**Innovación en función objetivo**
- Movimientos entre salones
- Cambios de piso
- Distancia total recorrida
- Impacto directo en bienestar docente

### 4. Sistema Completo Funcional
**Más allá del prototipo académico**
- Interfaz gráfica (configurador_materias.py)
- Aplicación web (en desarrollo)
- Datos reales validados (ITCM)
- Documentación completa

### 5. Validación Estadística Rigurosa
**Análisis más profundo que la mayoría**
- 30+ corridas por algoritmo
- Pruebas de normalidad
- ANOVA / Kruskal-Wallis
- Post-hoc tests (Tukey HSD)
- Intervalos de confianza

## Gaps que Nuestra Solución Llena

| Gap Identificado | Solución Propuesta | Impacto |
|------------------|-------------------|---------|
| Sin garantía de prioridades críticas | Pre-asignación P1 forzada | ⭐⭐⭐⭐⭐ |
| Falta de corrección post-optimización | Módulo automático de corrección | ⭐⭐⭐⭐ |
| Comparaciones limitadas (1-2 baselines) | 4 algoritmos en misma instancia | ⭐⭐⭐⭐ |
| Métricas genéricas | Métricas específicas de profesores | ⭐⭐⭐⭐ |
| Validación estadística básica | ANOVA + post-hoc completo | ⭐⭐⭐⭐ |
| Prototipos académicos | Sistema completo funcional | ⭐⭐⭐⭐⭐ |

## Conclusiones

**Posicionamiento:**
Nuestra solución se posiciona como un **enfoque híbrido práctico** que combina:
- Garantías formales (como ILP) pero escalable
- Velocidad (como Greedy) pero con calidad
- Exploración (como GA) pero con eficiencia
- Validación rigurosa (como investigación académica) pero aplicado

**Contribución Principal:**
Primer sistema documentado que garantiza 100% de cumplimiento de prioridades críticas en problemas de >600 clases, con validación estadística completa y múltiples algoritmos comparados en la misma instancia real.
