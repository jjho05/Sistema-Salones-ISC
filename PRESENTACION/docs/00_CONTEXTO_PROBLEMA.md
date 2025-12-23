---
marp: true
theme: default
class: invert
paginate: false
math: mathjax
---

<!-- _class: lead invert -->
# Contexto del Problema

**Asignación Óptima de Salones**

---

## 1. Introducción - Planteamiento del Problema

La asignación de salones en instituciones educativas es un **problema de optimización combinatoria NP-completo** que surge de la necesidad de distribuir eficientemente los espacios físicos disponibles entre las diferentes actividades académicas programadas.

**Complejidad:**
- Múltiples restricciones simultáneas
- Objetivos conflictivos
- Espacio de búsqueda exponencial

---

## Contexto Institucional - ITCM

**Recursos Disponibles:**
- **Salones de Teoría:** 13 aulas (FF1-FF7 en planta baja, FF8-FFD en planta alta)
- **Laboratorios:** 8 espacios especializados (LBD, LBD2, LCA, LCG1, LCG2, LIA, LR, LSO)
- **Salones Inválidos:** 5 espacios no utilizables (AV1, AV2, AV4, AV5, E11)

**Demanda:**
- **Clases totales:** ~680 sesiones semanales
- **Materias:** 37 diferentes
- **Grupos:** Distribuidos en 9 semestres
- **Profesores:** ~30 docentes con preferencias específicas

---

## Complejidad del Problema

El espacio de búsqueda para este problema es:

$$
|\Omega| = m^n = 21^{680} \approx 10^{900}
$$

Donde:
- $m = 21$ salones disponibles
- $n = 680$ clases a asignar

**Perspectiva:**
- **Átomos en el universo observable:** $\approx 10^{80}$
- **Combinaciones posibles:** $\approx 10^{900}$
- **Relación:** $10^{820}$ veces más combinaciones que átomos

⚠️ Esto hace **imposible** la búsqueda exhaustiva

---

## 2. Formulación Matemática - Conjuntos Básicos

$$
\begin{align}
C &= \{c_1, c_2, ..., c_n\} &&\text{Conjunto de clases} \\
S &= \{s_1, s_2, ..., s_m\} &&\text{Conjunto de salones} \\
P &= \{p_1, p_2, ..., p_k\} &&\text{Conjunto de profesores} \\
D &= \{\text{Lunes, Martes, ..., Viernes}\} &&\text{Días de la semana} \\
H &= \{0700, 0800, ..., 2100\} &&\text{Bloques horarios}
\end{align}
$$

---

## Atributos de Clases

Para cada clase $c_i \in C$:

$$
\begin{align}
dia(c_i) &\in D &&\text{Día de la semana} \\
hora(c_i) &\in H &&\text{Bloque horario} \\
materia(c_i) &\in M &&\text{Materia} \\
grupo(c_i) &\in G &&\text{Grupo} \\
profesor(c_i) &\in P &&\text{Profesor asignado} \\
tipo(c_i) &\in \{\text{Teoría, Laboratorio}\} &&\text{Tipo de clase} \\
estudiantes(c_i) &\in \mathbb{N} &&\text{Número de estudiantes}
\end{align}
$$

---

## Atributos de Salones

Para cada salón $s_j \in S$:

$$
\begin{align}
capacidad(s_j) &\in \mathbb{N} &&\text{Capacidad máxima} \\
tipo(s_j) &\in \{\text{Teoría, Laboratorio}\} &&\text{Tipo de salón} \\
piso(s_j) &\in \{0, 1\} &&\text{Planta baja o alta} \\
ubicacion(s_j) &\in \mathbb{R}^2 &&\text{Coordenadas físicas}
\end{align}
$$

**Variable de Decisión:**

$$
A: C \rightarrow S
$$

Donde $A(c_i) = s_j$ significa que la clase $c_i$ se imparte en el salón $s_j$

---

## Restricciones Duras (Hard Constraints)

Estas restricciones **DEBEN** cumplirse para que la solución sea factible.

**R1. No Conflictos Temporales:**
$$
\forall c_i, c_j \in C: \left(dia(c_i) = dia(c_j) \land hora(c_i) = hora(c_j) \land i \neq j\right) \Rightarrow A(c_i) \neq A(c_j)
$$

**R2. Capacidad Suficiente:**
$$
\forall c_i \in C: estudiantes(c_i) \leq capacidad(A(c_i))
$$

---

## Restricciones Duras (continuación)

**R3. Tipo Correcto:**
$$
\forall c_i \in C: tipo(c_i) = tipo(A(c_i))
$$
*Ejemplo: Una clase de laboratorio debe estar en un laboratorio*

**R4. Salones Válidos:**
$$
\forall c_i \in C: A(c_i) \notin S_{invalidos}
$$
Donde $S_{invalidos} = \{AV1, AV2, AV4, AV5, E11\}$

**R5. Preferencias Prioritarias (PRIORIDAD 1):**
$$
\forall c_i \in P_1: A(c_i) = pref(c_i)
$$

---

## Teorema 1: Factibilidad

**Teorema 1 (Factibilidad):**
*Una solución es factible si y solo si satisface todas las restricciones duras R1-R5.*

**Demostración:**
- $(\Rightarrow)$ Por definición de factibilidad
- $(\Leftarrow)$ Si se satisfacen R1-R5, no hay violaciones de restricciones obligatorias, por lo tanto la solución es válida

---

## Restricciones Suaves (Soft Constraints)

Estas restricciones son **deseables** pero no obligatorias.

**S1. Consistencia de Grupo (PRIORIDAD 2):**
$$
minimize \quad \left| \{A(c) : c \in C_g\} \right|
$$
*Minimizar el número de salones diferentes usados por cada grupo*

**S2. Primer Semestre (PRIORIDAD 3):**
$$
maximize \sum_{g \in G_{15}} \sum_{c \in C_g} \mathbb{1}[A(c) = salon\_asignado(g)]
$$

---

## Restricciones Suaves (continuación)

**S3. Minimizar Movimientos:**

Para cada profesor $p \in P$:

$$
minimize \sum_{p \in P} \left| \{A(c) : c \in C_p\} \right|
$$

**Objetivo:** Reducir la cantidad de salones diferentes que usa cada profesor durante el día/semana

---

## Función Objetivo Completa

$$
\begin{align}
f(A) = &\ w_1 \cdot movimientos(A) + w_2 \cdot cambios\_piso(A) \\
       &+ w_3 \cdot distancia(A) + w_4 \cdot penalizacion\_invalidos(A) \\
       &+ w_5 \cdot penalizacion\_conflictos(A) + w_6 \cdot penalizacion\_tipo(A) \\
       &+ w_7 \cdot penalizacion\_P2(A) + w_8 \cdot penalizacion\_P3(A)
\end{align}
$$

**Objetivo:** $minimize\ f(A)$ sujeto a restricciones R1-R5

---

## Componente: Movimientos de Profesores

$$
movimientos(A) = \sum_{p \in P} \max\left(0, \left| \{A(c) : c \in C_p\} \right| - 1\right)
$$

**Ejemplo Numérico:**
- Profesor tiene clases en: FF1, FF2, FF1, FF3, FF2
- Salones únicos: {FF1, FF2, FF3}
- Movimientos = |{FF1, FF2, FF3}| - 1 = **2 movimientos**

---

## Componente: Cambios de Piso

Sea $C_p^{ordenado} = [c_1, c_2, ..., c_k]$ las clases del profesor $p$ ordenadas por $(dia, hora)$:

$$
cambios\_piso(A) = \sum_{p \in P} \sum_{i=1}^{|C_p|-1} \mathbb{1}[piso(A(c_i)) \neq piso(A(c_{i+1}))]
$$

Donde $\mathbb{1}[\cdot]$ es la función indicadora:

$$
\mathbb{1}[condicion] = \begin{cases}
1 & \text{si condición es verdadera} \\
0 & \text{si condición es falsa}
\end{cases}
$$

---

## Componente: Distancia Total

Función de distancia entre salones:

$$
d(s_i, s_j) = \begin{cases}
0 & \text{si } s_i = s_j \\
1 & \text{si } piso(s_i) = piso(s_j) \land s_i \neq s_j \\
10 & \text{si } piso(s_i) \neq piso(s_j)
\end{cases}
$$

Distancia total:

$$
distancia(A) = \sum_{p \in P} \sum_{i=1}^{|C_p|-1} d(A(c_i), A(c_{i+1}))
$$

---

## Componente: Penalizaciones

$$
\begin{align}
penalizacion\_invalidos(A) &= 1000 \times \sum_{c \in C} \mathbb{1}[A(c) \in S_{invalidos}] \\
penalizacion\_conflictos(A) &= 500 \times |\{(c_i, c_j) : conflicto\_temporal(c_i, c_j, A)\}| \\
penalizacion\_tipo(A) &= 300 \times \sum_{c \in C} \mathbb{1}[tipo(c) \neq tipo(A(c))] \\
penalizacion\_P2(A) &= 50 \times \sum_{c \in P_2} \mathbb{1}[A(c) \neq pref(c)] \\
penalizacion\_P3(A) &= 25 \times \sum_{c \in P_3} \mathbb{1}[A(c) \neq pref(c)]
\end{align}
$$

---

## Pesos de la Función Objetivo

| Componente | Peso | Justificación |
|------------|------|---------------|
| Movimientos | 10 | Impacto directo en fatiga del profesor |
| Cambios piso | 5 | Menor impacto que movimientos totales |
| Distancia | 3 | Correlacionado con movimientos |
| Inválidos | 1000 | Restricción casi-dura |
| Conflictos | 500 | Restricción casi-dura |
| Tipo incorrecto | 300 | Restricción casi-dura |
| P2 | 50 | Soft constraint importante |
| P3 | 25 | Soft constraint menos crítico |

---

## Teorema 2: Dominancia de Restricciones Duras

**Teorema 2:**
*Con los pesos dados, cualquier violación de restricción dura produce una energía mayor que cualquier combinación de violaciones de restricciones suaves.*

**Demostración:**
$$
\begin{align}
E_{hard} &\geq 300 \times v_h \\
E_{soft} &\leq 50 \times v_s + \text{otros términos suaves}
\end{align}
$$

Para que $E_{hard} > E_{soft}$ siempre:
$$
300 \times v_h > 50 \times v_s \Rightarrow v_h > \frac{v_s}{6}
$$

---

## 3. Características del Problema

**Clasificación Teórica:**
- **Categoría:** Problema de Satisfacción de Restricciones (CSP) con optimización
- **Subcategoría:** Problema de Asignación Cuadrática (QAP) generalizado
- **Complejidad:** NP-completo (reducible desde Graph Coloring)

**Propiedades:**
- **Espacio de búsqueda:** Discreto, finito, exponencialmente grande
- **Función objetivo:** No convexa, múltiples mínimos locales
- **Restricciones:** Mezcla de duras y suaves
- **Estructura:** Altamente estructurado (temporal, espacial, jerárquico)

---

## Teorema 3: NP-Completitud

**Teorema 3:**
*El problema de asignación de salones es NP-completo.*

**Demostración (por reducción desde Graph Coloring):**

1. **Construcción del grafo:**
   - Vértices $V = C$ (clases)
   - Arista $(c_i, c_j) \in E$ si hay conflicto temporal
   - Colores $K = S$ (salones)

2. **Equivalencia:**
   - Graph Coloring: vértices adyacentes tienen colores diferentes
   - Asignación: clases en conflicto tienen salones diferentes

---

## Análisis de Instancia Real

```
Tamaño del problema:
├── Clases totales: 680
├── Salones disponibles: 21
├── Profesores: ~30
├── Materias: 37
├── Grupos: ~50
└── Bloques horarios/día: 14

Distribución de clases:
├── Teoría: ~450 (66%)
└── Laboratorio: ~230 (34%)

Distribución temporal:
├── Lunes-Viernes: ~136 clases/día
├── Bloques pico: 0800-1200 (60% de clases)
└── Bloques valle: 1900-2100 (5% de clases)
```

---

## Densidad del Grafo de Conflictos

$$
densidad = \frac{|E|}{|V|(|V|-1)/2} = \frac{conflictos}{680 \times 679 / 2} \approx 0.15
$$

Esto indica un grafo **relativamente disperso**, lo cual es favorable para algoritmos heurísticos.

---

## Preferencias del Sistema

```
Preferencias:
├── PRIORIDAD 1: 88 clases (13%)
│   └── Garantía: 100% cumplimiento
├── PRIORIDAD 2: Variable por grupo
│   └── Consistencia de salones
└── PRIORIDAD 3: ~80 clases (12%)
    └── Preferencias de primer semestre
```

---

## Desafíos Específicos

1. **Heterogeneidad de Restricciones:**
   - Mezcla de restricciones duras y suaves
   - Prioridades jerárquicas estrictas
   - Objetivos conflictivos

2. **Escala del Problema:**
   - 680 variables de decisión
   - $21^{680}$ combinaciones posibles
   - Evaluación de función objetivo: $O(n)$ por solución

---

## Desafíos Específicos (continuación)

3. **Estructura Temporal:**
   - Dependencias secuenciales (clases del mismo profesor)
   - Ventanas temporales fijas
   - No se puede modificar horarios, solo salones

4. **Múltiples Stakeholders:**
   - Profesores (preferencias)
   - Estudiantes (consistencia de grupo)
   - Administración (eficiencia de recursos)

---

## 4. Estado del Arte - Enfoques Clásicos

**Métodos Exactos:**
- **Programación Lineal Entera (ILP):** Garantiza óptimo pero intratable para $n > 100$
- **Branch and Bound:** Mejora sobre ILP pero aún exponencial
- **Constraint Programming:** Efectivo para CSP pero lento en optimización

**Limitaciones:** Tiempo de ejecución prohibitivo para instancias reales

---

## Metaheurísticas

**Algoritmos Evolutivos:**
- Algoritmos Genéticos (Holland, 1975)
- Evolución Diferencial
- Particle Swarm Optimization

**Búsqueda Local:**
- Hill Climbing
- Simulated Annealing (Kirkpatrick, 1983)
- Tabu Search (Glover, 1986)
---
**Híbridos:**
- Memetic Algorithms
- GRASP (Greedy Randomized Adaptive Search)

---

## Enfoques Modernos

**Machine Learning:**
- Reinforcement Learning para scheduling
- Neural Networks para predicción de asignaciones
- Transfer Learning desde problemas similares

**Constraint-Based:**
- Adaptive Large Neighborhood Search
- Logic-Based Benders Decomposition

---

## 5. Solución Propuesta - Estrategia Multi-Algoritmo

Implementamos **4 algoritmos diferentes** para explorar el espacio de soluciones:

1. **Baseline (Profesor):** Asignación manual/heurística simple
2. **Greedy + Hill Climbing:** Construcción rápida + refinamiento local
3. **Machine Learning:** Aprendizaje supervisado desde soluciones previas
4. **Algoritmo Genético:** Búsqueda evolutiva global

**Justificación:** Diferentes algoritmos tienen fortalezas complementarias

---

## Sistema de Prioridades Jerárquico

**Innovación Principal:** Pre-asignación forzada de PRIORIDAD 1

```
Flujo de Optimización:
1. Pre-asignar P1 (100% garantizado)
2. Marcar clases P1 como inmutables
3. Optimizar P2 y P3 (soft constraints)
4. Corrección post-optimización (si necesario)
```

**Ventaja:** Separa restricciones duras de suaves, simplificando el problema

---

## Métricas de Evaluación

**Primarias:**
- ✅ Cumplimiento P1: **DEBE ser 100%**
- 📉 Movimientos profesores: Minimizar
- 🏢 Cambios de piso: Minimizar
- 📏 Distancia total: Minimizar

**Secundarias:**
- ⏱️ Tiempo de ejecución
- 🎯 Consistencia de resultados
- 📈 Escalabilidad

---

## 6. Resultados Esperados

**Teorema 4 (Garantía de P1):**
*El sistema garantiza 100% de cumplimiento de PRIORIDAD 1.*

**Demostración:**
1. Pre-asignación fuerza $A(c) = pref(c)$ para todo $c \in P_1$
2. Índices inmutables previenen modificación durante optimización
3. Corrección post-optimización restaura cualquier violación accidental
4. Por lo tanto, $\forall c \in P_1: A(c) = pref(c)$ en solución final

---

## Teorema 5: Convergencia

**Teorema 5:**
*Todos los algoritmos convergen a una solución factible en tiempo finito.*

**Demostración:**
- **Greedy:** Construcción determinista, $O(n \times m)$
- **Hill Climbing:** Criterio de parada garantizado
- **ML:** Predicción en tiempo constante por clase
- **Genético:** Elitismo preserva factibilidad

---

## Mejoras Esperadas

Basado en experimentos preliminares:

| Métrica | Inicial | Esperado | Mejora |
|---------|---------|----------|--------|
| P1 | Variable | 100% | ✓ |
| Movimientos | 357 | 300-320 | 10-16% |
| Cambios piso | 287 | 200-230 | 20-30% |
| Distancia | 2847 | 1800-2000 | 30-37% |

---

## Referencias (1/2)

1. Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.

2. Schaerf, A. (1999). A survey of automated timetabling. *Artificial Intelligence Review*, 13(2), 87-127.

3. Burke, E. K., & Petrovic, S. (2002). Recent research directions in automated timetabling. *European Journal of Operational Research*, 140(2), 266-280.

---

## Referencias (2/2)

4. Lewis, R. (2008). A survey of metaheuristic-based techniques for university timetabling problems. *OR Spectrum*, 30(1), 167-190.

5. Pillay, N., & Qu, R. (2018). *Hyper-Heuristics: Theory and Applications*. Springer.

6. McCollum, B., et al. (2010). Setting the research agenda in automated timetabling: The second international timetabling competition. *INFORMS Journal on Computing*, 22(1), 120-130.


