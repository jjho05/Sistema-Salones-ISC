#!/usr/bin/env python3
"""
1. Elimina TODOS los emojis del documento LaTeX
2. Divide el documento en partes para Overleaf
"""

import re

def remove_emojis_and_split():
    """Elimina emojis y divide el documento LaTeX"""
    
    # Leer archivo
    with open('ARTICULO_LATEX/presentacion_completa.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Lista completa de emojis a eliminar
    emojis = [
        '🎯', '📚', '🔢', '💻', '🛠️', '⚙️', '🧪', '📊', '📈', '📑',
        '🎨', '🚀', '🔗', '📞', '🐛', '✅', '❌', '⚠️', '🔥', '🥇',
        '🥈', '🥉', '📄', '⏳', '🧬', '🤖', '🔨', '📖', '🎲', '🏆',
        '🎓', '💡', '📝', '🔍', '📌', '🎉', '👨‍💻', '👩‍💻', '🌟', '⭐',
        '🔧', '📦', '🗂️', '📂', '📁', '🖥️', '⌨️', '🖱️', '💾', '💿',
        '📀', '🎬', '🎥', '📷', '📸', '🖼️', '🗃️', '🗄️', '📋', '📇',
        '📅', '📆', '🗓️', '📉', '📐', '📏', '🔬', '🔭', '📡', '🛰️',
        '🧮', '🧪', '⚗️', '🧫', '🧬', '🔮', '🎯', '🎰', '🎲', '🎮',
        '🕹️', '🎴', '🃏', '🀄', '🎭', '🖼️', '🎨', '🧵', '🧶', '👓',
        '🥽', '🥼', '🦺', '👔', '👕', '👖', '🧣', '🧤', '🧥', '🧦',
        '👗', '👘', '🥻', '🩱', '🩲', '🩳', '👙', '👚', '👛', '👜',
        '👝', '🎒', '👞', '👟', '🥾', '🥿', '👠', '👡', '🩰', '👢'
    ]
    
    # Eliminar emojis
    for emoji in emojis:
        content = content.replace(emoji, '')
    
    # Eliminar emojis usando regex (cualquier carácter emoji)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    content = emoji_pattern.sub('', content)
    
    # Guardar archivo sin emojis
    with open('ARTICULO_LATEX/presentacion_completa.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Emojis eliminados del documento")
    
    # Ahora dividir el documento
    lines = content.split('\n')
    
    # Encontrar donde empieza el contenido (después de \newpage)
    start_content = 0
    for i, line in enumerate(lines):
        if '\\newpage' in line:
            start_content = i + 1
            break
    
    # Separar preámbulo y contenido
    preamble = '\n'.join(lines[:start_content])
    body_lines = lines[start_content:]
    
    # Encontrar \end{document}
    end_doc_idx = len(body_lines) - 1
    for i in range(len(body_lines) - 1, -1, -1):
        if '\\end{document}' in body_lines[i]:
            end_doc_idx = i
            break
    
    # Contenido sin \end{document}
    body_lines = body_lines[:end_doc_idx]
    
    # Dividir por secciones principales
    sections = []
    current_section = []
    section_count = 0
    
    for line in body_lines:
        current_section.append(line)
        
        # Dividir cada ~2000 líneas aproximadamente
        if line.startswith('\\section{') and len(current_section) > 1500:
            sections.append('\n'.join(current_section[:-1]))  # No incluir la nueva sección
            current_section = [line]  # Empezar nueva sección
            section_count += 1
    
    # Agregar última sección
    if current_section:
        sections.append('\n'.join(current_section))
    
    # Guardar documento principal
    main_doc = preamble + '\n\n'
    
    for i in range(len(sections)):
        filename = f'parte_{i+1:02d}.tex'
        main_doc += f'\\input{{{filename}}}\n'
        
        # Guardar cada parte
        with open(f'ARTICULO_LATEX/{filename}', 'w', encoding='utf-8') as f:
            f.write(sections[i])
        
        print(f"✅ Creada: {filename} ({len(sections[i].split(chr(10)))} líneas)")
    
    main_doc += '\n\\end{document}\n'
    
    # Guardar documento principal
    with open('ARTICULO_LATEX/documento_principal.tex', 'w', encoding='utf-8') as f:
        f.write(main_doc)
    
    print(f"\n✅ Documento principal creado: documento_principal.tex")
    print(f"📄 Total de partes: {len(sections)}")
    print(f"\n💡 Sube todos los archivos a Overleaf y compila documento_principal.tex")

if __name__ == "__main__":
    remove_emojis_and_split()
