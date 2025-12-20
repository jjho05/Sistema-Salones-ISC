# Método de Optimización: Algoritmo Genético Evolutivo

## 📚 Índice

1. [Introducción](#introducción)
2. [Fundamentos Teóricos](#fundamentos-teóricos)
3. [Representación Cromosómica](#representación-cromosómica)
4. [Función de Fitness](#función-de-fitness)
5. [Operadores Genéticos](#operadores-genéticos)
6. [Algoritmo Evolutivo](#algoritmo-evolutivo)
7. [Restricciones](#restricciones)
8. [Fórmulas Matemáticas](#fórmulas-matemáticas)
9. [Parámetros y Configuración](#parámetros-y-configuración)
10. [Comparación con Otros Métodos](#comparación-con-otros-métodos)

---

## Introducción

El **Algoritmo Genético (AG)** es una metaheurística inspirada en la evolución biológica que utiliza mecanismos de selección natural, cruzamiento y mutación para encontrar soluciones óptimas o cercanas al óptimo en espacios de búsqueda complejos.

### Ventajas del Enfoque Genético

- ✅ **Exploración global**: Evita quedar atrapado en óptimos locales
- ✅ **No requiere gradientes**: Funciona con funciones no diferenciables
- ✅ **Paralelizable**: Evalúa múltiples soluciones simultáneamente
- ✅ **Flexible**: Fácil adaptar a nuevas restricciones
- ✅ **Robusto**: Maneja espacios de búsqueda discontinuos

### Desventajas

- ❌ **No garantiza óptimo global**: Es una heurística
- ❌ **Requiere ajuste de parámetros**: Tasa de mutación, cruzamiento, etc.
- ❌ **Computacionalmente intensivo**: Muchas evaluaciones de fitness
- ❌ **Convergencia lenta**: Puede necesitar muchas generaciones

---

## Fundamentos Teóricos

### Principios de la Evolución

El algoritmo genético se basa en tres principios darwinianos:

1. **Selección Natural**: Los individuos más aptos tienen mayor probabilidad de reproducirse
2. **Herencia**: Los descendientes heredan características de sus padres
3. **Variación**: Las mutaciones introducen diversidad genética

### Ciclo Evolutivo

```
┌─────────────────────────────────────────────────────┐
│              POBLACIÓN INICIAL (Gen 0)              │
│  Individuos aleatorios o heurísticos                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  EVALUACIÓN FITNESS  │
        │  Calcular aptitud    │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  ¿CRITERIO PARADA?   │
        │  (Gen max / Fitness) │
        └──────┬───────┬───────┘
               │       │
          NO   │       │ SÍ
               │       │
               ▼       ▼
        ┌──────────┐  SOLUCIÓN
        │ SELECCIÓN│  ÓPTIMA
        │ Padres   │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │CRUZAMIENTO│
        │ Offspring │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ MUTACIÓN │
        │ Diversidad│
        └────┬─────┘
             │
             ▼
        ┌──────────────────┐
        │ NUEVA GENERACIÓN │
        └────────┬─────────┘
                 │
                 └──────► (Volver a Evaluación)
```

---

## Representación Cromosómica

### Estructura del Cromosoma

Cada **individuo** (solución) se representa como un cromosoma que codifica una asignación completa de salones:

**Cromosoma** = Secuencia de genes, donde cada gen representa una asignación

$$
\text{Cromosoma} = [g_1, g_2, g_3, ..., g_n]
$$

Donde:
- $n$ = número total de asignaciones (680 en nuestro caso)
- $g_i$ = gen que codifica el salón asignado a la clase $i$

### Codificación de Genes

Cada gen $g_i$ contiene:

```python
gen_i = {
    'grupo': str,           # Código del grupo (ej: "1A")
    'materia': str,         # Nombre de la materia
    'dia': str,             # Día de la semana
    'bloque': str,          # Bloque horario (ej: "0809")
    'profesor': str,        # ID del profesor
    'salon': str,           # SALÓN ASIGNADO (variable a optimizar)
    'tipo_requerido': str   # 'Teoría' o 'Laboratorio'
}
```

### Espacio de Búsqueda

Para cada asignación, el espacio de salones posibles es:

$$
S = \{\text{FF1, FF2, ..., FF7, FF8, ..., FFD, LR, LSO, ..., LCG3}\}
$$

$$
|S| = 21 \text{ salones válidos}
$$

**Tamaño del espacio de búsqueda total:**

$$
|\Omega| = 21^{680} \approx 10^{900}
$$

Este espacio astronómico justifica el uso de metaheurísticas.

---

## Función de Fitness

La función de fitness $F$ evalúa la calidad de una solución (cromosoma). **Mayor fitness = mejor solución**.

### Función de Fitness Compuesta

$$
F(\text{cromosoma}) = -\left(\sum_{i=1}^{m} w_i \cdot P_i + \sum_{j=1}^{n} w_j \cdot C_j\right)
$$

Donde:
- $P_i$ = Penalizaciones por violar restricciones hard
- $C_j$ = Costos por restricciones soft
- $w_i, w_j$ = Pesos de penalización/costo

### Componentes de Penalización (Hard Constraints)

#### P1: Salones Inválidos

$$
P_{\text{inválidos}} = 1000 \times \sum_{i=1}^{n} \mathbb{1}[\text{salon}_i \in \{\text{AV1, AV2, AV4, AV5, E11}\}]
$$

**Peso**: $w_1 = 1000$ (penalización muy alta)

#### P2: Conflictos de Horario

$$
P_{\text{conflictos}} = 500 \times \sum_{(i,j): i \neq j} \mathbb{1}[\text{salon}_i = \text{salon}_j \land \text{hora}_i = \text{hora}_j \land \text{dia}_i = \text{dia}_j]
$$

**Peso**: $w_2 = 500$

#### P3: Tipo de Salón Incorrecto

$$
P_{\text{tipo}} = 300 \times \sum_{i=1}^{n} \mathbb{1}[\text{requiere\_lab}_i \land \neg\text{es\_lab}(\text{salon}_i)]
$$

**Peso**: $w_3 = 300$

#### P4: Grupos de Primer Semestre

$$
P_{\text{1er\_sem}} = 400 \times \sum_{g \in G_1} \mathbb{1}[|\{\text{salones\_teoría}(g)\}| > 1]
$$

**Peso**: $w_4 = 400$

#### P5: Capacidad Insuficiente

$$
P_{\text{capacidad}} = 200 \times \sum_{i=1}^{n} \max(0, \text{estudiantes}_i - \text{capacidad}(\text{salon}_i))
$$

**Peso**: $w_5 = 200$

### Componentes de Costo (Soft Constraints)

#### C1: Movimientos de Profesores

$$
C_{\text{movimientos}} = \sum_{p \in P} \sum_{t=1}^{T_p-1} \mathbb{1}[\text{salon}_{p,t} \neq \text{salon}_{p,t+1}]
$$

**Peso**: $w_6 = 10$

#### C2: Cambios de Piso

$$
C_{\text{pisos}} = \sum_{p \in P} \sum_{t=1}^{T_p-1} \mathbb{1}[\text{piso}_{p,t} \neq \text{piso}_{p,t+1}]
$$

**Peso**: $w_7 = 5$

#### C3: Distancia Total

$$
C_{\text{distancia}} = \sum_{p \in P} \sum_{t=1}^{T_p-1} d(\text{salon}_{p,t}, \text{salon}_{p,t+1})
$$

**Peso**: $w_8 = 3$

#### C4: Desbalance de Uso

$$
C_{\text{balance}} = \text{Var}(\{\text{uso}(s) : s \in S\})
$$

Donde $\text{uso}(s)$ = número de veces que se usa el salón $s$

**Peso**: $w_9 = 2$

### Función de Fitness Final

$$
F = -\left(1000 P_1 + 500 P_2 + 300 P_3 + 400 P_4 + 200 P_5 + 10 C_1 + 5 C_2 + 3 C_3 + 2 C_4\right)
$$

**Objetivo**: Maximizar $F$ (equivalente a minimizar penalizaciones y costos)

---

## Operadores Genéticos

### 1. Selección

Selecciona individuos para reproducción basándose en su fitness.

#### Selección por Torneo

$$
P(\text{seleccionar } i) = \frac{1}{k} \text{ si } F(i) = \max_{j \in T} F(j)
$$

Donde:
- $T$ = torneo de $k$ individuos seleccionados aleatoriamente
- $k$ = tamaño del torneo (típicamente 3-5)

**Algoritmo:**
```python
def seleccion_torneo(poblacion, k=3):
    torneo = random.sample(poblacion, k)
    return max(torneo, key=lambda ind: ind.fitness)
```

#### Selección por Ruleta

$$
P(\text{seleccionar } i) = \frac{F(i) - F_{\min}}{\sum_{j=1}^{N} (F(j) - F_{\min})}
$$

Donde $F_{\min}$ = fitness del peor individuo

### 2. Cruzamiento (Crossover)

Combina genes de dos padres para crear descendencia.

#### Cruzamiento de Un Punto

$$
\text{Hijo}_1 = [\text{Padre}_1[1:c], \text{Padre}_2[c:n]]
$$
$$
\text{Hijo}_2 = [\text{Padre}_2[1:c], \text{Padre}_1[c:n]]
$$

Donde $c$ = punto de cruzamiento aleatorio

#### Cruzamiento Uniforme

$$
\text{Hijo}[i] = \begin{cases}
\text{Padre}_1[i] & \text{con probabilidad } 0.5 \\
\text{Padre}_2[i] & \text{con probabilidad } 0.5
\end{cases}
$$

#### Cruzamiento Inteligente (Específico del Problema)

Preserva asignaciones buenas:

```python
def cruzamiento_inteligente(padre1, padre2):
    hijo = []
    for i in range(len(padre1)):
        # Si ambos padres tienen el mismo salón, heredarlo
        if padre1[i].salon == padre2[i].salon:
            hijo.append(padre1[i])
        # Si uno viola restricción y otro no, elegir el válido
        elif es_valido(padre1[i]) and not es_valido(padre2[i]):
            hijo.append(padre1[i])
        elif es_valido(padre2[i]) and not es_valido(padre1[i]):
            hijo.append(padre2[i])
        # Si ambos válidos, elegir el de mejor fitness local
        else:
            hijo.append(max([padre1[i], padre2[i]], 
                          key=lambda g: fitness_local(g)))
    return hijo
```

**Probabilidad de cruzamiento**: $P_c = 0.8$ (80%)

### 3. Mutación

Introduce variación aleatoria para mantener diversidad.

#### Mutación Simple

$$
\text{Gen}[i].\text{salon} = \begin{cases}
\text{salón aleatorio de } S & \text{con probabilidad } P_m \\
\text{Gen}[i].\text{salon} & \text{con probabilidad } 1 - P_m
\end{cases}
$$

**Probabilidad de mutación**: $P_m = 0.1$ (10%)

#### Mutación Adaptativa

$$
P_m(t) = P_{m,\max} - \frac{(P_{m,\max} - P_{m,\min}) \cdot t}{T_{\max}}
$$

Donde:
- $t$ = generación actual
- $T_{\max}$ = generaciones máximas
- $P_{m,\max} = 0.2$, $P_{m,\min} = 0.01$

#### Mutación Inteligente

Solo muta a salones válidos que mejoren restricciones:

```python
def mutacion_inteligente(gen, prob=0.1):
    if random.random() < prob:
        # Obtener salones candidatos válidos
        candidatos = obtener_salones_validos(gen)
        if candidatos:
            # Elegir el que minimice violaciones
            gen.salon = min(candidatos, 
                          key=lambda s: evaluar_violaciones(gen, s))
    return gen
```

### 4. Elitismo

Preserva los mejores individuos de generación en generación.

$$
\text{Elite} = \{i \in P_t : F(i) \geq F_{(k)}\}
$$

Donde $F_{(k)}$ = k-ésimo mejor fitness

**Tasa de elitismo**: 5-10% de la población

---

## Algoritmo Evolutivo

### Pseudocódigo Completo

```
ALGORITMO: Algoritmo_Genético_Salones

ENTRADA:
    - horario_inicial: Asignaciones iniciales
    - tam_poblacion: Tamaño de la población (100-200)
    - num_generaciones: Generaciones máximas (500-1000)
    - prob_cruzamiento: Probabilidad de cruzamiento (0.8)
    - prob_mutacion: Probabilidad de mutación (0.1)
    - tasa_elitismo: % de elite (0.1)

SALIDA:
    - mejor_solucion: Cromosoma con mejor fitness

PASOS:

1. INICIALIZACIÓN
   poblacion = []
   
   # Individuo 1: Horario inicial
   poblacion.append(horario_inicial)
   
   # Individuos 2-N: Variaciones aleatorias
   for i = 2 to tam_poblacion:
       individuo = generar_individuo_aleatorio()
       poblacion.append(individuo)
   
   # Evaluar población inicial
   for ind in poblacion:
       ind.fitness = calcular_fitness(ind)
   
   mejor_global = max(poblacion, key=lambda x: x.fitness)
   historial_fitness = [mejor_global.fitness]

2. EVOLUCIÓN (Generaciones)
   for generacion = 1 to num_generaciones:
       
       2.1. SELECCIÓN
           padres = []
           for i = 1 to tam_poblacion:
               padre = seleccion_torneo(poblacion, k=3)
               padres.append(padre)
       
       2.2. CRUZAMIENTO
           hijos = []
           for i = 1 to tam_poblacion step 2:
               if random() < prob_cruzamiento:
                   hijo1, hijo2 = cruzamiento_uniforme(
                       padres[i], padres[i+1]
                   )
               else:
                   hijo1, hijo2 = padres[i], padres[i+1]
               
               hijos.append(hijo1)
               hijos.append(hijo2)
       
       2.3. MUTACIÓN
           for hijo in hijos:
               for gen in hijo:
                   if random() < prob_mutacion:
                       gen.salon = mutacion_inteligente(gen)
       
       2.4. REPARACIÓN (Asegurar validez)
           for hijo in hijos:
               reparar_restricciones_hard(hijo)
       
       2.5. EVALUACIÓN
           for hijo in hijos:
               hijo.fitness = calcular_fitness(hijo)
       
       2.6. ELITISMO
           num_elite = int(tam_poblacion * tasa_elitismo)
           elite = sorted(poblacion, 
                         key=lambda x: x.fitness, 
                         reverse=True)[:num_elite]
       
       2.7. REEMPLAZO
           poblacion = elite + hijos[:(tam_poblacion - num_elite)]
       
       2.8. ACTUALIZAR MEJOR
           mejor_gen = max(poblacion, key=lambda x: x.fitness)
           if mejor_gen.fitness > mejor_global.fitness:
               mejor_global = mejor_gen
           
           historial_fitness.append(mejor_global.fitness)
       
       2.9. CRITERIO DE PARADA
           # Convergencia: sin mejora en N generaciones
           if len(historial_fitness) > 50:
               ultimos_50 = historial_fitness[-50:]
               if max(ultimos_50) == min(ultimos_50):
                   print(f"Convergencia en generación {generacion}")
                   break
       
       2.10. LOGGING
           if generacion % 50 == 0:
               print(f"Gen {generacion}: Mejor Fitness = {mejor_global.fitness}")

3. RETORNAR SOLUCIÓN
   return mejor_global, historial_fitness
```

---

## Restricciones

### Manejo de Restricciones Hard

**Estrategia 1: Penalización Fuerte**
- Asignar fitness muy bajo a soluciones inválidas
- Permite explorar espacio infactible temporalmente

**Estrategia 2: Reparación**
- Corregir violaciones después de cruzamiento/mutación
- Garantiza que todos los individuos sean válidos

**Estrategia 3: Operadores Especializados**
- Diseñar cruzamiento/mutación que preserven validez
- Más eficiente pero más complejo

### Implementación Híbrida

```python
def reparar_restricciones_hard(cromosoma):
    # R1: Eliminar salones inválidos
    for gen in cromosoma:
        if gen.salon in SALONES_INVALIDOS:
            gen.salon = elegir_salon_valido_aleatorio(gen)
    
    # R2: Resolver conflictos de horario
    conflictos = detectar_conflictos(cromosoma)
    for conflicto in conflictos:
        # Reasignar el de menor fitness local
        gen_a_cambiar = min(conflicto, key=lambda g: fitness_local(g))
        gen_a_cambiar.salon = buscar_salon_disponible(gen_a_cambiar)
    
    # R3: Grupos de primer semestre
    for grupo in grupos_primer_semestre:
        asignaciones_teoria = [g for g in cromosoma 
                              if g.grupo == grupo and g.tipo == 'Teoría']
        if len(set(g.salon for g in asignaciones_teoria)) > 1:
            # Unificar al salón más frecuente
            salon_comun = mode([g.salon for g in asignaciones_teoria])
            for g in asignaciones_teoria:
                g.salon = salon_comun
    
    return cromosoma
```

---

## Fórmulas Matemáticas

### Diversidad de la Población

$$
D(P_t) = \frac{1}{N(N-1)} \sum_{i=1}^{N} \sum_{j=i+1}^{N} d(C_i, C_j)
$$

Donde:
- $d(C_i, C_j)$ = distancia de Hamming entre cromosomas

$$
d(C_i, C_j) = \sum_{k=1}^{n} \mathbb{1}[C_i[k].\text{salon} \neq C_j[k].\text{salon}]
$$

### Presión Selectiva

$$
\text{Presión} = \frac{F_{\max}}{F_{\text{avg}}}
$$

Donde:
- $F_{\max}$ = mejor fitness de la población
- $F_{\text{avg}}$ = fitness promedio

**Ideal**: 1.2 - 1.5

### Tasa de Mejora

$$
\text{Mejora}(t) = \frac{F_{\text{mejor}}(t) - F_{\text{mejor}}(t-1)}{F_{\text{mejor}}(t-1)} \times 100\%
$$

---

## Parámetros y Configuración

| Parámetro | Valor Recomendado | Justificación |
|-----------|-------------------|---------------|
| **Tamaño Población** | 150 | Balance exploración/explotación |
| **Generaciones Máx** | 500 | Suficiente para convergencia |
| **Prob. Cruzamiento** | 0.8 | Alta recombinación |
| **Prob. Mutación** | 0.1 | Mantener diversidad |
| **Tasa Elitismo** | 0.1 | Preservar mejores 15 individuos |
| **Tamaño Torneo** | 3 | Presión selectiva moderada |
| **Criterio Parada** | 50 gen sin mejora | Evitar ejecución innecesaria |

---

## Comparación con Otros Métodos

| Aspecto | Genético | Machine Learning | ILP |
|---------|----------|------------------|-----|
| **Garantía Óptimo** | ❌ No | ❌ No | ✅ Sí* |
| **Velocidad** | ⚠️ Media | ✅ Rápida | ❌ Lenta |
| **Escalabilidad** | ✅ Excelente | ✅ Excelente | ❌ Limitada |
| **Calidad Solución** | ✅ Muy buena | ⚠️ Buena | ✅ Óptima* |
| **Flexibilidad** | ✅ Alta | ⚠️ Media | ❌ Baja |
| **Requiere Datos** | ❌ No | ✅ Sí | ❌ No |
| **Interpretabilidad** | ⚠️ Media | ❌ Baja | ✅ Alta |
| **Manejo Restricciones** | ✅ Flexible | ⚠️ Aproximado | ✅ Exacto |

*Si converge y tiempo suficiente

### Cuándo Usar Genético

✅ **Ideal para:**
- Espacios de búsqueda muy grandes
- Múltiples objetivos conflictivos
- Restricciones complejas y dinámicas
- Cuando se necesita buena solución (no necesariamente óptima)
- Problemas combinatorios NP-hard

❌ **No recomendado para:**
- Problemas pequeños (< 100 variables)
- Cuando se requiere garantía de optimalidad
- Tiempo de ejecución muy limitado
- Funciones de fitness muy costosas de evaluar

---

## Resultados Esperados

### Métricas de Éxito

1. **Asignaciones Inválidas**: 0 (eliminación completa)
2. **Movimientos de Profesores**: Reducción 40-60%
3. **Cambios de Piso**: Reducción 50-70%
4. **Distancia Total**: Reducción 30-50%
5. **Convergencia**: < 300 generaciones
6. **Tiempo de Ejecución**: 2-5 minutos

### Ventajas Esperadas vs Otros Métodos

- **vs ML**: Mayor optimización de movimientos (explora más soluciones)
- **vs ILP**: Más rápido y escalable
- **vs Profesor**: Optimización sistemática y reproducible

---

## Referencias

- Holland, J. H. (1992). Adaptation in Natural and Artificial Systems
- Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning
- Michalewicz, Z. (1996). Genetic Algorithms + Data Structures = Evolution Programs
- Deb, K. (2001). Multi-Objective Optimization using Evolutionary Algorithms
