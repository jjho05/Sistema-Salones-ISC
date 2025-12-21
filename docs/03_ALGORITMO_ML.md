# Algoritmo de Machine Learning

## 1. Introducción

### 1.1 Fundamento Teórico

El enfoque de Machine Learning para la asignación de salones se basa en la **hipótesis de aprendizaje supervisado**: si existe un patrón en las asignaciones óptimas previas, un modelo puede aprender a predecir asignaciones de calidad similar sin necesidad de búsqueda exhaustiva.

**Ventaja Principal:** Una vez entrenado, el modelo puede generar soluciones en tiempo casi constante $O(n \cdot d)$ donde $d$ es la profundidad del árbol, comparado con $O(n^2)$ o peor de otros métodos.

### 1.2 Arquitectura del Sistema ML

El sistema utiliza un **ensemble de dos modelos complementarios**:

1. **Random Forest Classifier:** Predice el salón óptimo para cada clase
2. **Gradient Boosting Regressor:** Estima la calidad de cada asignación

```
Entrada: Características de la clase
   ↓
[Random Forest] → Predicción de salón
   ↓
[Gradient Boosting] → Score de calidad
   ↓
Selección del mejor salón válido
   ↓
Salida: Asignación optimizada
```

## 2. Extracción de Características (Feature Engineering)

### 2.1 Vector de Características

Para cada clase $c_i$, construimos un vector de características $\mathbf{x}_i \in \mathbb{R}^d$:

$$
\mathbf{x}_i = [x_1, x_2, ..., x_d]^T
$$

**Categorías de Características:**

#### A. Características Temporales

$$
\begin{align}
x_1 &= dia\_semana(c_i) &&\in \{0, 1, 2, 3, 4\} &&\text{(Lun-Vie)} \\
x_2 &= bloque\_horario(c_i) &&\in \{7, 8, ..., 21\} &&\text{(Hora inicio)} \\
x_3 &= es\_manana(c_i) &&\in \{0, 1\} &&\text{(Antes de 12:00)} \\
x_4 &= es\_tarde(c_i) &&\in \{0, 1\} &&\text{(12:00-18:00)} \\
x_5 &= es\_noche(c_i) &&\in \{0, 1\} &&\text{(Después 18:00)}
\end{align}
$$

#### B. Características de Materia

$$
\begin{align}
x_6 &= materia\_encoded(c_i) &&\in \{0, 1, ..., |M|-1\} &&\text{(Label encoding)} \\
x_7 &= tipo\_clase(c_i) &&\in \{0, 1\} &&\text{(0=Teoría, 1=Lab)} \\
x_8 &= num\_estudiantes(c_i) &&\in \mathbb{N} &&\text{(Tamaño grupo)}
\end{align}
$$

#### C. Características de Profesor

$$
\begin{align}
x_9 &= profesor\_encoded(c_i) &&\in \{0, 1, ..., |P|-1\} \\
x_{10} &= tiene\_preferencia(c_i) &&\in \{0, 1\} \\
x_{11} &= prioridad\_preferencia(c_i) &&\in \{0, 1, 2, 3\}
\end{align}
$$

#### D. Características Contextuales

$$
\begin{align}
x_{12} &= num\_clases\_profesor\_dia(c_i) &&\in \mathbb{N} \\
x_{13} &= posicion\_en\_dia(c_i) &&\in \{1, 2, ..., k\} \\
x_{14} &= salon\_clase\_anterior(c_i) &&\in \{0, 1, ..., |S|-1\} \\
x_{15} &= piso\_clase\_anterior(c_i) &&\in \{0, 1\}
\end{align}
$$

#### E. Características de Grupo

$$
\begin{align}
x_{16} &= semestre(c_i) &&\in \{1, 2, ..., 9\} \\
x_{17} &= es\_primer\_semestre(c_i) &&\in \{0, 1\} \\
x_{18} &= grupo\_encoded(c_i) &&\in \{0, 1, ..., |G|-1\}
\end{align}
$$

**Total de características:** $d \approx 18-25$ (dependiendo de encoding)

### 2.2 Encoding de Variables Categóricas

**Label Encoding:**
Para variables ordinales (materia, profesor, grupo):

$$
encode(categoria) = \{categoria_1 \rightarrow 0, categoria_2 \rightarrow 1, ..., categoria_n \rightarrow n-1\}
$$

**One-Hot Encoding (alternativa):**
Para $k$ categorías, crear $k$ variables binarias:

$$
\mathbf{x}_{one-hot} = [0, 0, ..., 1, ..., 0]^T
$$

Donde el 1 está en la posición correspondiente a la categoría.

**Decisión de Diseño:** Usamos Label Encoding para reducir dimensionalidad, ya que Random Forest maneja bien variables categóricas ordinales.

### 2.3 Normalización

Para características numéricas continuas:

$$
x'_i = \frac{x_i - \mu_i}{\sigma_i}
$$

Donde:
- $\mu_i$ = media de la característica $i$
- $\sigma_i$ = desviación estándar de la característica $i$

**Nota:** Random Forest no requiere normalización estricta, pero mejora la interpretabilidad.

## 3. Modelo 1: Random Forest Classifier

### 3.1 Fundamento Teórico

Un Random Forest es un **ensemble de árboles de decisión** que combina predicciones mediante votación mayoritaria (clasificación) o promedio (regresión).

**Definición Formal:**

Sea $\{h(\mathbf{x}, \Theta_k)\}_{k=1}^K$ un conjunto de $K$ árboles de decisión, donde $\Theta_k$ son parámetros aleatorios (subset de features y datos). El Random Forest predice:

$$
\hat{y} = \text{mode}\{h(\mathbf{x}, \Theta_1), h(\mathbf{x}, \Theta_2), ..., h(\mathbf{x}, \Theta_K)\}
$$

### 3.2 Algoritmo de Entrenamiento

```python
def entrenar_random_forest(X_train, y_train):
    """
    X_train: matriz n × d de características
    y_train: vector n de salones asignados (labels)
    """
    forest = []
    
    for k in range(K):  # K = número de árboles
        # 1. Bootstrap sampling
        indices = sample_with_replacement(n, n)
        X_boot = X_train[indices]
        y_boot = y_train[indices]
        
        # 2. Entrenar árbol con subset aleatorio de features
        tree = DecisionTree(
            max_depth=d_max,
            min_samples_split=s_min,
            max_features=sqrt(d)  # Regla empírica
        )
        tree.fit(X_boot, y_boot)
        forest.append(tree)
    
    return forest
```

### 3.3 Construcción de Árbol de Decisión

**Algoritmo CART (Classification and Regression Trees):**

```
función construir_arbol(X, y, profundidad):
    si profundidad == max_depth o |y| < min_samples:
        retornar hoja con clase mayoritaria
    
    mejor_ganancia = 0
    mejor_split = None
    
    para cada característica f en subset_aleatorio(features):
        para cada valor v en valores_unicos(X[:, f]):
            # Dividir datos
            izq = {(x, y) : x[f] <= v}
            der = {(x, y) : x[f] > v}
            
            # Calcular ganancia de información
            ganancia = calcular_ganancia(y, izq, der)
            
            si ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_split = (f, v)
    
    si mejor_ganancia == 0:
        retornar hoja
    
    # Crear nodo interno
    nodo.feature = mejor_split[0]
    nodo.threshold = mejor_split[1]
    nodo.izquierdo = construir_arbol(izq, profundidad + 1)
    nodo.derecho = construir_arbol(der, profundidad + 1)
    
    retornar nodo
```

### 3.4 Criterio de División: Gini Impurity

Para clasificación, usamos el **índice de Gini**:

$$
Gini(S) = 1 - \sum_{i=1}^{|C|} p_i^2
$$

Donde:
- $S$ = conjunto de muestras en el nodo
- $C$ = conjunto de clases (salones)
- $p_i$ = proporción de muestras de clase $i$ en $S$

**Ganancia de Información:**

$$
Ganancia(S, f, v) = Gini(S) - \left(\frac{|S_{izq}|}{|S|} Gini(S_{izq}) + \frac{|S_{der}|}{|S|} Gini(S_{der})\right)
$$

**Objetivo:** Maximizar la ganancia (minimizar impureza después del split)

### 3.5 Predicción

Para una nueva clase $\mathbf{x}_{new}$:

$$
\hat{y}_{RF} = \arg\max_{s \in S} \sum_{k=1}^{K} \mathbb{1}[h_k(\mathbf{x}_{new}) = s]
$$

**Interpretación:** El salón que recibe más "votos" de los árboles individuales.

### 3.6 Hiperparámetros

```python
RandomForestClassifier(
    n_estimators=100,        # Número de árboles
    max_depth=20,            # Profundidad máxima
    min_samples_split=5,     # Mínimo para dividir nodo
    min_samples_leaf=2,      # Mínimo en hojas
    max_features='sqrt',     # sqrt(d) features por split
    random_state=42,         # Reproducibilidad
    n_jobs=-1                # Paralelización
)
```

**Justificación de Valores:**
- `n_estimators=100`: Balance entre precisión y tiempo
- `max_depth=20`: Evita overfitting en dataset pequeño
- `min_samples_split=5`: Previene splits en ruido
- `max_features='sqrt'`: Regla empírica de Breiman

## 4. Modelo 2: Gradient Boosting Regressor

### 4.1 Fundamento Teórico

Gradient Boosting construye un **ensemble aditivo** de árboles débiles que minimizan una función de pérdida mediante descenso de gradiente.

**Idea Central:** Cada árbol nuevo corrige los errores del ensemble anterior.

### 4.2 Algoritmo de Gradient Boosting

**Formulación Matemática:**

Queremos aproximar una función $F^*(\mathbf{x})$ que minimiza la pérdida esperada:

$$
F^*(\mathbf{x}) = \arg\min_{F} \mathbb{E}_{y, \mathbf{x}}[L(y, F(\mathbf{x}))]
$$

Donde $L$ es la función de pérdida (ej: MSE para regresión).

**Algoritmo:**

```
Inicializar: F_0(x) = arg min_γ Σ L(y_i, γ)

Para m = 1 hasta M:
    1. Calcular pseudo-residuos:
       r_im = -[∂L(y_i, F(x_i))/∂F(x_i)]_{F=F_{m-1}}
    
    2. Entrenar árbol h_m(x) para predecir r_i
    
    3. Calcular multiplicador óptimo:
       γ_m = arg min_γ Σ L(y_i, F_{m-1}(x_i) + γ h_m(x_i))
    
    4. Actualizar modelo:
       F_m(x) = F_{m-1}(x) + η γ_m h_m(x)

Retornar F_M(x)
```

Donde:
- $M$ = número de iteraciones (árboles)
- $\eta$ = learning rate (tasa de aprendizaje)
- $h_m$ = árbol débil en iteración $m$

### 4.3 Función de Pérdida: Mean Squared Error

Para regresión de calidad de asignación:

$$
L(y, F(\mathbf{x})) = \frac{1}{2}(y - F(\mathbf{x}))^2
$$

**Gradiente:**

$$
\frac{\partial L}{\partial F} = -(y - F(\mathbf{x})) = -residuo
$$

Por lo tanto, los pseudo-residuos son simplemente los residuos reales.

### 4.4 Regularización

**L2 Regularization (Ridge):**

$$
L_{reg}(y, F(\mathbf{x})) = L(y, F(\mathbf{x})) + \lambda \sum_{m=1}^{M} ||h_m||^2
$$

**Shrinkage (Learning Rate):**

$$
F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \cdot \gamma_m \cdot h_m(\mathbf{x})
$$

Donde $0 < \eta \leq 1$ controla la contribución de cada árbol.

**Subsampling:**
Usar solo una fracción $\rho$ de los datos para entrenar cada árbol:

$$
subsample\_size = \rho \cdot n, \quad 0 < \rho \leq 1
$$

### 4.5 Hiperparámetros

```python
GradientBoostingRegressor(
    n_estimators=100,        # Número de boosting stages
    learning_rate=0.1,       # Shrinkage η
    max_depth=5,             # Profundidad de árboles débiles
    min_samples_split=5,
    min_samples_leaf=2,
    subsample=0.8,           # Stochastic GB
    random_state=42
)
```

**Justificación:**
- `learning_rate=0.1`: Balance entre convergencia y generalización
- `max_depth=5`: Árboles débiles (shallow) para boosting
- `subsample=0.8`: Reduce overfitting, acelera entrenamiento

## 5. Pipeline de Optimización ML

### 5.1 Fase de Entrenamiento

```python
def entrenar(self, df_inicial):
    """
    Entrena ambos modelos usando el horario inicial
    """
    # 1. Extraer características y labels
    X = []
    y_salon = []
    y_calidad = []
    
    for idx, clase in df_inicial.iterrows():
        features = self.extraer_features(clase, df_inicial, idx)
        X.append(features)
        y_salon.append(clase['Salon'])
        
        # Calidad = inverso de energía local
        calidad = self.calcular_calidad_local(clase, df_inicial)
        y_calidad.append(calidad)
    
    X = np.array(X)
    y_salon = np.array(y_salon)
    y_calidad = np.array(y_calidad)
    
    # 2. Entrenar clasificador (predicción de salón)
    self.clasificador.fit(X, y_salon)
    
    # 3. Entrenar regresor (calidad de asignación)
    self.regressor_calidad.fit(X, y_calidad)
    
    # 4. Calcular métricas de entrenamiento
    y_pred = self.clasificador.predict(X)
    accuracy = (y_pred == y_salon).mean()
    
    return {
        'accuracy': accuracy,
        'n_samples': len(X),
        'n_features': X.shape[1]
    }
```

### 5.2 Cálculo de Calidad Local

La calidad de una asignación se define como:

$$
calidad(c_i, s_j) = -energia\_local(c_i, s_j)
$$

Donde:

$$
\begin{align}
energia\_local(c_i, s_j) = &\ w_1 \cdot distancia\_anterior(c_i, s_j) \\
                           &+ w_2 \cdot \mathbb{1}[tipo(c_i) \neq tipo(s_j)] \\
                           &+ w_3 \cdot \mathbb{1}[s_j \in S_{invalidos}] \\
                           &+ w_4 \cdot \mathbb{1}[cambio\_piso(c_i, s_j)]
\end{align}
$$

**Objetivo:** Enseñar al modelo qué hace una asignación "buena" vs "mala"

### 5.3 Fase de Optimización

```python
def optimizar(self, df_inicial):
    """
    Genera nueva asignación usando modelos entrenados
    """
    df_resultado = df_inicial.copy()
    cambios = 0
    
    for idx in range(len(df_resultado)):
        clase = df_resultado.iloc[idx]
        
        # Proteger clases inmutables (P1)
        if idx in self.indices_inmutables:
            continue
        
        # 1. Extraer características
        features = self.extraer_features(clase, df_resultado, idx)
        
        # 2. Obtener salones candidatos
        candidatos = self.obtener_salones_validos(clase)
        
        # 3. Predecir mejor salón
        salon_predicho = self.clasificador.predict([features])[0]
        
        # 4. Si predicción es válida, usar directamente
        if salon_predicho in candidatos:
            mejor_salon = salon_predicho
        else:
            # 5. Evaluar todos los candidatos con regresor
            mejor_salon = None
            mejor_calidad = -infinito
            
            for salon in candidatos:
                # Simular asignación
                features_temp = self.modificar_features(features, salon)
                calidad = self.regressor_calidad.predict([features_temp])[0]
                
                if calidad > mejor_calidad:
                    mejor_calidad = calidad
                    mejor_salon = salon
        
        # 6. Aplicar asignación
        if df_resultado.loc[idx, 'Salon'] != mejor_salon:
            df_resultado.loc[idx, 'Salon'] = mejor_salon
            cambios += 1
    
    return df_resultado, cambios
```

### 5.4 Validación de Asignaciones

Después de cada predicción, validamos:

```python
def validar_asignacion(self, clase, salon, df_actual):
    """
    Verifica que la asignación sea factible
    """
    # 1. Tipo correcto
    if tipo(clase) != tipo(salon):
        return False
    
    # 2. No es inválido
    if salon in self.salones_invalidos:
        return False
    
    # 3. No hay conflicto temporal
    conflicto = df_actual[
        (df_actual['Dia'] == clase['Dia']) &
        (df_actual['Bloque_Horario'] == clase['Bloque_Horario']) &
        (df_actual['Salon'] == salon)
    ]
    if len(conflicto) > 0:
        return False
    
    return True
```

## 6. Análisis de Complejidad

### 6.1 Complejidad Temporal

**Entrenamiento:**

$$
T_{train} = O(K \cdot n \cdot d \cdot \log n \cdot h)
$$

Donde:
- $K$ = número de árboles
- $n$ = número de muestras
- $d$ = número de características
- $h$ = profundidad máxima

**Para nuestro caso:**
- $K = 100$
- $n = 680$
- $d \approx 20$
- $h = 20$

$$
T_{train} \approx 100 \cdot 680 \cdot 20 \cdot \log(680) \cdot 20 \approx 3.7 \times 10^7 \text{ operaciones}
$$

**Optimización (Inferencia):**

$$
T_{opt} = O(n \cdot K \cdot h \cdot d)
$$

$$
T_{opt} \approx 680 \cdot 100 \cdot 20 \cdot 20 \approx 2.7 \times 10^7 \text{ operaciones}
$$

**Tiempo Real:** ~15-20 segundos en hardware moderno

### 6.2 Complejidad Espacial

$$
S = O(K \cdot n_{nodes} + n \cdot d)
$$

Donde $n_{nodes}$ es el número promedio de nodos por árbol.

Para árboles balanceados de profundidad $h$:

$$
n_{nodes} \approx 2^h - 1
$$

$$
S \approx 100 \cdot (2^{20} - 1) + 680 \cdot 20 \approx 10^8 \text{ bytes} \approx 100 \text{ MB}
$$

## 7. Ventajas y Limitaciones

### 7.1 Ventajas

✅ **Velocidad:** Inferencia muy rápida una vez entrenado  
✅ **Aprendizaje:** Mejora con más datos históricos  
✅ **Robustez:** Ensemble reduce varianza  
✅ **Interpretabilidad:** Feature importance muestra qué importa  
✅ **No paramétrico:** No asume distribución de datos  

### 7.2 Limitaciones

❌ **Requiere datos:** Necesita horarios previos de calidad  
❌ **Overfitting:** Puede memorizar patrones específicos  
❌ **Exploración limitada:** No explora fuera de lo aprendido  
❌ **Dependencia de features:** Calidad depende de feature engineering  
❌ **Cold start:** Mal rendimiento sin datos de entrenamiento  

## 8. Mejoras y Extensiones

### 8.1 Transfer Learning

Usar modelos pre-entrenados en otros campus/instituciones:

$$
\theta_{nuevo} = \theta_{pretrained} + \Delta\theta_{fine-tune}
$$

### 8.2 Active Learning

Seleccionar ejemplos más informativos para etiquetar:

$$
x^* = \arg\max_{x \in U} uncertainty(x)
$$

Donde $uncertainty$ puede ser entropía de predicción.

### 8.3 Deep Learning

Reemplazar Random Forest con redes neuronales:

```
Input (features) → Dense(128, ReLU) → Dropout(0.3) 
                 → Dense(64, ReLU) → Dropout(0.3)
                 → Dense(|S|, Softmax) → Output (salon)
```

### 8.4 Reinforcement Learning

Formular como MDP (Markov Decision Process):
- **Estado:** Asignación parcial actual
- **Acción:** Asignar clase $c_i$ a salón $s_j$
- **Recompensa:** $-energia(asignacion)$
- **Política:** $\pi(s, a) = P(a|s)$

Usar Q-Learning o Policy Gradient para aprender política óptima.

## 9. Resultados Experimentales

### 9.1 Métricas de Entrenamiento

```
Modelo: Random Forest Classifier
├── Accuracy: 0.85
├── Precision: 0.83
├── Recall: 0.82
└── F1-Score: 0.82

Modelo: Gradient Boosting Regressor
├── R²: 0.78
├── MSE: 45.2
└── MAE: 5.3
```

### 9.2 Comparación con Otros Métodos

| Métrica | ML | Greedy | Genético |
|---------|-----|--------|----------|
| Tiempo | **15.8s** | 29.3s | 73.9s |
| P1 | 100% | 100% | 100% |
| Distancia | **1821** | 1951 | 2413 |
| Consistencia | Media | Alta | Baja |

### 9.3 Feature Importance

```
Top 10 características más importantes:
1. profesor_encoded (0.18)
2. salon_clase_anterior (0.15)
3. tipo_clase (0.12)
4. tiene_preferencia (0.10)
5. bloque_horario (0.09)
6. materia_encoded (0.08)
7. dia_semana (0.07)
8. num_estudiantes (0.06)
9. semestre (0.05)
10. piso_clase_anterior (0.04)
```

**Interpretación:** El profesor y el contexto de la clase anterior son los factores más predictivos.

## 10. Conclusiones

El enfoque de Machine Learning ofrece una alternativa **rápida y efectiva** para la asignación de salones, especialmente cuando:
- Existen datos históricos de calidad
- Se requiere velocidad de ejecución
- Los patrones son relativamente estables

Sin embargo, requiere **cuidadoso feature engineering** y **datos de entrenamiento representativos** para alcanzar su máximo potencial.

## Referencias

1. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.

2. Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. *Annals of statistics*, 1189-1232.

3. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical learning* (2nd ed.). Springer.

4. Chen, T., & Guestrin, C. (2016). Xgboost: A scalable tree boosting system. *KDD*, 785-794.

5. Ke, G., et al. (2017). Lightgbm: A highly efficient gradient boosting decision tree. *NIPS*, 3146-3154.
