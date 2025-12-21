#!/usr/bin/env python3
"""
Optimizador de Salones - Método Algoritmo Genético
Implementación de algoritmo evolutivo para optimización de asignaciones
Incluye análisis de movimientos de profesores
ACTUALIZADO: Integra restricciones de teoría/lab y preferencias de profesores
"""

import pandas as pd
import numpy as np
import random
import copy
from collections import defaultdict
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analizar_movimientos import AnalizadorMovimientos
from utils_restricciones import (
    cargar_configuraciones,
    determinar_tipo_hora,
    obtener_preferencia_profesor,
    es_preferencia_prioritaria,
    filtrar_salones_por_tipo
)
import warnings
warnings.filterwarnings('ignore')

class Cromosoma:
    """Representa una solución completa (asignación de todos los salones)"""
    
    def __init__(self, genes):
        self.genes = genes  # Lista de asignaciones
        self.fitness = None
        self.penalizaciones = {}
        self.costos = {}
    
    def __len__(self):
        return len(self.genes)
    
    def copy(self):
        """Crea una copia profunda del cromosoma"""
        nuevo = Cromosoma(copy.deepcopy(self.genes))
        nuevo.fitness = self.fitness
        return nuevo

class OptimizadorGenetico:
    """
    Optimizador de salones usando Algoritmo Genético
    
    Parámetros evolutivos:
    - Población: 150 individuos
    - Generaciones: 500 máximo
    - Cruzamiento: 80%
    - Mutación: 10% (adaptativa)
    - Elitismo: 10%
    """
    
    def __init__(self, tam_poblacion=150, num_generaciones=500, 
                 prob_cruzamiento=0.8, prob_mutacion=0.1, 
                 tasa_elitismo=0.1, verbose=True):
        
        self.tam_poblacion = tam_poblacion
        self.num_generaciones = num_generaciones
        self.prob_cruzamiento = prob_cruzamiento
        self.prob_mutacion_inicial = prob_mutacion
        self.tasa_elitismo = tasa_elitismo
        self.verbose = verbose
        
        # Cargar configuraciones de restricciones
        self._log("📂 Cargando configuraciones de restricciones...")
        self.config_materias, self.preferencias_profesores = cargar_configuraciones()
        
        # Catálogos
        self.salones_validos = self._inicializar_salones()
        self.salones_invalidos = {'AV1', 'AV2', 'AV4', 'AV5', 'E11'}
        self.laboratorios = {'LBD', 'LBD2', 'LCA', 'LCG1', 'LCG2', 'LIA', 'LR', 'LSO'}
        self.salones_teoria = {'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'}
        
        # Pesos de fitness
        self.pesos = {
            'invalidos': 1000,
            'conflictos': 500,
            'tipo_incorrecto': 300,
            'preferencia_prioritaria': 400,  # NUEVO
            'preferencia_opcional': 50,      # NUEVO
            'primer_semestre': 400,
            'capacidad': 200,
            'movimientos': 10,
            'cambios_piso': 5,
            'distancia': 3,
            'balance': 2
        }
        
        # Analizador de movimientos
        self.analizador_mov = AnalizadorMovimientos()
        
        # Historial
        self.historial_fitness = []
        self.mejor_global = None
    
    def _inicializar_salones(self):
        """Inicializa catálogo de salones válidos"""
        salones = {
            'planta_baja': ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7'],
            'planta_alta': ['FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'],
            'labs_p1': ['LR', 'LSO', 'LIA', 'LCG1', 'LCG2'],
            'labs_p2': ['LBD', 'LCA', 'LBD2', 'LCG3']
        }
        
        todos = []
        for categoria in salones.values():
            todos.extend(categoria)
        
        return todos
    
    def _log(self, mensaje):
        """Imprime mensaje si verbose=True"""
        if self.verbose:
            print(mensaje)
    
    def df_a_cromosoma(self, df):
        """Convierte DataFrame a cromosoma"""
        genes = []
        for idx, row in df.iterrows():
            gen = {
                'idx': idx,
                'grupo': row['Grupo'],
                'materia': row['Materia'],
                'dia': row['Dia'],
                'bloque': row['Bloque_Horario'],
                'profesor': row['Profesor'],
                'salon': row['Salon'],
                'tipo_requerido': row['Tipo_Salon'],
                'es_primer_semestre': row['Es_Primer_Semestre'] == 1
            }
            genes.append(gen)
        
        return Cromosoma(genes)
    
    def cromosoma_a_df(self, cromosoma, df_base):
        """Convierte cromosoma a DataFrame"""
        df = df_base.copy()
        for gen in cromosoma.genes:
            df.at[gen['idx'], 'Salon'] = gen['salon']
            
            # Actualizar tipo y piso según salón
            if gen['salon'].startswith('L'):
                df.at[gen['idx'], 'Tipo_Salon'] = 'Laboratorio'
                if gen['salon'] in ['LR', 'LSO', 'LIA', 'LCG1', 'LCG2']:
                    df.at[gen['idx'], 'Piso'] = 'Primer Piso'
                else:
                    df.at[gen['idx'], 'Piso'] = 'Segundo Piso'
            else:
                df.at[gen['idx'], 'Tipo_Salon'] = 'Teoría'
                if gen['salon'] in ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7']:
                    df.at[gen['idx'], 'Piso'] = 'Planta Baja'
                else:
                    df.at[gen['idx'], 'Piso'] = 'Planta Alta'
            
            df.at[gen['idx'], 'Es_Invalido'] = 1 if gen['salon'] in self.salones_invalidos else 0
        
        return df
    
    def calcular_fitness(self, cromosoma):
        """
        Calcula fitness del cromosoma
        Mayor fitness = mejor solución
        """
        penalizaciones = {}
        costos = {}
        
        # P1: Salones inválidos
        invalidos = sum(1 for g in cromosoma.genes if g['salon'] in self.salones_invalidos)
        penalizaciones['invalidos'] = invalidos
        
        # P2: Conflictos de horario (mismo salón, mismo día/hora)
        conflictos = 0
        for i, g1 in enumerate(cromosoma.genes):
            for g2 in cromosoma.genes[i+1:]:
                if (g1['salon'] == g2['salon'] and 
                    g1['dia'] == g2['dia'] and 
                    g1['bloque'] == g2['bloque']):
                    conflictos += 1
        penalizaciones['conflictos'] = conflictos
        
        # P3: Tipo de salón incorrecto
        tipo_incorrecto = 0
        for g in cromosoma.genes:
            es_lab = g['salon'] in self.laboratorios
            requiere_lab = g['tipo_requerido'] == 'Laboratorio'
            if es_lab != requiere_lab:
                tipo_incorrecto += 1
        penalizaciones['tipo_incorrecto'] = tipo_incorrecto
        
        # P4: Preferencias de profesores (NUEVO)
        pref_prioritarias_violadas = 0
        pref_opcionales_violadas = 0
        
        for g in cromosoma.genes:
            profesor = g['profesor']
            tipo_req = g['tipo_requerido']
            salon = g['salon']
            
            pref_salon = obtener_preferencia_profesor(profesor, tipo_req, self.preferencias_profesores)
            if pref_salon:
                es_prioritaria = es_preferencia_prioritaria(profesor, tipo_req, self.preferencias_profesores)
                if pref_salon != salon:
                    if es_prioritaria:
                        pref_prioritarias_violadas += 1
                    else:
                        pref_opcionales_violadas += 1
        
        penalizaciones['preferencia_prioritaria'] = pref_prioritarias_violadas
        penalizaciones['preferencia_opcional'] = pref_opcionales_violadas
        
        # P5: Grupos de primer semestre (más de un salón de teoría)
        grupos_1er = defaultdict(set)
        for g in cromosoma.genes:
            if g['es_primer_semestre'] and g['tipo_requerido'] == 'Teoría':
                grupos_1er[g['grupo']].add(g['salon'])
        
        primer_sem_violaciones = sum(1 for salones in grupos_1er.values() if len(salones) > 1)
        penalizaciones['primer_semestre'] = primer_sem_violaciones
        
        # P5: Capacidad (simplificado - asumimos capacidad suficiente por ahora)
        penalizaciones['capacidad'] = 0
        
        # Convertir a DataFrame temporal para calcular costos
        df_temp = pd.DataFrame([{
            'Grupo': g['grupo'],
            'Materia': g['materia'],
            'Dia': g['dia'],
            'Bloque_Horario': g['bloque'],
            'Profesor': g['profesor'],
            'Salon': g['salon']
        } for g in cromosoma.genes])
        
        # C1, C2, C3: Movimientos, cambios de piso, distancia
        metricas_mov = self.analizador_mov.analizar_todos_profesores(df_temp)
        costos['movimientos'] = metricas_mov['agregado']['total_movimientos']
        costos['cambios_piso'] = metricas_mov['agregado']['total_cambios_piso']
        costos['distancia'] = metricas_mov['agregado']['total_distancia']
        
        # C4: Desbalance de uso de salones
        uso_salones = df_temp['Salon'].value_counts()
        if len(uso_salones) > 0:
            costos['balance'] = uso_salones.var()
        else:
            costos['balance'] = 0
        
        # Calcular fitness total (negativo de la suma ponderada)
        fitness = -(
            self.pesos['invalidos'] * penalizaciones['invalidos'] +
            self.pesos['conflictos'] * penalizaciones['conflictos'] +
            self.pesos['tipo_incorrecto'] * penalizaciones['tipo_incorrecto'] +
            self.pesos['preferencia_prioritaria'] * penalizaciones['preferencia_prioritaria'] +
            self.pesos['preferencia_opcional'] * penalizaciones['preferencia_opcional'] +
            self.pesos['primer_semestre'] * penalizaciones['primer_semestre'] +
            self.pesos['capacidad'] * penalizaciones['capacidad'] +
            self.pesos['movimientos'] * costos['movimientos'] +
            self.pesos['cambios_piso'] * costos['cambios_piso'] +
            self.pesos['distancia'] * costos['distancia'] +
            self.pesos['balance'] * costos['balance']
        )
        
        cromosoma.fitness = fitness
        cromosoma.penalizaciones = penalizaciones
        cromosoma.costos = costos
        
        return fitness
    
    def generar_individuo_aleatorio(self, base):
        """Genera un individuo con asignaciones aleatorias válidas"""
        individuo = base.copy()
        
        for gen in individuo.genes:
            # Elegir salón aleatorio válido
            if gen['tipo_requerido'] == 'Laboratorio':
                # Solo laboratorios
                salones_candidatos = [s for s in self.salones_validos if s.startswith('L')]
            else:
                # Preferir teoría pero permitir labs
                salones_candidatos = self.salones_validos
            
            gen['salon'] = random.choice(salones_candidatos)
        
        return individuo
    
    def seleccion_torneo(self, poblacion, k=3):
        """Selección por torneo"""
        torneo = random.sample(poblacion, k)
        return max(torneo, key=lambda ind: ind.fitness)
    
    def cruzamiento_uniforme(self, padre1, padre2):
        """Cruzamiento uniforme"""
        hijo1 = padre1.copy()
        hijo2 = padre2.copy()
        
        for i in range(len(padre1)):
            if random.random() < 0.5:
                hijo1.genes[i]['salon'] = padre2.genes[i]['salon']
                hijo2.genes[i]['salon'] = padre1.genes[i]['salon']
        
        return hijo1, hijo2
    
    def mutacion(self, cromosoma, prob_mutacion):
        """Mutación inteligente"""
        for gen in cromosoma.genes:
            if random.random() < prob_mutacion:
                # Mutar a salón válido
                if gen['tipo_requerido'] == 'Laboratorio':
                    candidatos = [s for s in self.salones_validos if s.startswith('L')]
                else:
                    candidatos = self.salones_validos
                
                gen['salon'] = random.choice(candidatos)
        
        return cromosoma
    
    def reparar_restricciones(self, cromosoma):
        """Repara violaciones de restricciones hard"""
        
        # R0: FORZAR preferencias prioritarias (PRIMERO, antes que todo)
        for gen in cromosoma.genes:
            profesor = gen['profesor']
            tipo_req = gen['tipo_requerido']
            
            pref_salon = obtener_preferencia_profesor(profesor, tipo_req, self.preferencias_profesores)
            es_prioritaria = es_preferencia_prioritaria(profesor, tipo_req, self.preferencias_profesores)
            
            # Si hay preferencia PRIORITARIA, forzar ese salón (sin excepciones)
            if es_prioritaria and pref_salon:
                gen['salon'] = pref_salon
        
        # R1: Eliminar salones inválidos
        for gen in cromosoma.genes:
            if gen['salon'] in self.salones_invalidos:
                # Verificar si tiene preferencia prioritaria
                profesor = gen['profesor']
                tipo_req = gen['tipo_requerido']
                pref_salon = obtener_preferencia_profesor(profesor, tipo_req, self.preferencias_profesores)
                es_prioritaria = es_preferencia_prioritaria(profesor, tipo_req, self.preferencias_profesores)
                
                # Si tiene preferencia prioritaria, usar esa
                if es_prioritaria and pref_salon:
                    gen['salon'] = pref_salon
                else:
                    # Buscar alternativa del tipo correcto
                    if gen['tipo_requerido'] == 'Laboratorio':
                        candidatos = [s for s in self.salones_validos if s in self.laboratorios]
                    else:
                        candidatos = [s for s in self.salones_validos if s in self.salones_teoria]
                    
                    if candidatos:
                        gen['salon'] = random.choice(candidatos)
        
        # R2: Resolver conflictos de horario
        # (Simplificado - en versión completa se haría más exhaustivo)
        
        # R3: Grupos de primer semestre
        grupos_1er = defaultdict(list)
        for gen in cromosoma.genes:
            if gen['es_primer_semestre'] and gen['tipo_requerido'] == 'Teoría':
                grupos_1er[gen['grupo']].append(gen)
        
        for grupo, genes in grupos_1er.items():
            if len(genes) > 0:
                # Unificar al salón más común
                salones = [g['salon'] for g in genes]
                salon_comun = max(set(salones), key=salones.count)
                for g in genes:
                    g['salon'] = salon_comun
        
        return cromosoma
    
    def evolucionar(self, df_inicial):
        """
        Ejecuta el algoritmo genético completo
        """
        self._log("\n" + "="*80)
        self._log("🧬 ALGORITMO GENÉTICO - OPTIMIZACIÓN EVOLUTIVA")
        self._log("="*80 + "\n")
        
        # 1. INICIALIZACIÓN
        self._log("📊 Inicializando población...")
        
        # Agregar columna tipo_requerido basada en configuración
        df_trabajo = df_inicial.copy()
        horas_asignadas = {}
        tipos_requeridos = []
        
        for idx, row in df_trabajo.iterrows():
            grupo = row['Grupo']
            materia = row['Materia']
            key = (grupo, materia)
            indice_hora = horas_asignadas.get(key, 0)
            tipo_req = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas[key] = indice_hora + 1
            tipos_requeridos.append(tipo_req)
        
        df_trabajo['Tipo_Salon'] = tipos_requeridos  # Sobrescribir con tipo correcto
        poblacion = []
        
        # Individuo 1: Horario inicial
        individuo_inicial = self.df_a_cromosoma(df_trabajo) # Use df_trabajo with new column
        poblacion.append(individuo_inicial)
        
        # Individuos 2-N: Variaciones aleatorias
        for i in range(1, self.tam_poblacion):
            individuo = self.generar_individuo_aleatorio(individuo_inicial)
            poblacion.append(individuo)
        
        # Evaluar población inicial
        for ind in poblacion:
            self.calcular_fitness(ind)
        
        self.mejor_global = max(poblacion, key=lambda x: x.fitness)
        self.historial_fitness = [self.mejor_global.fitness]
        
        self._log(f"✅ Población inicial: {self.tam_poblacion} individuos")
        self._log(f"   Mejor fitness inicial: {self.mejor_global.fitness:.0f}")
        self._log(f"   Inválidos: {self.mejor_global.penalizaciones['invalidos']}")
        
        # 2. EVOLUCIÓN
        self._log(f"\n🔄 Iniciando evolución ({self.num_generaciones} generaciones máx)...\n")
        
        generaciones_sin_mejora = 0
        
        for generacion in range(1, self.num_generaciones + 1):
            # 2.1 SELECCIÓN
            padres = []
            for _ in range(self.tam_poblacion):
                padre = self.seleccion_torneo(poblacion, k=3)
                padres.append(padre)
            
            # 2.2 CRUZAMIENTO
            hijos = []
            for i in range(0, self.tam_poblacion - 1, 2):
                if random.random() < self.prob_cruzamiento:
                    hijo1, hijo2 = self.cruzamiento_uniforme(padres[i], padres[i+1])
                else:
                    hijo1, hijo2 = padres[i].copy(), padres[i+1].copy()
                
                hijos.append(hijo1)
                hijos.append(hijo2)
            
            # Si falta uno (población impar)
            if len(hijos) < self.tam_poblacion:
                hijos.append(padres[-1].copy())
            
            # 2.3 MUTACIÓN (adaptativa)
            prob_mutacion = self.prob_mutacion_inicial * (1 - generacion / self.num_generaciones)
            for hijo in hijos:
                self.mutacion(hijo, prob_mutacion)
            
            # 2.4 REPARACIÓN
            for hijo in hijos:
                self.reparar_restricciones(hijo)
            
            # 2.5 EVALUACIÓN
            for hijo in hijos:
                self.calcular_fitness(hijo)
            
            # 2.6 ELITISMO
            num_elite = int(self.tam_poblacion * self.tasa_elitismo)
            elite = sorted(poblacion, key=lambda x: x.fitness, reverse=True)[:num_elite]
            
            # 2.7 REEMPLAZO
            poblacion = elite + hijos[:(self.tam_poblacion - num_elite)]
            
            # 2.8 ACTUALIZAR MEJOR
            mejor_gen = max(poblacion, key=lambda x: x.fitness)
            if mejor_gen.fitness > self.mejor_global.fitness:
                self.mejor_global = mejor_gen.copy()
                generaciones_sin_mejora = 0
            else:
                generaciones_sin_mejora += 1
            
            self.historial_fitness.append(self.mejor_global.fitness)
            
            # 2.9 CRITERIO DE PARADA
            if generaciones_sin_mejora >= 50:
                self._log(f"\n⏹️  Convergencia alcanzada en generación {generacion}")
                self._log(f"   (50 generaciones sin mejora)")
                break
            
            # 2.10 LOGGING
            if generacion % 50 == 0 or generacion == 1:
                inv = self.mejor_global.penalizaciones.get('invalidos', 0) if self.mejor_global.penalizaciones else 0
                mov = self.mejor_global.costos.get('movimientos', 0) if self.mejor_global.costos else 0
                dist = self.mejor_global.costos.get('distancia', 0) if self.mejor_global.costos else 0
                
                self._log(f"Gen {generacion:3d}: Fitness={self.mejor_global.fitness:8.0f} | "
                         f"Inválidos={inv:2d} | "
                         f"Movimientos={mov:3d} | "
                         f"Distancia={dist:4.0f}")
        
        # 3. RESULTADO FINAL
        self._log("\n" + "="*80)
        self._log("✅ EVOLUCIÓN COMPLETADA")
        self._log("="*80)
        self._log(f"\n📊 Mejor solución encontrada:")
        self._log(f"   Fitness: {self.mejor_global.fitness:.0f}")
        self._log(f"   Generación final: {len(self.historial_fitness)}")
        self._log(f"\n🎯 Penalizaciones:")
        for k, v in self.mejor_global.penalizaciones.items():
            self._log(f"   {k}: {v}")
        self._log(f"\n📉 Costos:")
        for k, v in self.mejor_global.costos.items():
            self._log(f"   {k}: {v:.1f}")
        
        return self.cromosoma_a_df(self.mejor_global, df_inicial)

def main():
    """Función principal"""
    print("🧬 Optimizador Genético - Sistema de Salones ISC")
    print("="*80)
    print("Método: Algoritmo Genético Evolutivo")
    print("="*80 + "\n")
    
    # Cargar datos
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    df_inicial = pd.read_csv(csv_inicial)
    
    # Crear optimizador con parámetros reducidos para velocidad
    optimizador = OptimizadorGenetico(
        tam_poblacion=15,      # 10% de 150
        num_generaciones=100,  # Reducido de 500
        prob_cruzamiento=0.8,
        prob_mutacion=0.1,
        tasa_elitismo=0.1,
        verbose=True
    )
    
    # Evolucionar
    df_resultado = optimizador.evolucionar(df_inicial)
    
    # Analizar movimientos del resultado
    print("\n📊 Analizando movimientos de profesores...")
    analizador_mov = AnalizadorMovimientos()
    comparativa_mov = analizador_mov.comparar_horarios(df_inicial, df_resultado)
    
    print("\n" + "="*80)
    print("📈 RESULTADOS FINALES")
    print("="*80)
    print(f"\n🚶 Movimientos de Profesores:")
    print(f"   Inicial:    {comparativa_mov['inicial']['total_movimientos']} movimientos")
    print(f"   Optimizado: {comparativa_mov['optimizado']['total_movimientos']} movimientos")
    print(f"   Mejora:     {comparativa_mov['mejora']['movimientos']:+d} ({comparativa_mov['mejora']['movimientos_pct']:+.1f}%)")
    
    print(f"\n🏢 Cambios de Piso:")
    print(f"   Inicial:    {comparativa_mov['inicial']['total_cambios_piso']} cambios")
    print(f"   Optimizado: {comparativa_mov['optimizado']['total_cambios_piso']} cambios")
    print(f"   Mejora:     {comparativa_mov['mejora']['cambios_piso']:+d} ({comparativa_mov['mejora']['cambios_piso_pct']:+.1f}%)")
    
    print(f"\n📏 Distancia Total:")
    print(f"   Inicial:    {comparativa_mov['inicial']['total_distancia']:.0f} unidades")
    print(f"   Optimizado: {comparativa_mov['optimizado']['total_distancia']:.0f} unidades")
    print(f"   Mejora:     {comparativa_mov['mejora']['distancia']:+.0f} ({comparativa_mov['mejora']['distancia_pct']:+.1f}%)")
    
    # Guardar resultado
    output_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/04_Horario_Optimizado_Genetico.csv"
    df_resultado.to_csv(output_path, index=False)
    print(f"\n💾 Resultado guardado: {output_path}")
    
    # Guardar métricas de movimientos
    metricas_mov_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/03_inicial_vs_genetico/metricas_movimientos.csv"
    os.makedirs(os.path.dirname(metricas_mov_path), exist_ok=True)
    
    df_metricas_mov = pd.DataFrame([
        {'Metrica': 'Total Movimientos', 
         'Inicial': comparativa_mov['inicial']['total_movimientos'], 
         'Optimizado': comparativa_mov['optimizado']['total_movimientos'], 
         'Mejora': comparativa_mov['mejora']['movimientos'], 
         'Mejora (%)': comparativa_mov['mejora']['movimientos_pct']},
        {'Metrica': 'Cambios de Piso', 
         'Inicial': comparativa_mov['inicial']['total_cambios_piso'], 
         'Optimizado': comparativa_mov['optimizado']['total_cambios_piso'], 
         'Mejora': comparativa_mov['mejora']['cambios_piso'], 
         'Mejora (%)': comparativa_mov['mejora']['cambios_piso_pct']},
        {'Metrica': 'Distancia Total', 
         'Inicial': comparativa_mov['inicial']['total_distancia'], 
         'Optimizado': comparativa_mov['optimizado']['total_distancia'], 
         'Mejora': comparativa_mov['mejora']['distancia'], 
         'Mejora (%)': comparativa_mov['mejora']['distancia_pct']},
    ])
    
    df_metricas_mov.to_csv(metricas_mov_path, index=False)
    print(f"💾 Métricas de movimientos guardadas: {metricas_mov_path}")
    
    print("\n" + "="*80)
    print("✅ PROCESO COMPLETADO")
    print("="*80)
    print("\n📊 Próximo paso: Generar comparativa")
    print("   - Inicial vs Genético")
    print("   - Comparativa final de todos los métodos\n")

if __name__ == "__main__":
    main()
