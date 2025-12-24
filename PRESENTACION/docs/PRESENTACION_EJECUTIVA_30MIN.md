---
marp: true
theme: default
paginate: true
math: mathjax
style: |
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap');
  
  :root {
    font-family: Outfit, Helvetica, Arial;
  }
  
  .MathJax, .MathJax_Display, mjx-container {
    font-family: 'Times New Roman', Times, serif !important;
  }
  
  section {
    background-color: #ffffff;
    background-image: linear-gradient(to bottom right, #cadaf7 5%, #87a7e4 95%);
  }
  
  h1, h2, h3, h4, h5, h6 {
    color: #214484;
    font-weight: 700;
  }
  
  a {
    color: #303ca6;
  }
  
  code {
    background-color: #ffffffad;
  }
  
  section::after {
    font-size: 0.75em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    color: #303ca6;
  }
---

<!-- _class: lead blue -->
# Sistema de Asignación de Salones ISC

**Optimización Inteligente de Espacios Académicos**

**Jesús Olvera**

Ingeniería en Sistemas Computacionales
Instituto Tecnológico de Ciudad Madero

---

## Agenda

1. Contexto del Problema
2. Estado del Arte
3. Modelo Matemático
4. Algoritmos Implementados
5. Resultados Experimentales
6. Pruebas Estadísticas
7. Conclusiones

**Duración:** ~30-40 minutos

---

## Contexto del Problema

**Desafío:** Asignar 680 clases a 21 salones

**Datos del problema:**
- 680 clases del programa ISC
- 21 salones disponibles
- ~30 profesores
- 85 preferencias prioritarias (P1)

---

## Objetivos de Optimización

**Minimizar:**
- Movimientos de profesores entre salones
- Cambios de piso
- Distancia total recorrida

**Garantizar:**
- 100% cumplimiento de preferencias P1
- Capacidad suficiente
- Compatibilidad teoría/laboratorio

---

## Sistema de Prioridades

**PRIORIDAD 1 (Hard Constraint):**
- Preferencias de profesores
- **100% garantizado** mediante pre-asignación

**PRIORIDAD 2 (Soft Constraint):**
- Consistencia de grupos (mismo salón)

**PRIORIDAD 3 (Soft Constraint):**
- Primer semestre en salones específicos

---

## Estado del Arte

**Revisión de 15 artículos científicos (2018-2025)**

Enfoques principales:
- Metaheurísticas (Tabu Search, Simulated Annealing)
- Machine Learning (Deep Learning, Reinforcement Learning)
- Programación Lineal/Entera
- Algoritmos Híbridos

---

## Comparativa de Enfoques

| Enfoque | Ventaja | Limitación | Tiempo |
|---------|---------|------------|--------|
| **Metaheurísticas** | Buena calidad | Tiempo alto | Horas |
| **Machine Learning** | Rápido | Necesita datos | Minutos |
| **Prog. Lineal** | Óptimo garantizado | No escala | Días |
| **Híbridos** | Balance | Complejidad | Variable |

---

## Nuestra Contribución

**Enfoque híbrido con 4 algoritmos:**
1. Heurística del profesor (baseline)
2. Greedy + Hill Climbing
3. Machine Learning (Random Forest)
4. Algoritmo Genético

**Innovación:** Pre-asignación P1 + Comparación rigurosa

---

## Modelo Matemático

**Conjuntos:**
- $C$: Clases (n = 680)
- $S$: Salones (m = 21)
- $P$: Profesores (k ≈ 30)

**Variable de decisión:**
- $A: C \rightarrow S$ (asignación de clase a salón)

---

## Función Objetivo

$$
E(A) = 10 \cdot movimientos + 5 \cdot cambios\_piso + 1 \cdot distancia
$$

**Pesos justificados:**
- Movimientos: Objetivo principal (10.0)
- Cambios de piso: Importante (5.0)
- Distancia: Refinamiento (1.0)

---

## Restricciones Duras

**R1. Unicidad temporal:**
$$
\forall c_i, c_j: (dia_i = dia_j \land hora_i = hora_j) \Rightarrow A(c_i) \neq A(c_j)
$$

**R2. Capacidad:**
$$
\forall c \in C: capacidad(A(c)) \geq estudiantes(c)
$$

**R3. Tipo compatible:**
- Laboratorios → Salones de laboratorio
- Teoría → Cualquier salón válido

---

## Pre-Asignación de PRIORIDAD 1

**Objetivo:** Garantizar 100% cumplimiento de P1

**Proceso:**
1. Identificar 85 preferencias P1
2. Asignar forzosamente antes de optimización
3. Marcar como inmutables
4. Proteger durante optimización

**Resultado:** Base sólida para todos los algoritmos

---

## Ventajas de Pre-Asignación

**Beneficios:**
- ✅ Simplifica el problema (680 → 595 clases libres)
- ✅ Garantiza cumplimiento P1
- ✅ Separa restricciones duras de suaves
- ✅ Permite enfocar optimización en P2 y P3

**Implementación:** `pre_asignar_p1.py`

---

## Algoritmo 1: Greedy + Hill Climbing

**Fase 1: Construcción Voraz**
- Asignar clases una por una
- Seleccionar salón de menor costo incremental

**Fase 2: Hill Climbing**
- Explorar vecindario (intercambios)
- Aceptar solo mejoras
- Criterio de parada: 50 iteraciones sin mejora

---

## Greedy + HC: Características

**Ventajas:**
- Balance calidad/tiempo
- Convergencia garantizada a óptimo local
- Resultados consistentes

**Parámetros:**
- max_iteraciones: 1000
- max_sin_mejora: 50
- Tiempo típico: ~30 segundos

---

## Algoritmo 2: Machine Learning

**Enfoque:**
- Entrenar Random Forest con horarios previos
- Predecir salón óptimo para cada clase

**Features extraídas:**
- Número de estudiantes (35% importancia)
- Tipo de clase (25%)
- Hora del día (15%)
- Profesor (15%)
- Día de la semana (10%)

---

## ML: Características

**Ventajas:**
- Más rápido (~16s)
- Aprende de datos históricos
- Buena precisión (94%)

**Parámetros:**
- n_estimators: 100 árboles
- max_depth: 20
- min_samples_split: 5

---

## Algoritmo 3: Genético

**Componentes:**
- Población: 100 individuos
- Selección: Torneo (tamaño 3)
- Cruce: Un punto (prob. 0.8)
- Mutación: Aleatoria (prob. 0.1)
- Elitismo: 5 mejores

**Generaciones:** 200

---

## Genético: Características

**Ventajas:**
- Exploración amplia del espacio
- Múltiples soluciones de calidad
- Robustez

**Desventajas:**
- Más lento (~74s)
- Mayor variabilidad
- Configuración compleja

---

## Parámetros Críticos

**Greedy + Hill Climbing:**
- Pesos: movimientos (10.0), piso (5.0), distancia (1.0)
- max_iteraciones: 1000
- max_sin_mejora: 50

**Machine Learning:**
- n_estimators: 100
- max_depth: 20
- min_samples_split: 5

**Genético:**
- Población: 100
- Generaciones: 200
- Prob. cruce: 0.8, mutación: 0.1

---

## Análisis de Sensibilidad

**Experimento: Variación de pesos (Greedy+HC)**

| w_movimientos | Movimientos | Energía |
|---------------|-------------|---------|
| 5.0 | 320 | 5780 |
| **10.0** | **314** | **5181** ✅ |
| 15.0 | 312 | 6045 |
| 20.0 | 310 | 7285 |

**Conclusión:** w=10.0 es óptimo

---

## Ejemplo Didáctico: Greedy + HC

**Problema simplificado:**
- 10 clases
- 4 salones
- 4 profesores

**Objetivo:** Demostrar funcionamiento del algoritmo

---

## Ejemplo: Construcción Voraz

```python
# Asignar cada clase al salón de menor costo
for clase in clases:
    mejor_salon = None
    menor_costo = infinito
    
    for salon in salones_compatibles:
        costo = calcular_costo_incremental(clase, salon)
        if costo < menor_costo:
            menor_costo = costo
            mejor_salon = salon
    
    asignar(clase, mejor_salon)
```

---

## Ejemplo: Hill Climbing

```python
# Mejorar solución iterativamente
mejora = True
while mejora:
    mejora = False
    for intercambio in vecindario:
        if energia(intercambio) < energia(actual):
            actual = intercambio
            mejora = True
            break
```

---

## Ejemplo: Resultados

**Solución inicial (voraz):**
- Movimientos: 6
- Energía: 85

**Solución final (HC):**
- Movimientos: 3
- Energía: 42

**Mejora: 50%** ✅

---

## Resultados Experimentales

**Metodología:**
- 30 corridas por algoritmo
- 90 experimentos totales
- Semillas aleatorias: 1-30
- Métricas: movimientos, cambios piso, distancia, tiempo

---

## Resultados: Movimientos

| Algoritmo | Media | Std | Min | Max |
|-----------|-------|-----|-----|-----|
| Inicial | 357 | - | - | - |
| **Greedy+HC** | **314.2** | 2.1 | 311 | 318 |
| ML | 365.8 | 2.4 | 362 | 370 |
| Genético | 378.5 | 3.1 | 374 | 385 |

**Ganador:** Greedy+HC (-12% vs inicial)

---

## Resultados: Cambios de Piso

| Algoritmo | Media | Std | Min | Max |
|-----------|-------|-----|-----|-----|
| Inicial | 287 | - | - | - |
| **Greedy+HC** | **206.1** | 2.0 | 203 | 210 |
| ML | 223.2 | 2.2 | 220 | 227 |
| Genético | 286.3 | 3.2 | 282 | 293 |

**Ganador:** Greedy+HC (-28% vs inicial)

---

## Resultados: Distancia

| Algoritmo | Media | Std | Min | Max |
|-----------|-------|-----|-----|-----|
| Inicial | 2847 | - | - | - |
| Greedy+HC | 1951.3 | 10.2 | 1938 | 1972 |
| **ML** | **1821.5** | 10.8 | 1810 | 1845 |
| Genético | 2413.2 | 16.5 | 2392 | 2448 |

**Ganador:** ML (-36% vs inicial)

---

## Resultados: Tiempo de Ejecución

| Algoritmo | Media (s) | Std | Min | Max |
|-----------|-----------|-----|-----|-----|
| **ML** | **15.9** | 0.3 | 15.5 | 16.5 |
| Greedy+HC | 29.5 | 0.6 | 28.7 | 30.4 |
| Genético | 74.1 | 1.2 | 72.5 | 76.1 |

**Ganador:** ML (más rápido)

---

## Comparación Global

| Métrica | Greedy+HC | ML | Genético | Mejor |
|---------|-----------|-----|----------|-------|
| Movimientos | **314** ↓12% | 366 ↑2% | 379 ↑6% | Greedy |
| Cambios Piso | **206** ↓28% | 223 ↓22% | 286 ↓0% | Greedy |
| Distancia | 1951 ↓31% | **1821** ↓36% | 2413 ↓15% | ML |
| Tiempo | 30s | **16s** | 74s | ML |

---

## Energía Total

**Función:**
$$
E = 10 \cdot mov + 5 \cdot piso + 1 \cdot dist
$$

| Algoritmo | Energía | Ranking |
|-----------|---------|---------|
| **Greedy+HC** | **5182** | 🥇 1° |
| ML | 5890 | 🥈 2° |
| Genético | 6648 | 🥉 3° |
| Inicial | 7002 | - |

**Mejora Greedy+HC:** -26% vs inicial

---

## Pruebas Estadísticas

**Objetivo:** Validar que las diferencias son significativas

**Pruebas aplicadas:**
1. Shapiro-Wilk (normalidad)
2. Levene (homogeneidad de varianzas)
3. ANOVA de un factor
4. Tukey HSD (post-hoc)
5. Cohen's d (tamaño de efecto)

---

## Normalidad (Shapiro-Wilk)

| Algoritmo | W | p-value | ¿Normal? |
|-----------|---|---------|----------|
| Greedy+HC | 0.982 | 0.891 | ✅ Sí |
| ML | 0.979 | 0.823 | ✅ Sí |
| Genético | 0.975 | 0.687 | ✅ Sí |

**Conclusión:** Todas las distribuciones son normales → Usar ANOVA

---

## ANOVA

**Hipótesis:**
- H₀: μ₁ = μ₂ = μ₃ (medias iguales)
- H₁: Al menos una media diferente

**Resultados:**
- F-statistic: 1847.32
- p-value: < 0.001

**Conclusión:** Rechazar H₀ → **Diferencias significativas** ✅

---

## Post-Hoc: Tukey HSD

| Comparación | Diferencia | p-ajustado | ¿Significativo? |
|-------------|------------|------------|-----------------|
| Greedy vs ML | -51.6 | <0.001 | ✅ Sí |
| Greedy vs Genético | -64.3 | <0.001 | ✅ Sí |
| ML vs Genético | -12.7 | <0.001 | ✅ Sí |

**Conclusión:** Todas las diferencias son reales

---

## Tamaños de Efecto (Cohen's d)

| Comparación | Cohen's d | Interpretación |
|-------------|-----------|----------------|
| Greedy vs ML | **22.4** | 🔥 Muy grande |
| Greedy vs Genético | **28.1** | 🔥 Muy grande |
| ML vs Genético | **5.2** | 🔥 Grande |

**Escala:** pequeño (0.2), mediano (0.5), grande (0.8)

---

## Intervalos de Confianza 95%

| Algoritmo | Media | IC 95% |
|-----------|-------|--------|
| Greedy+HC | 314.2 | [313.4, 315.0] |
| ML | 365.8 | [365.0, 366.6] |
| Genético | 378.5 | [377.4, 379.6] |

**Intervalos NO se traslapan** → Diferencias reales ✅

---

## Post-Procesamiento

**Corrección de violaciones P1:**

**Proceso:**
1. Detectar violaciones (si existen)
2. Intentar corrección simple
3. Resolver conflictos mediante desplazamiento
4. Validar resultado final

**Script:** `corregir_prioridades.py`

---

## Validación del Sistema

**Verificaciones automáticas:**
- ✅ Sin conflictos horarios
- ✅ Capacidad respetada
- ✅ Tipo compatible
- ✅ P1 al 100%
- ✅ Métricas calculadas correctamente

**Implementación:** `utils_restricciones.py`

---

## Arquitectura de Archivos

**Datos de entrada:**
- `01_Horario_Inicial.csv` (680 clases)
- `preferencias_profesores_p1.json` (85 preferencias)
- `salones.json` (21 salones con capacidades)

**Datos de salida:**
- Horarios optimizados (CSV/Excel)
- Comparativas y gráficos
- Logs de ejecución

---

## Implementación

**Arquitectura del sistema:**

```
Horario Inicial
    ↓
pre_asignar_p1.py (P1 garantizado)
    ↓
optimizador_*.py (Greedy/ML/Genético)
    ↓
corregir_prioridades.py (Validación)
    ↓
Horario Optimizado
```

---

## Ejecución

**Opción 1: Automática**
```bash
python3 ejecutar_todos.py
```

**Opción 2: Paso a paso**
```bash
python3 pre_asignar_p1.py
python3 optimizador_greedy.py
python3 corregir_prioridades.py
```

---

## Salidas Generadas

**CSV:**
- `00_Horario_PreAsignado_P1.csv`
- `04_Horario_Optimizado_Greedy.csv`
- `05_Horario_Optimizado_ML.csv`
- `06_Horario_Optimizado_Genetico.csv`

**Excel:**
- Horarios formateados
- Comparativa completa
- Gráficos

---

## Visualizaciones Generadas

**Gráficos comparativos:**
- Movimientos por algoritmo (barras)
- Cambios de piso (barras)
- Distancia total (barras)
- Evolución temporal (líneas)
- Box plots de distribuciones

**Formato:** PNG de alta resolución

---

## Caso de Uso Real

**Escenario:** Semestre Ago-Dic 2024

**Problema inicial:**
- 357 movimientos de profesores
- 287 cambios de piso
- Quejas de profesores por movimientos excesivos

**Solución con Greedy+HC:**
- 314 movimientos (-12%)
- 206 cambios de piso (-28%)
- Satisfacción mejorada

---

## Beneficios Medibles

**Impacto en profesores:**
- Menos tiempo perdido en traslados
- Mejor organización del día
- Reducción de fatiga

**Impacto institucional:**
- Optimización de recursos
- Mejor experiencia docente
- Proceso automatizado y repetible

---

## Conclusiones

### Hallazgos Clave

1. ✅ **Greedy+HC es el mejor** para minimizar movimientos
2. ✅ **ML es el más rápido** (16s vs 30s vs 74s)
3. ✅ **Diferencias estadísticamente significativas** (p<0.001)
4. ✅ **100% cumplimiento P1** en todos los algoritmos

---

## Recomendación

**Para producción: Greedy + Hill Climbing**

**Justificación:**
- Minimiza movimientos (objetivo principal)
- Reduce cambios de piso significativamente
- Tiempo aceptable (~30s)
- Resultados consistentes (std = 2.1)
- Validación estadística rigurosa

---

## Mejoras vs Horario Inicial

| Métrica | Inicial | Greedy+HC | Mejora |
|---------|---------|-----------|--------|
| Movimientos | 357 | 314 | **-12%** ✅ |
| Cambios Piso | 287 | 206 | **-28%** ✅ |
| Distancia | 2847 | 1951 | **-31%** ✅ |
| P1 | - | 100% | **100%** ✅ |

---

## Limitaciones Actuales

**Restricciones suaves (P2, P3):**
- Implementadas parcialmente
- No completamente optimizadas
- Trabajo futuro prioritario

**Escalabilidad:**
- Probado hasta 1000 clases
- >2000 clases requiere optimización adicional

**App web:**
- Estado BETA
- Sin autenticación
- No lista para producción

---

## Lecciones Aprendidas

**Técnicas:**
- Pre-asignación es crucial para P1
- Greedy+HC ofrece mejor balance
- Validación estadística es esencial

**Proceso:**
- Documentación extensa facilita mantenimiento
- Ejemplos didácticos ayudan a comprensión
- Comparación rigurosa justifica decisiones

---

## Trabajo Futuro

**Corto plazo (v2.1.0):**
- Implementar PRIORIDAD 2 y 3 completamente
- Optimizar tiempos de ejecución
- App web mejorada con autenticación
- API REST

---

## Trabajo Futuro (cont.)

**Largo plazo (v3.0.0):**
- Soporte multi-campus
- Optimización de horarios (no solo salones)
- Dashboard interactivo
- Integración con sistema institucional
- Single Sign-On (SSO)

---

## Documentación

**Disponible en GitHub:**
- README.md (486 líneas)
- INSTALACION.md (351 líneas)
- PARAMETROS.md (577 líneas)
- EJECUCION.md (797 líneas)
- RESULTADOS.md (455 líneas)
- PRUEBAS_ESTADISTICAS.md (108 líneas)

**Total:** ~2800 líneas de documentación

---

## Repositorio

**GitHub:**
https://github.com/jjho05/Sistema-Salones-ISC

**Incluye:**
- Código fuente completo
- Ejemplos didácticos
- Documentación técnica
- Presentaciones
- Datos de prueba

---

<!-- _class: lead blue -->
# ¡Gracias!

**¿Preguntas?**

---

## Contacto

**Jesús Olvera**

- **GitHub:** [@jjho05](https://github.com/jjho05)
- **Email:** jjho.reivaj05@gmail.com
- **Institución:** Instituto Tecnológico de Ciudad Madero
- **Programa:** Ingeniería en Sistemas Computacionales

**Repositorio:**
https://github.com/jjho05/Sistema-Salones-ISC

---

<!-- _class: lead blue -->

# "Por mi patria y por mi bien"

**Orgullo Tec Madero**

🎓
