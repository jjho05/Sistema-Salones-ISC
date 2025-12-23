# 📦 Guía de Instalación - Sistema de Asignación de Salones ISC

Esta guía detalla el proceso completo de instalación del sistema en diferentes sistemas operativos.

---

## 📋 Requisitos Previos

### Software Necesario

- **Python 3.8 o superior**
  - Verificar versión: `python3 --version`
  - Descargar: https://www.python.org/downloads/

- **pip (Gestor de paquetes de Python)**
  - Incluido con Python 3.4+
  - Verificar: `pip3 --version`

- **Git** (opcional, para clonar el repositorio)
  - Descargar: https://git-scm.com/downloads

### Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **RAM** | 4 GB | 8 GB |
| **Almacenamiento** | 500 MB | 1 GB |
| **CPU** | 2 cores | 4+ cores |
| **SO** | Windows 10, macOS 10.14, Ubuntu 18.04 | Versiones más recientes |

---

## 🐧 Instalación en Linux/macOS

### Paso 1: Clonar el Repositorio

```bash
# Opción A: Clonar con Git
git clone https://github.com/jjho05/Sistema-Salones-ISC.git
cd Sistema-Salones-ISC

# Opción B: Descargar ZIP y extraer
# Luego navegar a la carpeta
cd Sistema-Salones-ISC
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Paso 4: Verificar Instalación

```bash
# Verificar que pandas está instalado
python3 -c "import pandas; print(f'pandas {pandas.__version__} instalado correctamente')"

# Verificar scikit-learn
python3 -c "import sklearn; print(f'scikit-learn {sklearn.__version__} instalado correctamente')"
```

---

## 🪟 Instalación en Windows

### Paso 1: Instalar Python

1. Descargar Python desde https://www.python.org/downloads/
2. **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación
3. Verificar instalación:
   ```cmd
   python --version
   pip --version
   ```

### Paso 2: Clonar el Repositorio

```cmd
# Opción A: Con Git
git clone https://github.com/jjho05/Sistema-Salones-ISC.git
cd Sistema-Salones-ISC

# Opción B: Descargar ZIP desde GitHub
# Extraer y abrir CMD en la carpeta
```

### Paso 3: Crear Entorno Virtual

```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

### Paso 4: Instalar Dependencias

```cmd
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Verificar Instalación

```cmd
python -c "import pandas; print('pandas instalado correctamente')"
python -c "import sklearn; print('scikit-learn instalado correctamente')"
```

---

## 🐍 Instalación Manual de Dependencias

Si `requirements.txt` no funciona, instalar manualmente:

```bash
# Dependencias principales
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install scikit-learn==1.3.2
pip install matplotlib==3.8.2
pip install seaborn==0.13.0
pip install openpyxl==3.1.2

# Dependencias adicionales
pip install Flask==3.0.0
pip install reportlab==4.0.7
pip install fuzzywuzzy==0.18.0
pip install python-Levenshtein==0.23.0
```

---

## 🔧 Configuración Inicial

### 1. Verificar Estructura de Carpetas

```bash
# Verificar que existen las carpetas necesarias
ls -la datos_estructurados/
ls -la comparativas/
ls -la ejemplos_didacticos/
```

Si faltan carpetas, crearlas:

```bash
mkdir -p datos_estructurados comparativas/graficos
```

### 2. Configurar Datos Iniciales

```bash
# Ejecutar configurador (si es primera vez)
python3 configurador_materias.py
```

### 3. Prueba Rápida

```bash
# Ejecutar ejemplo didáctico para verificar
python3 ejemplos_didacticos/01_greedy_hill_climbing.py
```

Si se ejecuta sin errores, ¡la instalación fue exitosa! ✅

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "python: command not found"

**Solución:**
```bash
# Usar python3 en lugar de python
python3 --version

# O crear alias (Linux/macOS)
alias python=python3
```

### Problema 2: "pip: command not found"

**Solución:**
```bash
# Instalar pip
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python3  # macOS

# O usar python -m pip
python3 -m pip install pandas
```

### Problema 3: "Permission denied"

**Solución:**
```bash
# Opción A: Usar --user
pip install --user -r requirements.txt

# Opción B: Usar entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problema 4: "ModuleNotFoundError: No module named 'tkinter'"

**Solución:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (con Homebrew)
brew install python-tk

# Windows: Reinstalar Python con opción "tcl/tk and IDLE"
```

### Problema 5: Errores de compilación en Windows

**Solución:**
```cmd
# Instalar Microsoft C++ Build Tools
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# O usar versiones pre-compiladas
pip install --only-binary :all: scikit-learn
```

### Problema 6: "SSL Certificate Error"

**Solución:**
```bash
# Opción A: Actualizar certificados
pip install --upgrade certifi

# Opción B: Usar --trusted-host (temporal)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas
```

---

## 🧪 Verificación Completa

Ejecutar este script para verificar todas las dependencias:

```python
# verificar_instalacion.py
import sys

def verificar_modulo(nombre, version_min=None):
    try:
        modulo = __import__(nombre)
        version = getattr(modulo, '__version__', 'desconocida')
        print(f"✅ {nombre:20} v{version}")
        return True
    except ImportError:
        print(f"❌ {nombre:20} NO INSTALADO")
        return False

print("=" * 50)
print("VERIFICACIÓN DE DEPENDENCIAS")
print("=" * 50)

modulos = [
    'pandas',
    'numpy',
    'sklearn',
    'matplotlib',
    'seaborn',
    'openpyxl',
    'flask',
    'reportlab',
    'fuzzywuzzy'
]

resultados = [verificar_modulo(m) for m in modulos]

print("=" * 50)
if all(resultados):
    print("✅ TODAS LAS DEPENDENCIAS INSTALADAS CORRECTAMENTE")
else:
    print("❌ FALTAN ALGUNAS DEPENDENCIAS")
    print("Ejecutar: pip install -r requirements.txt")
```

Ejecutar:
```bash
python3 verificar_instalacion.py
```

---

## 🚀 Próximos Pasos

Una vez instalado correctamente:

1. ✅ Leer el [README.md](README.md) principal
2. ✅ Revisar [ejemplos didácticos](ejemplos_didacticos/README.md)
3. ✅ Ejecutar `python3 ejecutar_todos.py` para primera prueba
4. ✅ Explorar la [documentación](literatura/)

---

## 📞 Soporte

Si encuentras problemas:

1. 📖 Revisar esta guía completa
2. 🔍 Buscar en [GitHub Issues](https://github.com/jjho05/Sistema-Salones-ISC/issues)
3. 📧 Contactar: jjho.reivaj05@gmail.com
4. 🐛 Reportar bug: [Crear issue](https://github.com/jjho05/Sistema-Salones-ISC/issues/new)

---

## 📝 Notas Adicionales

- **Entorno virtual:** Siempre recomendado para evitar conflictos
- **Versiones:** Las versiones en `requirements.txt` son las probadas
- **Actualizaciones:** Ejecutar `pip install --upgrade -r requirements.txt` periódicamente
- **Desinstalación:** `pip uninstall -r requirements.txt -y`

---

<div align="center">

**¿Instalación exitosa? ¡Comienza a optimizar! 🚀**

[⬆ Volver al README](README.md)

</div>
