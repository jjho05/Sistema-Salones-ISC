#!/usr/bin/env python3
"""
Script de Análisis de Datos - Sistema de Optimización de Salones ISC
Analiza los archivos CSV y extrae estadísticas clave
"""

import pandas as pd
import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

class AnalizadorHorarios:
    def __init__(self, archivo_csv: str):
        self.archivo = archivo_csv
        self.df = None
        self.profesores = {}
        self.grupos = []
        self.salones_usados = set()
        self.horarios = set()
        
        # Catálogo de salones
        self.salones_planta_baja = {'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7'}
        self.salones_planta_alta = {'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'}
        self.labs_primer_piso = {'LR', 'LSO', 'LIA', 'LCG1', 'LCG2'}
        self.labs_segundo_piso = {'LBD', 'LCA', 'LBD2', 'LCG3'}
        
        # Salones INVÁLIDOS que deben eliminarse
        self.salones_invalidos = {'AV1', 'AV2', 'AV4', 'AV5', 'E11'}
        
        # Salones válidos totales
        self.salones_validos = (self.salones_planta_baja | self.salones_planta_alta | 
                               self.labs_primer_piso | self.labs_segundo_piso)
        
    def cargar_datos(self):
        """Carga el archivo CSV"""
        self.df = pd.read_csv(self.archivo, encoding='utf-8')
        print(f"✅ Archivo cargado: {self.archivo}")
        print(f"   Total de filas: {len(self.df)}")
        
    def parsear_horario(self, horario_str: str) -> Tuple[str, str]:
        """
        Parsea un string de horario como '0809/FF2'
        Retorna: (hora, salon)
        """
        if pd.isna(horario_str) or horario_str == '':
            return None, None
            
        match = re.match(r'(\d{4})/([A-Z0-9]+)', str(horario_str))
        if match:
            hora = match.group(1)
            salon = match.group(2)
            return hora, salon
        return None, None
    
    def es_primer_semestre(self, codigo_grupo: str) -> bool:
        """Verifica si un grupo es de primer semestre"""
        if pd.isna(codigo_grupo):
            return False
        return str(codigo_grupo).startswith('1')
    
    def extraer_profesores(self):
        """Extrae información de todos los profesores"""
        profesor_actual = None
        
        for idx, row in self.df.iterrows():
            grupo = str(row['Grupo'])
            
            # Detectar línea de profesor
            if 'PROFESOR' in grupo:
                profesor_actual = grupo.strip()
                self.profesores[profesor_actual] = {
                    'materias': [],
                    'horarios': [],
                    'salones_usados': set(),
                    'movimientos_por_dia': {'Lunes': 0, 'Martes': 0, 'Miercoles': 0, 'Jueves': 0, 'Viernes': 0}
                }
            elif profesor_actual and grupo and 'PROFESOR' not in grupo:
                # Es una materia del profesor actual
                materia_col = 'Materia.' if 'Materia.' in self.df.columns else 'Materia'
                materia_info = {
                    'grupo': grupo,
                    'materia': row[materia_col],
                    'horas_semana': row['Class']
                }
                self.profesores[profesor_actual]['materias'].append(materia_info)
                
                # Analizar horarios por día
                for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
                    hora, salon = self.parsear_horario(row[dia])
                    if salon:
                        self.profesores[profesor_actual]['salones_usados'].add(salon)
                        self.salones_usados.add(salon)
                        
    def calcular_movimientos_profesor(self, profesor: str) -> Dict:
        """Calcula los movimientos de un profesor entre salones"""
        if profesor not in self.profesores:
            return {}
            
        movimientos = {
            'total_cambios': 0,
            'cambios_por_dia': {},
            'cambios_piso': 0,
            'salones_diferentes': len(self.profesores[profesor]['salones_usados'])
        }
        
        # Analizar movimientos por día
        for materia in self.profesores[profesor]['materias']:
            # Aquí se necesitaría analizar el horario completo del profesor
            # por ahora solo contamos salones diferentes
            pass
            
        return movimientos
    
    def analizar_grupos_primer_semestre(self):
        """Analiza si los grupos de 1er semestre cumplen la restricción"""
        grupos_1er_sem = []
        materia_col = 'Materia.' if 'Materia.' in self.df.columns else 'Materia'
        
        for idx, row in self.df.iterrows():
            grupo = str(row['Grupo'])
            
            if self.es_primer_semestre(grupo) and 'PROFESOR' not in grupo:
                salones_teoria = set()
                salones_lab = set()
                
                for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
                    hora, salon = self.parsear_horario(row[dia])
                    if salon:
                        if salon.startswith('L'):
                            salones_lab.add(salon)
                        else:
                            salones_teoria.add(salon)
                
                cumple_restriccion = len(salones_teoria) <= 1
                
                grupos_1er_sem.append({
                    'grupo': grupo,
                    'materia': row[materia_col],
                    'salones_teoria': salones_teoria,
                    'salones_lab': salones_lab,
                    'cumple_restriccion': cumple_restriccion
                })
        
        return grupos_1er_sem
    
    def analizar_salones_invalidos(self):
        """Detecta asignaciones a salones inválidos (AV y E11)"""
        asignaciones_invalidas = []
        
        for idx, row in self.df.iterrows():
            grupo = str(row['Grupo'])
            
            if 'PROFESOR' not in grupo and grupo and grupo != 'nan':
                for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
                    hora, salon = self.parsear_horario(row[dia])
                    if salon and salon in self.salones_invalidos:
                        asignaciones_invalidas.append({
                            'grupo': grupo,
                            'materia': row['Materia.'] if 'Materia.' in row else row.get('Materia', ''),
                            'dia': dia,
                            'hora': hora,
                            'salon_invalido': salon
                        })
        
        return asignaciones_invalidas

    
    def generar_estadisticas(self):
        """Genera estadísticas generales"""
        asignaciones_invalidas = self.analizar_salones_invalidos()
        
        stats = {
            'total_profesores': len(self.profesores),
            'total_salones_usados': len(self.salones_usados),
            'asignaciones_invalidas': len(asignaciones_invalidas),
            'salones_invalidos_unicos': len(set(a['salon_invalido'] for a in asignaciones_invalidas)),
            'salones_por_tipo': {
                'planta_baja': len(self.salones_usados & self.salones_planta_baja),
                'planta_alta': len(self.salones_usados & self.salones_planta_alta),
                'labs_piso_1': len(self.salones_usados & self.labs_primer_piso),
                'labs_piso_2': len(self.salones_usados & self.labs_segundo_piso),
                'invalidos': len(self.salones_usados & self.salones_invalidos)
            }
        }
        
        return stats
    
    def imprimir_reporte(self):
        """Imprime un reporte completo del análisis"""
        print("\n" + "="*80)
        print("📊 REPORTE DE ANÁLISIS DE HORARIOS")
        print("="*80)
        
        # Estadísticas generales
        stats = self.generar_estadisticas()
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   Total de profesores: {stats['total_profesores']}")
        print(f"   Total de salones usados: {stats['total_salones_usados']}")
        print(f"\n🏢 DISTRIBUCIÓN DE SALONES:")
        print(f"   Planta Baja (FF1-FF7): {stats['salones_por_tipo']['planta_baja']}")
        print(f"   Planta Alta (FF8-FFD): {stats['salones_por_tipo']['planta_alta']}")
        print(f"   Labs Piso 1: {stats['salones_por_tipo']['labs_piso_1']}")
        print(f"   Labs Piso 2: {stats['salones_por_tipo']['labs_piso_2']}")
        print(f"   ⚠️  INVÁLIDOS (AV/E11): {stats['salones_por_tipo']['invalidos']}")
        
        # Análisis de salones inválidos
        asignaciones_inv = self.analizar_salones_invalidos()
        print(f"\n🚨 ASIGNACIONES A SALONES INVÁLIDOS:")
        print(f"   Total de asignaciones inválidas: {stats['asignaciones_invalidas']}")
        print(f"   Salones inválidos usados: {stats['salones_invalidos_unicos']}")
        
        if asignaciones_inv:
            print(f"\n   ⚠️  Detalle de asignaciones inválidas:")
            # Agrupar por salón inválido
            por_salon = {}
            for asig in asignaciones_inv:
                salon = asig['salon_invalido']
                if salon not in por_salon:
                    por_salon[salon] = []
                por_salon[salon].append(asig)
            
            for salon, asigs in sorted(por_salon.items()):
                print(f"\n      Salón {salon}: {len(asigs)} asignaciones")
                for asig in asigs[:5]:  # Mostrar solo las primeras 5
                    print(f"         - {asig['grupo']} ({asig['dia']} {asig['hora']})")
                if len(asigs) > 5:
                    print(f"         ... y {len(asigs) - 5} más")
        else:
            print(f"   ✅ No hay asignaciones inválidas")
        
        # Análisis de grupos de 1er semestre
        print(f"\n📚 GRUPOS DE PRIMER SEMESTRE:")
        grupos_1er = self.analizar_grupos_primer_semestre()
        total_1er = len(grupos_1er)
        cumplen = sum(1 for g in grupos_1er if g['cumple_restriccion'])
        no_cumplen = total_1er - cumplen
        
        print(f"   Total de grupos: {total_1er}")
        print(f"   ✅ Cumplen restricción (1 salón teoría): {cumplen}")
        print(f"   ❌ NO cumplen restricción: {no_cumplen}")
        
        if no_cumplen > 0:
            print(f"\n   ⚠️  Grupos que NO cumplen:")
            for g in grupos_1er:
                if not g['cumple_restriccion']:
                    print(f"      - {g['grupo']}: {g['salones_teoria']}")
        
        # Top profesores con más materias
        print(f"\n👨‍🏫 TOP 5 PROFESORES CON MÁS MATERIAS:")
        prof_materias = [(p, len(info['materias'])) for p, info in self.profesores.items()]
        prof_materias.sort(key=lambda x: x[1], reverse=True)
        for i, (prof, num_mat) in enumerate(prof_materias[:5], 1):
            salones = len(self.profesores[prof]['salones_usados'])
            print(f"   {i}. {prof}: {num_mat} materias, {salones} salones diferentes")
        
        # Salones más usados
        print(f"\n🏫 SALONES MÁS UTILIZADOS:")
        contador_salones = Counter()
        for prof_info in self.profesores.values():
            for salon in prof_info['salones_usados']:
                contador_salones[salon] += 1
        
        for i, (salon, count) in enumerate(contador_salones.most_common(10), 1):
            tipo = self._tipo_salon(salon)
            print(f"   {i}. {salon} ({tipo}): usado por {count} profesores")
        
        print("\n" + "="*80)
    
    def _tipo_salon(self, salon: str) -> str:
        """Retorna el tipo de salón"""
        if salon in self.salones_planta_baja:
            return "Planta Baja"
        elif salon in self.salones_planta_alta:
            return "Planta Alta"
        elif salon in self.labs_primer_piso:
            return "Lab Piso 1"
        elif salon in self.labs_segundo_piso:
            return "Lab Piso 2"
        elif salon in self.salones_especiales:
            return "Especial"
        else:
            return "Desconocido"
    
    def comparar_con_optimizado(self, archivo_optimizado: str):
        """Compara con el archivo optimizado del profesor"""
        print(f"\n🔄 COMPARANDO CON OPTIMIZACIÓN DEL PROFESOR...")
        
        analizador_opt = AnalizadorHorarios(archivo_optimizado)
        analizador_opt.cargar_datos()
        analizador_opt.extraer_profesores()
        
        print(f"\n📊 COMPARATIVA:")
        print(f"   Archivo Original: {self.archivo}")
        print(f"   Archivo Optimizado: {archivo_optimizado}")
        
        # Comparar grupos de 1er semestre
        grupos_orig = self.analizar_grupos_primer_semestre()
        grupos_opt = analizador_opt.analizar_grupos_primer_semestre()
        
        cumplen_orig = sum(1 for g in grupos_orig if g['cumple_restriccion'])
        cumplen_opt = sum(1 for g in grupos_opt if g['cumple_restriccion'])
        
        print(f"\n   Grupos 1er sem. que cumplen restricción:")
        print(f"   Original: {cumplen_orig}/{len(grupos_orig)}")
        print(f"   Optimizado: {cumplen_opt}/{len(grupos_opt)}")
        
        if cumplen_opt > cumplen_orig:
            print(f"   ✅ Mejora: +{cumplen_opt - cumplen_orig} grupos")
        elif cumplen_opt < cumplen_orig:
            print(f"   ❌ Empeora: {cumplen_orig - cumplen_opt} grupos")
        else:
            print(f"   ➡️  Sin cambios")


def main():
    """Función principal"""
    print("🚀 Iniciando análisis de horarios...")
    
    # Rutas de archivos
    archivo_original = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/PROBLEMA SALONES ISC TEC/HorariosAgoDic2025.csv"
    archivo_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/PROBLEMA SALONES ISC TEC/grouped_optimized_schedule.csv"
    
    # Analizar archivo original
    analizador = AnalizadorHorarios(archivo_original)
    analizador.cargar_datos()
    analizador.extraer_profesores()
    analizador.imprimir_reporte()
    
    # Comparar con optimizado
    analizador.comparar_con_optimizado(archivo_optimizado)
    
    print("\n✅ Análisis completado!")


if __name__ == "__main__":
    main()
