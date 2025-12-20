# Método de Optimización: Machine Learning

## 📚 Índice

1. [Introducción](#introducción)
2. [Fundamentos Teóricos](#fundamentos-teóricos)
3. [Arquitectura del Modelo](#arquitectura-del-modelo)
4. [Ingeniería de Características](#ingeniería-de-características)
5. [Función Objetivo y Métricas](#función-objetivo-y-métricas)
6. [Restricciones](#restricciones)
7. [Algoritmo de Optimización](#algoritmo-de-optimización)
8. [Fórmulas Matemáticas](#fórmulas-matemáticas)
9. [Implementación](#implementación)
10. [Comparación con Otros Métodos](#comparación-con-otros-métodos)

---

## Introducción

El método de **Machine Learning (ML)** para optimización de salones utiliza técnicas de aprendizaje supervisado y no supervisado para aprender patrones óptimos de asignación a partir de datos históricos y la optimización manual del profesor.

### Ventajas del Enfoque ML

- ✅ **Aprende de experiencia**: Captura el conocimiento implícito del profesor
- ✅ **Adaptativo**: Mejora con más datos
- ✅ **Escalable**: Maneja restricciones complejas mediante features
- ✅ **Rápido**: Una vez entrenado, genera soluciones en segundos
- ✅ **Flexible**: Fácil agregar nuevas restricciones

### Desventajas

- ❌ **Requiere datos de entrenamiento**: Necesita ejemplos de buenas asignaciones
- ❌ **No garantiza óptimo global**: Es una aproximación heurística
- ❌ **Caja negra parcial**: Menos interpretable que modelos matemáticos

---

## Fundamentos Teóricos

### 1. Aprendizaje Supervisado

El problema se modela como **clasificación multi-clase** donde:

- **Entrada (X)**: Características de una asignación (grupo, materia, día, hora, profesor)
- **Salida (y)**: Salón asignado
- **Objetivo**: Aprender la función $f: X \rightarrow y$ que minimiza el error

**Función de Aprendizaje:**

$$
\hat{f} = \arg\min_{f \in \mathcal{F}} \sum_{i=1}^{n} L(y_i, f(x_i)) + \lambda R(f)
$$

Donde:
- $L$ = función de pérdida (cross-entropy)
- $R(f)$ = regularización
- $\lambda$ = parámetro de regularización
- $n$ = número de ejemplos de entrenamiento

### 2. Aprendizaje por Refuerzo (Componente)

Para optimización iterativa, usamos **Q-Learning** modificado:

$$
Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]
$$

Donde:
- $s$ = estado actual (asignaciones parciales)
- $a$ = acción (asignar salón a grupo)
- $r$ = recompensa (negativa si viola restricciones)
- $\alpha$ = tasa de aprendizaje
- $\gamma$ = factor de descuento

### 3. Clustering para Patrones

Usamos **K-Means** para identificar patrones de asignación:

$$
\arg\min_{C} \sum_{i=1}^{k} \sum_{x \in C_i} ||x - \mu_i||^2
$$

Donde:
- $C_i$ = cluster $i$
- $\mu_i$ = centroide del cluster $i$
- $k$ = número de clusters

---

## Arquitectura del Modelo

### Modelo Híbrido: Ensemble de 3 Componentes

```
┌─────────────────────────────────────────────────────┐
│           ENTRADA: Asignación a Optimizar           │
│  (Grupo, Materia, Día, Hora, Profesor, Contexto)   │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌───────────────┐
│  Clasificador │    │   Regressor   │
│  Multi-Clase  │    │  de Calidad   │
│  (Random      │    │  (Gradient    │
│   Forest)     │    │   Boosting)   │
└───────┬───────┘    └───────┬───────┘
        │                    │
        │    ┌───────────────┴───────────────┐
        │    │                               │
        ▼    ▼                               ▼
    ┌────────────┐                  ┌────────────────┐
    │  Votación  │                  │  Optimizador   │
    │  Ponderada │                  │  de           │
    │            │◄─────────────────┤  Restricciones │
    └─────┬──────┘                  └────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  SALIDA: Salón Óptimo Asignado      │
│  + Score de Confianza               │
└─────────────────────────────────────┘
```

### Componente 1: Clasificador Random Forest

**Propósito**: Predecir el salón más probable

**Fórmula de Predicción:**

$$
\hat{y} = \text{mode}\left(\{h_1(x), h_2(x), ..., h_T(x)\}\right)
$$

Donde:
- $h_t$ = árbol de decisión $t$
- $T$ = número total de árboles
- mode = moda (valor más frecuente)

**Ventajas**:
- Robusto a overfitting
- Maneja features categóricas y numéricas
- Proporciona importancia de features

### Componente 2: Gradient Boosting Regressor

**Propósito**: Predecir score de calidad de asignación

**Fórmula Iterativa:**

$$
F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)
$$

Donde:
- $F_m$ = modelo en iteración $m$
- $\nu$ = learning rate
- $h_m$ = árbol que ajusta residuos

**Score de Calidad:**

$$
\text{Score}(x, y) = -\left(w_1 \cdot \text{Movimientos} + w_2 \cdot \text{Inválidos} + w_3 \cdot \text{Conflictos}\right)
$$

### Componente 3: Optimizador de Restricciones

**Propósito**: Ajustar predicciones para satisfacer restricciones hard

**Algoritmo de Ajuste:**

```python
def ajustar_restricciones(asignacion_predicha, restricciones):
    if viola_restriccion_hard(asignacion_predicha):
        candidatos = generar_candidatos_validos(asignacion_predicha)
        return max(candidatos, key=lambda c: score_modelo(c))
    return asignacion_predicha
```

---

## Ingeniería de Características

### Features de Entrada (X)

#### 1. Features del Grupo

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `grupo_codigo` | Categórica | Código del grupo | - |
| `es_primer_semestre` | Binaria | ¿Es 1er semestre? | $\mathbb{1}[\text{código}[0] = '1']$ |
| `num_estudiantes` | Numérica | Tamaño del grupo | - |
| `semestre` | Ordinal | Semestre (1-9) | $\text{int}(\text{código}[0])$ |

#### 2. Features de la Materia

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `materia_nombre` | Categórica | Nombre de materia | - |
| `horas_teoria` | Numérica | Horas teóricas | - |
| `horas_practica` | Numérica | Horas prácticas | - |
| `requiere_lab` | Binaria | ¿Necesita lab? | $\mathbb{1}[\text{horas\_practica} > 0]$ |
| `tipo_clase` | Categórica | Teoría/Lab/Mixta | - |

#### 3. Features Temporales

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `dia_semana` | Categórica | Lun-Vie | - |
| `bloque_horario` | Categórica | HHMM | - |
| `hora_inicio` | Numérica | Hora (7-19) | $\text{int}(\text{bloque}[:2])$ |
| `es_hora_pico` | Binaria | ¿Hora pico? | $\mathbb{1}[10 \leq \text{hora} \leq 14]$ |

#### 4. Features del Profesor

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `profesor_id` | Categórica | ID del profesor | - |
| `tiene_movilidad_reducida` | Binaria | ¿Movilidad limitada? | - |
| `num_materias` | Numérica | Materias que imparte | - |
| `preferencia_piso` | Categórica | Baja/Alta/Sin pref | - |

#### 5. Features Contextuales

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `salon_anterior` | Categórica | Salón en hora anterior | - |
| `salon_siguiente` | Categórica | Salón en hora siguiente | - |
| `num_cambios_dia` | Numérica | Cambios de salón en día | - |
| `distancia_anterior` | Numérica | Distancia desde anterior | $d(\text{salon}_t, \text{salon}_{t-1})$ |

#### 6. Features del Salón Candidato

| Feature | Tipo | Descripción | Fórmula |
|---------|------|-------------|---------|
| `salon_codigo` | Categórica | Código del salón | - |
| `tipo_salon` | Categórica | Teoría/Lab/Inválido | - |
| `piso` | Categórica | Baja/Alta/P1/P2 | - |
| `capacidad` | Numérica | Capacidad del salón | - |
| `disponible` | Binaria | ¿Está libre? | - |
| `uso_actual` | Numérica | % de uso en horario | $\frac{\text{horas\_ocupadas}}{\text{horas\_totales}}$ |

### Feature Engineering Avanzado

#### Interacciones de Features

$$
\text{feature\_interaccion} = f_1 \times f_2
$$

Ejemplos:
- `es_primer_semestre × salon_tipo`
- `hora_inicio × dia_semana`
- `profesor_movilidad × salon_piso`

#### Features Agregadas

$$
\text{movimientos\_profesor} = \sum_{t=1}^{T} \mathbb{1}[\text{salon}_t \neq \text{salon}_{t-1}]
$$

$$
\text{cambios\_piso} = \sum_{t=1}^{T} \mathbb{1}[\text{piso}_t \neq \text{piso}_{t-1}]
$$

---

## Función Objetivo y Métricas

### Función de Pérdida Compuesta

$$
\mathcal{L}_{\text{total}} = \alpha \mathcal{L}_{\text{clasificación}} + \beta \mathcal{L}_{\text{restricciones}} + \gamma \mathcal{L}_{\text{optimización}}
$$

#### 1. Pérdida de Clasificación

$$
\mathcal{L}_{\text{clasificación}} = -\frac{1}{N}\sum_{i=1}^{N} \log P(y_i | x_i)
$$

#### 2. Pérdida de Restricciones (Penalización)

$$
\mathcal{L}_{\text{restricciones}} = \sum_{r \in R_{\text{hard}}} w_r \cdot \mathbb{1}[\text{viola}(r)]
$$

Donde:
- $R_{\text{hard}}$ = conjunto de restricciones hard
- $w_r$ = peso de penalización (muy alto, ej: 1000)

#### 3. Pérdida de Optimización (Soft Constraints)

$$
\mathcal{L}_{\text{optimización}} = \sum_{c \in C_{\text{soft}}} w_c \cdot \text{costo}(c)
$$

**Costos específicos:**

$$
\text{costo\_movimientos} = \sum_{p \in P} \sum_{t=1}^{T_p-1} d(\text{salon}_{p,t}, \text{salon}_{p,t+1})
$$

$$
\text{costo\_inválidos} = 1000 \times |\{\text{asignaciones a AV/E11}\}|
$$

$$
\text{costo\_capacidad} = \sum_{i} \max(0, \text{estudiantes}_i - \text{capacidad}_i)
$$

### Métricas de Evaluación

| Métrica | Fórmula | Objetivo |
|---------|---------|----------|
| **Accuracy** | $\frac{\text{correctas}}{total}$ | Maximizar |
| **F1-Score** | $2 \cdot \frac{P \cdot R}{P + R}$ | Maximizar |
| **MAE Movimientos** | $\frac{1}{N}\sum\|\text{pred} - \text{real}\|$ | Minimizar |
| **Violaciones Hard** | $\sum \mathbb{1}[\text{viola}]$ | = 0 |
| **Score Optimización** | $-\mathcal{L}_{\text{optimización}}$ | Maximizar |

---

## Restricciones

### Restricciones Hard (Obligatorias)

#### H1: Grupos de Primer Semestre

$$
\forall g \in G_1, \forall t_1, t_2 \in T_{\text{teoría}}: \text{salon}_{g,t_1} = \text{salon}_{g,t_2}
$$

**Implementación ML**: Feature `es_primer_semestre` con penalización alta

#### H2: Salones Inválidos

$$
\forall i: \text{salon}_i \notin \{\text{AV1, AV2, AV4, AV5, E11}\}
$$

**Implementación ML**: Filtrado post-predicción + penalización $10^6$

#### H3: Capacidad

$$
\forall i: \text{estudiantes}_i \leq \text{capacidad}(\text{salon}_i)
$$

**Implementación ML**: Feature `capacidad_suficiente` + validación

#### H4: Tipo de Salón

$$
\text{Si horas\_practica} > 0 \Rightarrow \text{salon} \in \text{Labs}
$$

**Implementación ML**: Feature `tipo_compatible` + regla de negocio

#### H5: Disponibilidad

$$
\forall i, j: i \neq j \Rightarrow (\text{salon}_i, \text{hora}_i) \neq (\text{salon}_j, \text{hora}_j)
$$

**Implementación ML**: Matriz de disponibilidad + validación

#### H6: Movilidad Reducida (Futuro)

$$
\text{Si profesor\_movilidad} = \text{reducida} \Rightarrow \text{salon} \in \text{Planta Baja} \cup \text{Labs P1}
$$

**Implementación ML**: Feature `compatible_movilidad` + filtrado

### Restricciones Soft (Deseables)

#### S1: Minimizar Movimientos de Profesores

$$
\min \sum_{p \in P} \sum_{t=1}^{T_p-1} \mathbb{1}[\text{salon}_{p,t} \neq \text{salon}_{p,t+1}]
$$

**Peso**: $w_1 = 10$

#### S2: Minimizar Cambios de Piso

$$
\min \sum_{p \in P} \sum_{t=1}^{T_p-1} \mathbb{1}[\text{piso}_{p,t} \neq \text{piso}_{p,t+1}]
$$

**Peso**: $w_2 = 5$

#### S3: Minimizar Distancia Total

$$
\min \sum_{p \in P} \sum_{t=1}^{T_p-1} d(\text{salon}_{p,t}, \text{salon}_{p,t+1})
$$

**Peso**: $w_3 = 3$

#### S4: Balancear Uso de Salones

$$
\min \text{Var}(\{\text{uso}(\text{salon}_s) : s \in S\})
$$

**Peso**: $w_4 = 2$

---

## Algoritmo de Optimización

### Fase 1: Entrenamiento

```python
ALGORITMO: Entrenar_Modelo_ML

ENTRADA:
    - D_inicial: Horario inicial
    - D_optimizado: Horario optimizado por profesor
    - restricciones: Lista de restricciones

SALIDA:
    - modelo_entrenado: Modelo ML listo para predecir

PASOS:
1. Extraer features de D_inicial y D_optimizado
   X_train, y_train = extraer_features(D_inicial, D_optimizado)

2. Agregar features contextuales
   X_train = agregar_contexto(X_train, D_inicial)

3. Entrenar clasificador Random Forest
   clf = RandomForest(n_estimators=100, max_depth=20)
   clf.fit(X_train, y_train)

4. Entrenar regressor de calidad
   reg = GradientBoosting(n_estimators=100, learning_rate=0.1)
   scores = calcular_scores_calidad(D_optimizado)
   reg.fit(X_train, scores)

5. Validar con cross-validation
   cv_score = cross_val_score(clf, X_train, y_train, cv=5)

6. Retornar modelo ensemble
   return Ensemble(clf, reg, restricciones)
```

### Fase 2: Predicción y Optimización

```python
ALGORITMO: Optimizar_Horario_ML

ENTRADA:
    - D_inicial: Horario a optimizar
    - modelo: Modelo entrenado
    - restricciones: Restricciones a satisfacer

SALIDA:
    - D_optimizado: Horario optimizado

PASOS:
1. Inicializar horario vacío
   D_opt = {}

2. Ordenar asignaciones por prioridad
   asignaciones = ordenar_por_prioridad(D_inicial)
   # Prioridad: 1er semestre > labs > teoría

3. Para cada asignación a en asignaciones:
   
   3.1. Extraer features
       x = extraer_features(a, D_opt)
   
   3.2. Predecir top-k salones candidatos
       candidatos = modelo.predict_proba(x).top_k(k=5)
   
   3.3. Filtrar por restricciones hard
       candidatos_validos = [c for c in candidatos 
                            if satisface_hard(c, restricciones)]
   
   3.4. Si no hay candidatos válidos:
       candidatos_validos = buscar_alternativas(a, D_opt)
   
   3.5. Evaluar calidad de cada candidato
       scores = [modelo.score(x, c) for c in candidatos_validos]
   
   3.6. Seleccionar mejor candidato
       mejor = candidatos_validos[argmax(scores)]
   
   3.7. Asignar y actualizar
       D_opt[a] = mejor
       actualizar_contexto(D_opt, a, mejor)

4. Optimización local (hill climbing)
   D_opt = mejorar_local(D_opt, modelo, restricciones)

5. Retornar solución
   return D_opt
```

### Fase 3: Refinamiento Iterativo

```python
ALGORITMO: Refinar_Solución

ENTRADA:
    - D_opt: Solución inicial
    - modelo: Modelo ML
    - max_iter: Iteraciones máximas

SALIDA:
    - D_final: Solución refinada

PASOS:
1. score_actual = evaluar(D_opt)

2. Para i = 1 hasta max_iter:
   
   2.1. Seleccionar asignación aleatoria a
   
   2.2. Generar vecinos (cambiar salón de a)
       vecinos = generar_vecinos(D_opt, a)
   
   2.3. Evaluar vecinos
       scores_vecinos = [evaluar(v) for v in vecinos]
   
   2.4. Si max(scores_vecinos) > score_actual:
       D_opt = vecinos[argmax(scores_vecinos)]
       score_actual = max(scores_vecinos)
   
   2.5. Si no mejora en k iteraciones:
       break

3. return D_opt
```

---

## Fórmulas Matemáticas Detalladas

### 1. Cálculo de Distancia entre Salones

**Matriz de Distancias** (ejemplo simplificado):

$$
D = \begin{bmatrix}
0 & 1 & 2 & 3 & 10 \\
1 & 0 & 1 & 2 & 9 \\
2 & 1 & 0 & 1 & 8 \\
3 & 2 & 1 & 0 & 7 \\
10 & 9 & 8 & 7 & 0
\end{bmatrix}
$$

**Función de Distancia:**

$$
d(s_1, s_2) = \begin{cases}
0 & \text{si } s_1 = s_2 \\
1 & \text{si mismo piso, adyacentes} \\
2 & \text{si mismo piso, no adyacentes} \\
5 & \text{si diferente piso, mismo edificio} \\
10 & \text{si diferente edificio}
\end{cases}
$$

### 2. Score de Calidad de Asignación

$$
Q(a, s) = \sum_{i=1}^{n} w_i \cdot f_i(a, s)
$$

Donde:
- $f_1$ = compatibilidad de tipo (0 o 1)
- $f_2$ = utilización del salón (0-1)
- $f_3$ = distancia normalizada (0-1)
- $f_4$ = preferencia histórica (0-1)

**Normalización:**

$$
f_{\text{norm}} = \frac{f - f_{\min}}{f_{\max} - f_{\min}}
$$

### 3. Probabilidad de Asignación (Softmax)

$$
P(\text{salon}_j | x) = \frac{e^{z_j}}{\sum_{k=1}^{K} e^{z_k}}
$$

Donde:
- $z_j = w_j^T x + b_j$ (score del salón $j$)
- $K$ = número total de salones

### 4. Importancia de Features (Random Forest)

$$
\text{Importancia}(f) = \frac{1}{T} \sum_{t=1}^{T} \sum_{n \in N_t} \Delta i(n, f)
$$

Donde:
- $\Delta i(n, f)$ = reducción de impureza en nodo $n$ por feature $f$
- $N_t$ = nodos del árbol $t$

---

## Implementación

### Tecnologías y Librerías

```python
# Core ML
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# Optimización
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Visualización
import matplotlib.pyplot as plt
import seaborn as sns
```

### Estructura de Clases

```python
class OptimizadorML:
    def __init__(self, restricciones):
        self.clf = RandomForestClassifier(...)
        self.reg = GradientBoostingRegressor(...)
        self.restricciones = restricciones
        self.encoder = LabelEncoder()
        self.scaler = StandardScaler()
    
    def entrenar(self, X, y):
        """Entrena el modelo con datos históricos"""
        pass
    
    def predecir(self, X):
        """Predice salón óptimo para asignación"""
        pass
    
    def optimizar(self, horario_inicial):
        """Optimiza horario completo"""
        pass
    
    def evaluar(self, horario):
        """Evalúa calidad de horario"""
        pass
```

---

## Comparación con Otros Métodos

| Aspecto | Machine Learning | ILP (Matemático) | Genético |
|---------|-----------------|------------------|----------|
| **Garantía de Óptimo** | ❌ No | ✅ Sí (si converge) | ❌ No |
| **Velocidad** | ✅ Rápido (post-entrenamiento) | ❌ Lento | ⚠️ Medio |
| **Escalabilidad** | ✅ Excelente | ❌ Limitada | ✅ Buena |
| **Interpretabilidad** | ⚠️ Media | ✅ Alta | ❌ Baja |
| **Requiere Datos** | ✅ Sí | ❌ No | ❌ No |
| **Manejo Restricciones** | ⚠️ Aproximado | ✅ Exacto | ⚠️ Aproximado |
| **Adaptabilidad** | ✅ Alta | ❌ Baja | ✅ Alta |
| **Complejidad Impl.** | ⚠️ Media | ✅ Baja | ⚠️ Media |

### Cuándo Usar Cada Método

**Machine Learning**:
- ✅ Hay datos históricos de buenas asignaciones
- ✅ Se necesita velocidad en producción
- ✅ Las restricciones son complejas pero flexibles
- ✅ Se espera que el problema evolucione

**ILP (Matemático)**:
- ✅ Se necesita garantía de optimalidad
- ✅ El problema es de tamaño pequeño-mediano
- ✅ Las restricciones son rígidas y bien definidas
- ✅ No hay datos históricos

**Genético**:
- ✅ El espacio de búsqueda es muy grande
- ✅ Se acepta una buena solución (no necesariamente óptima)
- ✅ Las restricciones son difíciles de modelar matemáticamente
- ✅ Se necesita diversidad de soluciones

---

## Resultados Esperados

### Métricas de Éxito

1. **Asignaciones Inválidas**: 0 (vs 51 inicial)
2. **Movimientos de Profesores**: Reducción del 30-50%
3. **Accuracy de Predicción**: > 85%
4. **Tiempo de Ejecución**: < 30 segundos
5. **Satisfacción de Restricciones Hard**: 100%

### Diferencias con Otros Métodos

Los resultados del ML serán **diferentes** porque:

- **Aprende patrones** del profesor (puede replicar decisiones subóptimas)
- **Balancea** múltiples objetivos de forma diferente
- **Prioriza** features según importancia aprendida
- **Puede ser más conservador** (prefiere asignaciones conocidas)

---

## Próximos Pasos

1. ✅ Documentación completa
2. ⏳ Implementar extracción de features
3. ⏳ Entrenar modelo con datos existentes
4. ⏳ Implementar algoritmo de optimización
5. ⏳ Validar con restricciones
6. ⏳ Generar comparativa vs inicial y profesor
7. ⏳ Crear visualizaciones y PDF

---

## Referencias

- Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
- Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine.
- Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning.
