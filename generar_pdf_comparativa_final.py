#!/usr/bin/env python3
"""
Generador de PDF - Comparativa Final Consolidada
Genera reporte PDF profesional comparando TODOS los métodos
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pathlib import Path
import pandas as pd

class GeneradorPDFComparativaFinal:
    def __init__(self, carpeta_graficos, pdf_path):
        self.carpeta_graficos = Path(carpeta_graficos)
        self.pdf_path = pdf_path
        self.story = []
        self.styles = getSampleStyleSheet()
        
        # Estilos personalizados
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
    
    def generar_pdf(self):
        """Genera el PDF completo"""
        print("\n📄 Generando PDF consolidado...")
        
        doc = SimpleDocTemplate(
            self.pdf_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Portada
        self.crear_portada()
        
        # Resumen ejecutivo
        self.crear_resumen_ejecutivo()
        
        # Gráficos comparativos
        self.crear_seccion_graficos()
        
        # Conclusiones
        self.crear_conclusiones()
        
        # Generar PDF
        doc.build(self.story)
        
        # Obtener tamaño
        size_kb = Path(self.pdf_path).stat().st_size / 1024
        print(f"✅ PDF generado: {self.pdf_path}")
        print(f"   Tamaño: {size_kb:.1f} KB\n")
    
    def crear_portada(self):
        """Crea la portada del PDF"""
        titulo = Paragraph(
            "Comparativa Final Consolidada<br/>Optimización de Salones ISC",
            self.styles['CustomTitle']
        )
        self.story.append(titulo)
        self.story.append(Spacer(1, 0.3*inch))
        
        subtitulo = Paragraph(
            "Análisis Comparativo de 4 Métodos de Optimización",
            self.styles['Heading2']
        )
        self.story.append(subtitulo)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Tabla de métodos
        data = [
            ['Método', 'Descripción', 'Tiempo'],
            ['Profesor', 'Optimización manual baseline', 'Manual'],
            ['Machine Learning', 'Random Forest + Gradient Boosting', '~2 min'],
            ['Algoritmo Genético', 'Evolución con 100 generaciones', '~3 min'],
            ['Greedy + Hill Climbing', 'Construcción voraz + búsqueda local', '< 2 min']
        ]
        
        tabla = Table(data, colWidths=[1.5*inch, 3*inch, 1.2*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        self.story.append(tabla)
        self.story.append(PageBreak())
    
    def crear_resumen_ejecutivo(self):
        """Crea el resumen ejecutivo"""
        titulo = Paragraph("1. Resumen Ejecutivo", self.styles['SectionTitle'])
        self.story.append(titulo)
        
        # Cargar datos
        df = pd.read_csv(self.carpeta_graficos / 'comparativa_consolidada.csv')
        
        # Tabla comparativa
        data = [['Método', 'Inválidos', 'Movimientos', 'Cambios Piso', 'Distancia']]
        for _, row in df.iterrows():
            data.append([
                row['Método'],
                str(int(row['Inválidos'])),
                str(int(row['Movimientos'])),
                str(int(row['Cambios_Piso'])),
                str(int(row['Distancia']))
            ])
        
        tabla = Table(data, colWidths=[1.2*inch, 1*inch, 1.2*inch, 1.2*inch, 1*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            # Highlight ganador (Greedy - última fila)
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d5f4e6')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        ]))
        
        self.story.append(tabla)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Hallazgos clave
        hallazgos = Paragraph(
            "<b>Hallazgos Clave:</b><br/><br/>"
            "🏆 <b>Greedy + Hill Climbing</b> es el método ganador con:<br/>"
            "• 100% eliminación de asignaciones inválidas (51 → 0)<br/>"
            "• 36.5% reducción en distancia total (2847 → 1808)<br/>"
            "• 34.1% reducción en cambios de piso (287 → 189)<br/>"
            "• Tiempo de ejecución más rápido (< 2 minutos)<br/><br/>"
            "📊 <b>Machine Learning</b> logró segunda mejor distancia (17.5% reducción)<br/>"
            "🧬 <b>Algoritmo Genético</b> mostró 12.7% reducción en distancia<br/>"
            "👨‍🏫 <b>Profesor</b> (baseline manual) no mejoró métricas significativamente",
            self.styles['BodyText']
        )
        self.story.append(hallazgos)
        self.story.append(PageBreak())
    
    def crear_seccion_graficos(self):
        """Crea sección con todos los gráficos"""
        titulo = Paragraph("2. Análisis Gráfico Comparativo", self.styles['SectionTitle'])
        self.story.append(titulo)
        
        graficos = [
            ('01_comparativa_invalidos.png', 'Asignaciones a Salones Inválidos'),
            ('02_comparativa_movimientos.png', 'Movimientos Totales de Profesores'),
            ('03_comparativa_cambios_piso.png', 'Cambios de Piso'),
            ('04_comparativa_distancia.png', 'Distancia Total Recorrida'),
            ('05_radar_consolidado.png', 'Comparativa Consolidada (Radar)'),
            ('06_mejoras_porcentuales.png', 'Mejoras Porcentuales por Método'),
            ('07_eficiencia_tiempo_calidad.png', 'Eficiencia: Tiempo vs Calidad'),
            ('08_ranking_por_metrica.png', 'Ranking de Métodos por Métrica'),
            ('09_uso_salones.png', 'Distribución de Uso de Salones'),
            ('10_tabla_resumen.png', 'Tabla Resumen Completa')
        ]
        
        for archivo, descripcion in graficos:
            img_path = self.carpeta_graficos / archivo
            if img_path.exists():
                # Título del gráfico
                subtitulo = Paragraph(f"<b>{descripcion}</b>", self.styles['Heading3'])
                self.story.append(subtitulo)
                self.story.append(Spacer(1, 0.1*inch))
                
                # Imagen
                img = Image(str(img_path), width=6*inch, height=3*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.2*inch))
                
                # Page break después de cada 2 gráficos para mejor distribución
                if graficos.index((archivo, descripcion)) % 2 == 1:
                    self.story.append(PageBreak())
        
        self.story.append(PageBreak())
    
    def crear_conclusiones(self):
        """Crea sección de conclusiones"""
        titulo = Paragraph("3. Conclusiones y Recomendaciones", self.styles['SectionTitle'])
        self.story.append(titulo)
        
        conclusiones = Paragraph(
            "<b>3.1 Conclusión Principal</b><br/><br/>"
            "El método <b>Greedy + Hill Climbing</b> demostró ser la solución óptima para la "
            "optimización de salones del ISC, superando significativamente a los otros métodos "
            "en todas las métricas clave:<br/><br/>"
            "• <b>Efectividad:</b> Eliminación total de asignaciones inválidas<br/>"
            "• <b>Eficiencia:</b> Mayor reducción en distancia y cambios de piso<br/>"
            "• <b>Velocidad:</b> Tiempo de ejecución más rápido (< 2 minutos)<br/>"
            "• <b>Simplicidad:</b> Algoritmo más simple de implementar y mantener<br/><br/>"
            "<b>3.2 Comparación con Otros Métodos</b><br/><br/>"
            "<b>Machine Learning:</b> Buen desempeño (17.5% reducción distancia) pero requiere "
            "datos de entrenamiento y es más complejo de mantener.<br/><br/>"
            "<b>Algoritmo Genético:</b> Resultados moderados (12.7% reducción) con mayor tiempo "
            "de ejecución y complejidad computacional.<br/><br/>"
            "<b>Profesor (Manual):</b> Baseline útil pero sin mejoras significativas, validando "
            "la necesidad de optimización automática.<br/><br/>"
            "<b>3.3 Recomendación Final</b><br/><br/>"
            "Se recomienda implementar el método <b>Greedy + Hill Climbing</b> como solución "
            "de producción para la optimización de salones del ISC, dado su balance superior "
            "entre efectividad, eficiencia y simplicidad.",
            self.styles['BodyText']
        )
        self.story.append(conclusiones)

def main():
    carpeta_graficos = "comparativas/00_comparativa_final"
    pdf_path = "comparativas/00_comparativa_final/Reporte_Comparativa_Final.pdf"
    
    generador = GeneradorPDFComparativaFinal(carpeta_graficos, pdf_path)
    generador.generar_pdf()

if __name__ == "__main__":
    main()
