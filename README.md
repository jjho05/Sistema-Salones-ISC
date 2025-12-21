# 🏫 Sistema de Optimización de Salones ISC

> Sistema inteligente de optimización de horarios para el Instituto de Sistemas Computacionales usando múltiples algoritmos de optimización.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Resultados](#-resultados)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Métodos de Optimización](#-métodos-de-optimización)
- [Aplicación Web](#-aplicación-web)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)

## ✨ Características

- 🎯 **4 Métodos de Optimización** implementados y comparados
- 📊 **Análisis Comparativo Completo** con 15 gráficos profesionales por método
- 📈 **Reducción de hasta 36.5%** en distancia total recorrida
- 🚀 **Optimización Rápida** (< 2 minutos con Greedy + Hill Climbing)
- 🌐 **Aplicación Web** con interfaz intuitiva
- 🔍 **Detección Automática** de columnas en Excel (95%+ precisión)
- 📱 **Diseño Responsive** para cualquier dispositivo
- 💾 **Historial de Optimizaciones** con SQLite

## 🏆 Resultados

### Comparativa de Métodos

| Método | Inválidos | Movimientos | Cambios Piso | Distancia | Tiempo |
|--------|-----------|-------------|--------------|-----------|--------|
| **Inicial** | 51 | 357 | 287 | 2847 | - |
| Profesor (Manual) | 51 | 362 (-1.4%) | 287 (0%) | 2842 (+0.2%) | Manual |
| Machine Learning | 0 ✅ | 356 (+0.3%) | 267 (+7.0%) | 2350 (+17.5%) | ~2 min |
| Algoritmo Genético | 0 ✅ | 368 (-3.1%) | 274 (+4.5%) | 2486 (+12.7%) | ~3 min |
| **Greedy + Hill Climbing** 🏆 | **0** ✅ | **331** (+7.3%) | **189** (+34.1%) | **1808** (+36.5%) | **< 2 min** |

### Ganador: Greedy + Hill Climbing

- ✅ **36.5% reducción** en distancia total
- ✅ **34.1% reducción** en cambios de piso
- ✅ **7.3% reducción** en movimientos de profesores
- ✅ **100% eliminación** de asignaciones inválidas
- ✅ **Más rápido** de todos los métodos

## 🚀 Instalación

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Sistema-Salones-ISC.git
cd Sistema-Salones-ISC

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias Principales

```
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
reportlab==4.0.7
openpyxl==3.1.2
```

## 💻 Uso

### 1. Optimización por Línea de Comandos

#### Greedy + Hill Climbing (Recomendado)

```bash
python3 optimizador_greedy.py
```

#### Machine Learning

```bash
python3 optimizador_ml.py
```

#### Algoritmo Genético

```bash
python3 optimizador_genetico.py
```

### 2. Generar Comparativas

```bash
# Comparativa individual (ejemplo: Greedy)
python3 pipeline_comparativo_greedy.py

# Comparativa final consolidada
python3 generar_comparativa_final.py

# Excel comparativo de salones (NUEVO)
python3 generar_excel_comparativo_salones.py
```

**Excel Comparativo de Salones:**
- 📊 Agrupa por materia/grupo
- 🔄 Muestra 5 métodos juntos para cada grupo
- 🎨 Código de colores para identificación rápida
- 📋 Formato: Lunes a Viernes (sin sábado)
- ✅ Comparación visual instantánea

### 3. Aplicación Web

```bash
cd webapp
python3 app.py
```

Abrir navegador en: **http://localhost:5001**

## 🧠 Métodos de Optimización

### 1. Greedy + Hill Climbing 🏆

**Enfoque:** Construcción voraz seguida de búsqueda local

**Ventajas:**
- Más rápido (< 2 minutos)
- Mejores resultados (36.5% reducción distancia)
- Simple de implementar y mantener

**Ideal para:** Uso en producción

### 2. Machine Learning

**Enfoque:** Random Forest + Gradient Boosting

**Ventajas:**
- Aprende de datos históricos
- Adaptativo
- Buenos resultados (17.5% reducción)

**Ideal para:** Cuando hay datos de entrenamiento

### 3. Algoritmo Genético

**Enfoque:** Evolución con 100 generaciones

**Ventajas:**
- Explora amplio espacio de soluciones
- Resultados moderados (12.7% reducción)

**Ideal para:** Problemas muy complejos

### 4. Profesor (Baseline)

**Enfoque:** Optimización manual

**Uso:** Referencia para comparación

## 🌐 Aplicación Web

### Características

- 📤 **Drag & Drop** para subir Excel
- 🔍 **Detección Automática** de columnas con fuzzy matching
- 🎯 **Selección de Método** de optimización
- 📊 **Visualización Interactiva** con Chart.js
- 📜 **Historial** de optimizaciones
- 💾 **Descarga** de resultados (Excel + PDF)

### Capturas de Pantalla

![Interfaz Principal](docs/screenshots/main.png)
![Resultados](docs/screenshots/results.png)

### Uso de la Web App

1. **Subir Excel:** Arrastra tu archivo o haz clic para seleccionar
2. **Verificar Mapeo:** El sistema detecta automáticamente las columnas
3. **Seleccionar Método:** Elige Greedy (recomendado), ML o Genético
4. **Optimizar:** Haz clic en "Optimizar Horario"
5. **Descargar:** Obtén el Excel optimizado y el reporte PDF

## 📁 Estructura del Proyecto

```
Sistema-Salones-ISC/
├── 📊 datos_estructurados/          # CSVs de horarios
│   ├── 01_Horario_Inicial.csv
│   ├── 02_Horario_Optimizado_Profesor.csv
│   ├── 03_Horario_Optimizado_ML.csv
│   ├── 04_Horario_Optimizado_Genetico.csv
│   └── 04_Horario_Optimizado_Greedy.csv
│
├── 🤖 optimizador_*.py              # Optimizadores
│   ├── optimizador_greedy.py        # Greedy + Hill Climbing
│   ├── optimizador_ml.py            # Machine Learning
│   └── optimizador_genetico.py      # Algoritmo Genético
│
├── 📈 comparativas/                 # Análisis comparativos
│   ├── 00_comparativa_final/        # Consolidado (10 gráficos)
│   ├── 01_inicial_vs_profesor/      # 15 gráficos + PDF
│   ├── 02_inicial_vs_ml/            # 15 gráficos + PDF
│   ├── 03_inicial_vs_genetico/      # 15 gráficos + PDF
│   ├── 04_inicial_vs_greedy/        # 15 gráficos + PDF
│   └── excel_comparativo/           # Excel comparativo de salones
│
├── 🌐 webapp/                       # Aplicación Web
│   ├── app.py                       # Servidor Flask
│   ├── routes/                      # API endpoints
│   ├── services/                    # Lógica de negocio
│   ├── models/                      # Base de datos
│   ├── templates/                   # HTML
│   └── static/                      # CSS/JS
│
├── 📚 documentacion_metodos/        # Documentación técnica
│   ├── metodo_machine_learning.md
│   ├── metodo_genetico.md
│   └── metodo_greedy_hc.md
│
└── 🛠️ utils/                        # Utilidades
    ├── analizar_movimientos.py
    ├── generar_analisis_comparativo.py
    ├── generar_reporte_pdf.py
    ├── generar_excel_formateado.py
    └── generar_excel_comparativo_salones.py  # NUEVO
```

## 📚 Documentación

### Documentación Técnica

Cada método tiene documentación detallada en `documentacion_metodos/`:

- [Machine Learning](documentacion_metodos/metodo_machine_learning.md)
- [Algoritmo Genético](documentacion_metodos/metodo_genetico.md)
- [Greedy + Hill Climbing](documentacion_metodos/metodo_greedy_hc.md)

### Reportes Generados

Cada optimización genera:

- ✅ **15 gráficos** profesionales (300 DPI)
- ✅ **Reporte PDF** completo con análisis
- ✅ **Excel formateado** con resultados
- ✅ **CSV de métricas** para análisis

## 🔬 Metodología

### Métricas Evaluadas

1. **Asignaciones Inválidas:** Clases en salones no válidos
2. **Movimientos de Profesores:** Total de cambios de salón
3. **Cambios de Piso:** Movimientos entre pisos
4. **Distancia Total:** Suma de distancias recorridas

### Restricciones

- ✅ Salones válidos: FF1-FF9, FFA-FFD (teoría)
- ✅ Laboratorios: LBD, LBD2, LCA, LCG1, LCG2, LIA, LR, LSO
- ✅ Sin conflictos de horario
- ✅ Respeto de tipo de salón (teoría vs laboratorio)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Jesús Olvera** - *Desarrollo inicial* - Instituto de Sistemas Computacionales

## 🙏 Agradecimientos

- Instituto de Sistemas Computacionales
- Profesores del ISC por proporcionar datos reales
- Comunidad de Python por las excelentes librerías

## 📞 Contacto

- Email: lic.ing.jesusolvera@gmail.com
- GitHub: [@jjho05](https://github.com/jjho05)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

**Hecho con ❤️ para el ISC**
