#!/usr/bin/env python3
"""
Conversor de Presentación Markdown a LaTeX (MDPI Format)
Convierte PRESENTACION_COMPLETA V3.md a formato LaTeX en español
"""

import re
import sys

def convert_markdown_to_latex(md_file, tex_file):
    """Convierte archivo Markdown a LaTeX"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Eliminar frontmatter de Marp
    content = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    # Iniciar documento LaTeX
    latex = r"""%  LaTeX - Sistema de Asignación de Salones ISC
\documentclass[algorithms,article,submit,pdftex]{Definitions/mdpi} 

\firstpage{1} 
\makeatletter 
\setcounter{page}{\@firstpage} 
\makeatother
\pubvolume{1}
\issuenum{1}
\articlenumber{0}
\pubyear{2026}
\copyrightyear{2025}

\Title{Sistema de Asignación de Salones ISC: Optimización Inteligente de Espacios Académicos}

\Author{Anónimo}
\AuthorNames{Anónimo}

\address{Instituto Tecnológico de Ciudad Madero, Tecnológico Nacional de México}

\corres{Correspondencia: contacto@ejemplo.com}

\abstract{Sistema inteligente de optimización para la asignación de 680 clases a 21 salones en el programa de Ingeniería en Sistemas Computacionales del Instituto Tecnológico de Ciudad Madero. El sistema implementa cuatro algoritmos de optimización: heurística del profesor, Greedy con Hill Climbing, Machine Learning (Random Forest) y Algoritmo Genético. Se presenta un mecanismo de pre-asignación que garantiza el 100\% de cumplimiento de las preferencias prioritarias (Prioridad 1) mientras optimiza tres objetivos: minimizar movimientos de profesores entre salones, reducir cambios de piso y disminuir la distancia total recorrida. Los resultados experimentales de 90 ejecuciones demuestran que el enfoque Greedy+Hill Climbing logra el mejor rendimiento general con 314 movimientos (mejora del 12\% sobre la línea base), 206 cambios de piso (reducción del 28\%) y resultados consistentes. La validación estadística mediante ANOVA, pruebas post-hoc de Tukey HSD y análisis de tamaño de efecto de Cohen confirma diferencias significativas entre todos los algoritmos. El sistema está implementado en Python con documentación completa y está disponible como software de código abierto.}

\keyword{asignación de salones; optimización combinatoria; algoritmos híbridos; hill climbing; machine learning; algoritmo genético; programación académica; satisfacción de restricciones}

\begin{document}

"""
    
    # Procesar contenido
    lines = content.split('\n')
    in_code_block = False
    in_equation = False
    section_level = 0
    
    for line in lines:
        # Detectar bloques de código
        if line.strip().startswith('```'):
            if not in_code_block:
                lang = line.strip()[3:].strip()
                if lang in ['python', 'bash', 'javascript', 'diff']:
                    latex += f"\\begin{{lstlisting}}[language={lang.capitalize()}]\n"
                else:
                    latex += "\\begin{verbatim}\n"
                in_code_block = True
            else:
                if 'lstlisting' in latex.split('\n')[-5:]:
                    latex += "\\end{lstlisting}\n\n"
                else:
                    latex += "\\end{verbatim}\n\n"
                in_code_block = False
            continue
        
        if in_code_block:
            latex += line + "\n"
            continue
        
        # Detectar ecuaciones
        if line.strip().startswith('$$'):
            if not in_equation:
                latex += "\\begin{equation}\n"
                in_equation = True
            else:
                latex += "\\end{equation}\n\n"
                in_equation = False
            continue
        
        if in_equation:
            # Limpiar ecuación
            eq_line = line.replace('\\cdot', '\\cdot ')
            eq_line = eq_line.replace('\_', '_')
            latex += eq_line + "\n"
            continue
        
        # Ignorar líneas de separación de Marp
        if line.strip() == '---':
            latex += "\n"
            continue
        
        # Ignorar comentarios de Marp
        if line.strip().startswith('<!--'):
            continue
        
        # Convertir encabezados
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            
            # Limpiar emojis y markdown
            title = re.sub(r'[🎯📚🔢💻🛠️⚙️🧪📊📈📑🎨🚀🔗📞🐛✅❌⚠️🔥🥇🥈🥉📄⏳🧬🤖🔨📖🎲🏆]', '', title)
            title = title.replace('**', '')
            
            if level == 1:
                latex += f"\\section{{{title}}}\n\n"
            elif level == 2:
                latex += f"\\subsection{{{title}}}\n\n"
            elif level == 3:
                latex += f"\\subsubsection{{{title}}}\n\n"
            elif level == 4:
                latex += f"\\paragraph{{{title}}}\n\n"
            continue
        
        # Convertir listas
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            item = line.strip()[2:]
            # Limpiar markdown
            item = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', item)
            item = re.sub(r'\*(.*?)\*', r'\\textit{\1}', item)
            item = re.sub(r'`(.*?)`', r'\\texttt{\1}', item)
            item = re.sub(r'[✅❌⚠️🔥]', '', item)
            
            if not latex.strip().endswith('\\begin{itemize}'):
                latex += "\\begin{itemize}\n"
            latex += f"\\item {item}\n"
            continue
        elif latex.strip().endswith('\\item'):
            latex += "\\end{itemize}\n\n"
        
        # Convertir listas numeradas
        if re.match(r'^\d+\.\s', line.strip()):
            item = re.sub(r'^\d+\.\s', '', line.strip())
            item = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', item)
            item = re.sub(r'\*(.*?)\*', r'\\textit{\1}', item)
            item = re.sub(r'`(.*?)`', r'\\texttt{\1}', item)
            
            if not latex.strip().endswith('\\begin{enumerate}'):
                latex += "\\begin{enumerate}\n"
            latex += f"\\item {item}\n"
            continue
        elif latex.strip().endswith('\\item') and '\\begin{enumerate}' in latex:
            latex += "\\end{enumerate}\n\n"
        
        # Convertir tablas (simplificado)
        if '|' in line and not line.strip().startswith('<!--'):
            # Detectar tabla
            continue  # Las tablas requieren procesamiento especial
        
        # Texto normal
        if line.strip():
            # Limpiar markdown inline
            text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', line)
            text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)
            text = re.sub(r'`(.*?)`', r'\\texttt{\1}', text)
            text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', text)
            text = re.sub(r'[🎯📚🔢💻🛠️⚙️🧪📊📈📑🎨🚀🔗📞🐛✅❌⚠️🔥🥇🥈🥉📄⏳🧬🤖🔨📖🎲🏆]', '', text)
            
            latex += text + "\n\n"
    
    # Cerrar documento
    latex += r"""
\end{document}
"""
    
    # Escribir archivo
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"✅ Conversión completada: {tex_file}")
    print(f"📄 Líneas procesadas: {len(lines)}")

if __name__ == "__main__":
    md_file = "PRESENTACION/docs/PRESENTACION_COMPLETA V3.md"
    tex_file = "ARTICULO_LATEX/presentacion_completa.tex"
    
    convert_markdown_to_latex(md_file, tex_file)
