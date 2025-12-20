# 🌐 Aplicación Web - Optimizador de Salones ISC

> Interfaz web intuitiva para optimización inteligente de horarios con detección automática de columnas.

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python app.py

# Abrir navegador
open http://localhost:5001
```

## ✨ Características

### 🎯 Detección Inteligente de Columnas

- **Fuzzy Matching:** Detecta automáticamente columnas con 95%+ precisión
- **Palabras Clave:** Busca variaciones de "Grupo", "Materia", "Salón", etc.
- **Aprendizaje:** Guarda mapeos para reutilizar en futuros archivos
- **Interfaz Visual:** Mapeo manual si la detección falla

### 🤖 Múltiples Métodos de Optimización

| Método | Tiempo | Mejora Distancia | Recomendado |
|--------|--------|------------------|-------------|
| **Greedy + Hill Climbing** | < 2 min | 36.5% | ✅ Sí |
| Machine Learning | ~2 min | 17.5% | Para datos históricos |
| Algoritmo Genético | ~3 min | 12.7% | Casos complejos |

### 📊 Visualización Interactiva

- **Chart.js:** Gráficos interactivos en tiempo real
- **Comparativas:** Antes vs Después
- **Métricas:** Inválidos, Movimientos, Cambios Piso, Distancia
- **Exportación:** Excel + PDF descargables

### 💾 Historial de Optimizaciones

- **SQLite:** Base de datos local
- **Búsqueda:** Encuentra optimizaciones anteriores
- **Reutilización:** Carga configuraciones previas
- **Estadísticas:** Tendencias de mejora

## 📋 Requisitos

- Python 3.11+
- Flask 3.0+
- pandas, openpyxl
- fuzzywuzzy, python-Levenshtein
- Chart.js (incluido vía CDN)

## 🏗️ Arquitectura

### Backend (Flask)

```
app.py                    # Servidor principal
├── routes/
│   ├── upload.py        # Endpoint de subida
│   ├── optimize.py      # Endpoint de optimización
│   └── history.py       # Endpoint de historial
├── services/
│   ├── excel_detector.py      # Detección de columnas
│   ├── optimizer_service.py   # Integración optimizadores
│   └── chart_generator.py     # Generación de gráficos
└── models/
    └── database.py      # SQLite ORM
```

### Frontend (HTML/CSS/JS)

```
templates/
├── index.html          # Página principal
├── mapper.html         # Interfaz de mapeo
└── results.html        # Resultados
static/
├── css/main.css        # Estilos
└── js/app.js           # Lógica
```

## 🎨 Interfaz de Usuario

### 1. Página Principal

- **Drag & Drop:** Zona de arrastre para Excel
- **Detección Automática:** Muestra confianza y mapeo
- **Selección de Método:** Cards interactivas
- **Historial:** Últimas 5 optimizaciones

### 2. Resultados

- **Cards de Métricas:** Resumen visual
- **Gráficos Interactivos:** Chart.js
- **Botones de Descarga:** Excel y PDF
- **Información de Ejecución:** Método y tiempo

### 3. Mapeo Manual (Opcional)

- **Drag & Drop:** Arrastra columnas
- **Validación:** En tiempo real
- **Guardado:** Para reutilizar

## 🔧 Configuración

### Variables de Entorno

```python
# app.py
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
SECRET_KEY = 'isc-salones-2024'
```

### Puerto

Por defecto: `5001` (evita conflicto con AirPlay en macOS)

Para cambiar:
```python
app.run(debug=True, host='0.0.0.0', port=TU_PUERTO)
```

## 📊 API Endpoints

### POST /api/upload

Sube archivo Excel y detecta columnas.

**Request:**
```javascript
FormData {
  file: Excel file
}
```

**Response:**
```json
{
  "success": true,
  "filename": "horario.xlsx",
  "detection": {
    "columns": ["GRUPO", "MATERIA", ...],
    "mapping": {
      "Grupo": "GRUPO",
      "Materia": "MATERIA",
      ...
    },
    "confidence": {
      "Grupo": 95,
      "Materia": 90,
      ...
    },
    "total_confidence": 92.5
  }
}
```

### POST /api/optimize

Ejecuta optimización.

**Request:**
```json
{
  "filepath": "uploads/horario.xlsx",
  "method": "greedy",
  "column_mapping": {
    "Grupo": "GRUPO",
    "Materia": "MATERIA",
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "method": "greedy",
    "elapsed_time": 1.8,
    "metrics": {
      "invalidos": {
        "inicial": 51,
        "optimizado": 0,
        "mejora_pct": 100
      },
      ...
    },
    "output_path": "outputs/optimizado_greedy_123456.csv"
  }
}
```

### GET /api/history

Obtiene historial de optimizaciones.

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "timestamp": "2024-12-20 12:00:00",
      "filename": "horario.xlsx",
      "method": "greedy",
      "metrics": {...},
      "elapsed_time": 1.8
    },
    ...
  ]
}
```

## 🐛 Solución de Problemas

### Puerto en uso

```bash
# Error: Address already in use
# Solución: Cambiar puerto en app.py o deshabilitar AirPlay Receiver
```

### Módulo no encontrado

```bash
# Error: ModuleNotFoundError: No module named 'fuzzywuzzy'
# Solución:
pip install -r requirements.txt
```

### Excel no se detecta

```bash
# Verificar formato: .xlsx o .xls
# Verificar tamaño: < 10MB
# Verificar que tenga columnas con nombres
```

## 🚀 Despliegue

### Desarrollo

```bash
python app.py  # Debug mode ON
```

### Producción

```bash
# Usar Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker (Opcional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📈 Rendimiento

- **Detección de Columnas:** < 1 segundo
- **Optimización Greedy:** < 2 minutos
- **Generación de Gráficos:** < 5 segundos
- **Tamaño de Base de Datos:** ~1MB por 100 optimizaciones

## 🔐 Seguridad

- ✅ Validación de tamaño de archivo (10MB max)
- ✅ Sanitización de nombres de archivo
- ✅ Validación de formato Excel
- ✅ Límite de uploads concurrentes
- ✅ Limpieza automática de archivos temporales

## 🤝 Contribuir

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) en el repositorio principal.

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE)

---

**Desarrollado con ❤️ para el ISC**
