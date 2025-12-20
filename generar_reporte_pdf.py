#!/usr/bin/env python3
"""
Generador de Reporte PDF Profesional
Crea un documento detallado con análisis comparativo completo
"""

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pathlib import Path
from datetime import datetime

class GeneradorReportePDF:
    def __init__(self, csv_inicial, csv_optimizado, carpeta_graficos, output_path, nombre_metodo="Profesor"):
        self.df_inicial = pd.read_csv(csv_inicial)
        self.df_optimizado = pd.read_csv(csv_optimizado)
        self.carpeta_graficos = Path(carpeta_graficos)
        self.output_path = output_path
        self.nombre_metodo = nombre_metodo  # "Profesor", "Machine Learning", "Genético", "ILP"
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='Centered',
            parent=self.styles['Heading1'],
            alignment=TA_CENTER,
            fontSize=18,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.story = []
    
    def calcular_estadisticas(self):
        """Calcula todas las estadísticas comparativas"""
        stats = {}
        
        # Básicas
        stats['total_ini'] = len(self.df_inicial)
        stats['total_opt'] = len(self.df_optimizado)
        stats['diff_total'] = stats['total_opt'] - stats['total_ini']
        
        # Inválidos
        stats['inv_ini'] = int(self.df_inicial['Es_Invalido'].sum())
        stats['inv_opt'] = int(self.df_optimizado['Es_Invalido'].sum())
        stats['diff_inv'] = stats['inv_opt'] - stats['inv_ini']
        stats['mejora_inv_pct'] = ((stats['inv_ini'] - stats['inv_opt']) / stats['inv_ini'] * 100) if stats['inv_ini'] > 0 else 0
        
        # Salones
        stats['salones_ini'] = self.df_inicial['Salon'].nunique()
        stats['salones_opt'] = self.df_optimizado['Salon'].nunique()
        stats['diff_salones'] = stats['salones_opt'] - stats['salones_ini']
        
        # Materias
        stats['materias_ini'] = self.df_inicial['Materia'].nunique()
        stats['materias_opt'] = self.df_optimizado['Materia'].nunique()
        
        # Grupos
        stats['grupos_ini'] = self.df_inicial['Grupo'].nunique()
        stats['grupos_opt'] = self.df_optimizado['Grupo'].nunique()
        
        # Profesores
        stats['profesores_ini'] = self.df_inicial['Profesor'].nunique()
        stats['profesores_opt'] = self.df_optimizado['Profesor'].nunique()
        
        # Por tipo
        stats['teoria_ini'] = len(self.df_inicial[self.df_inicial['Tipo_Salon']=='Teoría'])
        stats['teoria_opt'] = len(self.df_optimizado[self.df_optimizado['Tipo_Salon']=='Teoría'])
        stats['lab_ini'] = len(self.df_inicial[self.df_inicial['Tipo_Salon']=='Laboratorio'])
        stats['lab_opt'] = len(self.df_optimizado[self.df_optimizado['Tipo_Salon']=='Laboratorio'])
        
        return stats
    
    def crear_portada(self):
        """Crea la portada del reporte"""
        # Título
        titulo = Paragraph(
            "<b>REPORTE COMPARATIVO</b><br/>Sistema de Optimización de Salones ISC",
            self.styles['Centered']
        )
        self.story.append(titulo)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Subtítulo dinámico
        subtitulo = Paragraph(
            f"Horario Inicial vs Horario Optimizado ({self.nombre_metodo})",
            self.styles['SubHeading']
        )
        self.story.append(subtitulo)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Información del reporte
        fecha = datetime.now().strftime("%d de %B de %Y")
        info = f"""
        <b>Fecha de generación:</b> {fecha}<br/>
        <b>Proyecto:</b> Optimización de Asignación de Salones<br/>
        <b>Departamento:</b> Ingeniería en Sistemas Computacionales<br/>
        <b>Institución:</b> Tecnológico Nacional de México
        """
        info_para = Paragraph(info, self.styles['Normal'])
        self.story.append(info_para)
        self.story.append(PageBreak())
    
    def crear_resumen_ejecutivo(self, stats):
        """Crea el resumen ejecutivo"""
        titulo = Paragraph("<b>1. RESUMEN EJECUTIVO</b>", self.styles['SubHeading'])
        self.story.append(titulo)
        
        resumen_text = f"""
        Este reporte presenta un análisis comparativo detallado entre el horario inicial 
        (HorariosAgoDic2025) y el horario optimizado manualmente por el profesor 
        (grouped_optimized_schedule). El análisis incluye métricas clave, visualizaciones 
        y evaluación de mejoras implementadas.
        <br/><br/>
        <b>Hallazgos Principales:</b>
        <br/>
        • Total de asignaciones procesadas: {stats['total_ini']} registros<br/>
        • Asignaciones inválidas (AV/E11): {stats['inv_ini']} → {stats['inv_opt']} 
        ({stats['diff_inv']:+d}, {stats['mejora_inv_pct']:.1f}% de mejora)<br/>
        • Salones utilizados: {stats['salones_ini']} → {stats['salones_opt']} 
        ({stats['diff_salones']:+d})<br/>
        • Materias únicas: {stats['materias_ini']}<br/>
        • Grupos únicos: {stats['grupos_ini']}<br/>
        • Profesores: {stats['profesores_ini']}
        """
        
        resumen_para = Paragraph(resumen_text, self.styles['Normal'])
        self.story.append(resumen_para)
        self.story.append(Spacer(1, 0.3*inch))
    
    def crear_tabla_comparativa(self, stats):
        """Crea tabla comparativa de métricas"""
        titulo = Paragraph("<b>2. TABLA COMPARATIVA DE MÉTRICAS</b>", self.styles['SubHeading'])
        self.story.append(titulo)
        self.story.append(Spacer(1, 0.2*inch))
        
        data = [
            ['Métrica', 'Inicial', 'Optimizado', 'Diferencia', 'Cambio (%)'],
            ['Total Asignaciones', f"{stats['total_ini']}", f"{stats['total_opt']}", 
             f"{stats['diff_total']:+d}", '0%'],
            ['⚠️ Asignaciones Inválidas', f"{stats['inv_ini']}", f"{stats['inv_opt']}", 
             f"{stats['diff_inv']:+d}", f"{stats['mejora_inv_pct']:.1f}%"],
            ['Salones Utilizados', f"{stats['salones_ini']}", f"{stats['salones_opt']}", 
             f"{stats['diff_salones']:+d}", '0%'],
            ['Materias Únicas', f"{stats['materias_ini']}", f"{stats['materias_opt']}", '0', '0%'],
            ['Grupos Únicos', f"{stats['grupos_ini']}", f"{stats['grupos_opt']}", '0', '0%'],
            ['Profesores', f"{stats['profesores_ini']}", f"{stats['profesores_opt']}", '0', '0%'],
            ['Asignaciones Teoría', f"{stats['teoria_ini']}", f"{stats['teoria_opt']}", 
             f"{stats['teoria_opt']-stats['teoria_ini']:+d}", '0%'],
            ['Asignaciones Laboratorio', f"{stats['lab_ini']}", f"{stats['lab_opt']}", 
             f"{stats['lab_opt']-stats['lab_ini']:+d}", '0%'],
        ]
        
        table = Table(data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def agregar_graficos(self, stats):
        """Agrega los 15 gráficos con explicaciones detalladas al reporte"""
        titulo = Paragraph("<b>3. VISUALIZACIONES COMPARATIVAS</b>", self.styles['SubHeading'])
        self.story.append(titulo)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Cargar métricas de movimientos si existen
        metricas_mov_path = self.carpeta_graficos / 'metricas_movimientos.csv'
        metricas_mov = {}
        if metricas_mov_path.exists():
            df_mov = pd.read_csv(metricas_mov_path)
            for _, row in df_mov.iterrows():
                # Calcular mejora si no existe
                if 'Mejora' in row:
                    mejora = row['Mejora']
                else:
                    mejora = row['Inicial'] - row['Optimizado']
                
                # Calcular mejora_pct si no existe
                if 'Mejora (%)' in row:
                    mejora_pct = row['Mejora (%)']
                else:
                    mejora_pct = (mejora / row['Inicial'] * 100) if row['Inicial'] > 0 else 0
                
                metricas_mov[row['Metrica']] = {
                    'inicial': row['Inicial'],
                    'optimizado': row['Optimizado'],
                    'mejora': mejora,
                    'mejora_pct': mejora_pct
                }
        
        # Definir las 15 gráficas con sus explicaciones
        graficos_info = [
            {
                'archivo': '01_asignaciones_invalidas.png',
                'titulo': 'Figura 1: Asignaciones a Salones Inválidos',
                'explicacion': f"""
                Esta gráfica muestra la comparación directa de asignaciones a salones inválidos 
                (AV1, AV2, AV4, AV5, E11) entre ambos horarios. Los salones AV no existen físicamente 
                y E11 está en otro campus, por lo que todas estas asignaciones deben eliminarse.
                <br/><br/>
                <b>Resultado:</b> {stats['inv_ini']} → {stats['inv_opt']} asignaciones inválidas 
                ({stats['mejora_inv_pct']:.1f}% de mejora). Este es el principal indicador de 
                éxito de la optimización.
                """
            },
            {
                'archivo': '02_distribucion_salones.png',
                'titulo': 'Figura 2: Distribución de Uso de Salones',
                'explicacion': """
                Muestra los 15 salones más utilizados en cada horario. Esta visualización permite 
                identificar si hay sobrecarga en ciertos salones y subutilización en otros.
                <br/><br/>
                <b>Observación:</b> Los laboratorios (LCG1, LIA, LSO) son los más utilizados, 
                seguidos por salones de teoría (FF7, FFA, FFD). Una distribución más equilibrada 
                reduciría conflictos y mejoraría la disponibilidad.
                """
            },
            {
                'archivo': '03_tipo_salon.png',
                'titulo': 'Figura 3: Distribución por Tipo de Salón',
                'explicacion': """
                Gráfico de pastel que muestra la proporción de asignaciones entre salones de teoría, 
                laboratorios y salones inválidos. Permite visualizar rápidamente el balance entre 
                tipos de espacios.
                <br/><br/>
                <b>Observación:</b> La distribución refleja la naturaleza práctica de las materias 
                de ISC, con una proporción significativa de clases en laboratorio.
                """
            },
            {
                'archivo': '04_uso_por_dia.png',
                'titulo': 'Figura 4: Uso de Salones por Día de la Semana',
                'explicacion': """
                Gráfico de líneas que compara el número de asignaciones por día entre lunes y viernes. 
                Permite identificar días con mayor o menor carga de clases.
                <br/><br/>
                <b>Observación:</b> La distribución es relativamente uniforme de lunes a jueves, 
                con una ligera reducción el viernes. Esto es típico en horarios académicos.
                """
            },
            {
                'archivo': '05_salones_invalidos_detalle.png',
                'titulo': 'Figura 5: Detalle de Salones Inválidos por Tipo',
                'explicacion': """
                Desglosa las asignaciones inválidas por tipo de salón (AV1, AV2, AV4, AV5, E11), 
                mostrando cuáles son los más problemáticos.
                <br/><br/>
                <b>Observación:</b> Permite identificar patrones en el uso de salones inválidos 
                y priorizar su eliminación según frecuencia.
                """
            },
            {
                'archivo': '06_heatmap_uso.png',
                'titulo': 'Figura 6: Mapa de Calor de Uso por Día y Hora',
                'explicacion': """
                Mapa de calor que muestra la intensidad de uso de salones por bloque horario y día. 
                Los colores más intensos indican mayor número de asignaciones simultáneas.
                <br/><br/>
                <b>Observación:</b> Los bloques de 10-11, 11-12 y 13-14 muestran mayor actividad. 
                Esta información es valiosa para redistribuir clases y reducir conflictos en horas pico.
                """
            },
            {
                'archivo': '07_uso_por_piso.png',
                'titulo': 'Figura 7: Distribución por Piso/Ubicación',
                'explicacion': """
                Compara el uso de salones entre planta baja, planta alta, y laboratorios de piso 1 y 2.
                Ayuda a identificar si hay desequilibrio en el uso de diferentes niveles del edificio.
                <br/><br/>
                <b>Observación:</b> Importante para considerar restricciones de movilidad de profesores 
                y optimizar desplazamientos verticales.
                """
            },
            {
                'archivo': '08_top_materias.png',
                'titulo': 'Figura 8: Top 10 Materias con Más Asignaciones',
                'explicacion': """
                Muestra las materias que tienen mayor número de grupos o sesiones asignadas.
                <br/><br/>
                <b>Observación:</b> Las materias de tronco común y especialidad tienen más secciones, 
                lo que requiere mayor disponibilidad de salones apropiados.
                """
            },
            {
                'archivo': '09_distribucion_horas.png',
                'titulo': 'Figura 9: Distribución por Bloque Horario',
                'explicacion': """
                Muestra cuántas asignaciones hay en cada bloque horario del día (07:00 a 19:00).
                <br/><br/>
                <b>Observación:</b> Permite identificar horas con mayor demanda de salones y 
                planificar mejor la capacidad disponible.
                """
            },
            {
                'archivo': '10_grupos_primer_semestre.png',
                'titulo': 'Figura 10: Análisis de Grupos de Primer Semestre',
                'explicacion': """
                Analiza específicamente los grupos de primer semestre, que tienen la restricción 
                de usar un solo salón de teoría para facilitar adaptación de estudiantes.
                <br/><br/>
                <b>Observación:</b> Verificar que esta restricción se cumpla es crítico para 
                la experiencia de estudiantes nuevos.
                """
            },
            {
                'archivo': '11_resumen_metricas.png',
                'titulo': 'Figura 11: Resumen de Métricas Clave',
                'explicacion': """
                Panel con 4 métricas fundamentales: total de asignaciones, salones únicos, 
                materias y profesores. Vista rápida del alcance del horario.
                <br/><br/>
                <b>Observación:</b> Las métricas estructurales (materias, grupos, profesores) 
                se mantienen constantes, mientras que el uso de salones es optimizable.
                """
            },
            {
                'archivo': '12_comparativa_final.png',
                'titulo': 'Figura 12: Comparativa Final de Todas las Métricas',
                'explicacion': """
                Gráfico de barras agrupadas que resume todas las métricas clave lado a lado. 
                Permite una comparación visual rápida del impacto de la optimización.
                <br/><br/>
                <b>Observación:</b> Vista consolidada para evaluar el impacto global de la optimización 
                en todos los aspectos del horario.
                """
            },
            {
                'archivo': '13_movimientos_profesores.png',
                'titulo': 'Figura 13: Movimientos de Profesores',
                'explicacion': f"""
                <b>MÉTRICA CRÍTICA DE OPTIMIZACIÓN:</b> Compara movimientos entre salones, 
                cambios de piso y distancia total recorrida por profesores.
                <br/><br/>
                <b>Resultados:</b><br/>
                • Movimientos: {metricas_mov.get('Total Movimientos', {}).get('inicial', 'N/A')} → 
                {metricas_mov.get('Total Movimientos', {}).get('optimizado', 'N/A')} 
                ({metricas_mov.get('Total Movimientos', {}).get('mejora_pct', 0):+.1f}%)<br/>
                • Cambios de piso: {metricas_mov.get('Cambios de Piso', {}).get('inicial', 'N/A')} → 
                {metricas_mov.get('Cambios de Piso', {}).get('optimizado', 'N/A')} 
                ({metricas_mov.get('Cambios de Piso', {}).get('mejora_pct', 0):+.1f}%)<br/>
                • Distancia: {metricas_mov.get('Distancia Total', {}).get('inicial', 'N/A')} → 
                {metricas_mov.get('Distancia Total', {}).get('optimizado', 'N/A')} unidades 
                ({metricas_mov.get('Distancia Total', {}).get('mejora_pct', 0):+.1f}%)
                <br/><br/>
                <b>Impacto:</b> Reducir movimientos mejora la experiencia docente, reduce tiempos 
                muertos y minimiza fatiga física.
                """
            },
            {
                'archivo': '14_distribucion_movimientos.png',
                'titulo': 'Figura 14: Distribución de Movimientos por Profesor',
                'explicacion': """
                Muestra los 15 profesores con más movimientos entre salones, comparando 
                horario inicial vs optimizado.
                <br/><br/>
                <b>Observación:</b> Permite identificar casos específicos donde la optimización 
                tuvo mayor impacto y profesores que aún requieren mejoras. Algunos profesores 
                pueden tener hasta 20+ movimientos semanales que deben reducirse.
                """
            },
            {
                'archivo': '15_metricas_optimizacion.png',
                'titulo': 'Figura 15: Resumen Completo de Optimización',
                'explicacion': """
                Panel consolidado con las 4 métricas principales de optimización: asignaciones 
                inválidas, movimientos de profesores, cambios de piso y distancia total.
                <br/><br/>
                <b>Conclusión:</b> Esta gráfica resume el éxito global de la optimización. 
                Un método efectivo debe mostrar mejoras (barras verdes más bajas) en todas 
                las métricas simultáneamente.
                """
            },
        ]
        
        for idx, grafico_info in enumerate(graficos_info):
            ruta_img = self.carpeta_graficos / grafico_info['archivo']
            if ruta_img.exists():
                # Título de la figura
                cap_para = Paragraph(f"<b>{grafico_info['titulo']}</b>", self.styles['Normal'])
                self.story.append(cap_para)
                self.story.append(Spacer(1, 0.1*inch))
                
                # Imagen
                img = Image(str(ruta_img), width=6*inch, height=3.5*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.15*inch))
                
                # Explicación
                explicacion_para = Paragraph(grafico_info['explicacion'], self.styles['Normal'])
                self.story.append(explicacion_para)
                self.story.append(Spacer(1, 0.3*inch))
                
                # Page break después de cada 2 gráficos
                if idx % 2 == 1 and idx < len(graficos_info) - 1:
                    self.story.append(PageBreak())

    
    def crear_conclusiones(self, stats):
        """Crea la sección de conclusiones"""
        titulo = Paragraph("<b>4. CONCLUSIONES Y OBSERVACIONES</b>", self.styles['SubHeading'])
        self.story.append(titulo)
        
        # Cargar métricas de movimientos
        metricas_mov_path = self.carpeta_graficos / 'metricas_movimientos.csv'
        mov_text = ""
        if metricas_mov_path.exists():
            df_mov = pd.read_csv(metricas_mov_path)
            
            # Buscar "Movimientos Totales"
            mov_row = df_mov[df_mov['Metrica'] == 'Movimientos Totales']
            if not mov_row.empty:
                mov_inicial = int(mov_row['Inicial'].values[0])
                mov_opt = int(mov_row['Optimizado'].values[0])
                mov_mejora = mov_inicial - mov_opt
                mov_pct = (mov_mejora / mov_inicial * 100) if mov_inicial > 0 else 0
                
                mov_text = f"""
                <b>Movimientos de Profesores:</b><br/>
                • Movimientos totales: {mov_inicial} → {mov_opt} ({mov_pct:+.1f}%)<br/>
                • Impacto en experiencia docente y eficiencia operativa<br/><br/>
                """
        
        conclusiones_text = f"""
        <b>4.1 Resultados Principales</b><br/><br/>
        
        El análisis comparativo entre el horario inicial y el horario optimizado revela 
        los siguientes hallazgos:<br/><br/>
        
        <b>Asignaciones Inválidas:</b><br/>
        • Se mantienen {stats['inv_opt']} asignaciones a salones inválidos (AV1, AV2, AV4, AV5, E11)<br/>
        • Esto representa un área de oportunidad para futuras optimizaciones<br/>
        • El objetivo es reducir estas asignaciones a 0<br/><br/>
        
        {mov_text}
        
        <b>Uso de Salones:</b><br/>
        • Se utilizan {stats['salones_opt']} salones diferentes<br/>
        • Distribución entre teoría ({stats['teoria_opt']} asignaciones) y 
        laboratorio ({stats['lab_opt']} asignaciones)<br/><br/>
        
        <b>4.2 Áreas de Mejora Identificadas</b><br/><br/>
        
        1. <b>Eliminación de Salones Inválidos:</b> Prioridad alta para reasignar las 
        {stats['inv_opt']} asignaciones actuales<br/>
        2. <b>Optimización de Movimientos:</b> Reducir desplazamientos de profesores entre salones 
        y cambios de piso<br/>
        3. <b>Grupos de Primer Semestre:</b> Mantener restricción de un solo salón por grupo<br/>
        4. <b>Restricciones de Movilidad:</b> Considerar profesores con limitaciones físicas<br/>
        5. <b>Balanceo de Carga:</b> Distribuir mejor el uso de salones para evitar sobrecarga<br/><br/>
        
        <b>4.3 Próximos Pasos</b><br/><br/>
        
        Los siguientes métodos de optimización se aplicarán para mejorar estos resultados:<br/>
        • <b>Machine Learning:</b> Aprendizaje de patrones óptimos de asignación<br/>
        • <b>Programación Lineal Entera (ILP):</b> Modelo matemático exacto<br/>
        • <b>Algoritmo Genético Evolutivo:</b> Búsqueda heurística avanzada<br/><br/>
        
        Cada método será evaluado con las mismas 15 métricas visuales y métricas de movimientos 
        para comparación objetiva y reproducible.
        """
        
        conclusiones_para = Paragraph(conclusiones_text, self.styles['Normal'])
        self.story.append(conclusiones_para)
    
    def generar_pdf(self):
        """Genera el PDF completo"""
        print(f"\n📄 Generando reporte PDF...")
        
        # Crear documento
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Calcular estadísticas
        stats = self.calcular_estadisticas()
        
        # Construir contenido
        self.crear_portada()
        self.crear_resumen_ejecutivo(stats)
        self.crear_tabla_comparativa(stats)
        self.story.append(PageBreak())
        self.agregar_graficos(stats)
        self.crear_conclusiones(stats)
        
        # Generar PDF
        doc.build(self.story)
        print(f"✅ PDF generado: {self.output_path}")
        print(f"   Páginas: ~{len(self.story) // 10 + 1}")
        print(f"   Tamaño: {Path(self.output_path).stat().st_size / 1024:.1f} KB")

def main():
    """Función principal"""
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    csv_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/02_Horario_Optimizado_Profesor.csv"
    carpeta_graficos = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/01_inicial_vs_profesor"
    output_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/01_inicial_vs_profesor/Reporte_Comparativo_01.pdf"
    
    generador = GeneradorReportePDF(csv_inicial, csv_optimizado, carpeta_graficos, output_path, nombre_metodo="Profesor")
    generador.generar_pdf()
    
    print("\n🎯 Reporte profesional completado")
    print("   Listo para presentación o artículo de investigación\n")

if __name__ == "__main__":
    main()
