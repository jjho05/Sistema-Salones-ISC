#!/usr/bin/env python3
"""
Pre-asignación FORZADA de PRIORIDAD 1
Garantiza 100% de cumplimiento ANTES de optimización
"""

import pandas as pd
import json

def pre_asignar_prioridad_1(df):
    """
    Pre-asigna TODAS las clases de PRIORIDAD 1 al 100%
    Retorna: (df_modificado, indices_inmutables)
    """
    print("="*80)
    print("🎯 PRE-ASIGNACIÓN FORZADA - PRIORIDAD 1")
    print("="*80)
    
    with open('preferencias_profesores.json') as f:
        prefs = json.load(f)
    
    indices_inmutables = set()
    asignaciones = 0
    
    for profesor, datos in prefs.items():
        if 'materias' not in datos:
            continue
            
        for materia, pref in datos['materias'].items():
            # TEORÍA
            if pref.get('prioridad_teoria') == 'Prioritario' and pref.get('salon_teoria') != 'Sin preferencia':
                salon_esperado = pref['salon_teoria']
                mask = (df['Profesor'] == profesor) & (df['Materia'] == materia) & (df['Tipo_Salon'] == 'Teoría')
                indices = df[mask].index.tolist()
                
                if len(indices) > 0:
                    df.loc[mask, 'Salon'] = salon_esperado
                    indices_inmutables.update(indices)
                    asignaciones += len(indices)
                    print(f"   ✅ {profesor} - {materia} (T): {len(indices)} clases → {salon_esperado}")
            
            # LABORATORIO
            if pref.get('prioridad_lab') == 'Prioritario' and pref.get('salon_lab') != 'Sin preferencia':
                salon_esperado = pref['salon_lab']
                mask = (df['Profesor'] == profesor) & (df['Materia'] == materia) & (df['Tipo_Salon'] == 'Laboratorio')
                indices = df[mask].index.tolist()
                
                if len(indices) > 0:
                    df.loc[mask, 'Salon'] = salon_esperado
                    indices_inmutables.update(indices)
                    asignaciones += len(indices)
                    print(f"   ✅ {profesor} - {materia} (L): {len(indices)} clases → {salon_esperado}")
    
    print("\n" + "="*80)
    print(f"✅ PRE-ASIGNACIÓN COMPLETADA")
    print("="*80)
    print(f"Total clases prioritarias: {asignaciones}")
    print(f"Clases inmutables: {len(indices_inmutables)}")
    print(f"Cumplimiento: 100%")
    print("="*80)
    
    return df, indices_inmutables

if __name__ == "__main__":
    # Cargar horario inicial (ya procesado)
    df = pd.read_csv('datos_estructurados/01_Horario_Inicial.csv')
    
    # Pre-asignar
    df_pre, inmutables = pre_asignar_prioridad_1(df)
    
    # Guardar
    df_pre.to_csv('datos_estructurados/00_Horario_PreAsignado_P1.csv', index=False)
    
    # Guardar índices inmutables
    with open('datos_estructurados/indices_inmutables_p1.json', 'w') as f:
        json.dump(list(inmutables), f)
    
    print(f"\n💾 Guardado:")
    print(f"   - datos_estructurados/00_Horario_PreAsignado_P1.csv")
    print(f"   - datos_estructurados/indices_inmutables_p1.json")
    print(f"\n🎯 Ahora los optimizadores deben usar este archivo y respetar los índices inmutables")
