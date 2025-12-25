#!/usr/bin/env python3
"""
Divide el documento LaTeX grande en archivos más pequeños para Overleaf
"""

def split_latex_document():
    """Divide presentacion_completa.tex en secciones más pequeñas"""
    
    with open('ARTICULO_LATEX/presentacion_completa.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar el inicio del documento
    parts = content.split('\\begin{document}')
    preamble = parts[0] + '\\begin{document}\n'
    body = parts[1].replace('\\end{document}', '')
    
    # Dividir por secciones principales
    sections = body.split('\\section{')
    
    # Crear documento principal
    main_doc = preamble
    
    # Procesar cada sección
    for i, section in enumerate(sections[1:], 1):  # Saltar la primera parte vacía
        section_title = section.split('}')[0]
        section_content = '\\section{' + section
        
        # Guardar sección en archivo separado
        filename = f'seccion_{i:02d}.tex'
        with open(f'ARTICULO_LATEX/{filename}', 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        # Agregar input al documento principal
        main_doc += f'\\input{{{filename}}}\n\n'
        
        print(f"✅ Creada: {filename} - {section_title}")
    
    # Cerrar documento principal
    main_doc += '\\end{document}\n'
    
    # Guardar documento principal
    with open('ARTICULO_LATEX/documento_principal.tex', 'w', encoding='utf-8') as f:
        f.write(main_doc)
    
    print(f"\n✅ Documento principal creado: documento_principal.tex")
    print(f"📄 Total de secciones: {len(sections)-1}")
    print(f"\n💡 Sube todos los archivos a Overleaf y compila documento_principal.tex")

if __name__ == "__main__":
    split_latex_document()
