#!/usr/bin/env python3
"""
Optimizador de Salones - Método Machine Learning
Implementación del modelo de aprendizaje automático para optimización de asignaciones
Incluye análisis de movimientos de profesores
ACTUALIZADO: Integra restricciones de teoría/lab y preferencias de profesores
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, classification_report
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

class OptimizadorML:
    """
    Optimizador de salones usando Machine Learning
    
    Combina:
    - Random Forest para clasificación (predecir salón)
    - Gradient Boosting para scoring (evaluar calidad)
    - Reglas de negocio para restricciones hard
    """
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        
        # Cargar configuraciones de restricciones
        self._log("📂 Cargando configuraciones de restricciones...")
        self.config_materias, self.preferencias_profesores = cargar_configuraciones()
        
        # Modelos
        self.clasificador = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.regressor_calidad = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        # Encoders
        self.encoders = {}
        self.feature_names = []
        
        # Catálogos
        self.salones_validos = self._inicializar_salones()
        self.salones_invalidos = {'AV1', 'AV2', 'AV4', 'AV5', 'E11'}
        self.laboratorios = {'LBD', 'LBD2', 'LCA', 'LCG1', 'LCG2', 'LIA', 'LR', 'LSO'}
        self.salones_teoria = {'FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9', 'FFA', 'FFB', 'FFC', 'FFD'}
        
        # Métricas
        self.metricas_entrenamiento = {}
    
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
        
        return set(todos)
    
    def _log(self, mensaje):
        """Imprime mensaje si verbose=True"""
        if self.verbose:
            print(mensaje)
    
    def extraer_features(self, df, incluir_target=True):
        """
        Extrae features del DataFrame de horarios
        
        Args:
            df: DataFrame con columnas [Grupo, Materia, Dia, Hora_Inicio, Salon, etc.]
            incluir_target: Si incluir columna target (Salon)
        
        Returns:
            X: Features
            y: Target (si incluir_target=True)
        """
        self._log("📊 Extrayendo features...")
        
        features = pd.DataFrame()
        
        # 1. Features del Grupo
        features['grupo_codigo'] = df['Grupo']
        features['es_primer_semestre'] = df['Grupo'].str[0] == '1'
        features['semestre'] = df['Grupo'].str[0].astype(int)
        
        # 2. Features de la Materia
        features['materia'] = df['Materia']
        features['horas_semana'] = df['Horas_Semana']
        
        # 3. Features Temporales
        features['dia_semana'] = df['Dia']
        features['bloque_horario'] = df['Bloque_Horario']
        features['hora_inicio'] = df['Hora_Inicio'].str[:2].astype(int)
        features['es_hora_pico'] = features['hora_inicio'].between(10, 14)
        
        # 4. Features del Profesor
        features['profesor'] = df['Profesor']
        
        # 5. Features del Tipo de Salón
        features['tipo_salon_actual'] = df['Tipo_Salon']
        features['piso_actual'] = df['Piso']
        
        # 6. Features Contextuales (agregadas por grupo)
        grupo_stats = df.groupby('Grupo').agg({
            'Salon': 'nunique',
            'Tipo_Salon': lambda x: (x == 'Laboratorio').sum()
        }).rename(columns={'Salon': 'num_salones_grupo', 'Tipo_Salon': 'num_labs_grupo'})
        
        features = features.join(grupo_stats, on='grupo_codigo')
        
        # 7. Features del Profesor (agregadas)
        prof_stats = df.groupby('Profesor').agg({
            'Grupo': 'nunique',
            'Salon': 'nunique'
        }).rename(columns={'Grupo': 'num_grupos_profesor', 'Salon': 'num_salones_profesor'})
        
        features = features.join(prof_stats, on='profesor')
    
        # 8. Features de Restricciones (NUEVO)
        # Rastrear horas asignadas por materia para determinar tipo
        horas_asignadas = {}
        es_teoria_list = []
        tiene_pref_list = []
        prioridad_pref_list = []
        
        for idx, row in df.iterrows():
            grupo = row['Grupo']
            materia = row['Materia']
            profesor = row['Profesor']
            
            # Determinar tipo de hora
            key = (grupo, materia)
            indice_hora = horas_asignadas.get(key, 0)
            tipo_requerido = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas[key] = indice_hora + 1
            
            es_teoria = 1 if tipo_requerido == 'Teoría' else 0
            es_teoria_list.append(es_teoria)
            
            # Verificar preferencia del profesor
            pref_salon = obtener_preferencia_profesor(profesor, tipo_requerido, self.preferencias_profesores)
            tiene_pref = 1 if pref_salon else 0
            tiene_pref_list.append(tiene_pref)
            
            # Prioridad de preferencia (0=ninguna, 1=opcional, 2=prioritaria)
            if pref_salon:
                es_prioritaria = es_preferencia_prioritaria(profesor, tipo_requerido, self.preferencias_profesores)
                prioridad = 2 if es_prioritaria else 1
            else:
                prioridad = 0
            prioridad_pref_list.append(prioridad)
        
        features['es_teoria'] = es_teoria_list
        features['tiene_preferencia_profesor'] = tiene_pref_list
        features['prioridad_preferencia'] = prioridad_pref_list
        
        # Codificar variables categóricas
        categorical_cols = ['grupo_codigo', 'materia', 'dia_semana', 'bloque_horario', 
                          'profesor', 'tipo_salon_actual', 'piso_actual']
        
        for col in categorical_cols:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                features[f'{col}_encoded'] = self.encoders[col].fit_transform(features[col].astype(str))
            else:
                # Para predicción, manejar valores no vistos
                features[f'{col}_encoded'] = features[col].apply(
                    lambda x: self.encoders[col].transform([str(x)])[0] 
                    if str(x) in self.encoders[col].classes_ 
                    else -1
                )
        
        # Seleccionar solo features numéricas para el modelo
        feature_cols = [col for col in features.columns if col.endswith('_encoded') or 
                       col in ['es_primer_semestre', 'semestre', 'horas_semana', 'hora_inicio', 
                              'es_hora_pico', 'num_salones_grupo', 'num_labs_grupo',
                              'num_grupos_profesor', 'num_salones_profesor',
                              'es_teoria', 'tiene_preferencia_profesor', 'prioridad_preferencia']]
        
        X = features[feature_cols].fillna(0)
        self.feature_names = feature_cols
        
        if incluir_target:
            # Codificar target (Salon)
            if 'salon_encoder' not in self.encoders:
                self.encoders['salon_encoder'] = LabelEncoder()
                y = self.encoders['salon_encoder'].fit_transform(df['Salon'])
            else:
                y = self.encoders['salon_encoder'].transform(df['Salon'])
            
            return X, y
        
        return X
    
    def calcular_scores_calidad(self, df):
        """
        Calcula score de calidad para cada asignación
        
        Score más alto = mejor asignación
        Score considera:
        - Salones inválidos (penalización alta)
        - Movimientos del profesor
        - Tipo de salón apropiado
        """
        scores = []
        
        for idx, row in df.iterrows():
            score = 100  # Score base
            
            # Penalización por salón inválido
            if row['Salon'] in self.salones_invalidos:
                score -= 1000
            
            # Bonus por tipo de salón apropiado
            if row['Tipo_Salon'] == 'Laboratorio' and row['Horas_Semana'] >= 4:
                score += 10
            elif row['Tipo_Salon'] == 'Teoría' and row['Horas_Semana'] <= 4:
                score += 5
            
            # Penalización por uso excesivo del salón (si tenemos esa info)
            # TODO: Agregar cuando tengamos datos de ocupación
            
            scores.append(score)
        
        return np.array(scores)
    
    def entrenar(self, df_inicial):
        """
        Entrena el modelo ML aprendiendo patrones del horario inicial
        
        El modelo aprende:
        - Qué tipo de salones se usan para cada tipo de materia
        - Patrones de asignación por día/hora
        - Preferencias de profesores
        - Distribución de uso de salones
        
        Args:
            df_inicial: DataFrame del horario inicial
        
        Returns:
            dict: Métricas de entrenamiento
        """
        self._log("\n" + "="*80)
        self._log("🎓 ENTRENANDO MODELO MACHINE LEARNING")
        self._log("="*80 + "\n")
        
        # Filtrar solo asignaciones válidas para aprender patrones correctos
        df_valido = df_inicial[df_inicial['Es_Invalido'] == 0].copy()
        
        self._log(f"📊 Dataset de entrenamiento:")
        self._log(f"   Total de asignaciones: {len(df_inicial)}")
        self._log(f"   Asignaciones válidas (para entrenamiento): {len(df_valido)}")
        self._log(f"   Asignaciones inválidas (a corregir): {len(df_inicial) - len(df_valido)}")
        
        # Extraer features de asignaciones válidas
        X, y = self.extraer_features(df_valido, incluir_target=True)
        
        self._log(f"   Features: {len(self.feature_names)}")
        self._log(f"   Clases (salones): {len(np.unique(y))}")
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Entrenar clasificador
        self._log("\n🌲 Entrenando Random Forest Classifier...")
        self._log("   Aprendiendo patrones de asignación de salones...")
        self.clasificador.fit(X_train, y_train)
        
        # Evaluar clasificador
        y_pred = self.clasificador.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        self._log(f"   ✅ Accuracy: {accuracy:.3f}")
        self._log(f"   ✅ F1-Score: {f1:.3f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.clasificador, X, y, cv=5)
        self._log(f"   ✅ CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        # Entrenar regressor de calidad
        self._log("\n📈 Entrenando Gradient Boosting Regressor...")
        self._log("   Aprendiendo a evaluar calidad de asignaciones...")
        scores_calidad = self.calcular_scores_calidad(df_valido)
        self.regressor_calidad.fit(X_train, scores_calidad[:len(X_train)])
        
        score_r2 = self.regressor_calidad.score(X_test, scores_calidad[len(X_train):])
        self._log(f"   ✅ R² Score: {score_r2:.3f}")
        
        # Feature importance
        self._log("\n🔍 Top 10 Features más importantes:")
        importances = self.clasificador.feature_importances_
        indices = np.argsort(importances)[::-1][:10]
        
        for i, idx in enumerate(indices, 1):
            self._log(f"   {i}. {self.feature_names[idx]}: {importances[idx]:.4f}")
        
        # Guardar métricas
        self.metricas_entrenamiento = {
            'accuracy': accuracy,
            'f1_score': f1,
            'cv_score_mean': cv_scores.mean(),
            'cv_score_std': cv_scores.std(),
            'r2_score': score_r2,
            'n_samples_total': len(df_inicial),
            'n_samples_validas': len(df_valido),
            'n_samples_invalidas': len(df_inicial) - len(df_valido),
            'n_features': len(self.feature_names),
            'n_classes': len(np.unique(y))
        }
        
        self._log("\n" + "="*80)
        self._log("✅ ENTRENAMIENTO COMPLETADO")
        self._log("="*80 + "\n")
        
        return self.metricas_entrenamiento
    
    def predecir_salon(self, asignacion_features, top_k=5):
        """
        Predice los top-k salones más probables para una asignación
        
        Args:
            asignacion_features: Features de la asignación
            top_k: Número de candidatos a retornar
        
        Returns:
            list: Lista de (salon, probabilidad) ordenada por probabilidad
        """
        # Predecir probabilidades
        probas = self.clasificador.predict_proba(asignacion_features.reshape(1, -1))[0]
        
        # Obtener top-k índices
        top_indices = np.argsort(probas)[::-1][:top_k]
        
        # Decodificar salones
        salones_candidatos = []
        for idx in top_indices:
            salon = self.encoders['salon_encoder'].inverse_transform([idx])[0]
            prob = probas[idx]
            salones_candidatos.append((salon, prob))
        
        return salones_candidatos
    
    def evaluar_calidad(self, asignacion_features):
        """
        Evalúa la calidad de una asignación
        
        Returns:
            float: Score de calidad (mayor = mejor)
        """
        return self.regressor_calidad.predict(asignacion_features.reshape(1, -1))[0]
    
    def validar_restricciones_hard(self, salon, asignacion, horario_actual):
        """
        Valida que un salón satisfaga todas las restricciones hard
        
        Args:
            salon: Salón candidato
            asignacion: Dict con info de la asignación
            horario_actual: DataFrame con asignaciones actuales
        
        Returns:
            bool: True si satisface todas las restricciones
        """
        # 1. Salón no debe estar en lista de inválidos
        if salon in self.salones_invalidos:
            return False
        
        # 2. No debe haber conflicto de horario (mismo salón, mismo día/hora)
        if len(horario_actual) > 0:
            conflictos = horario_actual[
                (horario_actual['Salon'] == salon) &
                (horario_actual['Dia'] == asignacion['dia']) &
                (horario_actual['Bloque_Horario'] == asignacion['bloque'])
            ]
            if len(conflictos) > 0:
                return False
        
        # 3. Validar tipo de salón (teoría vs laboratorio) - NUEVO
        es_lab = salon in self.laboratorios
        requiere_lab = asignacion.get('tipo_requerido', 'Teoría') == 'Laboratorio'
        if es_lab != requiere_lab:
            return False
        
        # 4. Validar preferencias prioritarias del profesor (RESTRICCIÓN DURA)
        profesor = asignacion.get('profesor')
        tipo_requerido = asignacion.get('tipo_requerido', 'Teoría')
        
        if profesor and tipo_requerido:
            pref_salon = obtener_preferencia_profesor(profesor, tipo_requerido, self.preferencias_profesores)
            es_prioritaria = es_preferencia_prioritaria(profesor, tipo_requerido, self.preferencias_profesores)
            
            # Si hay preferencia PRIORITARIA, SOLO ese salón es válido (sin excepciones)
            if es_prioritaria and pref_salon:
                if salon != pref_salon:
                    return False  # Rechazar cualquier otro salón
        
        # 5. Grupos de primer semestre (mismo salón para teoría)
        if asignacion.get('es_primer_semestre', False) and len(horario_actual) > 0:
            # Verificar si ya tiene asignación de teoría
            asigs_grupo = horario_actual[
                (horario_actual['Grupo'] == asignacion['grupo']) &
                (horario_actual['Tipo_Salon'] == 'Teoría')
            ]
            if len(asigs_grupo) > 0:
                salon_teoria_actual = asigs_grupo.iloc[0]['Salon']
                if salon != salon_teoria_actual and not salon.startswith('L'):
                    return False
        
        return True
    
    def optimizar(self, df_inicial):
        """
        Optimiza el horario completo usando el modelo entrenado
        
        Args:
            df_inicial: DataFrame con horario inicial
        
        Returns:
            DataFrame: Horario optimizado
        """
        self._log("\n" + "="*80)
        self._log("🚀 OPTIMIZANDO HORARIO CON MACHINE LEARNING")
        self._log("="*80 + "\n")
        
        # Copiar DataFrame
        df_optimizado = df_inicial.copy()
        horario_actual = pd.DataFrame()
        
        # Ordenar por prioridad (1er semestre primero, luego por hora)
        df_optimizado['prioridad'] = df_optimizado['Grupo'].str[0].astype(int)
        df_optimizado = df_optimizado.sort_values(['prioridad', 'Dia', 'Hora_Inicio'])
        
        total_asignaciones = len(df_optimizado)
        asignaciones_cambiadas = 0
        asignaciones_invalidas_eliminadas = 0
        
        self._log(f"📊 Total de asignaciones a procesar: {total_asignaciones}")
        self._log(f"🎯 Objetivo: Eliminar {df_inicial['Es_Invalido'].sum()} asignaciones inválidas\n")
        
        # Rastrear horas asignadas por materia
        horas_asignadas_optimizar = {}
        
        # Procesar cada asignación
        for idx, row in df_optimizado.iterrows():
            # Determinar tipo de hora requerido
            grupo = row['Grupo']
            materia = row['Materia']
            key = (grupo, materia)
            indice_hora = horas_asignadas_optimizar.get(key, 0)
            tipo_requerido = determinar_tipo_hora(materia, indice_hora, self.config_materias)
            horas_asignadas_optimizar[key] = indice_hora + 1
            
            # Extraer features de esta asignación
            asignacion_df = pd.DataFrame([row])
            X_asig = self.extraer_features(asignacion_df, incluir_target=False)
            
            # Predecir top-10 salones candidatos
            candidatos = self.predecir_salon(X_asig.iloc[0].values, top_k=10)
            
            # Preparar info de asignación para validación (con nuevos campos)
            asignacion_info = {
                'grupo': row['Grupo'],
                'dia': row['Dia'],
                'bloque': row['Bloque_Horario'],
                'profesor': row['Profesor'],
                'tipo_requerido': tipo_requerido,
                'es_primer_semestre': row['Grupo'][0] == '1'
            }
            
            # Filtrar candidatos válidos
            candidatos_validos = []
            for salon, prob in candidatos:
                if self.validar_restricciones_hard(salon, asignacion_info, horario_actual):
                    candidatos_validos.append((salon, prob))
            
            # Si no hay candidatos válidos, buscar cualquier salón válido
            if len(candidatos_validos) == 0:
                for salon in self.salones_validos:
                    if self.validar_restricciones_hard(salon, asignacion_info, horario_actual):
                        candidatos_validos.append((salon, 0.0))
                        break
            
            # Seleccionar mejor candidato
            if len(candidatos_validos) > 0:
                mejor_salon, prob = candidatos_validos[0]
                
                # Actualizar si es diferente
                if mejor_salon != row['Salon']:
                    salon_anterior = row['Salon']
                    df_optimizado.at[idx, 'Salon'] = mejor_salon
                    
                    # Actualizar tipo y piso
                    if mejor_salon.startswith('L'):
                        df_optimizado.at[idx, 'Tipo_Salon'] = 'Laboratorio'
                        if mejor_salon in ['LR', 'LSO', 'LIA', 'LCG1', 'LCG2']:
                            df_optimizado.at[idx, 'Piso'] = 'Primer Piso'
                        else:
                            df_optimizado.at[idx, 'Piso'] = 'Segundo Piso'
                    else:
                        df_optimizado.at[idx, 'Tipo_Salon'] = 'Teoría'
                        if mejor_salon in ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7']:
                            df_optimizado.at[idx, 'Piso'] = 'Planta Baja'
                        else:
                            df_optimizado.at[idx, 'Piso'] = 'Planta Alta'
                    
                    df_optimizado.at[idx, 'Es_Invalido'] = 0
                    
                    asignaciones_cambiadas += 1
                    if salon_anterior in self.salones_invalidos:
                        asignaciones_invalidas_eliminadas += 1
            
            # Agregar a horario actual
            horario_actual = pd.concat([horario_actual, df_optimizado.loc[[idx]]], ignore_index=True)
            
            # Progreso cada 100 asignaciones
            if (len(horario_actual) % 100 == 0):
                self._log(f"   Procesadas: {len(horario_actual)}/{total_asignaciones}")
        
        # Eliminar columna de prioridad
        df_optimizado = df_optimizado.drop('prioridad', axis=1)
        
        # Analizar movimientos
        self._log("\n📊 Analizando movimientos de profesores...")
        analizador_mov = AnalizadorMovimientos()
        comparativa_mov = analizador_mov.comparar_horarios(df_inicial, df_optimizado)
        
        # Resumen
        self._log("\n" + "="*80)
        self._log("✅ OPTIMIZACIÓN COMPLETADA")
        self._log("="*80)
        self._log(f"\n📊 Resultados:")
        self._log(f"   Asignaciones cambiadas: {asignaciones_cambiadas}/{total_asignaciones}")
        self._log(f"   Asignaciones inválidas eliminadas: {asignaciones_invalidas_eliminadas}")
        self._log(f"   Asignaciones inválidas restantes: {df_optimizado['Es_Invalido'].sum()}")
        self._log(f"   Tasa de cambio: {asignaciones_cambiadas/total_asignaciones*100:.1f}%")
        
        self._log(f"\n🚶 Movimientos de Profesores:")
        self._log(f"   Inicial:    {comparativa_mov['inicial']['total_movimientos']} movimientos")
        self._log(f"   Optimizado: {comparativa_mov['optimizado']['total_movimientos']} movimientos")
        self._log(f"   Mejora:     {comparativa_mov['mejora']['movimientos']:+d} ({comparativa_mov['mejora']['movimientos_pct']:+.1f}%)")
        
        self._log(f"\n🏢 Cambios de Piso:")
        self._log(f"   Inicial:    {comparativa_mov['inicial']['total_cambios_piso']} cambios")
        self._log(f"   Optimizado: {comparativa_mov['optimizado']['total_cambios_piso']} cambios")
        self._log(f"   Mejora:     {comparativa_mov['mejora']['cambios_piso']:+d} ({comparativa_mov['mejora']['cambios_piso_pct']:+.1f}%)")
        
        self._log(f"\n📏 Distancia Total:")
        self._log(f"   Inicial:    {comparativa_mov['inicial']['total_distancia']:.0f} unidades")
        self._log(f"   Optimizado: {comparativa_mov['optimizado']['total_distancia']:.0f} unidades")
        self._log(f"   Mejora:     {comparativa_mov['mejora']['distancia']:+.0f} ({comparativa_mov['mejora']['distancia_pct']:+.1f}%)")
        self._log("\n")
        
        # Guardar métricas de movimientos
        metricas_mov_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/comparativas/02_inicial_vs_ml/metricas_movimientos.csv"
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
        self._log(f"💾 Métricas de movimientos guardadas: {metricas_mov_path}")
        
        return df_optimizado

def main():
    """Función principal de prueba"""
    print("🤖 Optimizador ML - Sistema de Salones ISC")
    print("="*80)
    print("Método: Machine Learning Independiente")
    print("Entrena solo con horario inicial, sin usar optimización del profesor")
    print("="*80 + "\n")
    
    # Cargar datos
    csv_inicial = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/01_Horario_Inicial.csv"
    df_inicial = pd.read_csv(csv_inicial)
    
    # Crear optimizador
    optimizador = OptimizadorML(verbose=True)
    
    # Entrenar (solo con horario inicial)
    metricas = optimizador.entrenar(df_inicial)
    
    # Optimizar
    df_resultado = optimizador.optimizar(df_inicial)
    
    # Guardar resultado
    output_path = "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC/datos_estructurados/03_Horario_Optimizado_ML.csv"
    df_resultado.to_csv(output_path, index=False)
    print(f"\n💾 Resultado guardado: {output_path}\n")
    
    print("="*80)
    print("✅ PROCESO COMPLETADO")
    print("="*80)
    print("\n📊 Próximo paso: Generar comparativa")
    print("   - Inicial vs ML")
    print("   - Inicial vs Profesor")
    print("   - Inicial vs ILP (pendiente)")
    print("   - Inicial vs Genético (pendiente)")
    print("   - Comparativa final de todos\n")

if __name__ == "__main__":
    main()
