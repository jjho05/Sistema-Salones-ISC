#!/usr/bin/env python3
"""
Pipeline Comparativo - Inicial vs ML
Genera análisis completo del método Machine Learning
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generar_analisis_comparativo import AnalizadorComparativoExpandido
from generar_reporte_pdf import GeneradorReportePDF

def main():
    """Ejecuta pipeline comparativo para ML"""
    
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    csv_ml = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/03_Horario_Optimizado_ML.csv"
    nombre_comparativa = "02_inicial_vs_ml"
    carpeta_salida = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/02_inicial_vs_ml"
    
    print("\n" + "="*80)
    print(f"🚀 PIPELINE COMPARATIVO - {nombre_comparativa}")
    print("="*80 + "\n")
    
    # PASO 1: Generar gráficos
    print("📊 PASO 1/2: Generando gráficos comparativos...")
    print("-" * 80)
    
    analizador = AnalizadorComparativoExpandido(csv_inicial, csv_ml, carpeta_salida)
    analizador.generar_reporte_completo()
    
    print("\n" + "-" * 80)
    print("✅ Gráficos completados\n")
    
    # PASO 2: Generar PDF
    print("📄 PASO 2/2: Generando reporte PDF...")
    print("-" * 80)
    
    pdf_path = os.path.join(carpeta_salida, f"Reporte_{nombre_comparativa}.pdf")
    generador_pdf = GeneradorReportePDF(csv_inicial, csv_ml, carpeta_salida, pdf_path, nombre_metodo="Machine Learning")
    generador_pdf.generar_pdf()
    
    print("\n" + "-" * 80)
    print("✅ PDF completado\n")
    
    # PASO 3: Generar Excel formateado
    print("📊 PASO 3/3: Generando Excel formateado...")
    print("-" * 80)
    
    from generar_excel_formateado import generar_excel_formateado
    generar_excel_formateado(csv_ml, carpeta_salida, "Horario_Optimizado_ML")
    
    print("\n" + "-" * 80)
    print("✅ Excel completado\n")
    
    # RESUMEN FINAL
    print("="*80)
    print("✅ COMPARATIVA ML COMPLETADA")
    print("="*80)
    print(f"\n📁 Ubicación: {carpeta_salida}")
    print(f"\n📊 Archivos generados:")
    print(f"   • 15 gráficos profesionales (PNG 300 DPI)")
    print(f"   • 1 archivo de estadísticas (CSV)")
    print(f"   • 1 reporte completo (PDF con explicaciones)")
    print(f"   • 1 horario formateado (Excel)")
    print(f"\n🎯 Método Machine Learning documentado y analizado")
    print(f"\n📋 Próximos métodos:")
    print(f"   • ILP (Programación Lineal Entera)")
    print(f"   • Genético Evolutivo")
    print(f"   • Comparativa final de todos\n")

if __name__ == "__main__":
    main()
