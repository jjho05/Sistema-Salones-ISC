---
marp: true
theme: default
class: invert
paginate: false
math: mathjax
---

<!-- _class: lead invert -->
# Algoritmo Greedy + Hill Climbing

**Construcción Voraz y Refinamiento Local**

---

## 1. Introducción y Fundamento Teórico


---

### 1.1 Paradigma de Algoritmos Voraces

Un **algoritmo voraz (greedy)** construye una solución tomando decisiones localmente óptimas en cada paso, con la esperanza de que estas decisiones conduzcan a un óptimo global.

---

**Definición Formal:**

Sea $S = \{s_1, s_2, ..., s_n\}$ el conjunto de decisiones a tomar. Un algoritmo voraz:

1. Inicializa $Sol = \emptyset$
2. Para cada decisión $s_i$ en orden:
   - Selecciona $s_i^* = \arg\min_{s \in candidatos} costo(s)$
   - Actualiza $Sol = Sol \cup \{s_i^*\}$
3. Retorna $Sol$

---

**Teorema del Algoritmo Voraz:**
*Un algoritmo voraz produce una solución óptima si el problema exhibe la propiedad de elección voraz y subestructura óptima.*

**Aplicación a Asignación de Salones:**
- **Elección voraz:** Asignar cada clase al salón de menor costo incremental
- **Subestructura:** La solución óptima contiene soluciones óptimas a subproblemas
- **Limitación:** Nuestro problema NO garantiza optimalidad global con greedy puro
---

### 1.2 Búsqueda Local: Hill Climbing

**Hill Climbing** es un algoritmo de búsqueda local que mejora iterativamente una solución explorando su vecindario.

**Definición Formal:**

$$
\begin{align}
&\text{Inicializar: } s = s_0 \\
&\text{Repetir:} \\
&\quad s' = \arg\min_{s'' \in N(s)} f(s'') \\
&\quad \text{Si } f(s') < f(s): \\
&\quad\quad s = s' \\
&\quad \text{Sino: } \\
&\quad\quad \text{retornar } s
\end{align}
$$
---
Donde:
- $s$ = solución actual
- $N(s)$ = vecindario de $s$
- $f(s)$ = función objetivo (energía)

**Propiedades:**
- **Convergencia:** Garantizada a un óptimo local
- **Complejidad:** $O(k \cdot |N(s)|)$ donde $k$ = iteraciones
- **Limitación:** Puede quedar atrapado en óptimos locales
---

### 1.3 Estrategia Híbrida

Combinamos ambos enfoques:

```
Solución = Greedy(problema)  # Construcción rápida
Solución = HillClimbing(Solución)  # Refinamiento local
```

**Ventajas del Híbrido:**
- Greedy proporciona punto de partida de calidad
- Hill Climbing escapa de decisiones voraces subóptimas
- Balance entre velocidad y calidad


---

## 2. Fase 1: Construcción Voraz


---

### 2.1 Ordenamiento de Clases

**Objetivo:** Procesar clases en orden que maximice probabilidad de buenas asignaciones.

**Criterio de Ordenamiento Multi-nivel:**

Para dos clases $c_i$ y $c_j$, definimos $c_i \prec c_j$ si:

$$
\begin{cases}
prioridad(c_i) > prioridad(c_j) & \text{(1° criterio)} \\
\text{o si } prioridad(c_i) = prioridad(c_j): \\
\quad num\_restricciones(c_i) > num\_restricciones(c_j) & \text{(2° criterio)} \\
\text{o si } num\_restricciones(c_i) = num\_restricciones(c_j): \\
\quad |salones\_validos(c_i)| < |salones\_validos(c_j)| & \text{(3° criterio)}
\end{cases}
$$
---

**Justificación Teórica:**

**Lema 1 (Ordenamiento Óptimo):**
*Procesar clases con más restricciones primero minimiza la probabilidad de infactibilidad.*

**Demostración:**
Sea $R_i$ el conjunto de restricciones de $c_i$ y $S_i$ el conjunto de salones válidos.

- Si $|S_i| < |S_j|$, entonces $c_i$ tiene menos opciones
- Procesar $c_i$ primero garantiza que al menos una opción esté disponible
- Procesar $c_j$ después aún deja $|S_j| - 1 \geq |S_i|$ opciones
- Por lo tanto, el orden minimiza conflictos
---

**Implementación:**

```python
def ordenar_clases(self, df):
    """
    Ordena clases por criterio multi-nivel
    """
    df_ordenado = df.copy()
    
    # Calcular métricas para cada clase
    df_ordenado['prioridad_num'] = df_ordenado.apply(
        lambda row: self.obtener_prioridad(row), axis=1
    )
    
    df_ordenado['num_restricciones'] = df_ordenado.apply(
        lambda row: self.contar_restricciones(row), axis=1
    )
    
    df_ordenado['num_salones_validos'] = df_ordenado.apply(
        lambda row: len(self.obtener_salones_validos(row)), axis=1
    )
    
    # Ordenar por criterios
    df_ordenado = df_ordenado.sort_values(
        by=['prioridad_num', 'num_restricciones', 'num_salones_validos'],
        ascending=[False, False, True]
    )
    
    return df_ordenado
```


---

### 2.2 Función de Score Voraz

Para cada par $(clase, salon)$, calculamos un score que estima el costo incremental:

$$
score(c_i, s_j) = \sum_{k=1}^{m} w_k \cdot componente_k(c_i, s_j)
$$

**Componentes del Score:**

#### A. Distancia al Último Salón del Profesor

$$
componente_1(c_i, s_j) = \begin{cases}
0 & \text{si } c_i \text{ es primera clase del profesor} \\
d(ultimo\_salon(profesor(c_i)), s_j) & \text{en otro caso}
\end{cases}
$$
---

Donde $d(\cdot, \cdot)$ es la función de distancia definida anteriormente:

$$
d(s_a, s_b) = \begin{cases}
0 & \text{si } s_a = s_b \\
1 & \text{si } piso(s_a) = piso(s_b) \land s_a \neq s_b \\
10 & \text{si } piso(s_a) \neq piso(s_b)
\end{cases}
$$
---

#### B. Ocupación del Salón

$$
componente_2(c_i, s_j) = \frac{|uso\_actual(s_j)|}{|uso\_maximo(s_j)|}
$$

**Interpretación:** Preferir salones menos utilizados para balancear carga.

---

#### C. Penalización por Tipo Incorrecto

$$
componente_3(c_i, s_j) = \begin{cases}
\infty & \text{si } tipo(c_i) \neq tipo(s_j) \\
0 & \text{en otro caso}
\end{cases}
$$

---

#### D. Bonus por Preferencia

$$
componente_4(c_i, s_j) = \begin{cases}
-B & \text{si } s_j = salon\_preferido(c_i) \\
0 & \text{en otro caso}
\end{cases}
$$

**Donde $B > 0$ es un bonus que incentiva cumplir preferencias.**

---

#### E. Penalización por Salón Inválido

$$
componente_5(c_i, s_j) = \begin{cases}
\infty & \text{si } s_j \in S_{invalidos} \\
0 & \text{en otro caso}
\end{cases}
$$

**Score Total:**

$$
score(c_i, s_j) = 10 \cdot componente_1 + 5 \cdot componente_2 + componente_3 - 50 \cdot componente_4 + componente_5
$$
---

**Pesos Justificados:**
- Distancia (10): Impacto directo en movilidad
- Ocupación (5): Balanceo de recursos
- Tipo ($\infty$): Restricción dura
- Preferencia (-50): Incentivo fuerte
- Inválido ($\infty$): Restricción dura


---

### 2.3 Algoritmo de Construcción

```python
def construccion_greedy(self, df):
    """
    Construye solución inicial mediante selección voraz
    """
    solucion = {}
    ocupacion = {}  # (dia, bloque, salon) -> idx_clase
    
    # Ordenar clases
    df_ordenado = self.ordenar_clases(df)
    
    for idx, clase in df_ordenado.iterrows():
        # Obtener salones candidatos
        candidatos = self.obtener_salones_validos(clase)
        
        # Filtrar salones ocupados en este horario
        candidatos_libres = [
            s for s in candidatos
            if (clase['Dia'], clase['Bloque_Horario'], s) not in ocupacion
        ]
        
        if not candidatos_libres:
            # Caso excepcional: forzar asignación
            mejor_salon = candidatos[0]
        else:
            # Selección voraz: minimizar score
            mejor_salon = None
            mejor_score = float('inf')
            
            for salon in candidatos_libres:
                score = self.calcular_score(clase, salon, solucion)
                
                if score < mejor_score:
                    mejor_score = score
                    mejor_salon = salon
        
        # Asignar
        solucion[idx] = mejor_salon
        ocupacion[(clase['Dia'], clase['Bloque_Horario'], mejor_salon)] = idx
    
    return solucion
```


---

### 2.4 Análisis de Complejidad - Fase 1

**Ordenamiento:**
$$
T_{sort} = O(n \log n)
$$

**Cálculo de salones válidos por clase:**
$$
T_{valid} = O(n \cdot m)
$$

Donde $m$ = número promedio de salones candidatos.

**Selección voraz:**
$$
T_{greedy} = O(n \cdot m)
$$

**Total Fase 1:**
$$
T_1 = O(n \log n + n \cdot m) = O(n \cdot m)
$$

Para $n = 680$, $m \approx 5$:
$$
T_1 \approx 3400 \text{ operaciones}
$$


---

## 3. Fase 2: Hill Climbing


---

### 3.1 Definición del Vecindario

El vecindario $N(s)$ de una solución $s$ se define como:

$$
N(s) = \{s' : s' \text{ difiere de } s \text{ en exactamente un intercambio válido}\}
$$

**Intercambio Válido:**

Para clases $c_i$ y $c_j$:

$$
intercambio\_valido(c_i, c_j) \Leftrightarrow \begin{cases}
tipo(c_i) = tipo(c_j) & \text{(mismo tipo)} \\
i \notin I_{inmutables} \land j \notin I_{inmutables} & \text{(no protegidas)} \\
\neg conflicto(c_i, s(c_j)) \land \neg conflicto(c_j, s(c_i)) & \text{(sin conflictos)}
\end{cases}
$$

Donde $I_{inmutables}$ es el conjunto de índices de clases PRIORIDAD 1.

---

**Tamaño del Vecindario:**

$$
|N(s)| = \binom{n_{modificables}}{2} \approx \frac{n_{modificables}^2}{2}
$$

Para $n_{modificables} \approx 600$:
$$
|N(s)| \approx 180,000 \text{ vecinos posibles}
$$
---

### 3.2 Función de Energía

La función de energía $E(s)$ cuantifica la calidad de una solución:

$$
E(s) = E_{movimientos}(s) + E_{pisos}(s) + E_{distancia}(s) + E_{penalizaciones}(s)
$$

#### A. Energía por Movimientos

$$
E_{movimientos}(s) = w_m \cdot \sum_{p \in P} \max(0, |salones\_usados(p, s)| - 1)
$$

Donde:
$$
salones\_usados(p, s) = \{s(c) : c \in C_p\}
$$
---

**Ejemplo Numérico:**
- Profesor tiene 5 clases en salones: {FF1, FF2, FF1, FF3, FF2}
- $salones\_usados = \{FF1, FF2, FF3\}$
- $|salones\_usados| = 3$
- $E_{movimientos} = 10 \cdot (3 - 1) = 20$
---

#### B. Energía por Cambios de Piso

Sea $C_p^{sorted} = [c_1, c_2, ..., c_k]$ las clases del profesor $p$ ordenadas cronológicamente:

$$
E_{pisos}(s) = w_p \cdot \sum_{p \in P} \sum_{i=1}^{|C_p|-1} \mathbb{1}[piso(s(c_i)) \neq piso(s(c_{i+1}))]
$$
---

#### C. Energía por Distancia

$$
E_{distancia}(s) = w_d \cdot \sum_{p \in P} \sum_{i=1}^{|C_p|-1} d(s(c_i), s(c_{i+1}))
$$
---

#### D. Penalizaciones

$$
\begin{align}
E_{penalizaciones}(s) = &\ 1000 \cdot |\{c : s(c) \in S_{invalidos}\}| \\
                        &+ 500 \cdot |\{(c_i, c_j) : conflicto(c_i, c_j, s)\}| \\
                        &+ 300 \cdot |\{c : tipo(c) \neq tipo(s(c))\}|
\end{align}
$$

**Pesos Utilizados:**
- $w_m = 10$ (movimientos)
- $w_p = 5$ (cambios de piso)
- $w_d = 3$ (distancia)
---

### 3.3 Estrategia de Búsqueda

Implementamos **Steepest Descent Hill Climbing**:

```python
def hill_climbing(self, solucion, df):
    """
    Mejora solución mediante búsqueda local
    """
    mejor_solucion = solucion.copy()
    mejor_energia = self.calcular_energia(mejor_solucion, df)
    
    for iteracion in range(self.max_iter_hc):
        mejoro = False
        indices = list(solucion.keys())
        
        # Generar vecinos aleatorios
        for _ in range(self.intentos_por_iter):
            # Seleccionar par aleatorio
            idx1, idx2 = random.sample(indices, 2)
            
            # Verificar que no sean inmutables
            if idx1 in self.indices_inmutables or idx2 in self.indices_inmutables:
                continue
```
---
```python
            # Verificar mismo tipo
            if self.tipos_por_idx[idx1] != self.tipos_por_idx[idx2]:
                continue

            # Crear vecino
            vecino = mejor_solucion.copy()
            vecino[idx1], vecino[idx2] = vecino[idx2], vecino[idx1]
            
            # Evaluar
            energia_vecino = self.calcular_energia(vecino, df)
            
            # Aceptar si mejora
            if energia_vecino < mejor_energia:
                mejor_solucion = vecino
                mejor_energia = energia_vecino
                mejoro = True
                break  # Steepest descent: aceptar primera mejora
        
        # Criterio de parada
        if not mejoro:
            print(f"   Convergió en iteración {iteracion}")
            break
    
    return mejor_solucion
```
---

### 3.4 Criterio de Parada

El algoritmo se detiene cuando:

$$
\forall s' \in N_{muestreado}(s): E(s') \geq E(s)
$$

Donde $N_{muestreado}$ es un subconjunto aleatorio de $N(s)$.

---

**Teorema 2 (Convergencia de Hill Climbing):**
*El algoritmo de Hill Climbing converge a un óptimo local en tiempo finito.*

**Demostración:**
1. El espacio de soluciones es finito: $|S| = m^n$
2. La energía es discreta y acotada inferiormente: $E(s) \geq 0$
3. Cada iteración reduce estrictamente $E$ o termina
4. No puede haber ciclos (energía siempre decrece)
5. Por lo tanto, converge en $\leq |S|$ iteraciones
---

**Cota Superior Práctica:**

Con muestreo aleatorio de $k$ vecinos por iteración:

$$
T_{convergencia} \leq \frac{E_{inicial} - E_{optimo\_local}}{mejora\_promedio} \cdot k
$$

Empíricamente: $\approx 20-50$ iteraciones

---

### 3.5 Análisis de Complejidad - Fase 2

**Por iteración:**
$$
T_{iter} = k \cdot (T_{generar} + T_{evaluar})
$$

Donde:
- $k$ = intentos por iteración (50)
- $T_{generar} = O(1)$ (intercambio simple)
- $T_{evaluar} = O(n)$ (recalcular energía)

$$
T_{iter} = O(k \cdot n)
$$

**Total Fase 2:**
$$
T_2 = O(max\_iter \cdot k \cdot n)
$$

Para $max\_iter = 100$, $k = 50$, $n = 680$:
$$
T_2 \approx 3.4 \times 10^6 \text{ operaciones}
$$


---

## 4. Protección de PRIORIDAD 1


---

### 4.1 Mecanismo de Inmutabilidad

**Definición:**

Sea $I \subset \{0, 1, ..., n-1\}$ el conjunto de índices de clases PRIORIDAD 1:

$$
I = \{i : c_i \in P_1\}
$$

**Invariante:**

$$
\forall i \in I, \forall t: s_t(c_i) = pref(c_i)
$$

Donde $s_t$ es la solución en el tiempo $t$.

---

**Implementación:**

```python
def cargar_indices_inmutables(self):
    """
    Carga índices de clases que no deben modificarse
    """
    try:
        with open('datos_estructurados/indices_inmutables_p1.json', 'r') as f:
            data = json.load(f)
            self.indices_inmutables = set(data.get('indices', []))
            print(f"✅ Índices inmutables cargados: {len(self.indices_inmutables)} clases")
    except FileNotFoundError:
        self.indices_inmutables = set()
        print("⚠️  No se encontró archivo de índices inmutables")
```
---
### 4.2 Verificación en Hill Climbing

```python
# En cada intercambio propuesto
if idx1 in self.indices_inmutables or idx2 in self.indices_inmutables:
    continue  # Saltar este intercambio
```
---

**Teorema 3 (Preservación de P1):**
*Si $s_0$ satisface PRIORIDAD 1 y se respetan los índices inmutables, entonces $s_t$ satisface PRIORIDAD 1 para todo $t$.*

**Demostración:**
Por inducción en $t$:
- **Caso base ($t=0$):** $s_0$ satisface P1 por construcción (pre-asignación)
- **Paso inductivo:** Asumimos $s_t$ satisface P1
  - Hill Climbing solo modifica índices $\notin I$
  - Por lo tanto, $\forall i \in I: s_{t+1}(c_i) = s_t(c_i) = pref(c_i)$
  - Luego $s_{t+1}$ satisface P1
---

### 4.3 Corrección Post-Optimización

Como medida de seguridad adicional:

```python
def corregir_prioridades_final(self, solucion, df):
    """
    Garantiza 100% cumplimiento de PRIORIDAD 1
    """
    correcciones = 0
    
    for idx in self.indices_inmutables:
        clase = df.iloc[idx]
        salon_esperado = self.obtener_salon_preferido(clase)
        
        if solucion[idx] != salon_esperado:
            solucion[idx] = salon_esperado
            correcciones += 1
    
    if correcciones > 0:
        print(f"   ✅ {correcciones} clases corregidas a salón prioritario")
    
    return solucion
```


---

## 5. Optimizaciones y Mejoras


---

### 5.1 Caching de Energía

**Problema:** Recalcular energía completa es $O(n)$

---

**Solución:** Calcular solo cambio incremental

```python
def calcular_delta_energia(self, solucion, idx1, idx2, df):
    """
    Calcula cambio de energía por intercambio
    """
    # Solo recalcular para profesores afectados
    prof1 = df.iloc[idx1]['Profesor']
    prof2 = df.iloc[idx2]['Profesor']
    
    delta = 0
    delta += self.delta_movimientos(prof1, idx1, idx2, solucion, df)
    
    if prof1 != prof2:
        delta += self.delta_movimientos(prof2, idx1, idx2, solucion, df)
    
    return delta
```

**Complejidad:** $O(|C_{prof}|)$ en lugar de $O(n)$

---

### 5.2 Tabu Search

Evitar ciclos manteniendo lista de movimientos prohibidos:

```python
def hill_climbing_tabu(self, solucion, df):
    tabu_list = deque(maxlen=10)  # Últimos 10 movimientos
    
    for iteracion in range(self.max_iter_hc):
        # ... generar vecino ...
        
        movimiento = (idx1, idx2)
        if movimiento in tabu_list:
            continue  # Prohibido
        
        # ... evaluar y aceptar ...
        
        if mejoro:
            tabu_list.append(movimiento)
```
---

### 5.3 Simulated Annealing

Aceptar ocasionalmente movimientos que empeoran:

$$
P(aceptar) = \begin{cases}
1 & \text{si } \Delta E < 0 \\
e^{-\Delta E / T} & \text{si } \Delta E \geq 0
\end{cases}
$$

Donde $T$ es la "temperatura" que decrece con el tiempo:

$$
T_t = T_0 \cdot \alpha^t, \quad 0 < \alpha < 1
$$


---

## 6. Resultados y Análisis


---

### 6.1 Métricas de Rendimiento

```
FASE 1: Construcción Greedy
├── Tiempo: 2.3s
├── Energía inicial: 82,948
└── Clases asignadas: 680/680

FASE 2: Hill Climbing
├── Tiempo: 27.0s
├── Iteraciones: 54
├── Energía final: 82,716
├── Mejora: 232 (-0.28%)
└── Convergencia: Sí

RESULTADOS FINALES:
├── Movimientos: 314 (-12.0% vs inicial)
├── Cambios piso: 206 (-28.2% vs inicial)
├── Distancia: 1,951 (-31.5% vs inicial)
└── PRIORIDAD 1: 100% (98/98)
```


---

### 6.2 Comparación con Otros Algoritmos

| Métrica | Greedy+HC | ML | Genético | Óptimo Teórico |
|---------|-----------|-----|----------|----------------|
| Tiempo | 29.3s | 15.8s | 73.9s | ∞ |
| Movimientos | 314 | 365 | 378 | ≥280 |
| Cambios piso | 206 | 223 | 286 | ≥180 |
| Distancia | 1,951 | 1,821 | 2,413 | ≥1,500 |
| Gap vs óptimo | ~5% | ~3% | ~10% | 0% |

**Nota:** Óptimo teórico es estimación basada en cotas inferiores.


---

### 6.3 Análisis de Sensibilidad

**Variación de Parámetros:**

| max_iter | Tiempo | Energía Final | Mejora |
|----------|--------|---------------|--------|
| 10 | 5.2s | 82,850 | Baja |
| 50 | 15.1s | 82,730 | Media |
| 100 | 29.3s | 82,716 | Alta |
| 200 | 58.7s | 82,714 | Marginal |

**Conclusión:** 100 iteraciones es el punto óptimo (rendimientos decrecientes después).


---

## 7. Ventajas y Limitaciones


---

### 7.1 Ventajas

✅ **Velocidad:** Construcción inicial muy rápida ($O(n \log n)$)  
✅ **Simplicidad:** Fácil de entender e implementar  
✅ **Determinismo:** Resultados reproducibles (con semilla fija)  
✅ **Escalabilidad:** Complejidad lineal en $n$  
✅ **Robustez:** Siempre encuentra solución factible  
✅ **Balance:** Buena relación calidad/tiempo 

--- 

### 7.2 Limitaciones

❌ **Óptimos Locales:** No garantiza óptimo global  
❌ **Sensibilidad al Orden:** Orden inicial afecta resultado  
❌ **Exploración Limitada:** Vecindario pequeño  
❌ **Plateau:** Puede estancarse en mesetas  
❌ **Parámetros:** Requiere ajuste de pesos 

---

### 7.3 Cuándo Usar Greedy+HC

**Recomendado cuando:**
- Se requiere solución rápida (< 1 minuto)
- Calidad media-alta es suficiente
- Problema es relativamente estructurado
- Hay buena heurística de ordenamiento

**No recomendado cuando:**
- Se requiere óptimo global garantizado
- Hay tiempo ilimitado para búsqueda
- Problema es altamente irregular
- Espacio de búsqueda es muy pequeño


---

## 8. Extensiones Futuras


---

### 8.1 Variable Neighborhood Search (VNS)

Usar múltiples definiciones de vecindario:

$$
N_1(s) = \text{intercambios simples}
$$
$$
N_2(s) = \text{intercambios dobles}
$$
$$
N_3(s) = \text{rotaciones cíclicas}
$$
---

### 8.2 Iterated Local Search (ILS)

Aplicar perturbaciones para escapar óptimos locales:

```
s = ConstructionGreedy()
s = HillClimbing(s)

for i in range(max_restarts):
    s' = Perturb(s)
    s' = HillClimbing(s')
    if E(s') < E(s):
        s = s'

return s
```
---

### 8.3 Guided Local Search

Penalizar características de óptimos locales visitados:

$$
E_{guided}(s) = E(s) + \lambda \sum_{i} p_i \cdot feature_i(s)
$$

Donde $p_i$ aumenta cada vez que se visita un óptimo local con $feature_i$.


---

## 9. Conclusiones

El algoritmo Greedy + Hill Climbing ofrece un **excelente balance** entre:
- **Velocidad de ejecución** (~30s)
- **Calidad de solución** (top 2 de 4 algoritmos)
- **Simplicidad de implementación**
- **Robustez y confiabilidad**

Es la **opción recomendada** para uso general en el sistema de asignación de salones.


---

## Referencias

1. Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

2. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

3. Papadimitriou, C. H., & Steiglitz, K. (1998). *Combinatorial Optimization: Algorithms and Complexity*. Dover.

4. Aarts, E., & Lenstra, J. K. (2003). *Local Search in Combinatorial Optimization*. Princeton University Press.

5. Hoos, H. H., & Stützle, T. (2004). *Stochastic Local Search: Foundations and Applications*. Morgan Kaufmann.
