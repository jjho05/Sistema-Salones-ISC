# 📄 Documentos LaTeX - Sistema de Salones ISC

Este directorio contiene diferentes versiones del documento académico en formato LaTeX.

## 📋 Archivos Disponibles

### ✅ Documentos Compilables (Sin plantilla MDPI)

1. **`documento_compacto.tex`** ⭐ **Recomendado para empezar**
   - Versión compacta en español (~7 páginas)
   - Formato académico estándar
   - ✅ Compila sin problemas con BasicTeX
   - PDF generado: `documento_compacto.pdf`

2. **`documento_mdpi_style.tex`** 
   - Versión en inglés con estilo MDPI (~7 páginas)
   - Incluye números de línea
   - ✅ Compila sin problemas con BasicTeX
   - PDF generado: `documento_mdpi_style.pdf`

### 📦 Documentos Completos (Requieren plantilla MDPI)

3. **`main.tex`**
   - Versión completa para journal MDPI (~25 páginas)
   - **Requiere:** Archivo `Definitions/mdpi.cls`
   - ❌ No compila sin la plantilla oficial

4. **`documento_principal.tex`** + `parte_01.tex` + `parte_02.tex`
   - Versión dividida en partes
   - ❌ Tiene errores de compilación (lstlisting)

## 🚀 Compilación Rápida

### Opción 1: Usar el script automático

```bash
cd /ruta/al/proyecto
./compilar_latex.sh
```

### Opción 2: Compilar manualmente

```bash
cd ARTICULO_LATEX

# Compilar versión compacta (español)
pdflatex documento_compacto.tex
pdflatex documento_compacto.tex  # Segunda vez para referencias

# O compilar versión MDPI style (inglés)
pdflatex documento_mdpi_style.tex
pdflatex documento_mdpi_style.tex

# Abrir PDF
open documento_compacto.pdf
# o
open documento_mdpi_style.pdf
```

## 📥 Descargar Plantilla MDPI Oficial

Si quieres usar la plantilla oficial de MDPI para `main.tex`:

### Paso 1: Descargar plantilla

1. Ve a: https://www.mdpi.com/authors/latex
2. Descarga el archivo **"LaTeX Template and Guidelines"**
3. Extrae el archivo `mdpi.cls`

### Paso 2: Instalar en el proyecto

```bash
# Copiar mdpi.cls a la carpeta Definitions
cp /ruta/descarga/mdpi.cls ARTICULO_LATEX/Definitions/

# Verificar que esté instalado
ls ARTICULO_LATEX/Definitions/mdpi.cls
```

### Paso 3: Compilar con plantilla MDPI

```bash
cd ARTICULO_LATEX
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## 🌐 Alternativa: Usar Overleaf (Online)

Si prefieres no instalar nada localmente:

### Opción A: Subir archivos manualmente

1. Ve a [Overleaf](https://www.overleaf.com)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto → "Blank Project"
4. Sube los archivos `.tex` que quieras compilar
5. Compila con el botón "Recompile"

### Opción B: Usar plantilla MDPI en Overleaf

1. En Overleaf: New Project → "From Template"
2. Busca "MDPI"
3. Selecciona la plantilla oficial de MDPI
4. Copia el contenido de tu documento

## 📊 Comparación de Versiones

| Documento | Páginas | Idioma | Compila con BasicTeX | Formato |
|-----------|---------|--------|---------------------|---------|
| `documento_compacto.tex` | ~7 | Español | ✅ Sí | Estándar |
| `documento_mdpi_style.tex` | ~7 | Inglés | ✅ Sí | Estilo MDPI |
| `main.tex` | ~25 | Inglés | ❌ No* | MDPI Oficial |
| `documento_principal.tex` | ~50 | Español | ❌ No** | Dividido |

\* Requiere `mdpi.cls`  
\*\* Tiene errores de compilación

## 🎯 Recomendaciones

### Para presentaciones académicas rápidas:
→ Usa `documento_compacto.tex` (español, 7 páginas)

### Para enviar a journal MDPI:
→ Usa `main.tex` con plantilla oficial descargada

### Para trabajar online sin instalaciones:
→ Usa Overleaf con cualquier documento

## 🔧 Solución de Problemas

### Error: "pdflatex: command not found"

```bash
# Reiniciar terminal o ejecutar:
eval "$(/usr/libexec/path_helper)"
```

### Error: "File 'mdpi.cls' not found"

Descarga la plantilla oficial de MDPI (ver arriba) o usa `documento_compacto.tex` o `documento_mdpi_style.tex` que no la requieren.

### Error: Paquetes faltantes

```bash
# macOS con BasicTeX
sudo tlmgr update --self
sudo tlmgr install <nombre-paquete>
```

## 📧 Contacto

Para preguntas sobre los documentos LaTeX:
- Email: jjho.reivaj05@gmail.com
- GitHub: https://github.com/jjho05/Sistema-Salones-ISC

---

**Última actualización:** Enero 2026
