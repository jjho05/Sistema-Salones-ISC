#!/usr/bin/env python3
"""
Análisis Comparativo EXPANDIDO - Horario Inicial vs Optimizado
Versión profesional con gráficos adicionales y análisis profundo
Incluye análisis de movimientos de profesores
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analizar_movimientos import AnalizadorMovimientos
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo profesional
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300

class AnalizadorComparativoExpandido:
    def __init__(self, csv_inicial, csv_optimizado, output_dir):
        self.df_inicial = pd.read_csv(csv_inicial)
        self.df_optimizado = pd.read_csv(csv_optimizado)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar analizador de movimientos
        self.analizador_mov = AnalizadorMovimientos()
        self.metricas_movimientos = None
        
        print(f"📊 Datos cargados:")
        print(f"   Inicial: {len(self.df_inicial)} registros")
        print(f"   Optimizado: {len(self.df_optimizado)} registros")
    
    def calcular_metricas_movimientos(self):
        """Calcula métricas de movimientos de profesores"""
        if self.metricas_movimientos is None:
            print("📊 Calculando métricas de movimientos...")
            self.metricas_movimientos = self.analizador_mov.comparar_horarios(
                self.df_inicial, 
                self.df_optimizado
            )
        return self.metricas_movimientos
    
    def generar_estadisticas_generales(self):
        """Genera comparativa de estadísticas generales"""
        stats = {
            'Métrica': [],
            'Inicial': [],
            'Optimizado': [],
            'Diferencia': [],
            'Mejora (%)': []
        }
        
        metricas = [
            ('Total Asignaciones', len(self.df_inicial), len(self.df_optimizado)),
            ('⚠️ Asignaciones Inválidas', self.df_inicial['Es_Invalido'].sum(), self.df_optimizado['Es_Invalido'].sum()),
            ('Salones Utilizados', self.df_inicial['Salon'].nunique(), self.df_optimizado['Salon'].nunique()),
            ('Materias Únicas', self.df_inicial['Materia'].nunique(), self.df_optimizado['Materia'].nunique()),
            ('Grupos Únicos', self.df_inicial['Grupo'].nunique(), self.df_optimizado['Grupo'].nunique()),
            ('Profesores', self.df_inicial['Profesor'].nunique(), self.df_optimizado['Profesor'].nunique()),
            ('Salones Teoría', len(self.df_inicial[self.df_inicial['Tipo_Salon']=='Teoría']['Salon'].unique()),
             len(self.df_optimizado[self.df_optimizado['Tipo_Salon']=='Teoría']['Salon'].unique())),
            ('Laboratorios', len(self.df_inicial[self.df_inicial['Tipo_Salon']=='Laboratorio']['Salon'].unique()),
             len(self.df_optimizado[self.df_optimizado['Tipo_Salon']=='Laboratorio']['Salon'].unique())),
        ]
        
        for metrica, val_ini, val_opt in metricas:
            stats['Métrica'].append(metrica)
            stats['Inicial'].append(val_ini)
            stats['Optimizado'].append(val_opt)
            diff = val_opt - val_ini
            stats['Diferencia'].append(diff)
            
            if 'Inválidas' in metrica and val_ini > 0:
                mejora = ((val_ini - val_opt) / val_ini * 100)
                stats['Mejora (%)'].append(round(mejora, 2))
            else:
                stats['Mejora (%)'].append(0)
        
        df_stats = pd.DataFrame(stats)
        csv_path = self.output_dir / 'estadisticas_comparativas.csv'
        df_stats.to_csv(csv_path, index=False)
        print(f"✅ Estadísticas guardadas: {csv_path}")
        
        return df_stats
    
    def grafico_asignaciones_invalidas(self):
        """Gráfico de barras: Asignaciones inválidas"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        inv_inicial = self.df_inicial['Es_Invalido'].sum()
        inv_optimizado = self.df_optimizado['Es_Invalido'].sum()
        
        categorias = ['Horario Inicial', 'Horario Optimizado']
        valores = [inv_inicial, inv_optimizado]
        colores = ['#FF6B6B', '#4ECDC4']
        
        bars = ax.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        ax.set_ylabel('Número de Asignaciones Inválidas', fontsize=12, fontweight='bold')
        ax.set_title('Comparativa: Asignaciones a Salones Inválidos (AV/E11)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        ax.axhline(y=0, color='green', linestyle='--', linewidth=2, label='Objetivo: 0')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '01_asignaciones_invalidas.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 1/12 generado")
    
    def grafico_distribucion_salones(self):
        """Gráfico de distribución de uso de salones"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        salon_counts_ini = self.df_inicial['Salon'].value_counts().head(15)
        ax1.barh(range(len(salon_counts_ini)), salon_counts_ini.values, color='#3498db')
        ax1.set_yticks(range(len(salon_counts_ini)))
        ax1.set_yticklabels(salon_counts_ini.index)
        ax1.set_xlabel('Número de Asignaciones', fontweight='bold')
        ax1.set_title('Horario Inicial - Top 15 Salones', fontweight='bold', fontsize=13)
        ax1.grid(axis='x', alpha=0.3)
        
        salon_counts_opt = self.df_optimizado['Salon'].value_counts().head(15)
        ax2.barh(range(len(salon_counts_opt)), salon_counts_opt.values, color='#2ecc71')
        ax2.set_yticks(range(len(salon_counts_opt)))
        ax2.set_yticklabels(salon_counts_opt.index)
        ax2.set_xlabel('Número de Asignaciones', fontweight='bold')
        ax2.set_title('Horario Optimizado - Top 15 Salones', fontweight='bold', fontsize=13)
        ax2.grid(axis='x', alpha=0.3)
        
        plt.suptitle('Distribución de Uso de Salones', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / '02_distribucion_salones.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 2/12 generado")
    
    def grafico_tipo_salon(self):
        """Gráfico de pastel: Distribución por tipo de salón"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        tipo_ini = self.df_inicial['Tipo_Salon'].value_counts()
        colors1 = ['#3498db', '#e74c3c', '#95a5a6']
        ax1.pie(tipo_ini.values, labels=tipo_ini.index, autopct='%1.1f%%',
               startangle=90, colors=colors1, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Horario Inicial', fontweight='bold', fontsize=13)
        
        tipo_opt = self.df_optimizado['Tipo_Salon'].value_counts()
        ax2.pie(tipo_opt.values, labels=tipo_opt.index, autopct='%1.1f%%',
               startangle=90, colors=colors1, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title('Horario Optimizado', fontweight='bold', fontsize=13)
        
        plt.suptitle('Distribución por Tipo de Salón', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / '03_tipo_salon.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 3/12 generado")
    
    def grafico_uso_por_dia(self):
        """Gráfico de líneas: Uso de salones por día"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        dias_orden = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
        uso_ini = self.df_inicial['Dia'].value_counts().reindex(dias_orden, fill_value=0)
        uso_opt = self.df_optimizado['Dia'].value_counts().reindex(dias_orden, fill_value=0)
        
        ax.plot(dias_orden, uso_ini.values, marker='o', linewidth=2.5, 
               markersize=10, label='Inicial', color='#3498db')
        ax.plot(dias_orden, uso_opt.values, marker='s', linewidth=2.5,
               markersize=10, label='Optimizado', color='#2ecc71')
        
        ax.set_xlabel('Día de la Semana', fontweight='bold', fontsize=12)
        ax.set_ylabel('Número de Asignaciones', fontweight='bold', fontsize=12)
        ax.set_title('Uso de Salones por Día de la Semana', fontweight='bold', fontsize=14, pad=15)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '04_uso_por_dia.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 4/12 generado")
    
    def grafico_salones_invalidos_detalle(self):
        """Gráfico detallado de salones inválidos"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        inv_ini = self.df_inicial[self.df_inicial['Es_Invalido'] == 1]
        if len(inv_ini) > 0:
            salon_inv_ini = inv_ini['Salon'].value_counts()
            ax1.bar(salon_inv_ini.index, salon_inv_ini.values, color='#e74c3c', edgecolor='black')
            ax1.set_xlabel('Salón Inválido', fontweight='bold')
            ax1.set_ylabel('Número de Asignaciones', fontweight='bold')
            ax1.set_title('Horario Inicial', fontweight='bold', fontsize=13)
            ax1.grid(axis='y', alpha=0.3)
            for i, v in enumerate(salon_inv_ini.values):
                ax1.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
        
        inv_opt = self.df_optimizado[self.df_optimizado['Es_Invalido'] == 1]
        if len(inv_opt) > 0:
            salon_inv_opt = inv_opt['Salon'].value_counts()
            ax2.bar(salon_inv_opt.index, salon_inv_opt.values, color='#e74c3c', edgecolor='black')
            ax2.set_xlabel('Salón Inválido', fontweight='bold')
            ax2.set_ylabel('Número de Asignaciones', fontweight='bold')
            ax2.set_title('Horario Optimizado', fontweight='bold', fontsize=13)
            ax2.grid(axis='y', alpha=0.3)
            for i, v in enumerate(salon_inv_opt.values):
                ax2.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle('Detalle de Salones Inválidos por Tipo', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / '05_salones_invalidos_detalle.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 5/12 generado")
    
    def grafico_heatmap_uso(self):
        """Heatmap de uso de salones por día y hora"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        def crear_heatmap(df, ax, titulo):
            pivot = df.groupby(['Bloque_Horario', 'Dia']).size().unstack(fill_value=0)
            pivot = pivot.reindex(columns=['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'], fill_value=0)
            sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', ax=ax, 
                       cbar_kws={'label': 'Asignaciones'}, linewidths=0.5)
            ax.set_title(titulo, fontweight='bold', fontsize=13, pad=10)
            ax.set_xlabel('Día', fontweight='bold')
            ax.set_ylabel('Bloque Horario', fontweight='bold')
        
        crear_heatmap(self.df_inicial, ax1, 'Horario Inicial')
        crear_heatmap(self.df_optimizado, ax2, 'Horario Optimizado')
        
        plt.suptitle('Mapa de Calor: Uso de Salones por Día y Hora', 
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(self.output_dir / '06_heatmap_uso.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 6/12 generado")
    
    def grafico_uso_planta_baja_vs_alta(self):
        """Comparativa uso planta baja vs alta"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        def contar_por_piso(df):
            return {
                'Planta Baja': len(df[df['Piso'] == 'Planta Baja']),
                'Planta Alta': len(df[df['Piso'] == 'Planta Alta']),
                'Primer Piso Lab': len(df[df['Piso'] == 'Primer Piso']),
                'Segundo Piso Lab': len(df[df['Piso'] == 'Segundo Piso'])
            }
        
        pisos_ini = contar_por_piso(self.df_inicial)
        pisos_opt = contar_por_piso(self.df_optimizado)
        
        x = np.arange(len(pisos_ini))
        width = 0.35
        
        ax.bar(x - width/2, list(pisos_ini.values()), width, label='Inicial', color='#3498db')
        ax.bar(x + width/2, list(pisos_opt.values()), width, label='Optimizado', color='#2ecc71')
        
        ax.set_xlabel('Ubicación', fontweight='bold')
        ax.set_ylabel('Número de Asignaciones', fontweight='bold')
        ax.set_title('Distribución por Piso/Ubicación', fontweight='bold', fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(list(pisos_ini.keys()), rotation=15, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '07_uso_por_piso.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 7/12 generado")
    
    def grafico_top_materias(self):
        """Top 10 materias con más asignaciones"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        mat_ini = self.df_inicial['Materia'].value_counts().head(10)
        ax1.barh(range(len(mat_ini)), mat_ini.values, color='#9b59b6')
        ax1.set_yticks(range(len(mat_ini)))
        ax1.set_yticklabels([m[:30] + '...' if len(m) > 30 else m for m in mat_ini.index])
        ax1.set_xlabel('Asignaciones', fontweight='bold')
        ax1.set_title('Inicial - Top 10 Materias', fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        mat_opt = self.df_optimizado['Materia'].value_counts().head(10)
        ax2.barh(range(len(mat_opt)), mat_opt.values, color='#e67e22')
        ax2.set_yticks(range(len(mat_opt)))
        ax2.set_yticklabels([m[:30] + '...' if len(m) > 30 else m for m in mat_opt.index])
        ax2.set_xlabel('Asignaciones', fontweight='bold')
        ax2.set_title('Optimizado - Top 10 Materias', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        plt.suptitle('Materias con Más Asignaciones', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / '08_top_materias.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 8/12 generado")
    
    def grafico_distribucion_horas(self):
        """Distribución de bloques horarios"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        horas_ini = self.df_inicial['Bloque_Horario'].value_counts().sort_index()
        horas_opt = self.df_optimizado['Bloque_Horario'].value_counts().sort_index()
        
        x = np.arange(len(horas_ini))
        width = 0.35
        
        ax.bar(x - width/2, horas_ini.values, width, label='Inicial', color='#3498db', alpha=0.8)
        ax.bar(x + width/2, horas_opt.values, width, label='Optimizado', color='#2ecc71', alpha=0.8)
        
        ax.set_xlabel('Bloque Horario', fontweight='bold')
        ax.set_ylabel('Número de Asignaciones', fontweight='bold')
        ax.set_title('Distribución de Asignaciones por Bloque Horario', fontweight='bold', fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(horas_ini.index, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '09_distribucion_horas.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 9/12 generado")
    
    def grafico_grupos_primer_semestre(self):
        """Análisis de grupos de primer semestre"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        grupos_1er_ini = self.df_inicial[self.df_inicial['Es_Primer_Semestre'] == 1]['Grupo'].nunique()
        grupos_1er_opt = self.df_optimizado[self.df_optimizado['Es_Primer_Semestre'] == 1]['Grupo'].nunique()
        
        asig_1er_ini = len(self.df_inicial[self.df_inicial['Es_Primer_Semestre'] == 1])
        asig_1er_opt = len(self.df_optimizado[self.df_optimizado['Es_Primer_Semestre'] == 1])
        
        categorias = ['Grupos Únicos', 'Total Asignaciones']
        inicial = [grupos_1er_ini, asig_1er_ini]
        optimizado = [grupos_1er_opt, asig_1er_opt]
        
        x = np.arange(len(categorias))
        width = 0.35
        
        ax.bar(x - width/2, inicial, width, label='Inicial', color='#3498db')
        ax.bar(x + width/2, optimizado, width, label='Optimizado', color='#2ecc71')
        
        ax.set_ylabel('Cantidad', fontweight='bold')
        ax.set_title('Grupos de Primer Semestre', fontweight='bold', fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(categorias)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(inicial):
            ax.text(i - width/2, v, str(v), ha='center', va='bottom', fontweight='bold')
        for i, v in enumerate(optimizado):
            ax.text(i + width/2, v, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '10_grupos_primer_semestre.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 10/12 generado")
    
    def grafico_resumen_metricas(self):
        """Gráfico de resumen con múltiples métricas"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Métrica 1: Asignaciones totales
        ax1.bar(['Inicial', 'Optimizado'], 
               [len(self.df_inicial), len(self.df_optimizado)],
               color=['#3498db', '#2ecc71'])
        ax1.set_title('Total de Asignaciones', fontweight='bold')
        ax1.set_ylabel('Cantidad', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Métrica 2: Salones únicos
        ax2.bar(['Inicial', 'Optimizado'],
               [self.df_inicial['Salon'].nunique(), self.df_optimizado['Salon'].nunique()],
               color=['#9b59b6', '#e67e22'])
        ax2.set_title('Salones Únicos Utilizados', fontweight='bold')
        ax2.set_ylabel('Cantidad', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Métrica 3: Materias
        ax3.bar(['Inicial', 'Optimizado'],
               [self.df_inicial['Materia'].nunique(), self.df_optimizado['Materia'].nunique()],
               color=['#1abc9c', '#e74c3c'])
        ax3.set_title('Materias Únicas', fontweight='bold')
        ax3.set_ylabel('Cantidad', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # Métrica 4: Profesores
        ax4.bar(['Inicial', 'Optimizado'],
               [self.df_inicial['Profesor'].nunique(), self.df_optimizado['Profesor'].nunique()],
               color=['#f39c12', '#16a085'])
        ax4.set_title('Profesores', fontweight='bold')
        ax4.set_ylabel('Cantidad', fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Resumen de Métricas Clave', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(self.output_dir / '11_resumen_metricas.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 11/12 generado")
    
    def grafico_comparativa_final(self):
        """Gráfico comparativo final con score"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Calcular scores (menor es mejor para inválidos)
        inv_ini = self.df_inicial['Es_Invalido'].sum()
        inv_opt = self.df_optimizado['Es_Invalido'].sum()
        
        metricas = ['Asignaciones\nInválidas', 'Salones\nUtilizados', 'Materias', 'Grupos', 'Profesores']
        inicial_vals = [
            inv_ini,
            self.df_inicial['Salon'].nunique(),
            self.df_inicial['Materia'].nunique(),
            self.df_inicial['Grupo'].nunique(),
            self.df_inicial['Profesor'].nunique()
        ]
        optimizado_vals = [
            inv_opt,
            self.df_optimizado['Salon'].nunique(),
            self.df_optimizado['Materia'].nunique(),
            self.df_optimizado['Grupo'].nunique(),
            self.df_optimizado['Profesor'].nunique()
        ]
        
        x = np.arange(len(metricas))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, inicial_vals, width, label='Inicial', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x + width/2, optimizado_vals, width, label='Optimizado', color='#2ecc71', alpha=0.8)
        
        ax.set_ylabel('Valor', fontweight='bold', fontsize=12)
        ax.set_title('Comparativa Final: Todas las Métricas', fontweight='bold', fontsize=16, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metricas, fontsize=11)
        ax.legend(fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        # Añadir valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '12_comparativa_final.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 12/15 generado")
    
    def grafico_movimientos_profesores(self):
        """Gráfico de movimientos de profesores"""
        metricas = self.calcular_metricas_movimientos()
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        categorias = ['Movimientos\nentre Salones', 'Cambios\nde Piso', 'Distancia\nTotal (÷10)']
        inicial = [
            metricas['inicial']['total_movimientos'],
            metricas['inicial']['total_cambios_piso'],
            metricas['inicial']['total_distancia'] / 10  # Escalar para visualización
        ]
        optimizado = [
            metricas['optimizado']['total_movimientos'],
            metricas['optimizado']['total_cambios_piso'],
            metricas['optimizado']['total_distancia'] / 10
        ]
        
        x = np.arange(len(categorias))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, inicial, width, label='Inicial', color='#e74c3c', alpha=0.8)
        bars2 = ax.bar(x + width/2, optimizado, width, label='Optimizado', color='#2ecc71', alpha=0.8)
        
        ax.set_ylabel('Cantidad', fontweight='bold', fontsize=12)
        ax.set_title('Comparativa de Movimientos de Profesores', fontweight='bold', fontsize=16, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categorias, fontsize=11)
        ax.legend(fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        # Añadir valores y mejoras
        for i, (bars, vals) in enumerate([(bars1, inicial), (bars2, optimizado)]):
            for j, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height) if j < 2 else int(height*10)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Añadir porcentajes de mejora
        mejoras = [
            metricas['mejora']['movimientos_pct'],
            metricas['mejora']['cambios_piso_pct'],
            metricas['mejora']['distancia_pct']
        ]
        
        for i, mejora in enumerate(mejoras):
            color = 'green' if mejora > 0 else 'red'
            ax.text(i, max(inicial[i], optimizado[i]) * 1.1,
                   f'{mejora:+.1f}%',
                   ha='center', fontsize=11, fontweight='bold', color=color)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '13_movimientos_profesores.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 13/15 generado")
    
    def grafico_distribucion_movimientos(self):
        """Distribución de movimientos por profesor"""
        metricas_completas = self.analizador_mov.analizar_todos_profesores(self.df_inicial)
        metricas_completas_opt = self.analizador_mov.analizar_todos_profesores(self.df_optimizado)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Extraer movimientos por profesor
        movs_ini = []
        movs_opt = []
        profesores = []
        
        for prof, datos in metricas_completas['por_profesor'].items():
            if datos['movimientos'] > 0:  # Solo profesores con movimientos
                profesores.append(prof.replace('PROFESOR ', 'P'))
                movs_ini.append(datos['movimientos'])
        
        for prof in profesores:
            prof_completo = 'PROFESOR ' + prof[1:]
            if prof_completo in metricas_completas_opt['por_profesor']:
                movs_opt.append(metricas_completas_opt['por_profesor'][prof_completo]['movimientos'])
            else:
                movs_opt.append(0)
        
        # Top 15 profesores con más movimientos
        indices = np.argsort(movs_ini)[::-1][:15]
        
        # Inicial
        ax1.barh(range(len(indices)), [movs_ini[i] for i in indices], color='#e74c3c')
        ax1.set_yticks(range(len(indices)))
        ax1.set_yticklabels([profesores[i][:20] for i in indices], fontsize=9)
        ax1.set_xlabel('Movimientos', fontweight='bold')
        ax1.set_title('Inicial - Top 15 Profesores', fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Optimizado
        ax2.barh(range(len(indices)), [movs_opt[i] for i in indices], color='#2ecc71')
        ax2.set_yticks(range(len(indices)))
        ax2.set_yticklabels([profesores[i][:20] for i in indices], fontsize=9)
        ax2.set_xlabel('Movimientos', fontweight='bold')
        ax2.set_title('Optimizado - Top 15 Profesores', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        plt.suptitle('Distribución de Movimientos por Profesor', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(self.output_dir / '14_distribucion_movimientos.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 14/15 generado")
    
    def grafico_metricas_optimizacion(self):
        """Resumen de todas las métricas de optimización"""
        metricas = self.calcular_metricas_movimientos()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Asignaciones inválidas
        inv_ini = self.df_inicial['Es_Invalido'].sum()
        inv_opt = self.df_optimizado['Es_Invalido'].sum()
        ax1.bar(['Inicial', 'Optimizado'], [inv_ini, inv_opt], color=['#e74c3c', '#2ecc71'])
        ax1.set_title('Asignaciones Inválidas', fontweight='bold', fontsize=13)
        ax1.set_ylabel('Cantidad', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        for i, v in enumerate([inv_ini, inv_opt]):
            ax1.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
        
        # 2. Movimientos totales
        mov_ini = metricas['inicial']['total_movimientos']
        mov_opt = metricas['optimizado']['total_movimientos']
        ax2.bar(['Inicial', 'Optimizado'], [mov_ini, mov_opt], color=['#e74c3c', '#2ecc71'])
        ax2.set_title('Movimientos de Profesores', fontweight='bold', fontsize=13)
        ax2.set_ylabel('Cantidad', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        for i, v in enumerate([mov_ini, mov_opt]):
            ax2.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
        
        # 3. Cambios de piso
        piso_ini = metricas['inicial']['total_cambios_piso']
        piso_opt = metricas['optimizado']['total_cambios_piso']
        ax3.bar(['Inicial', 'Optimizado'], [piso_ini, piso_opt], color=['#e74c3c', '#2ecc71'])
        ax3.set_title('Cambios de Piso', fontweight='bold', fontsize=13)
        ax3.set_ylabel('Cantidad', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        for i, v in enumerate([piso_ini, piso_opt]):
            ax3.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
        
        # 4. Distancia total
        dist_ini = metricas['inicial']['total_distancia']
        dist_opt = metricas['optimizado']['total_distancia']
        ax4.bar(['Inicial', 'Optimizado'], [dist_ini, dist_opt], color=['#e74c3c', '#2ecc71'])
        ax4.set_title('Distancia Total Recorrida', fontweight='bold', fontsize=13)
        ax4.set_ylabel('Unidades', fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        for i, v in enumerate([dist_ini, dist_opt]):
            ax4.text(i, v, f'{int(v)}', ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle('Resumen Completo de Métricas de Optimización', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(self.output_dir / '15_metricas_optimizacion.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfico 15/15 generado")
    
    def generar_reporte_completo(self):
        """Genera todos los gráficos y estadísticas"""
        print("\n" + "="*80)
        print("📊 GENERANDO ANÁLISIS COMPARATIVO EXPANDIDO")
        print("="*80 + "\n")
        
        print("📈 Generando estadísticas...")
        stats = self.generar_estadisticas_generales()
        
        print("\n🎨 Generando 15 gráficos profesionales...")
        self.grafico_asignaciones_invalidas()
        self.grafico_distribucion_salones()
        self.grafico_tipo_salon()
        self.grafico_uso_por_dia()
        self.grafico_salones_invalidos_detalle()
        self.grafico_heatmap_uso()
        self.grafico_uso_planta_baja_vs_alta()
        self.grafico_top_materias()
        self.grafico_distribucion_horas()
        self.grafico_grupos_primer_semestre()
        self.grafico_resumen_metricas()
        self.grafico_comparativa_final()
        self.grafico_movimientos_profesores()
        self.grafico_distribucion_movimientos()
        self.grafico_metricas_optimizacion()
        
        print("\n" + "="*80)
        print("✅ ANÁLISIS EXPANDIDO COMPLETADO")
        print("="*80)
        print(f"\n📁 Ubicación: {self.output_dir}")
        print("\n📊 15 Gráficos profesionales creados (300 DPI)")
        print("📄 Estadísticas comparativas en CSV")
        print("\n🎯 Listo para artículo de investigación\n")

def main():
    """Función principal"""
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    csv_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/02_Horario_Optimizado_Profesor.csv"
    output_dir = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/01_inicial_vs_profesor"
    
    analizador = AnalizadorComparativoExpandido(csv_inicial, csv_optimizado, output_dir)
    analizador.generar_reporte_completo()

if __name__ == "__main__":
    main()
