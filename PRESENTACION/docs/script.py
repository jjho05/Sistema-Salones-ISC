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