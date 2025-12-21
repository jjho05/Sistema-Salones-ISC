# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [2.0.0] - 2025-12-21

### 🎉 Versión Mayor - Sistema de Prioridades Completo

Esta versión representa una reescritura completa del sistema de optimización con enfoque en garantizar 100% de cumplimiento de PRIORIDAD 1.

### Agregado

#### Sistema de Prioridades Jerárquico
- **Pre-asignación forzada** (`pre_asignar_p1.py`): Nuevo módulo que garantiza 100% P1 antes de optimización
- **Índices inmutables**: Sistema de protección que marca clases P1 como no modificables
- **Corrección post-optimización** (`corregir_prioridades.py`): Verificación y corrección automática después de cada optimizador
- **Triple capa de defensa**: Pre-asignación → Protección → Corrección

#### Nuevos Optimizadores
- **Optimizador Greedy + Hill Climbing** (`optimizador_greedy.py`): 
  - Construcción voraz inicial
  - Refinamiento mediante búsqueda local
  - Tiempo: ~30s, Calidad: Alta
  
- **Optimizador Machine Learning** (`optimizador_ml.py`):
  - Random Forest para predicción de salones
  - Gradient Boosting para calidad de asignación
  - Tiempo: ~16s, Calidad: Muy Alta
  
- **Optimizador Genético** (`optimizador_genetico.py`):
  - Población de 150 individuos
  - 500 generaciones
  - Operadores adaptativos
  - Tiempo: ~74s, Calidad: Alta (exploración amplia)

#### Sistema de Reportes
- **Excels formateados**: Formato "pivot table" con estilo profesional
  - Encabezado azul oscuro (#4472C4)
  - Filas alternadas grises (#D9E1F2)
  - Bordes negros, texto ajustado
  
- **Excel comparativo**: `Comparativa_Todos_Optimizadores.xlsx`
  - 5 optimizadores lado a lado (Inicial, Profesor, Greedy, ML, Genético)
  - 741 filas comparativas
  - Agrupado por Grupo/Materia
  
- **Gráficos profesionales**:
  - Tiempos de ejecución
  - Cumplimiento PRIORIDAD 1 (100% todos)
  - Comparativa de métricas
  - Mejora porcentual vs inicial

#### Documentación Técnica Completa
- `docs/00_CONTEXTO_PROBLEMA.md`: Formulación matemática, NP-completitud
- `docs/01_TEORIA_MATEMATICA.md`: Teoremas, complejidad, demostraciones
- `docs/02_ALGORITMO_GREEDY.md`: Greedy + Hill Climbing detallado
- `docs/03_ALGORITMO_ML.md`: Machine Learning con Random Forest y GB
- `docs/04_ALGORITMO_GENETICO.md`: Algoritmo evolutivo completo
- `docs/05_PRE_PROCESAMIENTO.md`: Pre-asignación P1
- `docs/06_POST_PROCESAMIENTO.md`: Corrección post-optimización
- `docs/07_ARQUITECTURA_CODIGO.md`: Arquitectura del sistema
- `docs/GUIA_USO.md`: Guía completa de usuario

#### Automatización
- **Script maestro** (`ejecutar_todos.py`):
  - Ejecuta todo el pipeline automáticamente
  - Pre-asignación → Optimizadores → Corrección → Comparativas
  - Logging de tiempos y resultados
  - Resumen final consolidado

### Cambiado

#### Configurador de Materias
- **Corrección de preferencias**: PROFESOR 3 ahora usa FFA (antes FF3 erróneamente)
- **Validación mejorada**: Verificación de consistencia en preferencias
- **Interfaz actualizada**: Mejor UX para configuración de prioridades

#### Optimizadores Existentes
- **Protección de P1**: Todos los optimizadores ahora respetan índices inmutables
- **Carga de horario**: Usan `00_Horario_PreAsignado_P1.csv` como entrada
- **Salidas numeradas**: 
  - 04_Horario_Optimizado_Greedy.csv
  - 05_Horario_Optimizado_ML.csv
  - 06_Horario_Optimizado_Genetico.csv

#### Sistema de Archivos
- **Estructura reorganizada**:
  ```
  datos_estructurados/
  ├── 00_Horario_PreAsignado_P1.csv (nuevo)
  ├── 01_Horario_Inicial.csv
  ├── 02_Horario_Optimizado_Profesor.csv
  ├── 04_Horario_Optimizado_Greedy.csv (renumerado)
  ├── 05_Horario_Optimizado_ML.csv (renumerado)
  ├── 06_Horario_Optimizado_Genetico.csv (renumerado)
  └── indices_inmutables_p1.json (nuevo)
  ```

#### Comparativas
- **Carpeta final**: `comparativas/final/` para resultados consolidados
- **Gráficos actualizados**: 4 gráficos clave en lugar de 15
- **Excel consolidado**: Resumen de todas las métricas

### Eliminado

#### Archivos Obsoletos
- ❌ PDFs antiguos de comparativas (01-15)
- ❌ PNGs antiguos de gráficos individuales
- ❌ `comparativas/excel_comparativo/` (carpeta completa)
- ❌ Excels temporales en `datos_estructurados/`:
  - `Horario_Inicial_Formateado.xlsx`
  - `Horario_Optimizado_Formateado.xlsx`
- ❌ CSVs obsoletos:
  - `03_Horario_Optimizado_ML.csv` (renumerado a 05)
  - `04_Horario_Optimizado_Genetico.csv` (renumerado a 06)

#### Código Legacy
- ❌ Lógica de penalización de P1 en función objetivo (reemplazado por pre-asignación)
- ❌ Intentos de corrección dentro de optimizadores (movido a post-procesamiento)
- ❌ Gráfico de heatmap (no era útil)

### Corregido

#### Bugs Críticos
- 🐛 **PRIORIDAD 1 < 100%**: Ahora garantizado al 100% en todos los optimizadores
  - Greedy: 98/98 (100%)
  - ML: 87/87 (100%)
  - Genético: 82/82 (100%)

- 🐛 **Conflictos de preferencias**: Sistema de resolución de conflictos mejorado
  - Desplazamiento en cadena
  - Priorización correcta
  - Manejo de casos especiales

- 🐛 **Grupos 11xx**: Restaurados después de clarificación (son clases online pero necesitan asignación)

- 🐛 **Salón FF3 vs FFA**: Corregido para PROFESOR 3

#### Mejoras de Rendimiento
- ⚡ Greedy: 43.7s → 29.3s (33% más rápido)
- ⚡ ML: 17.2s → 15.8s (8% más rápido)
- ⚡ Genético: Optimizado a 73.9s

#### Calidad de Soluciones
- 📈 Movimientos profesores: -12% (Greedy)
- 📈 Cambios de piso: -28% (Greedy)
- 📈 Distancia total: -31% (Greedy)

### Seguridad

- 🔒 **Validación de entrada**: Verificación de archivos CSV antes de procesar
- 🔒 **Protección de P1**: Triple capa de defensa contra violaciones
- 🔒 **Verificación automática**: Assertions en puntos críticos

## [1.5.0] - 2025-12-20

### Agregado
- Sistema de prioridades inicial (PRIORIDAD 1, 2, 3)
- Preferencias de profesores en JSON
- Configuración de materias

### Cambiado
- Migración de Excel a CSV para mejor rendimiento
- Estructura de datos optimizada

## [1.0.0] - 2025-12-15

### Agregado
- Versión inicial del sistema
- Optimizador básico del profesor
- Configurador de materias (GUI)
- Análisis de movimientos

---

## Tipos de Cambios

- `Agregado` para funcionalidades nuevas
- `Cambiado` para cambios en funcionalidades existentes
- `Obsoleto` para funcionalidades que serán eliminadas
- `Eliminado` para funcionalidades eliminadas
- `Corregido` para corrección de bugs
- `Seguridad` para vulnerabilidades

## Versionado

- **MAJOR** (X.0.0): Cambios incompatibles con versiones anteriores
- **MINOR** (0.X.0): Nuevas funcionalidades compatibles
- **PATCH** (0.0.X): Correcciones de bugs compatibles

## Próximas Versiones

### [2.1.0] - Planificado

#### Agregado
- Implementación de PRIORIDAD 2 (Consistencia de Grupos)
- Implementación de PRIORIDAD 3 (Grupos de Primer Semestre)
- Aplicación web (BETA) para visualización de horarios
- API REST para integración externa

#### Mejorado
- Optimización de tiempos de ejecución
- Interfaz gráfica mejorada
- Exportación a más formatos (PDF, iCal)

### [3.0.0] - Futuro

#### Agregado
- Soporte multi-campus
- Optimización de horarios (no solo salones)
- Sistema de notificaciones
- Dashboard web interactivo
- Integración con sistemas institucionales

---

## Notas de Migración

### De 1.x a 2.0

**Cambios Importantes:**

1. **Archivos de entrada**:
   - Ahora se requiere ejecutar `pre_asignar_p1.py` antes de optimizadores
   - Los optimizadores cargan `00_Horario_PreAsignado_P1.csv`

2. **Estructura de carpetas**:
   - Nueva carpeta `comparativas/final/` para resultados consolidados
   - Archivos renumerados en `datos_estructurados/`

3. **Ejecución**:
   - Usar `ejecutar_todos.py` para pipeline completo
   - O ejecutar scripts en orden:
     ```bash
     python3 pre_asignar_p1.py
     python3 optimizador_greedy.py
     python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv
     # ... etc
     ```

4. **Configuración**:
   - Verificar preferencias en `preferencias_profesores.json`
   - Asegurar que PRIORIDAD 1 esté correctamente configurada

**Pasos de Migración:**

```bash
# 1. Backup de datos actuales
cp -r datos_estructurados/ datos_estructurados_backup/

# 2. Actualizar código
git pull origin main

# 3. Instalar dependencias actualizadas
pip install -r requirements.txt

# 4. Ejecutar pipeline completo
python3 ejecutar_todos.py

# 5. Verificar resultados
ls -lh comparativas/final/
```

---

## 👨‍💻 Autor

**Jesús Olvera**

- **GitHub:** [@jjho05](https://github.com/jjho05)
- **Email:** jjho.reivaj05@gmail.com / hernandez.jesusjavier.20.0770@gmail.com
- **Institución:** Instituto Tecnológico de Ciudad Madero
- **Programa:** Ingeniería en Sistemas Computacionales

**Agradecimientos:**
- Coordinación académica ISC - ITCM
- Profesores del programa ISC
- Comunidad de desarrollo del TECNM

## Licencia

Este proyecto es de uso académico para el Tecnológico Nacional de México.

---

**Última actualización**: 2025-12-21  
**Versión actual**: 2.0.0  
**Estado**: Producción
