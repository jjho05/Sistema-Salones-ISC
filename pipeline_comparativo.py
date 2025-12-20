#!/usr/bin/env python3
"""
PIPELINE MAESTRO - Análisis Comparativo Completo
Genera gráficos + PDF en un solo proceso
Este será el script principal para todas las comparativas futuras
"""

import sys
import os

# Importar los módulos de análisis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generar_analisis_comparativo import AnalizadorComparativoExpandido
from generar_reporte_pdf import GeneradorReportePDF

def ejecutar_pipeline_comparativo(
    csv_inicial,
    csv_optimizado,
    nombre_comparativa,
    carpeta_salida
):
    """
    Ejecuta el pipeline completo de análisis comparativo
    
    Args:
        csv_inicial: Ruta al CSV del horario inicial
        csv_optimizado: Ruta al CSV del horario optimizado
        nombre_comparativa: Nombre de la comparativa (ej: "01_inicial_vs_profesor")
        carpeta_salida: Carpeta donde guardar resultados
    """
    
    print("\n" + "="*80)
    print(f"🚀 PIPELINE MAESTRO - {nombre_comparativa}")
    print("="*80 + "\n")
    
    # PASO 1: Generar gráficos
    print("📊 PASO 1/2: Generando gráficos comparativos...")
    print("-" * 80)
    
    analizador = AnalizadorComparativoExpandido(
        csv_inicial,
        csv_optimizado,
        carpeta_salida
    )
    analizador.generar_reporte_completo()
    
    print("\n" + "-" * 80)
    print("✅ Gráficos completados\n")
    
    # PASO 2: Generar PDF
    print("📄 PASO 2/2: Generando reporte PDF...")
    print("-" * 80)
    
    pdf_path = os.path.join(carpeta_salida, f"Reporte_{nombre_comparativa}.pdf")
    generador_pdf = GeneradorReportePDF(
        csv_inicial,
        csv_optimizado,
        carpeta_salida,
        pdf_path
    )
    generador_pdf.generar_pdf()
    
    print("\n" + "-" * 80)
    print("✅ PDF completado\n")
    
    # PASO 3: Generar Excel formateado
    print("📊 PASO 3/3: Generando Excel formateado...")
    print("-" * 80)
    
    from generar_excel_formateado import generar_excel_formateado
    generar_excel_formateado(csv_optimizado, carpeta_salida, "Horario_Optimizado_Profesor")
    
    print("\n" + "-" * 80)
    print("✅ Excel completado\n")
    
    # RESUMEN FINAL
    print("="*80)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*80)
    print(f"\n📁 Ubicación: {carpeta_salida}")
    print(f"\n📊 Archivos generados:")
    print(f"   • 15 gráficos profesionales (PNG 300 DPI)")
    print(f"   • 1 archivo de estadísticas (CSV)")
    print(f"   • 1 reporte completo (PDF con explicaciones)")
    print(f"   • 1 horario formateado (Excel)")
    print(f"\n🎯 Todo listo para análisis y presentación\n")
    
    return carpeta_salida

def main():
    """Función principal - Ejecuta comparativa 01"""
    
    # Configuración para Comparativa 01: Inicial vs Profesor
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    csv_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/02_Horario_Optimizado_Profesor.csv"
    nombre_comparativa = "01_inicial_vs_profesor"
    carpeta_salida = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/01_inicial_vs_profesor"
    
    # Ejecutar pipeline
    ejecutar_pipeline_comparativo(
        csv_inicial,
        csv_optimizado,
        nombre_comparativa,
        carpeta_salida
    )

if __name__ == "__main__":
    main()
