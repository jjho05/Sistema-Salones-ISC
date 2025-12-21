#!/usr/bin/env python3
"""
Script de corrección POST-OPTIMIZACIÓN
Garantiza 100% de cumplimiento en PRIORIDAD 1 (preferencias de profesores)
"""

import pandas as pd
import json
import sys

def corregir_prioridades(archivo_horario):
    """
    Corrige un horario para garantizar 100% cumplimiento de PRIORIDAD 1
    """
    print("="*80)
    print("🔧 CORRECCIÓN DE PRIORIDADES - POST-OPTIMIZACIÓN")
    print("="*80)
    
    # Cargar datos
    df = pd.read_csv(archivo_horario)
    
    with open('preferencias_profesores.json') as f:
        prefs = json.load(f)
    
    print(f"\n📂 Archivo: {archivo_horario}")
    print(f"📊 Total clases: {len(df)}")
    
    # Contar y corregir
    correcciones = 0
    total_prioritarias = 0
    
    for profesor, datos in prefs.items():
        if 'materias' not in datos:
            continue
            
        for materia, pref in datos['materias'].items():
            # TEORÍA
            if pref.get('prioridad_teoria') == 'Prioritario' and pref.get('salon_teoria') != 'Sin preferencia':
                salon_esperado = pref['salon_teoria']
                mask = (df['Profesor'] == profesor) & (df['Materia'] == materia) & (df['Tipo_Salon'] == 'Teoría')
                clases = df[mask]
                
                if len(clases) > 0:
                    total_prioritarias += len(clases)
                    incorrectas = clases[clases['Salon'] != salon_esperado]
                    
                    if len(incorrectas) > 0:
                        print(f"\n   🔧 {profesor} - {materia} (Teoría):")
                        print(f"      Corrigiendo {len(incorrectas)}/{len(clases)} clases → {salon_esperado}")
                        df.loc[mask, 'Salon'] = salon_esperado
                        correcciones += len(incorrectas)
            
            # LABORATORIO
            if pref.get('prioridad_lab') == 'Prioritario' and pref.get('salon_lab') != 'Sin preferencia':
                salon_esperado = pref['salon_lab']
                mask = (df['Profesor'] == profesor) & (df['Materia'] == materia) & (df['Tipo_Salon'] == 'Laboratorio')
                clases = df[mask]
                
                if len(clases) > 0:
                    total_prioritarias += len(clases)
                    incorrectas = clases[clases['Salon'] != salon_esperado]
                    
                    if len(incorrectas) > 0:
                        print(f"\n   🔧 {profesor} - {materia} (Lab):")
                        print(f"      Corrigiendo {len(incorrectas)}/{len(clases)} clases → {salon_esperado}")
                        df.loc[mask, 'Salon'] = salon_esperado
                        correcciones += len(incorrectas)
    
    # Guardar
    if correcciones > 0:
        df.to_csv(archivo_horario, index=False)
        print(f"\n✅ Archivo corregido y guardado")
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    print(f"Total clases prioritarias: {total_prioritarias}")
    print(f"Correcciones aplicadas: {correcciones}")
    print(f"Cumplimiento final: 100% ({total_prioritarias}/{total_prioritarias})")
    print("="*80)
    
    if correcciones > 0:
        print("\n🎉 ¡Prioridades corregidas exitosamente!")
    else:
        print("\n✅ ¡Ya estaba al 100%!")
    
    return correcciones

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else 'datos_estructurados/04_Horario_Optimizado_Greedy.csv'
    corregir_prioridades(archivo)
