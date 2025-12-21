#!/usr/bin/env python3
"""
Script maestro para ejecutar todos los optimizadores con el nuevo sistema de prioridades
"""

import subprocess
import time
import pandas as pd

print("="*80)
print("🚀 EJECUCIÓN COMPLETA - TODOS LOS OPTIMIZADORES")
print("="*80)
print("\nSistema de Prioridades:")
print("  ✅ PRIORIDAD 1: 100% (pre-asignado)")
print("  📊 PRIORIDAD 2 y 3: Optimización")
print("="*80)

# 1. Pre-asignación (ya está hecha, pero la ejecutamos por si acaso)
print("\n\n📍 PASO 1: Pre-asignación PRIORIDAD 1")
print("-"*80)
subprocess.run(["python3", "pre_asignar_p1.py"])

# 2. Greedy
print("\n\n📍 PASO 2: Optimizador Greedy + Hill Climbing")
print("-"*80)
start = time.time()
subprocess.run(["python3", "optimizador_greedy.py"])
tiempo_greedy = time.time() - start

# 3. Corrección Greedy
print("\n\n📍 PASO 3: Corrección Post-Optimización (Greedy)")
print("-"*80)
subprocess.run(["python3", "corregir_prioridades.py", "datos_estructurados/04_Horario_Optimizado_Greedy.csv"])

# 4. ML
print("\n\n📍 PASO 4: Optimizador ML")
print("-"*80)
start = time.time()
subprocess.run(["python3", "optimizador_ml.py"])
tiempo_ml = time.time() - start

# 5. Corrección ML
print("\n\n📍 PASO 5: Corrección Post-Optimización (ML)")
print("-"*80)
subprocess.run(["python3", "corregir_prioridades.py", "datos_estructurados/05_Horario_Optimizado_ML.csv"])

# 6. Genético
print("\n\n📍 PASO 6: Optimizador Genético")
print("-"*80)
start = time.time()
subprocess.run(["python3", "optimizador_genetico.py"])
tiempo_genetico = time.time() - start

# 7. Corrección Genético
print("\n\n📍 PASO 7: Corrección Post-Optimización (Genético)")
print("-"*80)
subprocess.run(["python3", "corregir_prioridades.py", "datos_estructurados/06_Horario_Optimizado_Genetico.csv"])

# 8. Generar comparativas y gráficos
print("\n\n📍 PASO 8: Generar Comparativas y Gráficos")
print("-"*80)
subprocess.run(["python3", "generar_comparativa_completa.py"])

# Resumen final
print("\n\n" + "="*80)
print("✅ EJECUCIÓN COMPLETADA")
print("="*80)
print(f"\n⏱️  Tiempos de ejecución:")
print(f"   Greedy:    {tiempo_greedy:.1f}s")
print(f"   ML:        {tiempo_ml:.1f}s")
print(f"   Genético:  {tiempo_genetico:.1f}s")
print(f"   TOTAL:     {tiempo_greedy + tiempo_ml + tiempo_genetico:.1f}s")

print(f"\n📁 Archivos generados:")
print(f"   - datos_estructurados/04_Horario_Optimizado_Greedy.csv")
print(f"   - datos_estructurados/05_Horario_Optimizado_ML.csv")
print(f"   - datos_estructurados/06_Horario_Optimizado_Genetico.csv")

print("\n🎯 Todos los optimizadores garantizan 100% en PRIORIDAD 1")
print("="*80)
