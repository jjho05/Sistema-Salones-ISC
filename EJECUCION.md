# FASE 6: Ejecución y Experimentos - Guía Completa

## Fecha de Creación
23 de diciembre de 2025

---

## 📋 Tabla de Contenidos

1. [Preparación del Entorno](#1-preparación-del-entorno)
2. [Opciones de Ejecución](#2-opciones-de-ejecución)
3. [Ejecución Paso a Paso](#3-ejecución-paso-a-paso)
4. [Logs y Salidas](#4-logs-y-salidas)
5. [Archivos Generados](#5-archivos-generados)
6. [Tiempos de Ejecución](#6-tiempos-de-ejecución)
7. [Checklist de Verificación](#7-checklist-de-verificación)
8. [Troubleshooting](#8-troubleshooting)
9. [Experimentos Reproducibles](#9-experimentos-reproducibles)

---

## 1. Preparación del Entorno

### 1.1 Verificar Instalación

```bash
# Verificar Python
python3 --version
# Debe mostrar: Python 3.8 o superior

# Verificar dependencias
python3 -c "import pandas, sklearn, matplotlib; print('✅ Dependencias OK')"
```

### 1.2 Estructura de Directorios

Verificar que existen las carpetas necesarias:

```bash
# Desde la raíz del proyecto
ls -la datos_estructurados/
ls -la comparativas/
ls -la comparativas/graficos/
```

Si faltan, crearlas:

```bash
mkdir -p datos_estructurados
mkdir -p comparativas/graficos
```

### 1.3 Datos de Entrada

Verificar que existe el horario inicial:

```bash
ls -lh datos_estructurados/01_Horario_Inicial.csv
```

**Formato esperado del CSV:**
```csv
Clave,Materia,Grupo,Profesor,Tipo,Estudiantes,Dia,Hora,Salon
SCD1008,Fundamentos de Programación,1501,Juan Pérez,T,30,Lunes,07:00,A101
...
```

---

## 2. Opciones de Ejecución

### Opción 1: Ejecución Completa (Recomendado)

**Comando:**
```bash
python3 ejecutar_todos.py
```

**Ejecuta automáticamente:**
1. Pre-asignación de PRIORIDAD 1
2. Optimizador Greedy + Hill Climbing
3. Optimizador Machine Learning
4. Optimizador Genético
5. Corrección de prioridades (todos)
6. Generación de comparativas

**Tiempo estimado:** ~2-3 minutos

**Ventajas:**
- ✅ Todo en un solo comando
- ✅ Garantiza orden correcto
- ✅ Genera comparativas automáticamente

---

### Opción 2: Ejecución Paso a Paso

Para mayor control o debugging:

```bash
# Paso 1: Pre-asignación P1
python3 pre_asignar_p1.py

# Paso 2: Ejecutar optimizador específico
python3 optimizador_greedy.py
# O
python3 optimizador_ml.py
# O
python3 optimizador_genetico.py

# Paso 3: Corregir prioridades (si necesario)
python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv

# Paso 4: Generar comparativas
python3 generar_comparativa_completa.py
```

**Ventajas:**
- ✅ Control fino de cada paso
- ✅ Útil para debugging
- ✅ Permite ejecutar solo un optimizador

---

### Opción 3: Configuración Inicial

Si es la primera vez o necesitas reconfigurar:

```bash
python3 configurador_materias.py
```

**Abre interfaz gráfica para:**
- Configurar materias y características
- Definir preferencias de profesores (P1, P2, P3)
- Asignar grupos de primer semestre
- Generar horario inicial

---

## 3. Ejecución Paso a Paso Detallada

### 3.1 Pre-asignación de PRIORIDAD 1

**Comando:**
```bash
python3 pre_asignar_p1.py
```

**Qué hace:**
- Lee `01_Horario_Inicial.csv`
- Identifica clases con preferencias P1
- Asigna forzosamente esos salones
- Marca clases como "inmutables"
- Genera `00_Horario_PreAsignado_P1.csv`

**Salida esperada:**
```
============================================================
PRE-ASIGNACIÓN DE PRIORIDAD 1
============================================================

Cargando horario inicial...
✅ Horario cargado: 680 clases

Identificando preferencias P1...
✅ Encontradas 85 preferencias P1

Pre-asignando salones...
✅ Pre-asignadas 85 clases

Guardando índices inmutables...
✅ Guardado: indices_inmutables_p1.json

Guardando horario pre-asignado...
✅ Guardado: 00_Horario_PreAsignado_P1.csv

Cumplimiento P1: 100.0%
============================================================
```

**Archivos generados:**
- `datos_estructurados/00_Horario_PreAsignado_P1.csv`
- `datos_estructurados/indices_inmutables_p1.json`

---

### 3.2 Optimizador Greedy + Hill Climbing

**Comando:**
```bash
python3 optimizador_greedy.py
```

**Qué hace:**
1. Carga horario pre-asignado
2. Carga índices inmutables
3. **Fase Greedy:** Construye solución inicial
4. **Fase Hill Climbing:** Mejora iterativamente
5. Guarda resultado optimizado

**Salida esperada:**
```
============================================================
OPTIMIZADOR GREEDY + HILL CLIMBING
============================================================

Cargando horario pre-asignado...
✅ Horario cargado: 680 clases

Cargando índices inmutables...
✅ Índices inmutables cargados: 85 clases

FASE 1: Construcción Greedy
----------------------------
Ordenando clases por profesor...
Asignando salones...
Progreso: [████████████████████] 100%

Solución inicial:
  Movimientos: 357
  Cambios de piso: 287
  Distancia: 2847
  Energía: 5181

FASE 2: Hill Climbing
---------------------
Iteración 0: Energía = 5181
Iteración 50: Energía = 4920
Iteración 100: Energía = 4756
Iteración 150: Energía = 4650
Iteración 200: Energía = 4620
Iteración 250: Energía = 4615

Convergencia alcanzada (sin mejora en 50 iteraciones)

Solución final:
  Movimientos: 314
  Cambios de piso: 206
  Distancia: 1951
  Energía: 4615

Mejora: 10.9%

Guardando resultado...
✅ Guardado: 04_Horario_Optimizado_Greedy.csv

Tiempo total: 29.3 segundos
============================================================
```

**Archivos generados:**
- `datos_estructurados/04_Horario_Optimizado_Greedy.csv`
- `comparativas/04_inicial_vs_greedy/metricas_movimientos.csv`
- `comparativas/04_inicial_vs_greedy/graficos/`

---

### 3.3 Optimizador Machine Learning

**Comando:**
```bash
python3 optimizador_ml.py
```

**Qué hace:**
1. Carga horario pre-asignado
2. Extrae features de cada clase
3. Entrena Random Forest
4. Predice asignaciones óptimas
5. Guarda resultado

**Salida esperada:**
```
============================================================
OPTIMIZADOR MACHINE LEARNING
============================================================

Cargando horario pre-asignado...
✅ Horario cargado: 680 clases

Extrayendo features...
Features extraídas: 15 por clase
✅ Features: (680, 15)

Entrenando Random Forest...
  n_estimators: 100
  max_depth: 20
  min_samples_split: 5

Entrenamiento completado
Precisión (validación cruzada): 94.2%

Prediciendo asignaciones...
Progreso: [████████████████████] 100%

Resultado:
  Movimientos: 365
  Cambios de piso: 223
  Distancia: 1821
  Energía: 5234

Guardando resultado...
✅ Guardado: 05_Horario_Optimizado_ML.csv

Tiempo total: 15.8 segundos
============================================================
```

**Archivos generados:**
- `datos_estructurados/05_Horario_Optimizado_ML.csv`
- `comparativas/05_inicial_vs_ml/`

---

### 3.4 Optimizador Genético

**Comando:**
```bash
python3 optimizador_genetico.py
```

**Qué hace:**
1. Carga horario pre-asignado
2. Crea población inicial (100 individuos)
3. Evoluciona durante 200 generaciones
4. Aplica selección, cruce y mutación
5. Guarda mejor solución

**Salida esperada:**
```
============================================================
OPTIMIZADOR GENÉTICO
============================================================

Cargando horario pre-asignado...
✅ Horario cargado: 680 clases

Configuración:
  Población: 100
  Generaciones: 200
  Prob. cruce: 0.8
  Prob. mutación: 0.1
  Elitismo: 5

Creando población inicial...
✅ Población creada

Evolución:
Gen 0:   Mejor=81962  Promedio=82534  Diversidad=0.45
Gen 10:  Mejor=81967  Promedio=82401  Diversidad=0.42
Gen 20:  Mejor=81962  Promedio=82298  Diversidad=0.38
...
Gen 190: Mejor=81962  Promedio=82156  Diversidad=0.18
Gen 200: Mejor=81962  Promedio=82134  Diversidad=0.15

Convergencia alcanzada

Mejor solución:
  Movimientos: 378
  Cambios de piso: 286
  Distancia: 2413
  Fitness: 0.0476

Guardando resultado...
✅ Guardado: 06_Horario_Optimizado_Genetico.csv

Tiempo total: 73.9 segundos
============================================================
```

**Archivos generados:**
- `datos_estructurados/06_Horario_Optimizado_Genetico.csv`
- `comparativas/06_inicial_vs_genetico/`

---

### 3.5 Corrección de Prioridades

**Comando:**
```bash
python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv
```

**Qué hace:**
- Verifica cumplimiento de P1
- Corrige si hay violaciones
- Actualiza archivo

**Salida esperada:**
```
============================================================
CORRECCIÓN DE PRIORIDADES
============================================================

Archivo: 04_Horario_Optimizado_Greedy.csv

Verificando P1...
✅ P1: 100% (85/85)

Verificando P2...
⚠️  P2: 87% (156/180)

Verificando P3...
⚠️  P3: 72% (43/60)

No se requieren correcciones de P1
============================================================
```

---

### 3.6 Generar Comparativas

**Comando:**
```bash
python3 generar_comparativa_completa.py
```

**Qué hace:**
- Lee todos los horarios optimizados
- Calcula métricas de cada uno
- Genera tablas comparativas
- Crea gráficos
- Genera Excel consolidado

**Salida esperada:**
```
============================================================
GENERACIÓN DE COMPARATIVAS
============================================================

Cargando horarios...
✅ Inicial
✅ Greedy
✅ ML
✅ Genético

Calculando métricas...
✅ Movimientos
✅ Cambios de piso
✅ Distancias
✅ Cumplimiento P1/P2/P3

Generando gráficos...
✅ grafico_tiempos.png
✅ grafico_cumplimiento.png
✅ grafico_metricas.png
✅ grafico_mejoras.png

Generando Excel consolidado...
✅ comparativa_completa.xlsx

Tiempo total: 3.2 segundos
============================================================
```

**Archivos generados:**
- `comparativas/comparativa_completa.xlsx`
- `comparativas/graficos/*.png`

---

## 4. Logs y Salidas

### 4.1 Niveles de Log

El sistema usa diferentes símbolos:

| Símbolo | Significado | Ejemplo |
|---------|-------------|---------|
| ✅ | Éxito | `✅ Horario cargado` |
| ⚠️  | Advertencia | `⚠️  P2: 87%` |
| ❌ | Error | `❌ Archivo no encontrado` |
| 📊 | Información | `📊 Métricas calculadas` |
| 🔄 | En progreso | `🔄 Procesando...` |

### 4.2 Interpretar Logs

**Ejemplo de log exitoso:**
```
✅ Horario cargado: 680 clases
✅ Índices inmutables cargados: 85 clases
✅ Guardado: 04_Horario_Optimizado_Greedy.csv
```
→ Todo funcionó correctamente

**Ejemplo de log con advertencias:**
```
✅ P1: 100% (85/85)
⚠️  P2: 87% (156/180)
⚠️  P3: 72% (43/60)
```
→ P1 perfecto, P2 y P3 parcialmente cumplidos (esperado)

**Ejemplo de log con error:**
```
❌ Error: Archivo no encontrado
   Ruta: datos_estructurados/01_Horario_Inicial.csv
```
→ Falta archivo de entrada

---

## 5. Archivos Generados

### 5.1 Estructura de Salidas

```
datos_estructurados/
├── 00_Horario_PreAsignado_P1.csv       # Pre-asignación P1
├── 04_Horario_Optimizado_Greedy.csv    # Resultado Greedy
├── 05_Horario_Optimizado_ML.csv        # Resultado ML
├── 06_Horario_Optimizado_Genetico.csv  # Resultado Genético
└── indices_inmutables_p1.json          # Índices protegidos

comparativas/
├── comparativa_completa.xlsx           # Excel consolidado
├── 04_inicial_vs_greedy/
│   ├── metricas_movimientos.csv
│   └── graficos/
├── 05_inicial_vs_ml/
│   └── ...
└── 06_inicial_vs_genetico/
    └── ...
```

### 5.2 Formato de Archivos CSV

**Horarios optimizados:**
```csv
Clave,Materia,Grupo,Profesor,Tipo,Estudiantes,Dia,Hora,Salon
SCD1008,Fundamentos,1501,Juan Pérez,T,30,Lunes,07:00,A101
```

**Métricas:**
```csv
Optimizador,Movimientos,Cambios_Piso,Distancia,P1,P2,P3,Tiempo
Greedy,314,206,1951,100,87,72,29.3
```

---

## 6. Tiempos de Ejecución

### 6.1 Tiempos Esperados

| Paso | Tiempo | Descripción |
|------|--------|-------------|
| **Pre-asignación P1** | ~2s | Rápido |
| **Greedy + HC** | ~30s | Medio |
| **Machine Learning** | ~16s | Rápido |
| **Algoritmo Genético** | ~74s | Lento |
| **Corrección** | ~1s | Muy rápido |
| **Comparativas** | ~3s | Rápido |
| **TOTAL (todos)** | ~2-3 min | - |

### 6.2 Factores que Afectan el Tiempo

- **Tamaño del problema:** 680 clases, 21 salones
- **CPU:** Más cores = más rápido (paralelización en ML y Genético)
- **RAM:** Mínimo 4GB recomendado
- **Disco:** SSD más rápido que HDD

---

## 7. Checklist de Verificación

### 7.1 Antes de Ejecutar

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Carpetas creadas (`datos_estructurados/`, `comparativas/`)
- [ ] Archivo inicial existe (`01_Horario_Inicial.csv`)
- [ ] Formato CSV correcto

### 7.2 Durante la Ejecución

- [ ] No hay errores en consola
- [ ] Logs muestran ✅ (no ❌)
- [ ] Tiempos dentro de lo esperado
- [ ] Uso de memoria < 2GB

### 7.3 Después de Ejecutar

- [ ] Archivos CSV generados
- [ ] P1 = 100% en todos los optimizadores
- [ ] Excel comparativo generado
- [ ] Gráficos PNG creados
- [ ] Métricas razonables (movimientos < 400)

---

## 8. Troubleshooting

### 8.1 Error: "Archivo no encontrado"

**Síntoma:**
```
❌ Error: Archivo no encontrado
   Ruta: datos_estructurados/01_Horario_Inicial.csv
```

**Solución:**
```bash
# Verificar que existe
ls datos_estructurados/01_Horario_Inicial.csv

# Si no existe, generarlo con configurador
python3 configurador_materias.py
```

---

### 8.2 Error: "ModuleNotFoundError"

**Síntoma:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solución:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar manualmente
pip install pandas scikit-learn matplotlib openpyxl
```

---

### 8.3 Error: "MemoryError"

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Solución:**
- Cerrar otros programas
- Aumentar RAM disponible
- Reducir tamaño de población en Genético:
  ```python
  # En optimizador_genetico.py
  POBLACION = 50  # En lugar de 100
  ```

---

### 8.4 Advertencia: "P1 < 100%"

**Síntoma:**
```
⚠️  P1: 95% (81/85)
```

**Solución:**
```bash
# Ejecutar corrección
python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv

# Verificar resultado
python3 verificar_cumplimiento.py datos_estructurados/04_Horario_Optimizado_Greedy.csv
```

---

### 8.5 Ejecución Muy Lenta

**Síntoma:**
- Greedy tarda > 2 minutos
- Genético tarda > 5 minutos

**Solución:**
```python
# Reducir iteraciones en optimizador_greedy.py
MAX_ITERACIONES = 500  # En lugar de 1000

# Reducir generaciones en optimizador_genetico.py
GENERACIONES = 100  # En lugar de 200
```

---

### 8.6 Gráficos No Se Generan

**Síntoma:**
```
⚠️  No se pudieron generar gráficos
```

**Solución:**
```bash
# Verificar matplotlib
python3 -c "import matplotlib; print('OK')"

# Si falla, reinstalar
pip install --upgrade matplotlib

# En macOS, puede requerir:
pip install --upgrade matplotlib --force-reinstall
```

---

## 9. Experimentos Reproducibles

### 9.1 Fijar Semilla Aleatoria

Para resultados reproducibles:

```python
# Agregar al inicio de cada optimizador
import random
import numpy as np

random.seed(42)
np.random.seed(42)
```

### 9.2 Ejecutar Múltiples Corridas

Script para 30 corridas:

```bash
#!/bin/bash
# run_experiments.sh

for i in {1..30}
do
    echo "Corrida $i/30"
    python3 optimizador_greedy.py
    mv datos_estructurados/04_Horario_Optimizado_Greedy.csv \
       resultados/greedy_run_$i.csv
done
```

### 9.3 Recolectar Estadísticas

```python
# analizar_corridas.py
import pandas as pd
import glob

# Leer todas las corridas
archivos = glob.glob('resultados/greedy_run_*.csv')
resultados = []

for archivo in archivos:
    df = pd.read_csv(archivo)
    movimientos = calcular_movimientos(df)
    resultados.append(movimientos)

# Estadísticas
print(f"Media: {np.mean(resultados)}")
print(f"Std: {np.std(resultados)}")
print(f"Min: {np.min(resultados)}")
print(f"Max: {np.max(resultados)}")
```

---

## 📊 Resumen Ejecutivo

### Comandos Esenciales

```bash
# Ejecución completa (recomendado)
python3 ejecutar_todos.py

# Ejecución paso a paso
python3 pre_asignar_p1.py
python3 optimizador_greedy.py
python3 optimizador_ml.py
python3 optimizador_genetico.py
python3 generar_comparativa_completa.py
```

### Tiempos Totales

- **Ejecución completa:** 2-3 minutos
- **Solo Greedy:** 30 segundos
- **Solo ML:** 16 segundos
- **Solo Genético:** 74 segundos

### Archivos Clave

- **Entrada:** `datos_estructurados/01_Horario_Inicial.csv`
- **Salidas:** `datos_estructurados/04_*.csv`, `05_*.csv`, `06_*.csv`
- **Comparativa:** `comparativas/comparativa_completa.xlsx`

---

**Autor:** Jesús Olvera  
**Fecha:** 23 de diciembre de 2025  
**Versión:** 1.0
