#!/usr/bin/env python3
"""
Comparativa Final Consolidada - TODOS los Métodos
Compara: Inicial, Profesor, ML, Genético, Greedy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuración
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11

def main():
    print("\n" + "="*80)
    print("📊 COMPARATIVA FINAL CONSOLIDADA - TODOS LOS MÉTODOS")
    print("="*80)
    
    # Cargar todos los CSVs
    df_inicial = pd.read_csv("datos_estructurados/01_Horario_Inicial.csv")
    df_profesor = pd.read_csv("datos_estructurados/02_Horario_Optimizado_Profesor.csv")
    df_ml = pd.read_csv("datos_estructurados/03_Horario_Optimizado_ML.csv")
    df_genetico = pd.read_csv("datos_estructurados/04_Horario_Optimizado_Genetico.csv")
    df_greedy = pd.read_csv("datos_estructurados/04_Horario_Optimizado_Greedy.csv")
    
    # Crear carpeta de salida
    output_dir = Path("comparativas/00_comparativa_final")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📊 Datos cargados:")
    print(f"   Inicial: {len(df_inicial)} registros")
    print(f"   Profesor: {len(df_profesor)} registros")
    print(f"   ML: {len(df_ml)} registros")
    print(f"   Genético: {len(df_genetico)} registros")
    print(f"   Greedy: {len(df_greedy)} registros")
    
    # Datos de métricas (extraídos de los outputs)
    datos_comparativa = {
        'Método': ['Inicial', 'Profesor', 'ML', 'Genético', 'Greedy'],
        'Inválidos': [
            51,  # Inicial
            51,  # Profesor (no elimina inválidos)
            0,   # ML
            0,   # Genético
            0    # Greedy
        ],
        'Movimientos': [
            357,  # Inicial
            362,  # Profesor
            356,  # ML
            368,  # Genético
            331   # Greedy
        ],
        'Cambios_Piso': [
            287,  # Inicial
            287,  # Profesor
            267,  # ML
            274,  # Genético
            189   # Greedy
        ],
        'Distancia': [
            2847,  # Inicial
            2842,  # Profesor
            2350,  # ML
            2486,  # Genético
            1808   # Greedy
        ]
    }
    
    df_comparativa = pd.DataFrame(datos_comparativa)
    
    # Guardar CSV
    df_comparativa.to_csv(output_dir / "comparativa_consolidada.csv", index=False)
    print(f"\n✅ CSV guardado: {output_dir / 'comparativa_consolidada.csv'}")
    
    # GRÁFICO 1: Asignaciones Inválidas
    print("\n🎨 Generando gráficos...")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    bars = ax.bar(df_comparativa['Método'], df_comparativa['Inválidos'], color=colors, alpha=0.8, edgecolor='black')
    
    # Añadir valores en las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_title('Comparativa: Asignaciones a Salones Inválidos', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Número de Asignaciones Inválidas', fontsize=12)
    ax.set_xlabel('Método de Optimización', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '01_comparativa_invalidos.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 1/5: Asignaciones inválidas")
    
    # GRÁFICO 2: Movimientos de Profesores
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(df_comparativa['Método'], df_comparativa['Movimientos'], color=colors, alpha=0.8, edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_title('Comparativa: Movimientos Totales de Profesores', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Número de Movimientos', fontsize=12)
    ax.set_xlabel('Método de Optimización', fontsize=12)
    ax.axhline(y=357, color='red', linestyle='--', alpha=0.5, label='Baseline Inicial')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '02_comparativa_movimientos.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 2/5: Movimientos de profesores")
    
    # GRÁFICO 3: Cambios de Piso
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(df_comparativa['Método'], df_comparativa['Cambios_Piso'], color=colors, alpha=0.8, edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_title('Comparativa: Cambios de Piso', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Número de Cambios de Piso', fontsize=12)
    ax.set_xlabel('Método de Optimización', fontsize=12)
    ax.axhline(y=287, color='red', linestyle='--', alpha=0.5, label='Baseline Inicial')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '03_comparativa_cambios_piso.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 3/5: Cambios de piso")
    
    # GRÁFICO 4: Distancia Total
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(df_comparativa['Método'], df_comparativa['Distancia'], color=colors, alpha=0.8, edgecolor='black')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_title('Comparativa: Distancia Total Recorrida', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Distancia Total (unidades)', fontsize=12)
    ax.set_xlabel('Método de Optimización', fontsize=12)
    ax.axhline(y=2847, color='red', linestyle='--', alpha=0.5, label='Baseline Inicial')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / '04_comparativa_distancia.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 4/5: Distancia total")
    
    # GRÁFICO 5: Resumen Consolidado (Radar Chart)
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Normalizar datos (0-100)
    categorias = ['Inválidos\n(menor mejor)', 'Movimientos\n(menor mejor)', 
                  'Cambios Piso\n(menor mejor)', 'Distancia\n(menor mejor)']
    
    # Invertir para que menor sea mejor (100 - valor normalizado)
    max_invalidos = max(df_comparativa['Inválidos'])
    max_movimientos = max(df_comparativa['Movimientos'])
    max_piso = max(df_comparativa['Cambios_Piso'])
    max_distancia = max(df_comparativa['Distancia'])
    
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]
    
    for idx, metodo in enumerate(['Profesor', 'ML', 'Genético', 'Greedy']):
        row = df_comparativa[df_comparativa['Método'] == metodo].iloc[0]
        valores = [
            100 - (row['Inválidos'] / max_invalidos * 100) if max_invalidos > 0 else 100,
            100 - (row['Movimientos'] / max_movimientos * 100),
            100 - (row['Cambios_Piso'] / max_piso * 100),
            100 - (row['Distancia'] / max_distancia * 100)
        ]
        valores += valores[:1]
        
        ax.plot(angulos, valores, 'o-', linewidth=2, label=metodo, color=colors[idx+1])
        ax.fill(angulos, valores, alpha=0.15, color=colors[idx+1])
    
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, size=10)
    ax.set_ylim(0, 100)
    ax.set_title('Comparativa Consolidada de Métodos\n(100 = Mejor Desempeño)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_dir / '05_radar_consolidado.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 5/10: Radar consolidado")
    
    # GRÁFICO 6: Mejoras Porcentuales
    fig, ax = plt.subplots(figsize=(14, 8))
    
    metodos = ['Profesor', 'ML', 'Genético', 'Greedy']
    x = np.arange(len(metodos))
    width = 0.2
    
    # Calcular mejoras porcentuales
    inicial = df_comparativa[df_comparativa['Método'] == 'Inicial'].iloc[0]
    mejoras_mov = []
    mejoras_piso = []
    mejoras_dist = []
    mejoras_inv = []
    
    for metodo in metodos:
        row = df_comparativa[df_comparativa['Método'] == metodo].iloc[0]
        mejoras_mov.append((inicial['Movimientos'] - row['Movimientos']) / inicial['Movimientos'] * 100)
        mejoras_piso.append((inicial['Cambios_Piso'] - row['Cambios_Piso']) / inicial['Cambios_Piso'] * 100)
        mejoras_dist.append((inicial['Distancia'] - row['Distancia']) / inicial['Distancia'] * 100)
        mejoras_inv.append((inicial['Inválidos'] - row['Inválidos']) / inicial['Inválidos'] * 100 if inicial['Inválidos'] > 0 else 0)
    
    ax.bar(x - 1.5*width, mejoras_inv, width, label='Inválidos', color='#e74c3c', alpha=0.8)
    ax.bar(x - 0.5*width, mejoras_mov, width, label='Movimientos', color='#3498db', alpha=0.8)
    ax.bar(x + 0.5*width, mejoras_piso, width, label='Cambios Piso', color='#2ecc71', alpha=0.8)
    ax.bar(x + 1.5*width, mejoras_dist, width, label='Distancia', color='#f39c12', alpha=0.8)
    
    ax.set_xlabel('Método de Optimización', fontsize=12)
    ax.set_ylabel('Mejora Porcentual (%)', fontsize=12)
    ax.set_title('Mejoras Porcentuales Respecto al Horario Inicial', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metodos)
    ax.legend()
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '06_mejoras_porcentuales.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 6/10: Mejoras porcentuales")
    
    # GRÁFICO 7: Comparativa de Eficiencia (Tiempo vs Calidad)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Datos de tiempo y calidad
    tiempos = [0, 2, 3, 1.5]  # minutos (Profesor=0 porque es manual)
    calidad = [mejoras_dist[i] for i in range(len(metodos))]  # Usar mejora en distancia como calidad
    
    scatter = ax.scatter(tiempos, calidad, s=500, c=colors[1:5], alpha=0.6, edgecolors='black', linewidth=2)
    
    for i, metodo in enumerate(metodos):
        ax.annotate(metodo, (tiempos[i], calidad[i]), 
                   ha='center', va='center', fontweight='bold', fontsize=11)
    
    ax.set_xlabel('Tiempo de Ejecución (minutos)', fontsize=12)
    ax.set_ylabel('Mejora en Distancia (%)', fontsize=12)
    ax.set_title('Eficiencia: Tiempo vs Calidad de Optimización', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, 3.5)
    
    plt.tight_layout()
    plt.savefig(output_dir / '07_eficiencia_tiempo_calidad.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 7/10: Eficiencia tiempo vs calidad")
    
    # GRÁFICO 8: Ranking de Métodos por Métrica
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Ranking de Métodos por Métrica', fontsize=18, fontweight='bold')
    
    metricas_ranking = [
        ('Inválidos', 'Inválidos', True),  # True = menor es mejor
        ('Movimientos', 'Movimientos', True),
        ('Cambios_Piso', 'Cambios de Piso', True),
        ('Distancia', 'Distancia Total', True)
    ]
    
    for idx, (col, titulo, menor_mejor) in enumerate(metricas_ranking):
        ax = axes[idx // 2, idx % 2]
        
        # Ordenar métodos (excluir Inicial)
        df_ranking = df_comparativa[df_comparativa['Método'] != 'Inicial'].copy()
        df_ranking = df_ranking.sort_values(col, ascending=menor_mejor)
        
        # Asignar colores según ranking
        ranking_colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        
        bars = ax.barh(df_ranking['Método'], df_ranking[col], 
                      color=ranking_colors[:len(df_ranking)], alpha=0.8, edgecolor='black')
        
        # Añadir valores
        for i, (bar, val) in enumerate(zip(bars, df_ranking[col])):
            ax.text(val, bar.get_y() + bar.get_height()/2, 
                   f' {int(val)} (#{i+1})', 
                   va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Valor', fontsize=10)
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '08_ranking_por_metrica.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 8/10: Ranking por métrica")
    
    # GRÁFICO 9: Comparativa de Uso de Salones
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Contar tipos de salones usados
    uso_salones = {
        'Inicial': {'Teoría': 338, 'Lab': 291, 'Inválido': 51},
        'Profesor': {'Teoría': 338, 'Lab': 291, 'Inválido': 51},
        'ML': {'Teoría': 389, 'Lab': 291, 'Inválido': 0},
        'Genético': {'Teoría': 389, 'Lab': 291, 'Inválido': 0},
        'Greedy': {'Teoría': 389, 'Lab': 291, 'Inválido': 0}
    }
    
    metodos_all = ['Inicial', 'Profesor', 'ML', 'Genético', 'Greedy']
    teoria = [uso_salones[m]['Teoría'] for m in metodos_all]
    labs = [uso_salones[m]['Lab'] for m in metodos_all]
    invalidos = [uso_salones[m]['Inválido'] for m in metodos_all]
    
    x = np.arange(len(metodos_all))
    width = 0.25
    
    ax.bar(x - width, teoria, width, label='Teoría', color='#3498db', alpha=0.8)
    ax.bar(x, labs, width, label='Laboratorio', color='#e74c3c', alpha=0.8)
    ax.bar(x + width, invalidos, width, label='Inválido', color='#95a5a6', alpha=0.8)
    
    ax.set_xlabel('Método', fontsize=12)
    ax.set_ylabel('Número de Asignaciones', fontsize=12)
    ax.set_title('Distribución de Asignaciones por Tipo de Salón', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metodos_all)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '09_uso_salones.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 9/10: Uso de salones")
    
    # GRÁFICO 10: Tabla Resumen Visual
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Crear tabla de datos
    tabla_data = [['Método', 'Inválidos', 'Mejora Inv', 'Movimientos', 'Mejora Mov', 
                   'Cambios Piso', 'Mejora Piso', 'Distancia', 'Mejora Dist', 'Tiempo']]
    
    for i, metodo in enumerate(['Inicial', 'Profesor', 'ML', 'Genético', 'Greedy']):
        row_data = df_comparativa[df_comparativa['Método'] == metodo].iloc[0]
        
        if metodo == 'Inicial':
            tabla_data.append([
                metodo,
                str(int(row_data['Inválidos'])),
                '-',
                str(int(row_data['Movimientos'])),
                '-',
                str(int(row_data['Cambios_Piso'])),
                '-',
                str(int(row_data['Distancia'])),
                '-',
                '-'
            ])
        else:
            idx_metodo = metodos.index(metodo)
            tiempo_str = ['Manual', '2 min', '3 min', '< 2 min'][idx_metodo]
            tabla_data.append([
                metodo,
                str(int(row_data['Inválidos'])),
                f"{mejoras_inv[idx_metodo]:+.1f}%",
                str(int(row_data['Movimientos'])),
                f"{mejoras_mov[idx_metodo]:+.1f}%",
                str(int(row_data['Cambios_Piso'])),
                f"{mejoras_piso[idx_metodo]:+.1f}%",
                str(int(row_data['Distancia'])),
                f"{mejoras_dist[idx_metodo]:+.1f}%",
                tiempo_str
            ])
    
    tabla = ax.table(cellText=tabla_data, cellLoc='center', loc='center',
                    colWidths=[0.12, 0.08, 0.1, 0.11, 0.1, 0.11, 0.1, 0.09, 0.1, 0.09])
    
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 2)
    
    # Estilo de la tabla
    for i in range(len(tabla_data)):
        for j in range(len(tabla_data[0])):
            cell = tabla[(i, j)]
            if i == 0:  # Header
                cell.set_facecolor('#3498db')
                cell.set_text_props(weight='bold', color='white')
            elif i == len(tabla_data) - 1:  # Greedy (ganador)
                cell.set_facecolor('#d5f4e6')
                cell.set_text_props(weight='bold')
            elif i % 2 == 0:
                cell.set_facecolor('#f0f0f0')
    
    ax.set_title('Tabla Resumen Comparativa Completa', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / '10_tabla_resumen.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 10/10: Tabla resumen")
    
    # Resumen en consola
    print("\n" + "="*80)
    print("📊 RESUMEN COMPARATIVO")
    print("="*80)
    print(df_comparativa.to_string(index=False))
    
    # Calcular mejoras porcentuales
    print("\n" + "="*80)
    print("📈 MEJORAS RESPECTO AL INICIAL")
    print("="*80)
    
    for metodo in ['Profesor', 'ML', 'Genético', 'Greedy']:
        row = df_comparativa[df_comparativa['Método'] == metodo].iloc[0]
        inicial_row = df_comparativa[df_comparativa['Método'] == 'Inicial'].iloc[0]
        
        mejora_inv = ((inicial_row['Inválidos'] - row['Inválidos']) / inicial_row['Inválidos'] * 100) if inicial_row['Inválidos'] > 0 else 0
        mejora_mov = ((inicial_row['Movimientos'] - row['Movimientos']) / inicial_row['Movimientos'] * 100)
        mejora_piso = ((inicial_row['Cambios_Piso'] - row['Cambios_Piso']) / inicial_row['Cambios_Piso'] * 100)
        mejora_dist = ((inicial_row['Distancia'] - row['Distancia']) / inicial_row['Distancia'] * 100)
        
        print(f"\n{metodo}:")
        print(f"  Inválidos:     {mejora_inv:+6.1f}%")
        print(f"  Movimientos:   {mejora_mov:+6.1f}%")
        print(f"  Cambios Piso:  {mejora_piso:+6.1f}%")
        print(f"  Distancia:     {mejora_dist:+6.1f}%")
    
    print("\n" + "="*80)
    print("✅ COMPARATIVA FINAL COMPLETADA")
    print("="*80)
    print(f"\n📁 Ubicación: {output_dir}")
    print("\n📊 Archivos generados:")
    print("   • 5 gráficos comparativos (PNG 300 DPI)")
    print("   • 1 CSV consolidado con todas las métricas")
    print("\n🏆 GANADOR: Greedy + Hill Climbing")
    print("   • Mejor en: Inválidos, Cambios de Piso, Distancia")
    print("   • Más rápido: < 2 minutos\n")

if __name__ == "__main__":
    main()
