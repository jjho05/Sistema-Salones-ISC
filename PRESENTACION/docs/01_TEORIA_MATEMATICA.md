---
marp: true
theme: default
class: invert
paginate: false
math: mathjax
---

<!-- _class: lead invert -->
# Teoría y Fundamentos Matemáticos

**Modelado Formal del Problema**

---

## 1. Modelado del Problema


---

### 1.1 Definición Formal

El problema de asignación de salones es un **problema de optimización combinatoria** que puede modelarse como:

**Entrada:**
- Conjunto de clases $C = \{c_1, c_2, ..., c_n\}$
- Conjunto de salones $S = \{s_1, s_2, ..., s_m\}$
- Conjunto de restricciones $R$
- Función de costo $f: C \times S \rightarrow \mathbb{R}$

**Salida:**
- Asignación $A: C \rightarrow S$ que minimiza $f$ sujeto a $R$


---

### 1.2 Clasificación del Problema

Este problema pertenece a la familia de **problemas NP-difíciles**, específicamente:

- **Tipo:** Problema de asignación con restricciones (Constraint Satisfaction Problem - CSP)
- **Complejidad:** NP-completo
- **Espacio de búsqueda:** $O(m^n)$ donde $m$ = salones, $n$ = clases
- **Ejemplo:** Para 680 clases y 21 salones: $21^{680} \approx 10^{900}$ combinaciones


---

### 1.3 Restricciones del Sistema

#### Restricciones Duras (Hard Constraints)

1. **Unicidad temporal:** Una clase solo puede estar en un salón a la vez
   $$\forall c_i, c_j \in C: (dia_i = dia_j \land hora_i = hora_j) \Rightarrow A(c_i) \neq A(c_j)$$

2. **Capacidad:** El salón debe tener capacidad suficiente
   $$\forall c \in C: capacidad(A(c)) \geq estudiantes(c)$$

3. **Tipo de salón:** Debe coincidir con el tipo de clase
   $$\forall c \in C: tipo(A(c)) = tipo\_requerido(c)$$

4. **Preferencias prioritarias (P1):** Cumplimiento obligatorio al 100%
   $$\forall c \in P1: A(c) = salon\_preferido(c)$$

#### Restricciones Suaves (Soft Constraints)

1. **Consistencia de grupo (P2):** Minimizar cambios de salón por grupo
   $$minimize \sum_{g \in Grupos} |salones\_distintos(g)|$$

2. **Primer semestre (P3):** Asignar grupos 15xx a salones específicos
   $$maximize \sum_{c \in Grupos15xx} \mathbb{1}[A(c) = salon\_asignado]$$


---

## 2. Función Objetivo


---

### 2.1 Formulación General

La función objetivo combina múltiples métricas con pesos:

$$
E(A) = w_1 \cdot movimientos(A) + w_2 \cdot cambios\_piso(A) + w_3 \cdot distancia(A) + \sum_{i} w_i \cdot penalizacion_i(A)
$$

Donde:
- $E(A)$: Energía/costo total de la asignación $A$
- $w_i$: Pesos de cada componente
- Objetivo: $minimize\ E(A)$
---
### 2.2 Componentes de la Función

#### Movimientos de Profesores

$$
movimientos(A) = \sum_{p \in Profesores} \left| \{A(c) : c \in clases(p)\} \right| - 1
$$

**Interpretación:** Número de veces que cada profesor cambia de salón

#### Cambios de Piso

$$
cambios\_piso(A) = \sum_{p \in Profesores} \sum_{i=1}^{|clases(p)|-1} \mathbb{1}[piso(A(c_i)) \neq piso(A(c_{i+1}))]
$$

**Interpretación:** Número de veces que cada profesor sube o baja de piso

---
#### Distancia Total

$$
distancia(A) = \sum_{p \in Profesores} \sum_{i=1}^{|clases(p)|-1} d(A(c_i), A(c_{i+1}))
$$

Donde $d(s_1, s_2)$ es la distancia entre salones:

$$
d(s_1, s_2) = \begin{cases}
0 & \text{si } s_1 = s_2 \\
1 & \text{si mismo piso, diferente salón} \\
10 & \text{si diferente piso}
\end{cases}
$$
---
### 2.3 Penalizaciones

#### Salones Inválidos

$$
penalizacion\_invalidos(A) = 1000 \times \sum_{c \in C} \mathbb{1}[A(c) \in S_{invalidos}]
$$

#### Conflictos de Horario

$$
penalizacion\_conflictos(A) = 500 \times |\{(c_i, c_j) : conflicto(c_i, c_j, A)\}|
$$

#### Tipo Incorrecto

$$
penalizacion\_tipo(A) = 300 \times \sum_{c \in C} \mathbb{1}[tipo(A(c)) \neq tipo\_requerido(c)]
$$

#### Preferencias (P2 y P3)

$$
penalizacion\_preferencias(A) = \sum_{c \in P2 \cup P3} w_{prioridad(c)} \times \mathbb{1}[A(c) \neq salon\_preferido(c)]
$$


---

## 3. Teoremas y Propiedades


---

### Teorema 1: Optimalidad Local vs Global

**Enunciado:** En el problema de asignación de salones, un óptimo local no garantiza ser óptimo global.

**Demostración:** 
- El espacio de búsqueda es no-convexo
- Existen múltiples mínimos locales
- Un intercambio de dos clases puede mejorar localmente pero empeorar globalmente

**Implicación:** Se requieren algoritmos que escapen de óptimos locales (e.g., algoritmos genéticos, simulated annealing)

---

### Teorema 2: Complejidad Computacional

**Enunciado:** El problema de asignación de salones con restricciones es NP-completo.

**Reducción:** Desde el problema de coloración de grafos:
- Vértices = Clases
- Aristas = Conflictos temporales
- Colores = Salones
- Restricciones adicionales = Preferencias y capacidades

---
### Teorema 3: Garantía de Factibilidad

**Enunciado:** Si existe al menos una asignación válida que satisface todas las restricciones duras, el algoritmo de pre-asignación garantiza encontrar una solución factible.

**Demostración:**
1. Pre-asignación fuerza P1 (restricción dura)
2. Algoritmo de resolución de conflictos desplaza clases no-prioritarias
3. Si hay suficientes salones disponibles, siempre existe una asignación válida


---

## 4. Análisis de Complejidad


---

### 4.1 Complejidad Temporal

| Algoritmo | Mejor Caso | Caso Promedio | Peor Caso |
|-----------|------------|---------------|-----------|
| Greedy | $O(n \log n)$ | $O(n^2)$ | $O(n^2)$ |
| Hill Climbing | $O(k \cdot n)$ | $O(k \cdot n^2)$ | $O(k \cdot n^2)$ |
| ML (entrenamiento) | $O(n \cdot m \cdot d)$ | $O(n \cdot m \cdot d)$ | $O(n \cdot m \cdot d)$ |
| ML (inferencia) | $O(n \cdot d)$ | $O(n \cdot d)$ | $O(n \cdot d)$ |
| Genético | $O(g \cdot p \cdot n)$ | $O(g \cdot p \cdot n)$ | $O(g \cdot p \cdot n^2)$ |
---
Donde:
- $n$ = número de clases
- $m$ = número de salones
- $k$ = iteraciones de Hill Climbing
- $d$ = profundidad de árboles (ML)
- $g$ = generaciones (Genético)
- $p$ = tamaño de población (Genético)

---

### 4.2 Complejidad Espacial

| Algoritmo | Espacio |
|-----------|---------|
| Greedy | $O(n + m)$ |
| Hill Climbing | $O(n)$ |
| ML | $O(n \cdot d + m)$ |
| Genético | $O(p \cdot n)$ |


---

## 5. Convergencia y Garantías


---

### 5.1 Greedy + Hill Climbing

**Garantía:** Converge a un óptimo local en tiempo finito

**Condición de parada:**
$$
\forall vecino \in N(A_{actual}): E(vecino) \geq E(A_{actual})
$$
---
### 5.2 Algoritmo Genético

**Teorema de Convergencia:** Con probabilidad 1, el algoritmo genético con elitismo converge al óptimo global cuando $t \rightarrow \infty$

**Condiciones:**
- Mutación con probabilidad $p_m > 0$
- Elitismo (preservar mejores individuos)
- Población suficientemente grande

---

### 5.3 Machine Learning

**Garantía:** Minimiza el error de predicción en el conjunto de entrenamiento

**Error esperado:**
$$
E_{error} = \mathbb{E}[(y - \hat{y})^2]
$$

Donde $y$ es la asignación óptima y $\hat{y}$ es la predicción


---

## 6. Heurísticas y Técnicas


---

### 6.1 Heurística de Construcción Voraz

**Criterio de selección:** Para cada clase $c$, elegir salón $s$ que minimiza:

$$
score(c, s) = \alpha \cdot distancia(s, ultimo\_salon(profesor(c))) + \beta \cdot ocupacion(s) + \gamma \cdot penalizacion(s, c)
$$


---

### 6.2 Operadores Genéticos

**Cruce (Crossover):** Punto único
$$
hijo_1[i] = \begin{cases}
padre_1[i] & \text{si } i < punto\_cruce \\
padre_2[i] & \text{si } i \geq punto\_cruce
\end{cases}
$$

**Mutación:** Intercambio aleatorio
$$
P(mutar(c)) = p_m \cdot (1 + \frac{generacion}{max\_generaciones})
$$
---

### 6.3 Búsqueda Local (Hill Climbing)

**Vecindario:** Intercambios de clases del mismo tipo

$$
N(A) = \{A' : \exists c_i, c_j \in C, tipo(c_i) = tipo(c_j), A'(c_i) = A(c_j), A'(c_j) = A(c_i)\}
$$

**Criterio de aceptación:** Descenso más pronunciado (steepest descent)

$$
A_{nuevo} = \arg\min_{A' \in N(A)} E(A')
$$


---

## Referencias

1. Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*
2. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*
3. Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*
4. Mitchell, T. M. (1997). *Machine Learning*
