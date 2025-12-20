#!/usr/bin/env python3
"""
Pipeline Comparativo: Inicial vs Profesor Optimizado
Genera análisis completo con 15 gráficos + PDF + Excel
"""

import sys
import os

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generar_analisis_comparativo import AnalizadorComparativoExpandido
from generar_reporte_pdf import GeneradorReportePDF
from generar_excel_formateado import generar_excel_formateado

def main():
    print("\n" + "="*80)
    print("🚀 PIPELINE COMPARATIVO - 01_inicial_vs_profesor")
    print("="*80)
    
    # Rutas
    csv_inicial = "datos_estructurados/01_Horario_Inicial.csv"
    csv_optimizado = "datos_estructurados/02_Horario_Optimizado_Profesor.csv"
    carpeta_salida = "comparativas/01_inicial_vs_profesor"
    
    # PASO 1: Generar gráficos comparativos
    print("\n📊 PASO 1/3: Generando gráficos comparativos...")
    print("-" * 80)
    
    analizador = AnalizadorComparativoExpandido(csv_inicial, csv_optimizado, carpeta_salida)
    estadisticas = analizador.generar_reporte_completo()
    
    print("\n" + "-" * 80)
    print("✅ Gráficos completados\n")
    
    # PASO 2: Generar PDF
    print("📄 PASO 2/3: Generando reporte PDF...")
    print("-" * 80)
    
    pdf_path = os.path.join(carpeta_salida, "Reporte_01_inicial_vs_profesor.pdf")
    generador_pdf = GeneradorReportePDF(csv_inicial, csv_optimizado, carpeta_salida, pdf_path, nombre_metodo="Optimización Manual del Profesor")
    generador_pdf.generar_pdf()
    
    print("\n" + "-" * 80)
    print("✅ PDF completado\n")
    
    # PASO 3: Generar Excel formateado
    print("📊 PASO 3/3: Generando Excel formateado...")
    print("-" * 80)
    
    generar_excel_formateado(
        archivo_csv=csv_optimizado,
        carpeta_salida=carpeta_salida,
        nombre_archivo="Horario_Optimizado_Profesor"
    )
    
    print("-" * 80)
    print("✅ Excel completado\n")
    
    # Resumen final
    print("="*80)
    print("✅ COMPARATIVA PROFESOR COMPLETADA")
    print("="*80)
    
    print(f"\n📁 Ubicación: {carpeta_salida}")
    print("\n📊 Archivos generados:")
    print("   • 15 gráficos profesionales (PNG 300 DPI)")
    print("   • 1 archivo de estadísticas (CSV)")
    print("   • 1 reporte completo (PDF con explicaciones)")
    print("   • 1 horario formateado (Excel)")
    
    print("\n🎯 Baseline del Profesor documentado y analizado")
    print("\n📋 Próximos métodos:")
    print("   • Machine Learning")
    print("   • Algoritmo Genético")
    print("   • Greedy + Hill Climbing")
    print("   • Comparativa final de todos\n")

if __name__ == "__main__":
    main()
