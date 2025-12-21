# Arquitectura del Código

## 1. Visión General del Sistema

### 1.1 Arquitectura de Alto Nivel

```
Sistema-Salones-ISC/
│
├── Capa de Presentación (UI)
│   └── configurador_materias.py
│
├── Capa de Procesamiento
│   ├── pre_asignar_p1.py
│   ├── optimizador_greedy.py
│   ├── optimizador_ml.py
│   ├── optimizador_genetico.py
│   └── corregir_prioridades.py
│
├── Capa de Utilidades
│   └── utils_restricciones.py
│
├── Capa de Orquestación
│   ├── ejecutar_todos.py
│   └── generar_comparativa_completa.py
│
└── Capa de Datos
    ├── datos_estructurados/
    ├── preferencias_profesores.json
    ├── configuracion_materias.json
    └── asignacion_grupos_1er_semestre.json
```

### 1.2 Flujo de Datos

```mermaid
graph LR
    A[Configuración] --> B[Horario Inicial]
    B --> C[Pre-asignación P1]
    C --> D[Optimizadores]
    D --> E[Corrección]
    E --> F[Comparativas]
    F --> G[Reportes]
```

## 2. Módulos Principales

### 2.1 configurador_materias.py

**Propósito:** Interfaz gráfica para configuración del sistema

**Clase Principal:**
```python
class ConfiguradorMaterias:
    """
    Aplicación Tkinter para configurar materias y preferencias
    """
    def __init__(self):
        self.root = tk.Tk()
        self.materias = {}
        self.preferencias = {}
        self.grupos_1er = {}
        
        self.crear_interfaz()
    
    # Métodos principales
    def crear_interfaz(self)
    def crear_tab_materias(self)
    def crear_tab_preferencias(self)
    def crear_tab_grupos(self)
    def guardar_todo(self)
    def cargar_todo(self)
```

**Responsabilidades:**
- Configurar características de materias (horas, distribución)
- Definir preferencias de profesores (salón + prioridad)
- Asignar grupos de primer semestre
- Guardar/cargar configuración en JSON

**Dependencias:**
- `tkinter` (UI)
- `json` (persistencia)
- `pandas` (validación)

**Archivos Generados:**
- `preferencias_profesores.json`
- `configuracion_materias.json`
- `asignacion_grupos_1er_semestre.json`

### 2.2 pre_asignar_p1.py

**Propósito:** Pre-asignación forzada de PRIORIDAD 1

**Funciones Principales:**
```python
def cargar_datos():
    """Carga horario inicial y preferencias"""
    
def identificar_clases_prioritarias(df, preferencias):
    """Identifica todas las clases P1"""
    
def asignar_forzadamente(df, clases_p1):
    """Asigna cada clase P1 a su salón preferido"""
    
def guardar_resultados(df, indices_inmutables):
    """Guarda horario pre-asignado e índices"""
```

**Algoritmo:**
1. Cargar horario inicial
2. Identificar clases P1 desde preferencias
3. Ordenar por complejidad
4. Asignar forzadamente (resolviendo conflictos)
5. Marcar índices como inmutables
6. Guardar resultados

**Archivos de Entrada:**
- `datos_estructurados/01_Horario_Inicial.csv`
- `preferencias_profesores.json`

**Archivos de Salida:**
- `datos_estructurados/00_Horario_PreAsignado_P1.csv`
- `datos_estructurados/indices_inmutables_p1.json`

### 2.3 optimizador_greedy.py

**Propósito:** Optimización mediante Greedy + Hill Climbing

**Clase Principal:**
```python
class OptimizadorGreedyHC:
    def __init__(self):
        self.indices_inmutables = set()
        self.max_iter_hc = 100
        self.pesos = {...}
    
    # Fase 1: Construcción
    def construccion_greedy(self, df):
        """Construye solución inicial vorazmente"""
    
    def calcular_score(self, clase, salon, solucion):
        """Calcula score para asignación"""
    
    # Fase 2: Refinamiento
    def hill_climbing(self, solucion, df):
        """Mejora mediante búsqueda local"""
    
    def calcular_energia(self, solucion, df):
        """Calcula energía total de solución"""
    
    # Utilidades
    def analizar_movimientos(self, df):
        """Analiza movimientos de profesores"""
```

**Flujo de Ejecución:**
1. Cargar horario pre-asignado
2. Cargar índices inmutables
3. Construcción greedy (respetando inmutables)
4. Hill Climbing (protegiendo inmutables)
5. Corrección final de P1
6. Análisis de métricas
7. Guardar resultado

**Archivos de Entrada:**
- `datos_estructurados/00_Horario_PreAsignado_P1.csv`
- `datos_estructurados/indices_inmutables_p1.json`
- `preferencias_profesores.json`
- `configuracion_materias.json`

**Archivos de Salida:**
- `datos_estructurados/04_Horario_Optimizado_Greedy.csv`
- `comparativas/04_inicial_vs_greedy/metricas_movimientos.csv`

### 2.4 optimizador_ml.py

**Propósito:** Optimización mediante Machine Learning

**Clase Principal:**
```python
class OptimizadorML:
    def __init__(self):
        self.clasificador = RandomForestClassifier(...)
        self.regressor_calidad = GradientBoostingRegressor(...)
        self.indices_inmutables = set()
    
    # Entrenamiento
    def entrenar(self, df_inicial):
        """Entrena modelos con horario inicial"""
    
    def extraer_features(self, clase, df, idx):
        """Extrae vector de características"""
    
    # Optimización
    def optimizar(self, df_inicial):
        """Genera nueva asignación usando modelos"""
    
    def predecir_salon(self, features):
        """Predice mejor salón para clase"""
```

**Flujo de Ejecución:**
1. Cargar horario pre-asignado
2. Cargar índices inmutables
3. Entrenar Random Forest (predicción de salón)
4. Entrenar Gradient Boosting (calidad de asignación)
5. Optimizar (predecir salón para cada clase)
6. Proteger clases inmutables
7. Análisis de métricas
8. Guardar resultado

**Archivos de Entrada:**
- `datos_estructurados/00_Horario_PreAsignado_P1.csv`
- `datos_estructurados/indices_inmutables_p1.json`

**Archivos de Salida:**
- `datos_estructurados/05_Horario_Optimizado_ML.csv`
- `comparativas/02_inicial_vs_ml/metricas_movimientos.csv`

### 2.5 optimizador_genetico.py

**Propósito:** Optimización mediante Algoritmo Genético

**Clase Principal:**
```python
class OptimizadorGenetico:
    def __init__(self):
        self.tam_poblacion = 150
        self.num_generaciones = 500
        self.prob_cruce = 0.8
        self.prob_mutacion = 0.1
        self.indices_inmutables = set()
    
    # Inicialización
    def generar_poblacion_inicial(self, df):
        """Genera población inicial"""
    
    # Operadores
    def seleccion_torneo(self, poblacion, fitness):
        """Selecciona padres por torneo"""
    
    def cruce_un_punto(self, padre1, padre2):
        """Cruza dos individuos"""
    
    def mutacion_intercambio(self, individuo):
        """Muta individuo"""
    
    # Evolución
    def evolucionar(self, df):
        """Ejecuta algoritmo genético"""
```

**Flujo de Ejecución:**
1. Cargar horario pre-asignado
2. Cargar índices inmutables
3. Generar población inicial
4. Evolucionar durante N generaciones:
   - Selección por torneo
   - Cruce (respetando inmutables)
   - Mutación (respetando inmutables)
   - Evaluación de fitness
   - Reemplazo con elitismo
5. Retornar mejor individuo
6. Análisis de métricas
7. Guardar resultado

**Archivos de Entrada:**
- `datos_estructurados/00_Horario_PreAsignado_P1.csv`
- `datos_estructurados/indices_inmutables_p1.json`

**Archivos de Salida:**
- `datos_estructurados/06_Horario_Optimizado_Genetico.csv`
- `comparativas/03_inicial_vs_genetico/metricas_movimientos.csv`

### 2.6 corregir_prioridades.py

**Propósito:** Corrección post-optimización de PRIORIDAD 1

**Funciones Principales:**
```python
def cargar_preferencias():
    """Carga preferencias de profesores"""

def identificar_violaciones(df, preferencias):
    """Identifica clases P1 en salón incorrecto"""

def corregir_violaciones(df, violaciones):
    """Corrige todas las violaciones"""

def verificar_cumplimiento(df, preferencias):
    """Verifica 100% cumplimiento"""
```

**Flujo de Ejecución:**
1. Cargar horario optimizado
2. Cargar preferencias
3. Identificar violaciones de P1
4. Si hay violaciones:
   - Ordenar por prioridad
   - Corregir una por una
   - Resolver conflictos
5. Verificar 100% cumplimiento
6. Guardar horario corregido

**Uso:**
```bash
python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv
```

### 2.7 utils_restricciones.py

**Propósito:** Funciones de utilidad para validación y restricciones

**Funciones Principales:**
```python
def validar_asignacion(clase, salon, df):
    """Verifica si asignación es válida"""

def obtener_salones_validos(clase, salones_teoria, laboratorios):
    """Retorna salones válidos para clase"""

def calcular_distancia(salon1, salon2):
    """Calcula distancia entre salones"""

def verificar_conflicto_temporal(clase1, clase2, asignacion):
    """Verifica si hay conflicto temporal"""

def pre_asignar_prioritarias(df, config, preferencias, ...):
    """Pre-asigna clases prioritarias (legacy)"""
```

**Uso:**
- Importado por todos los optimizadores
- Proporciona funciones comunes de validación
- Mantiene lógica de restricciones centralizada

### 2.8 ejecutar_todos.py

**Propósito:** Script maestro de orquestación

**Flujo:**
```python
def main():
    # 1. Pre-asignación
    ejecutar("pre_asignar_p1.py")
    
    # 2. Greedy
    ejecutar("optimizador_greedy.py")
    ejecutar("corregir_prioridades.py", "04_Horario_Optimizado_Greedy.csv")
    
    # 3. ML
    ejecutar("optimizador_ml.py")
    ejecutar("corregir_prioridades.py", "05_Horario_Optimizado_ML.csv")
    
    # 4. Genético
    ejecutar("optimizador_genetico.py")
    ejecutar("corregir_prioridades.py", "06_Horario_Optimizado_Genetico.csv")
    
    # 5. Comparativas
    ejecutar("generar_comparativa_completa.py")
    
    # 6. Resumen
    mostrar_resumen()
```

**Características:**
- Ejecución secuencial de todo el pipeline
- Medición de tiempos
- Logging de salidas
- Manejo de errores

### 2.9 generar_comparativa_completa.py

**Propósito:** Generación de reportes y gráficos

**Funciones Principales:**
```python
def generar_excel_formato(csv_file, output_file):
    """Genera Excel con formato bonito"""

def generar_excel_comparativo(dfs):
    """Genera Excel con todos los optimizadores"""

def generar_graficos(dfs):
    """Genera gráficos de análisis"""

def verificar_prioridad_1(dfs, preferencias):
    """Verifica cumplimiento P1"""
```

**Salidas Generadas:**
- Excels formateados por optimizador
- Excel comparativo (todos juntos)
- Gráficos de tiempos, cumplimiento, métricas
- Excel consolidado con resumen

## 3. Estructuras de Datos

### 3.1 Horario (DataFrame)

```python
# Estructura de datos principal
df = pd.DataFrame({
    'Dia': str,              # Lunes, Martes, ...
    'Bloque_Horario': int,   # 0700, 0800, ...
    'Materia': str,          # Nombre de materia
    'Grupo': str,            # 1527A, 2514/B, ...
    'Profesor': str,         # PROFESOR 3, ...
    'Salon': str,            # FF1, LBD, ...
    'Es_Invalido': int,      # 0 o 1
    'Tipo_Salon': str,       # Teoría, Laboratorio
    'Piso': int              # 0 o 1
})
```

### 3.2 Preferencias (JSON)

```json
{
  "PROFESOR 3": {
    "materias": {
      "LENGUAJES Y AUTÓMATAS I": {
        "salon_teoria": "FFA",
        "prioridad_teoria": "Prioritario",
        "salon_lab": "Sin preferencia",
        "prioridad_lab": "Normal"
      }
    }
  }
}
```

### 3.3 Índices Inmutables (JSON)

```json
{
  "indices": [12, 45, 67, ...],
  "total": 88,
  "timestamp": "2025-12-21T11:00:00",
  "version": "1.0"
}
```

### 3.4 Solución (Dict)

```python
# Representación interna de solución
solucion = {
    0: 'FF1',    # Clase 0 → Salón FF1
    1: 'LBD',    # Clase 1 → Salón LBD
    2: 'FF2',    # Clase 2 → Salón FF2
    ...
}
```

## 4. Patrones de Diseño

### 4.1 Strategy Pattern

Diferentes optimizadores implementan la misma interfaz:

```python
class OptimizadorBase:
    def optimizar(self, df_inicial):
        raise NotImplementedError

class OptimizadorGreedy(OptimizadorBase):
    def optimizar(self, df_inicial):
        # Implementación Greedy
        
class OptimizadorML(OptimizadorBase):
    def optimizar(self, df_inicial):
        # Implementación ML
```

### 4.2 Template Method

Estructura común de optimización:

```python
def optimizar(self, df):
    # 1. Cargar datos
    self.cargar_configuracion()
    
    # 2. Inicializar
    solucion = self.inicializar()
    
    # 3. Optimizar (método específico)
    solucion = self.algoritmo_especifico(solucion)
    
    # 4. Post-procesar
    solucion = self.post_procesar(solucion)
    
    # 5. Guardar
    self.guardar_resultado(solucion)
```

### 4.3 Facade Pattern

`ejecutar_todos.py` proporciona interfaz simple:

```python
# En lugar de ejecutar 7 scripts manualmente
python3 ejecutar_todos.py  # Un solo comando
```

## 5. Convenciones de Código

### 5.1 Nomenclatura

**Archivos:**
- `snake_case.py` para scripts
- `PascalCase` para clases
- Números prefijos para orden (01_, 02_, ...)

**Variables:**
- `snake_case` para variables y funciones
- `UPPER_CASE` para constantes
- `_private` para métodos privados

**Clases:**
- `PascalCase` para nombres de clase
- Nombres descriptivos (OptimizadorGreedy, no OG)

### 5.2 Documentación

**Docstrings:**
```python
def funcion(param1, param2):
    """
    Descripción breve de la función
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
    
    Returns:
        Descripción del valor de retorno
    """
```

**Comentarios:**
```python
# Comentarios explicativos para lógica compleja
# No comentar lo obvio
```

### 5.3 Manejo de Errores

```python
try:
    # Operación que puede fallar
    resultado = operacion_riesgosa()
except FileNotFoundError:
    print("❌ Archivo no encontrado")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    raise
```

## 6. Dependencias

### 6.1 Dependencias Externas

```
pandas>=1.5.0          # Manipulación de datos
openpyxl>=3.0.0        # Excel I/O
matplotlib>=3.5.0      # Gráficos
seaborn>=0.12.0        # Visualización
scikit-learn>=1.0.0    # Machine Learning
```

### 6.2 Dependencias Estándar

```python
import json            # Configuración
import random          # Aleatoriedad
import sys             # Sistema
import subprocess      # Ejecución de scripts
from pathlib import Path  # Manejo de rutas
from datetime import datetime  # Timestamps
```

## 7. Testing y Validación

### 7.1 Validación de Datos

```python
def validar_horario(df):
    """Valida estructura de horario"""
    assert 'Dia' in df.columns
    assert 'Salon' in df.columns
    assert len(df) == 680
    # ...
```

### 7.2 Verificación de Invariantes

```python
def verificar_invariantes(df, indices_inmutables, preferencias):
    """Verifica invariantes del sistema"""
    # Invariante 1: P1 al 100%
    assert verificar_p1(df, preferencias) == 100.0
    
    # Invariante 2: Sin conflictos temporales
    assert not tiene_conflictos(df)
    
    # Invariante 3: Salones válidos
    assert todos_salones_validos(df)
```

## 8. Optimizaciones de Rendimiento

### 8.1 Caching

```python
@lru_cache(maxsize=1000)
def calcular_distancia(salon1, salon2):
    """Cachea cálculos de distancia"""
    # ...
```

### 8.2 Vectorización

```python
# En lugar de loops
for i in range(len(df)):
    df.loc[i, 'Piso'] = obtener_piso(df.loc[i, 'Salon'])

# Usar operaciones vectorizadas
df['Piso'] = df['Salon'].apply(obtener_piso)
```

### 8.3 Paralelización

```python
# En Random Forest
RandomForestClassifier(n_jobs=-1)  # Usar todos los cores
```

## 9. Extensibilidad

### 9.1 Agregar Nuevo Optimizador

1. Crear `optimizador_nuevo.py`
2. Implementar interfaz estándar:
   ```python
   class OptimizadorNuevo:
       def __init__(self):
           self.indices_inmutables = cargar_inmutables()
       
       def optimizar(self, df):
           # Implementación
   ```
3. Agregar a `ejecutar_todos.py`
4. Agregar a `generar_comparativa_completa.py`

### 9.2 Agregar Nueva Restricción

1. Definir en `utils_restricciones.py`:
   ```python
   def verificar_nueva_restriccion(clase, salon):
       # Lógica de verificación
   ```
2. Integrar en función objetivo de optimizadores
3. Actualizar documentación

## 10. Deployment y Producción

### 10.1 Instalación

```bash
git clone <repo>
cd Sistema-Salones-ISC
pip install -r requirements.txt
```

### 10.2 Ejecución

```bash
# Configurar
python3 configurador_materias.py

# Ejecutar pipeline completo
python3 ejecutar_todos.py

# O ejecutar componentes individuales
python3 pre_asignar_p1.py
python3 optimizador_greedy.py
# ...
```

### 10.3 Monitoreo

```bash
# Ver logs
tail -f ejecucion_final.log

# Verificar resultados
ls -lh datos_estructurados/
ls -lh comparativas/final/
```

## 11. Mantenimiento

### 11.1 Actualización de Preferencias

1. Abrir `configurador_materias.py`
2. Modificar preferencias
3. Guardar
4. Re-ejecutar pipeline

### 11.2 Debugging

```python
# Activar modo debug
DEBUG = True

if DEBUG:
    print(f"Debug: {variable}")
    import pdb; pdb.set_trace()
```

### 11.3 Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='sistema.log'
)
```

## 12. Conclusiones

El sistema está diseñado con:

✅ **Modularidad:** Componentes independientes y reutilizables  
✅ **Escalabilidad:** Fácil agregar nuevos optimizadores  
✅ **Mantenibilidad:** Código limpio y bien documentado  
✅ **Robustez:** Validación en múltiples capas  
✅ **Extensibilidad:** Patrones de diseño facilitan extensiones  

Es un sistema **production-ready** para uso real en el Instituto Tecnológico de Ciudad Madero.

## Referencias

1. Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.

2. Gamma, E., et al. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

3. McConnell, S. (2004). *Code Complete* (2nd ed.). Microsoft Press.
