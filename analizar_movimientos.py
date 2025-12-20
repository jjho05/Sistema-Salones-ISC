#!/usr/bin/env python3
"""
Analizador de Movimientos de Profesores
Calcula métricas clave de optimización:
- Movimientos entre salones
- Cambios de piso
- Distancia total recorrida
"""

import pandas as pd
import numpy as np
from collections import defaultdict

class AnalizadorMovimientos:
    """Analiza movimientos y optimización de profesores"""
    
    def __init__(self):
        # Matriz de distancias entre salones (simplificada)
        self.distancias = self._inicializar_distancias()
        
        # Pisos
        self.planta_baja = {'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7'}
        self.planta_alta = {'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'}
        self.labs_p1 = {'LR', 'LSO', 'LIA', 'LCG1', 'LCG2'}
        self.labs_p2 = {'LBD', 'LCA', 'LBD2', 'LCG3'}
    
    def _inicializar_distancias(self):
        """
        Inicializa matriz de distancias entre salones
        Distancias aproximadas en "unidades" (1 unidad = salón adyacente)
        """
        distancias = {}
        
        # Planta Baja FF (en línea)
        pb = ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7']
        for i, s1 in enumerate(pb):
            for j, s2 in enumerate(pb):
                distancias[(s1, s2)] = abs(i - j)
        
        # Planta Alta FF (en línea)
        pa = ['FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD']
        for i, s1 in enumerate(pa):
            for j, s2 in enumerate(pa):
                distancias[(s1, s2)] = abs(i - j)
        
        # Labs Piso 1
        l1 = ['LR', 'LSO', 'LIA', 'LCG1', 'LCG2']
        for i, s1 in enumerate(l1):
            for j, s2 in enumerate(l1):
                distancias[(s1, s2)] = abs(i - j)
        
        # Labs Piso 2
        l2 = ['LBD', 'LCA', 'LBD2', 'LCG3']
        for i, s1 in enumerate(l2):
            for j, s2 in enumerate(l2):
                distancias[(s1, s2)] = abs(i - j)
        
        # Entre pisos del mismo edificio
        for s1 in pb:
            for s2 in pa:
                distancias[(s1, s2)] = 5  # Cambio de piso
                distancias[(s2, s1)] = 5
        
        # Entre edificios (FF ↔ Labs)
        for s1 in pb + pa:
            for s2 in l1 + l2:
                distancias[(s1, s2)] = 10  # Cambio de edificio
                distancias[(s2, s1)] = 10
        
        # Entre pisos de labs
        for s1 in l1:
            for s2 in l2:
                distancias[(s1, s2)] = 5
                distancias[(s2, s1)] = 5
        
        return distancias
    
    def obtener_distancia(self, salon1, salon2):
        """Obtiene distancia entre dos salones"""
        if salon1 == salon2:
            return 0
        
        # Buscar en matriz
        if (salon1, salon2) in self.distancias:
            return self.distancias[(salon1, salon2)]
        
        # Si no está en la matriz, asumir distancia grande (salones inválidos)
        return 15
    
    def obtener_piso(self, salon):
        """Obtiene el piso de un salón"""
        if salon in self.planta_baja:
            return 'Planta Baja'
        elif salon in self.planta_alta:
            return 'Planta Alta'
        elif salon in self.labs_p1:
            return 'Labs Piso 1'
        elif salon in self.labs_p2:
            return 'Labs Piso 2'
        else:
            return 'Inválido'
    
    def analizar_profesor(self, df_profesor):
        """
        Analiza movimientos de un profesor
        
        Args:
            df_profesor: DataFrame con asignaciones del profesor
        
        Returns:
            dict: Métricas del profesor
        """
        # Ordenar por día y hora
        df_sorted = df_profesor.sort_values(['Dia', 'Bloque_Horario'])
        
        metricas = {
            'total_clases': len(df_profesor),
            'salones_diferentes': df_profesor['Salon'].nunique(),
            'movimientos': 0,
            'cambios_piso': 0,
            'distancia_total': 0,
            'movimientos_por_dia': defaultdict(int),
            'salones_usados': list(df_profesor['Salon'].unique())
        }
        
        # Analizar por día
        for dia in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']:
            clases_dia = df_sorted[df_sorted['Dia'] == dia].sort_values('Bloque_Horario')
            
            if len(clases_dia) <= 1:
                continue
            
            salon_anterior = None
            piso_anterior = None
            
            for idx, row in clases_dia.iterrows():
                salon_actual = row['Salon']
                piso_actual = self.obtener_piso(salon_actual)
                
                if salon_anterior is not None:
                    # Contar movimiento
                    if salon_actual != salon_anterior:
                        metricas['movimientos'] += 1
                        metricas['movimientos_por_dia'][dia] += 1
                        
                        # Calcular distancia
                        distancia = self.obtener_distancia(salon_anterior, salon_actual)
                        metricas['distancia_total'] += distancia
                        
                        # Contar cambio de piso
                        if piso_actual != piso_anterior:
                            metricas['cambios_piso'] += 1
                
                salon_anterior = salon_actual
                piso_anterior = piso_actual
        
        return metricas
    
    def analizar_todos_profesores(self, df):
        """
        Analiza movimientos de todos los profesores
        
        Args:
            df: DataFrame completo
        
        Returns:
            dict: Métricas agregadas y por profesor
        """
        profesores = df['Profesor'].unique()
        
        resultados = {
            'por_profesor': {},
            'agregado': {
                'total_movimientos': 0,
                'total_cambios_piso': 0,
                'total_distancia': 0,
                'promedio_movimientos': 0,
                'promedio_distancia': 0,
                'max_movimientos': 0,
                'min_movimientos': float('inf'),
                'profesores_sin_movimientos': 0
            }
        }
        
        movimientos_lista = []
        
        for profesor in profesores:
            if 'SIN' in profesor or 'PROFESOR' not in profesor:
                continue
            
            df_prof = df[df['Profesor'] == profesor]
            metricas = self.analizar_profesor(df_prof)
            
            resultados['por_profesor'][profesor] = metricas
            
            # Agregar a totales
            resultados['agregado']['total_movimientos'] += metricas['movimientos']
            resultados['agregado']['total_cambios_piso'] += metricas['cambios_piso']
            resultados['agregado']['total_distancia'] += metricas['distancia_total']
            
            movimientos_lista.append(metricas['movimientos'])
            
            if metricas['movimientos'] == 0:
                resultados['agregado']['profesores_sin_movimientos'] += 1
        
        # Calcular promedios
        n_profesores = len(movimientos_lista)
        if n_profesores > 0:
            resultados['agregado']['promedio_movimientos'] = np.mean(movimientos_lista)
            resultados['agregado']['promedio_distancia'] = resultados['agregado']['total_distancia'] / n_profesores
            resultados['agregado']['max_movimientos'] = max(movimientos_lista)
            resultados['agregado']['min_movimientos'] = min(movimientos_lista)
        
        resultados['agregado']['n_profesores'] = n_profesores
        
        return resultados
    
    def comparar_horarios(self, df_inicial, df_optimizado):
        """
        Compara métricas entre dos horarios
        
        Returns:
            dict: Comparativa de métricas
        """
        print("\n📊 Analizando movimientos de profesores...")
        
        metricas_inicial = self.analizar_todos_profesores(df_inicial)
        metricas_optimizado = self.analizar_todos_profesores(df_optimizado)
        
        comparativa = {
            'inicial': metricas_inicial['agregado'],
            'optimizado': metricas_optimizado['agregado'],
            'mejora': {}
        }
        
        # Calcular mejoras
        ini = metricas_inicial['agregado']
        opt = metricas_optimizado['agregado']
        
        comparativa['mejora']['movimientos'] = ini['total_movimientos'] - opt['total_movimientos']
        comparativa['mejora']['movimientos_pct'] = (comparativa['mejora']['movimientos'] / ini['total_movimientos'] * 100) if ini['total_movimientos'] > 0 else 0
        
        comparativa['mejora']['cambios_piso'] = ini['total_cambios_piso'] - opt['total_cambios_piso']
        comparativa['mejora']['cambios_piso_pct'] = (comparativa['mejora']['cambios_piso'] / ini['total_cambios_piso'] * 100) if ini['total_cambios_piso'] > 0 else 0
        
        comparativa['mejora']['distancia'] = ini['total_distancia'] - opt['total_distancia']
        comparativa['mejora']['distancia_pct'] = (comparativa['mejora']['distancia'] / ini['total_distancia'] * 100) if ini['total_distancia'] > 0 else 0
        
        return comparativa
    
    def generar_reporte(self, comparativa):
        """Genera reporte de comparativa"""
        print("\n" + "="*80)
        print("📊 REPORTE DE MOVIMIENTOS DE PROFESORES")
        print("="*80 + "\n")
        
        ini = comparativa['inicial']
        opt = comparativa['optimizado']
        mej = comparativa['mejora']
        
        print(f"👥 Profesores analizados: {ini['n_profesores']}")
        print(f"\n📍 MOVIMIENTOS ENTRE SALONES:")
        print(f"   Inicial:    {ini['total_movimientos']} movimientos")
        print(f"   Optimizado: {opt['total_movimientos']} movimientos")
        print(f"   Mejora:     {mej['movimientos']:+d} ({mej['movimientos_pct']:+.1f}%)")
        
        print(f"\n🏢 CAMBIOS DE PISO:")
        print(f"   Inicial:    {ini['total_cambios_piso']} cambios")
        print(f"   Optimizado: {opt['total_cambios_piso']} cambios")
        print(f"   Mejora:     {mej['cambios_piso']:+d} ({mej['cambios_piso_pct']:+.1f}%)")
        
        print(f"\n📏 DISTANCIA TOTAL RECORRIDA:")
        print(f"   Inicial:    {ini['total_distancia']:.0f} unidades")
        print(f"   Optimizado: {opt['total_distancia']:.0f} unidades")
        print(f"   Mejora:     {mej['distancia']:+.0f} ({mej['distancia_pct']:+.1f}%)")
        
        print(f"\n📊 PROMEDIOS POR PROFESOR:")
        print(f"   Movimientos promedio (inicial):    {ini['promedio_movimientos']:.1f}")
        print(f"   Movimientos promedio (optimizado): {opt['promedio_movimientos']:.1f}")
        
        print(f"\n✅ Profesores sin movimientos:")
        print(f"   Inicial:    {ini['profesores_sin_movimientos']}")
        print(f"   Optimizado: {opt['profesores_sin_movimientos']}")
        
        print("\n" + "="*80 + "\n")

def main():
    """Función de prueba"""
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    csv_optimizado = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/02_Horario_Optimizado_Profesor.csv"
    
    df_inicial = pd.read_csv(csv_inicial)
    df_optimizado = pd.read_csv(csv_optimizado)
    
    analizador = AnalizadorMovimientos()
    comparativa = analizador.comparar_horarios(df_inicial, df_optimizado)
    analizador.generar_reporte(comparativa)
    
    # Guardar CSV
    output_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/01_inicial_vs_profesor/metricas_movimientos.csv"
    
    df_metricas = pd.DataFrame([
        {'Metrica': 'Total Movimientos', 'Inicial': comparativa['inicial']['total_movimientos'], 
         'Optimizado': comparativa['optimizado']['total_movimientos'], 
         'Mejora': comparativa['mejora']['movimientos'], 
         'Mejora (%)': comparativa['mejora']['movimientos_pct']},
        {'Metrica': 'Cambios de Piso', 'Inicial': comparativa['inicial']['total_cambios_piso'], 
         'Optimizado': comparativa['optimizado']['total_cambios_piso'], 
         'Mejora': comparativa['mejora']['cambios_piso'], 
         'Mejora (%)': comparativa['mejora']['cambios_piso_pct']},
        {'Metrica': 'Distancia Total', 'Inicial': comparativa['inicial']['total_distancia'], 
         'Optimizado': comparativa['optimizado']['total_distancia'], 
         'Mejora': comparativa['mejora']['distancia'], 
         'Mejora (%)': comparativa['mejora']['distancia_pct']},
    ])
    
    df_metricas.to_csv(output_path, index=False)
    print(f"💾 Métricas guardadas: {output_path}\n")

if __name__ == "__main__":
    main()
