#!/usr/bin/env python3
"""
Arregla el documento LaTeX para que compile correctamente
Cierra todos los entornos abiertos y asegura estructura válida
"""

def fix_latex_document():
    """Arregla presentacion_completa.tex para que compile"""
    
    with open('ARTICULO_LATEX/presentacion_completa.tex', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Contar entornos abiertos
    open_itemize = 0
    open_enumerate = 0
    open_equation = 0
    open_verbatim = 0
    open_lstlisting = 0
    
    fixed_lines = []
    
    for line in lines:
        # Contar aperturas
        if '\\begin{itemize}' in line:
            open_itemize += 1
        if '\\begin{enumerate}' in line:
            open_enumerate += 1
        if '\\begin{equation}' in line:
            open_equation += 1
        if '\\begin{verbatim}' in line:
            open_verbatim += 1
        if '\\begin{lstlisting}' in line:
            open_lstlisting += 1
        
        # Contar cierres
        if '\\end{itemize}' in line:
            open_itemize -= 1
        if '\\end{enumerate}' in line:
            open_enumerate -= 1
        if '\\end{equation}' in line:
            open_equation -= 1
        if '\\end{verbatim}' in line:
            open_verbatim -= 1
        if '\\end{lstlisting}' in line:
            open_lstlisting -= 1
        
        fixed_lines.append(line)
    
    # Cerrar entornos que quedaron abiertos
    if open_itemize > 0:
        for _ in range(open_itemize):
            fixed_lines.append('\\end{itemize}\n\n')
            print(f"⚠️  Cerrado itemize abierto")
    
    if open_enumerate > 0:
        for _ in range(open_enumerate):
            fixed_lines.append('\\end{enumerate}\n\n')
            print(f"⚠️  Cerrado enumerate abierto")
    
    if open_equation > 0:
        for _ in range(open_equation):
            fixed_lines.append('\\end{equation}\n\n')
            print(f"⚠️  Cerrada ecuación abierta")
    
    if open_verbatim > 0:
        for _ in range(open_verbatim):
            fixed_lines.append('\\end{verbatim}\n\n')
            print(f"⚠️  Cerrado verbatim abierto")
    
    if open_lstlisting > 0:
        for _ in range(open_lstlisting):
            fixed_lines.append('\\end{lstlisting}\n\n')
            print(f"⚠️  Cerrado lstlisting abierto")
    
    # Asegurar que termine con \end{document}
    content = ''.join(fixed_lines)
    if not content.strip().endswith('\\end{document}'):
        fixed_lines.append('\n\\end{document}\n')
        print(f"✅ Agregado \\end{{document}}")
    
    # Guardar archivo arreglado
    with open('ARTICULO_LATEX/presentacion_completa.tex', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"\n✅ Documento arreglado")
    print(f"📄 Total de líneas: {len(fixed_lines)}")
    print(f"\n💡 Ahora debería compilar correctamente en Overleaf")

if __name__ == "__main__":
    fix_latex_document()
