#!/usr/bin/env python3
"""
Análisis Detallado de Materias en Sistemas
Extrae SOLO las materias que aparecen en los CSV (que se toman en edificio de Sistemas)
"""

import pandas as pd
import re
from collections import Counter, defaultdict

def parsear_horario(horario_str):
    """Parsea '0809/FF2' -> ('0809', 'FF2')"""
    if pd.isna(horario_str) or horario_str == '':
        return None, None
    match = re.match(r'(\d{4})/([A-Z0-9]+)', str(horario_str))
    if match:
        return match.group(1), match.group(2)
    return None, None

def analizar_materias_csv(archivo_csv):
    """Analiza las materias que aparecen en el CSV"""
    df = pd.read_csv(archivo_csv, encoding='utf-8')
    
    # Detectar nombre de columna de materia
    materia_col = 'Materia.' if 'Materia.' in df.columns else 'Materia'
    
    materias_info = {}
    
    for idx, row in df.iterrows():
        grupo = str(row['Grupo'])
        
        # Saltar líneas de profesor o vacías
        if 'PROFESOR' in grupo or pd.isna(row[materia_col]) or grupo == 'nan':
            continue
        
        materia = str(row[materia_col]).strip()
        
        if materia not in materias_info:
            materias_info[materia] = {
                'grupos': [],
                'salones_ff_usados': set(),
                'salones_lab_usados': set(),
                'salones_invalidos': set(),
                'horas_totales': [],
                'horarios': []
            }
        
        # Analizar salones usados
        salones_ff = set()
        salones_lab = set()
        salones_inv = set()
        
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            hora, salon = parsear_horario(row[dia])
            if salon:
                if salon.startswith('L'):
                    salones_lab.add(salon)
                elif salon in {'AV1', 'AV2', 'AV4', 'AV5', 'E11'}:
                    salones_inv.add(salon)
                else:
                    salones_ff.add(salon)
        
        materias_info[materia]['grupos'].append(grupo)
        materias_info[materia]['salones_ff_usados'].update(salones_ff)
        materias_info[materia]['salones_lab_usados'].update(salones_lab)
        materias_info[materia]['salones_invalidos'].update(salones_inv)
        
        if 'Class' in row and not pd.isna(row['Class']):
            materias_info[materia]['horas_totales'].append(int(row['Class']))
    
    return materias_info

def imprimir_analisis(materias_info, titulo):
    """Imprime análisis detallado de materias"""
    print(f"\n{'='*100}")
    print(f"📚 {titulo}")
    print(f"{'='*100}")
    
    print(f"\n📊 Total de materias únicas: {len(materias_info)}")
    
    # Clasificar materias por tipo de salón
    solo_teoria = []
    solo_lab = []
    mixtas = []
    con_invalidos = []
    
    for materia, info in materias_info.items():
        tiene_ff = len(info['salones_ff_usados']) > 0
        tiene_lab = len(info['salones_lab_usados']) > 0
        tiene_inv = len(info['salones_invalidos']) > 0
        
        if tiene_inv:
            con_invalidos.append(materia)
        
        if tiene_ff and not tiene_lab:
            solo_teoria.append(materia)
        elif tiene_lab and not tiene_ff:
            solo_lab.append(materia)
        elif tiene_ff and tiene_lab:
            mixtas.append(materia)
    
    print(f"\n🏢 CLASIFICACIÓN POR TIPO DE SALÓN:")
    print(f"   Solo Teoría (FF): {len(solo_teoria)} materias")
    print(f"   Solo Laboratorio (L): {len(solo_lab)} materias")
    print(f"   Mixtas (FF + L): {len(mixtas)} materias")
    print(f"   ⚠️  Con salones inválidos: {len(con_invalidos)} materias")
    
    # Mostrar materias solo teoría
    if solo_teoria:
        print(f"\n📖 MATERIAS SOLO TEORÍA ({len(solo_teoria)}):")
        for mat in sorted(solo_teoria):
            grupos = len(materias_info[mat]['grupos'])
            salones = ', '.join(sorted(materias_info[mat]['salones_ff_usados']))
            print(f"   • {mat}")
            print(f"     Grupos: {grupos} | Salones: {salones}")
    
    # Mostrar materias solo lab
    if solo_lab:
        print(f"\n🔬 MATERIAS SOLO LABORATORIO ({len(solo_lab)}):")
        for mat in sorted(solo_lab):
            grupos = len(materias_info[mat]['grupos'])
            salones = ', '.join(sorted(materias_info[mat]['salones_lab_usados']))
            print(f"   • {mat}")
            print(f"     Grupos: {grupos} | Salones: {salones}")
    
    # Mostrar materias mixtas (las más comunes)
    if mixtas:
        print(f"\n🔀 MATERIAS MIXTAS (Teoría + Laboratorio) ({len(mixtas)}):")
        for mat in sorted(mixtas)[:15]:  # Mostrar solo las primeras 15
            grupos = len(materias_info[mat]['grupos'])
            ff = ', '.join(sorted(materias_info[mat]['salones_ff_usados']))
            labs = ', '.join(sorted(materias_info[mat]['salones_lab_usados']))
            print(f"   • {mat}")
            print(f"     Grupos: {grupos} | FF: {ff} | Labs: {labs}")
        if len(mixtas) > 15:
            print(f"   ... y {len(mixtas) - 15} más")
    
    # Mostrar materias con salones inválidos
    if con_invalidos:
        print(f"\n⚠️  MATERIAS CON SALONES INVÁLIDOS ({len(con_invalidos)}):")
        for mat in sorted(con_invalidos):
            grupos = len(materias_info[mat]['grupos'])
            inv = ', '.join(sorted(materias_info[mat]['salones_invalidos']))
            print(f"   • {mat}")
            print(f"     Grupos: {grupos} | Salones inválidos: {inv}")
    
    # Análisis de horas
    print(f"\n⏰ DISTRIBUCIÓN DE HORAS SEMANALES:")
    todas_horas = []
    for info in materias_info.values():
        todas_horas.extend(info['horas_totales'])
    
    if todas_horas:
        contador_horas = Counter(todas_horas)
        for horas in sorted(contador_horas.keys()):
            count = contador_horas[horas]
            print(f"   {horas} horas/semana: {count} grupos")
    
    # Top materias con más grupos
    print(f"\n👥 TOP 10 MATERIAS CON MÁS GRUPOS:")
    materias_por_grupos = [(mat, len(info['grupos'])) for mat, info in materias_info.items()]
    materias_por_grupos.sort(key=lambda x: x[1], reverse=True)
    
    for i, (mat, num_grupos) in enumerate(materias_por_grupos[:10], 1):
        print(f"   {i}. {mat}: {num_grupos} grupos")

def comparar_archivos(archivo1, archivo2):
    """Compara dos archivos CSV"""
    print(f"\n{'='*100}")
    print(f"🔄 COMPARACIÓN ENTRE ARCHIVOS")
    print(f"{'='*100}")
    
    materias1 = analizar_materias_csv(archivo1)
    materias2 = analizar_materias_csv(archivo2)
    
    # Contar salones inválidos
    inv1 = sum(1 for info in materias1.values() if len(info['salones_invalidos']) > 0)
    inv2 = sum(1 for info in materias2.values() if len(info['salones_invalidos']) > 0)
    
    print(f"\n📊 RESUMEN COMPARATIVO:")
    print(f"   Archivo Original: {archivo1.split('/')[-1]}")
    print(f"   Archivo Optimizado: {archivo2.split('/')[-1]}")
    print(f"\n   Materias con salones inválidos:")
    print(f"   Original: {inv1} materias")
    print(f"   Optimizado: {inv2} materias")
    
    if inv2 < inv1:
        print(f"   ✅ Mejora: -{inv1 - inv2} materias")
    elif inv2 > inv1:
        print(f"   ❌ Empeora: +{inv2 - inv1} materias")
    else:
        print(f"   ➡️  Sin cambios")

def main():
    """Función principal"""
    archivo_original = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/PROBLEMA SALONES ISC TEC/HorariosAgoDic2025.csv"
    archivo_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/PROBLEMA SALONES ISC TEC/grouped_optimized_schedule.csv"
    
    print("🚀 ANÁLISIS DETALLADO DE MATERIAS EN SISTEMAS")
    
    # Analizar archivo original
    materias_orig = analizar_materias_csv(archivo_original)
    imprimir_analisis(materias_orig, "ARCHIVO ORIGINAL (HorariosAgoDic2025.csv)")
    
    # Analizar archivo optimizado
    materias_opt = analizar_materias_csv(archivo_optimizado)
    imprimir_analisis(materias_opt, "ARCHIVO OPTIMIZADO (grouped_optimized_schedule.csv)")
    
    # Comparar
    comparar_archivos(archivo_original, archivo_optimizado)
    
    print(f"\n{'='*100}")
    print("✅ Análisis completado")
    print(f"{'='*100}\n")

if __name__ == "__main__":
    main()
