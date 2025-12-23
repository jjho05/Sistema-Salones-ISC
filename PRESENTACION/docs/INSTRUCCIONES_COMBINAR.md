# Cómo Combinar la Presentación

## Archivos Convertidos a Marp

Todos los archivos ya están en formato Marp y listos para combinar:

### Orden Sugerido:

1. **00_PORTADA.md** - Portada con tu nombre
2. **00_CONTEXTO_PROBLEMA.md** - Introducción y planteamiento del problema
3. **01_TEORIA_MATEMATICA.md** - Fundamentos matemáticos
4. **05_PRE_PROCESAMIENTO.md** - Preparación de datos
5. **02_ALGORITMO_GREEDY.md** - Algoritmo Greedy + Hill Climbing
6. **03_ALGORITMO_ML.md** - Algoritmo Machine Learning
7. **04_ALGORITMO_GENETICO.md** - Algoritmo Genético
8. **06_POST_PROCESAMIENTO.md** - Corrección y refinamiento
9. **07_ARQUITECTURA_CODIGO.md** - Implementación del sistema
10. **WEB_APP_BETA.md** - Aplicación web (opcional)
11. **FAQ.md** - Preguntas frecuentes (opcional)
12. **99_CIERRE.md** - Diapositiva final con lema del Tec

## Cómo Combinar Manualmente

### Opción 1: Copiar y Pegar en VSCode

1. Crea un nuevo archivo: `PRESENTACION_COMPLETA.md`
2. Copia el contenido de cada archivo en orden
3. **IMPORTANTE:** Quita el encabezado Marp de todos excepto del primero
4. Entre cada archivo, asegúrate de tener `---` para separar secciones

### Opción 2: Usar Comando en Terminal

```bash
cd /Users/lic.ing.jesusolvera/Documents/PROYECTOS\ PERSONALES/PRESENTACION/docs

# Extraer solo el header del primer archivo
head -7 00_PORTADA.md > PRESENTACION_COMPLETA.md

# Agregar contenido de cada archivo (sin headers)
for file in 00_PORTADA.md 00_CONTEXTO_PROBLEMA.md 01_TEORIA_MATEMATICA.md 05_PRE_PROCESAMIENTO.md 02_ALGORITMO_GREEDY.md 03_ALGORITMO_ML.md 04_ALGORITMO_GENETICO.md 06_POST_PROCESAMIENTO.md 07_ARQUITECTURA_CODIGO.md WEB_APP_BETA.md FAQ.md 99_CIERRE.md; do
    echo "" >> PRESENTACION_COMPLETA.md
    echo "---" >> PRESENTACION_COMPLETA.md
    echo "" >> PRESENTACION_COMPLETA.md
    tail -n +9 "$file" >> PRESENTACION_COMPLETA.md
done
```

### Opción 3: Script Python Automático

```python
import os

docs_dir = '/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/PRESENTACION/docs'
output_file = os.path.join(docs_dir, 'PRESENTACION_COMPLETA.md')

files_in_order = [
    '00_PORTADA.md',
    '00_CONTEXTO_PROBLEMA.md',
    '01_TEORIA_MATEMATICA.md',
    '05_PRE_PROCESAMIENTO.md',
    '02_ALGORITMO_GREEDY.md',
    '03_ALGORITMO_ML.md',
    '04_ALGORITMO_GENETICO.md',
    '06_POST_PROCESAMIENTO.md',
    '07_ARQUITECTURA_CODIGO.md',
    'WEB_APP_BETA.md',
    'FAQ.md',
    '99_CIERRE.md'
]

with open(output_file, 'w', encoding='utf-8') as outfile:
    for i, filename in enumerate(files_in_order):
        filepath = os.path.join(docs_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
            if i == 0:
                # Primer archivo: incluir todo
                outfile.write(content)
            else:
                # Otros archivos: saltar el header Marp (primeras 7 líneas)
                lines = content.split('\n')
                content_without_header = '\n'.join(lines[8:])  # Saltar header
                outfile.write('\n\n---\n\n')
                outfile.write(content_without_header)

print(f'✅ Presentación combinada creada: {output_file}')
```

## Exportar a PowerPoint

Una vez que tengas el archivo combinado:

1. Abre `PRESENTACION_COMPLETA.md` en VSCode
2. Usa la extensión Marp for VS Code
3. Click derecho → "Marp: Export Slide Deck..."
4. Selecciona formato: **PPTX (PowerPoint)**
5. Guarda el archivo

## Notas

- Cada archivo ya tiene separadores `---` entre secciones principales
- El tema oscuro (invert) está configurado en todos
- Las fórmulas matemáticas funcionan con MathJax
- La paginación está desactivada (puedes activarla cambiando `paginate: false` a `true`)
