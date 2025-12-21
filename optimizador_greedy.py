#!/usr/bin/env python3
"""
Optimizador Greedy + Hill Climbing - Sistema de Salones ISC
Rápido y efectivo: construcción voraz + búsqueda local
ACTUALIZADO: Integra restricciones de teoría/lab y preferencias de profesores
"""

import pandas as pd
import numpy as np
import random
from typing import Dict, List, Tuple
import sys
import os

# Importar analizador de movimientos y utilidades
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analizar_movimientos import AnalizadorMovimientos
from utils_restricciones import (
    cargar_configuraciones,
    determinar_tipo_hora,
    obtener_preferencia_profesor,
    es_preferencia_prioritaria,
    filtrar_salones_por_tipo
)

class OptimizadorGreedyHC:
    def __init__(self, max_iter_hc=100, verbose=True):
        """
        Optimizador Greedy + Hill Climbing
        
        Args:
            max_iter_hc: Iteraciones de hill climbing
            verbose: Mostrar progreso
        """
        self.max_iter_hc = max_iter_hc
        self.verbose = verbose
        
        # Cargar configuraciones de restricciones
        self._log("📂 Cargando configuraciones de restricciones...")
        self.config_materias, self.preferencias_profesores = cargar_configuraciones()
        
        # Catálogos (CORREGIDOS - basados en datos reales)
        self.salones_invalidos = {'AV1', 'AV2', 'AV4', 'AV5', 'E11'}
        self.laboratorios = {'LBD', 'LBD2', 'LCA', 'LCG1', 'LCG2', 'LIA', 'LR', 'LSO'}
        self.salones_teoria = {'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'}
        self.todos_salones = self.salones_teoria | self.laboratorios
        
        # Matriz de distancias
        self.matriz_distancias = self._crear_matriz_distancias()
        
    def _crear_matriz_distancias(self) -> Dict:
        """Crea matriz de distancias entre salones"""
        distancias = {}
        
        # FF entre sí
        salones_ff = ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD']
        for i, s1 in enumerate(salones_ff):
            for j, s2 in enumerate(salones_ff):
                distancias[(s1, s2)] = abs(i - j) * 5
        
        # FF a Labs
        labs = list(self.laboratorios)
        for s1 in salones_ff:
            for s2 in labs:
                distancias[(s1, s2)] = 50
                distancias[(s2, s1)] = 50
        
        # Labs entre sí
        for i, s1 in enumerate(labs):
            for j, s2 in enumerate(labs):
                distancias[(s1, s2)] = abs(i - j) * 8
        
        return distancias
    
    def _log(self, mensaje: str):
        if self.verbose:
            print(mensaje)
    
    def calcular_energia(self, solucion: Dict, df: pd.DataFrame) -> float:
        """Calcula energía de la solución (menor es mejor)"""
        energia = 0
        
        # Rastrear horas asignadas por materia
        horas_asignadas = {}
        
        for idx, salon in solucion.items():
            row = df.loc[idx]
            profesor = row['Profesor']
            grupo = row['Grupo']
            materia = row['Materia']
            
            # Determinar tipo de hora
            key = (grupo, materia)
            indice_hora = horas_asignadas.get(key, 0)
            tipo_requerido = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas[key] = indice_hora + 1
            
            # Penalización por asignación inválida (salón no válido)
            if salon in self.salones_invalidos:
                energia += 1000
            
            # Penalización por tipo incorrecto (teoría en lab o viceversa)
            es_lab = salon in self.laboratorios
            requiere_lab = tipo_requerido == 'Laboratorio'
            if es_lab != requiere_lab:
                energia += 500  # Penalización fuerte por tipo incorrecto
            
            # Penalización por violar preferencias prioritarias
            pref_salon = obtener_preferencia_profesor(profesor, tipo_requerido, self.preferencias_profesores)
            es_prioritaria = es_preferencia_prioritaria(profesor, tipo_requerido, self.preferencias_profesores)
            
            if es_prioritaria and pref_salon and pref_salon != salon:
                energia += 300  # Penalización muy fuerte por violar preferencia prioritaria
            elif pref_salon and pref_salon != salon:
                energia += 20  # Penalización leve por no respetar preferencia opcional
        
        # Calcular movimientos de profesores
        for profesor in df['Profesor'].unique():
            clases_profesor = df[df['Profesor'] == profesor].index
            salones_profesor = [solucion[i] for i in clases_profesor if i in solucion]
            
            # Contar cambios de salón
            for i in range(len(salones_profesor) - 1):
                if salones_profesor[i] != salones_profesor[i+1]:
                    dist = self.matriz_distancias.get((salones_profesor[i], salones_profesor[i+1]), 50)
                    energia += dist * 0.5
        
        # Conflictos de ocupación (dos clases en el mismo lugar a la misma hora)
        ocupacion = {}
        for idx, salon in solucion.items():
            key = (df.loc[idx]['Dia'], df.loc[idx]['Bloque_Horario'], salon)
            if key in ocupacion:
                energia += 5000  # Penalización muy alta por conflicto
            ocupacion[key] = idx
        
        return energia
    
    def construccion_greedy(self, df: pd.DataFrame) -> Dict:
        """Fase 1: Construcción voraz con restricciones"""
        self._log("\n📊 Fase 1: Construcción Greedy (con restricciones)...")
        solucion = {}
        ocupacion = {}  # (dia, bloque, salon) -> idx
        
        # Rastrear horas asignadas por materia para determinar tipo
        horas_asignadas = {}  # (grupo, materia) -> contador
        
        # Ordenar asignaciones por prioridad
        df_sorted = df.copy()
        df_sorted['prioridad'] = 0
        
        # Prioridad 1: Primer semestre
        df_sorted.loc[df_sorted['Grupo'].str[0] == '1', 'prioridad'] = 3
        
        # Prioridad 2: Labs (basado en Tipo_Salon original)
        df_sorted.loc[df_sorted['Tipo_Salon'] == 'Laboratorio', 'prioridad'] += 2
        
        df_sorted = df_sorted.sort_values('prioridad', ascending=False)
        
        # Asignar vorazmente
        for idx, row in df_sorted.iterrows():
            materia = row['Materia']
            grupo = row['Grupo']
            dia = row['Dia']
            bloque = row['Bloque_Horario']
            profesor = row['Profesor']
            
            # Determinar tipo de hora requerido
            key = (grupo, materia)
            indice_hora = horas_asignadas.get(key, 0)
            tipo_requerido = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas[key] = indice_hora + 1
            
            # Filtrar candidatos por tipo
            if tipo_requerido == 'Laboratorio':
                candidatos = list(self.laboratorios)
            else:
                candidatos = list(self.salones_teoria)
            
            # Verificar preferencia del profesor
            pref_salon = obtener_preferencia_profesor(profesor, tipo_requerido, self.preferencias_profesores)
            es_prioritaria = es_preferencia_prioritaria(profesor, tipo_requerido, self.preferencias_profesores)
            
            # Si hay preferencia prioritaria, intentar usarla
            if es_prioritaria and pref_salon and pref_salon in candidatos:
                if (dia, bloque, pref_salon) not in ocupacion:
                    # Usar salón prioritario
                    solucion[idx] = pref_salon
                    ocupacion[(dia, bloque, pref_salon)] = idx
                    continue
            
            # Evaluar candidatos
            mejor_salon = None
            mejor_score = float('-inf')
            
            for salon in candidatos:
                # Verificar disponibilidad
                if (dia, bloque, salon) in ocupacion:
                    continue
                
                # Calcular score
                score = 0
                
                # Bonificación por preferencia del profesor
                if pref_salon == salon:
                    score += 50  # Bonificación fuerte por preferencia
                
                # Preferir salones cercanos a clases anteriores del profesor
                clases_anteriores = [solucion[i] for i in solucion if df.loc[i]['Profesor'] == profesor]
                if clases_anteriores:
                    dist_promedio = np.mean([self.matriz_distancias.get((salon, s), 50) for s in clases_anteriores])
                    score -= dist_promedio
                
                # Preferir salones menos usados (balancear)
                uso = sum(1 for s in solucion.values() if s == salon)
                score -= uso * 2
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_salon = salon
            
            # Si no hay salón disponible, usar cualquiera del tipo correcto
            if mejor_salon is None:
                disponibles = [s for s in candidatos if (dia, bloque, s) not in ocupacion]
                if disponibles:
                    mejor_salon = random.choice(disponibles)
                else:
                    # Último recurso: usar cualquier salón del tipo
                    mejor_salon = random.choice(candidatos)
            
            solucion[idx] = mejor_salon
            ocupacion[(dia, bloque, mejor_salon)] = idx
        
        energia_inicial = self.calcular_energia(solucion, df)
        self._log(f"   Energía inicial: {energia_inicial:.0f}")
        
        return solucion
    
    def hill_climbing(self, solucion: Dict, df: pd.DataFrame) -> Dict:
        """Fase 2: Mejora por Hill Climbing (respetando restricciones)"""
        self._log("\n🔺 Fase 2: Hill Climbing...")
        
        mejor_solucion = solucion.copy()
        mejor_energia = self.calcular_energia(mejor_solucion, df)
        
        # Rastrear horas asignadas para determinar tipos
        horas_asignadas = {}
        tipos_por_idx = {}
        
        for idx in solucion.keys():
            row = df.loc[idx]
            grupo = row['Grupo']
            materia = row['Materia']
            key = (grupo, materia)
            indice_hora = horas_asignadas.get(key, 0)
            tipo = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas[key] = indice_hora + 1
            tipos_por_idx[idx] = tipo
        
        sin_mejora = 0
        
        for iteracion in range(self.max_iter_hc):
            mejoro = False
            
            # Probar swaps aleatorios (solo del mismo tipo)
            indices = list(solucion.keys())
            for _ in range(50):  # 50 intentos por iteración
                idx1, idx2 = random.sample(indices, 2)
                
                # Solo intercambiar si son del mismo tipo
                if tipos_por_idx[idx1] != tipos_por_idx[idx2]:
                    continue
                
                # Crear vecino
                vecino = mejor_solucion.copy()
                vecino[idx1], vecino[idx2] = vecino[idx2], vecino[idx1]
                
                # Evaluar
                energia = self.calcular_energia(vecino, df)
                
                if energia < mejor_energia:
                    mejor_solucion = vecino
                    mejor_energia = energia
                    mejoro = True
                    sin_mejora = 0
                    break
            
            if not mejoro:
                sin_mejora += 1
                if sin_mejora >= 10:  # Early stopping
                    self._log(f"   Convergió en iteración {iteracion}")
                    break
            
            if (iteracion + 1) % 20 == 0:
                self._log(f"   Iter {iteracion+1}: Energía = {mejor_energia:.0f}")
        
        self._log(f"   Energía final: {mejor_energia:.0f}")
        return mejor_solucion
    
    def optimizar(self, df: pd.DataFrame) -> Tuple[Dict, float]:
        """Ejecuta optimización completa"""
        self._log("\n" + "="*80)
        self._log("⚡ GREEDY + HILL CLIMBING - OPTIMIZACIÓN RÁPIDA")
        self._log("="*80)
        
        # Fase 1: Greedy
        solucion = self.construccion_greedy(df)
        
        # Fase 2: Hill Climbing
        solucion = self.hill_climbing(solucion, df)
        
        energia_final = self.calcular_energia(solucion, df)
        
        self._log("\n" + "="*80)
        self._log("✅ OPTIMIZACIÓN COMPLETADA")
        self._log("="*80)
        
        return solucion, energia_final

def main():
    """Función principal"""
    print("\n⚡ Optimizador Greedy + Hill Climbing - Sistema de Salones ISC")
    print("="*80)
    print("Método: Construcción Voraz + Búsqueda Local (Rápido)")
    print("="*80)
    
    # Cargar datos
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    df_inicial = pd.read_csv(csv_inicial)
    
    # Crear optimizador
    optimizador = OptimizadorGreedyHC(max_iter_hc=100, verbose=True)
    
    # Optimizar
    mejor_solucion, mejor_energia = optimizador.optimizar(df_inicial)
    
    # Aplicar solución
    df_resultado = df_inicial.copy()
    df_resultado['Salon'] = df_resultado.index.map(mejor_solucion)
    
    # Actualizar Es_Invalido, Tipo_Salon y Piso
    for idx in df_resultado.index:
        salon = df_resultado.loc[idx, 'Salon']
        
        # Actualizar Es_Invalido
        df_resultado.loc[idx, 'Es_Invalido'] = 1 if salon in optimizador.salones_invalidos else 0
        
        # Actualizar Tipo_Salon y Piso
        if salon in optimizador.laboratorios:
            df_resultado.loc[idx, 'Tipo_Salon'] = 'Laboratorio'
            # Determinar piso del lab
            if salon in ['LR', 'LSO', 'LIA', 'LCG1', 'LCG2']:
                df_resultado.loc[idx, 'Piso'] = 'Primer Piso'
            else:
                df_resultado.loc[idx, 'Piso'] = 'Segundo Piso'
        elif salon in optimizador.salones_teoria:
            df_resultado.loc[idx, 'Tipo_Salon'] = 'Teoría'
            # Determinar piso FF
            if salon in ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7']:
                df_resultado.loc[idx, 'Piso'] = 'Planta Baja'
            else:
                df_resultado.loc[idx, 'Piso'] = 'Planta Alta'
        else:
            # Salón inválido
            df_resultado.loc[idx, 'Tipo_Salon'] = 'INVÁLIDO'
    
    # Analizar movimientos
    print("\n📊 Analizando movimientos de profesores...")
    analizador = AnalizadorMovimientos()
    
    metricas_inicial = analizador.analizar_todos_profesores(df_inicial)
    metricas_optimizado = analizador.analizar_todos_profesores(df_resultado)
    
    # Mostrar resultados
    print("\n" + "="*80)
    print("📈 RESULTADOS FINALES")
    print("="*80)
    
    print("\n🚶 Movimientos de Profesores:")
    print(f"   Inicial:    {metricas_inicial['agregado']['total_movimientos']} movimientos")
    print(f"   Optimizado: {metricas_optimizado['agregado']['total_movimientos']} movimientos")
    mejora_mov = metricas_inicial['agregado']['total_movimientos'] - metricas_optimizado['agregado']['total_movimientos']
    pct_mov = (mejora_mov / metricas_inicial['agregado']['total_movimientos']) * 100 if metricas_inicial['agregado']['total_movimientos'] > 0 else 0
    print(f"   Mejora:     {'+' if mejora_mov > 0 else ''}{mejora_mov} ({'+' if pct_mov > 0 else ''}{pct_mov:.1f}%)")
    
    print("\n🏢 Cambios de Piso:")
    print(f"   Inicial:    {metricas_inicial['agregado']['total_cambios_piso']} cambios")
    print(f"   Optimizado: {metricas_optimizado['agregado']['total_cambios_piso']} cambios")
    mejora_piso = metricas_inicial['agregado']['total_cambios_piso'] - metricas_optimizado['agregado']['total_cambios_piso']
    pct_piso = (mejora_piso / metricas_inicial['agregado']['total_cambios_piso']) * 100 if metricas_inicial['agregado']['total_cambios_piso'] > 0 else 0
    print(f"   Mejora:     {'+' if mejora_piso > 0 else ''}{mejora_piso} ({'+' if pct_piso > 0 else ''}{pct_piso:.1f}%)")
    
    print("\n📏 Distancia Total:")
    print(f"   Inicial:    {metricas_inicial['agregado']['total_distancia']:.0f} unidades")
    print(f"   Optimizado: {metricas_optimizado['agregado']['total_distancia']:.0f} unidades")
    mejora_dist = metricas_inicial['agregado']['total_distancia'] - metricas_optimizado['agregado']['total_distancia']
    pct_dist = (mejora_dist / metricas_inicial['agregado']['total_distancia']) * 100 if metricas_inicial['agregado']['total_distancia'] > 0 else 0
    print(f"   Mejora:     {'+' if mejora_dist > 0 else ''}{mejora_dist:.0f} ({'+' if pct_dist > 0 else ''}{pct_dist:.1f}%)")
    
    # Guardar resultado
    output_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/04_Horario_Optimizado_Greedy.csv"
    df_resultado.to_csv(output_path, index=False)
    print(f"\n💾 Resultado guardado: {output_path}")
    
    # Guardar métricas
    os.makedirs("/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/04_inicial_vs_greedy", exist_ok=True)
    metricas_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/04_inicial_vs_greedy/metricas_movimientos.csv"
    
    metricas_df = pd.DataFrame({
        'Metrica': ['Movimientos Totales', 'Cambios de Piso', 'Distancia Total'],
        'Inicial': [
            metricas_inicial['agregado']['total_movimientos'], 
            metricas_inicial['agregado']['total_cambios_piso'], 
            metricas_inicial['agregado']['total_distancia']
        ],
        'Optimizado': [
            metricas_optimizado['agregado']['total_movimientos'], 
            metricas_optimizado['agregado']['total_cambios_piso'], 
            metricas_optimizado['agregado']['total_distancia']
        ]
    })
    metricas_df.to_csv(metricas_path, index=False)
    print(f"💾 Métricas guardadas: {metricas_path}")
    
    print("\n" + "="*80)
    print("✅ PROCESO COMPLETADO")
    print("="*80)
    print("\n📊 Próximo paso: Generar comparativa completa\n")

if __name__ == "__main__":
    main()
