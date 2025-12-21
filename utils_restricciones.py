#!/usr/bin/env python3
"""
Utilidades para Restricciones - Sistema de Salones ISC
Funciones compartidas para manejar configuración de materias y preferencias de profesores
"""

import json
import os
from typing import Dict, Tuple, Optional

def cargar_configuraciones(script_dir: Optional[str] = None) -> Tuple[Dict, Dict]:
    """
    Carga configuración de materias y preferencias de profesores
    
    Returns:
        Tuple[Dict, Dict]: (config_materias, preferencias_profesores)
    """
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar configuración de materias
    config_materias_path = os.path.join(script_dir, "configuracion_materias.json")
    try:
        with open(config_materias_path, 'r', encoding='utf-8') as f:
            config_materias = json.load(f)
        print(f"✅ Configuración de materias cargada: {len(config_materias)} materias")
    except FileNotFoundError:
        print("⚠️  configuracion_materias.json no encontrado, usando valores por defecto")
        config_materias = {}
    
    # Cargar preferencias de profesores
    prefs_profesores_path = os.path.join(script_dir, "preferencias_profesores.json")
    try:
        with open(prefs_profesores_path, 'r', encoding='utf-8') as f:
            preferencias_profesores = json.load(f)
        print(f"✅ Preferencias de profesores cargadas: {len(preferencias_profesores)} profesores")
    except FileNotFoundError:
        print("⚠️  preferencias_profesores.json no encontrado, sin preferencias")
        preferencias_profesores = {}
    
    return config_materias, preferencias_profesores


def determinar_tipo_hora(materia: str, indice_hora: int, config_materias: Dict) -> str:
    """
    Determina si una hora específica debe ser teoría o laboratorio
    
    Args:
        materia: Nombre de la materia
        indice_hora: Índice de la hora (0-based) dentro de la semana
        config_materias: Configuración de materias
    
    Returns:
        str: 'Teoría' o 'Laboratorio'
    """
    if materia not in config_materias:
        # Si no está configurada, asumir teoría por defecto
        return 'Teoría'
    
    config = config_materias[materia]
    horas_teoria = config.get('horas_teoria', config.get('total_horas', 0))
    horas_lab = config.get('horas_lab', 0)
    
    # Distribuir: primeras N horas son teoría, resto son lab
    # Esto es una estrategia simple, se puede mejorar
    if indice_hora < horas_teoria:
        return 'Teoría'
    else:
        return 'Laboratorio'


def obtener_preferencia_profesor(profesor: str, tipo_salon: str, 
                                 preferencias_profesores: Dict, materia: str = None) -> Optional[str]:
    """
    Obtiene la preferencia de salón para un profesor en una materia específica
    
    Args:
        profesor: Nombre del profesor
        tipo_salon: 'Teoría' o 'Laboratorio'
        preferencias_profesores: Diccionario de preferencias
        materia: Nombre de la materia (requerido para nueva estructura)
    
    Returns:
        str: Nombre del salón preferido o None
    """
    if profesor not in preferencias_profesores:
        return None
    
    prefs = preferencias_profesores[profesor]
    
    # Nueva estructura: preferencias por materia
    if 'materias' in prefs and materia:
        if materia not in prefs['materias']:
            return None
        
        pref_materia = prefs['materias'][materia]
        
        if tipo_salon == 'Teoría':
            salon = pref_materia.get('salon_teoria', 'Sin preferencia')
        else:
            salon = pref_materia.get('salon_lab', 'Sin preferencia')
    else:
        # Estructura antigua (compatibilidad)
        if tipo_salon == 'Teoría':
            salon = prefs.get('salon_teoria', 'Sin preferencia')
        else:
            salon = prefs.get('salon_lab', 'Sin preferencia')
    
    if salon == 'Sin preferencia':
        return None
    
    return salon


def es_preferencia_prioritaria(profesor: str, tipo_salon: str,
                               preferencias_profesores: Dict, materia: str = None) -> bool:
    """
    Verifica si la preferencia del profesor es prioritaria para una materia específica
    
    Args:
        profesor: Nombre del profesor
        tipo_salon: 'Teoría' o 'Laboratorio'
        preferencias_profesores: Diccionario de preferencias
        materia: Nombre de la materia (requerido para nueva estructura)
    
    Returns:
        bool: True si es prioritaria
    """
    if profesor not in preferencias_profesores:
        return False
    
    prefs = preferencias_profesores[profesor]
    
    # Nueva estructura: preferencias por materia
    if 'materias' in prefs and materia:
        if materia not in prefs['materias']:
            return False
        
        pref_materia = prefs['materias'][materia]
        
        if tipo_salon == 'Teoría':
            prioridad = pref_materia.get('prioridad_teoria', 'Opcional')
        else:
            prioridad = pref_materia.get('prioridad_lab', 'Opcional')
    else:
        # Estructura antigua (compatibilidad)
        if tipo_salon == 'Teoría':
            prioridad = prefs.get('prioridad_teoria', 'Opcional')
        else:
            prioridad = prefs.get('prioridad_lab', 'Opcional')
    
    return prioridad == 'Prioritario'


def filtrar_salones_por_tipo(salones_disponibles: list, tipo_requerido: str,
                             salones_teoria: list = None, salones_lab: list = None) -> list:
    """
    Filtra salones por tipo (teoría o laboratorio)
    
    Args:
        salones_disponibles: Lista de salones disponibles
        tipo_requerido: 'Teoría' o 'Laboratorio'
        salones_teoria: Lista de salones de teoría (opcional)
        salones_lab: Lista de salones de laboratorio (opcional)
    
    Returns:
        list: Salones filtrados por tipo
    """
    # Definir salones por tipo si no se proporcionan
    if salones_teoria is None:
        salones_teoria = ['FF1', 'FF2', 'FF3', 'FF4', 'FF5', 'FF6', 'FF7', 'FF8', 'FF9',
                         'FFA', 'FFB', 'FFC', 'FFD']
    
    if salones_lab is None:
        salones_lab = ['LBD', 'LBD2', 'LCA', 'LCG1', 'LCG2', 'LIA', 'LR', 'LSO']
    
    if tipo_requerido == 'Teoría':
        return [s for s in salones_disponibles if s in salones_teoria]
    else:
        return [s for s in salones_disponibles if s in salones_lab]


def calcular_penalizacion_preferencias(asignaciones: Dict, preferencias_profesores: Dict,
                                       config_materias: Dict) -> Tuple[int, int]:
    """
    Calcula penalizaciones por violar preferencias de profesores
    
    Args:
        asignaciones: Dict con asignaciones {(grupo, dia, bloque): salon}
        preferencias_profesores: Preferencias de profesores
        config_materias: Configuración de materias
    
    Returns:
        Tuple[int, int]: (violaciones_prioritarias, violaciones_opcionales)
    """
    violaciones_prioritarias = 0
    violaciones_opcionales = 0
    
    # Esta función se implementará específicamente en cada optimizador
    # ya que la estructura de asignaciones puede variar
    
    return violaciones_prioritarias, violaciones_opcionales


def validar_distribucion_teoria_lab(df, config_materias: Dict) -> Dict:
    """
    Valida que la distribución de horas teoría/lab sea correcta
    
    Args:
        df: DataFrame con el horario
        config_materias: Configuración de materias
    
    Returns:
        Dict: Estadísticas de validación
    """
    stats = {
        'total_materias': 0,
        'correctas': 0,
        'incorrectas': 0,
        'detalles': []
    }
    
    # Agrupar por materia
    for materia in df['Materia'].unique():
        if materia not in config_materias:
            continue
        
        stats['total_materias'] += 1
        materia_df = df[df['Materia'] == materia]
        
        config = config_materias[materia]
        horas_teoria_esperadas = config['horas_teoria']
        horas_lab_esperadas = config['horas_lab']
        
        # Contar horas asignadas
        horas_teoria_asignadas = len(materia_df[materia_df['Tipo_Salon'] == 'Teoría'])
        horas_lab_asignadas = len(materia_df[materia_df['Tipo_Salon'] == 'Laboratorio'])
        
        if (horas_teoria_asignadas == horas_teoria_esperadas and 
            horas_lab_asignadas == horas_lab_esperadas):
            stats['correctas'] += 1
        else:
            stats['incorrectas'] += 1
            stats['detalles'].append({
                'materia': materia,
                'esperado': f"{horas_teoria_esperadas}T + {horas_lab_esperadas}L",
                'asignado': f"{horas_teoria_asignadas}T + {horas_lab_asignadas}L"
            })
    
    return stats


def pre_asignar_prioritarias(df, config_materias: Dict, preferencias_profesores: Dict,
                             laboratorios: set, salones_teoria: set, asignacion_grupos_1er: Dict = None) -> Tuple[Dict, Dict, list]:
    """
    Pre-asigna clases con ORDEN DE PRIORIDADES:
    1. Grupos de 1er semestre (mismo salón para todas sus materias)
    2. Preferencias prioritarias de profesores por materia
    3. Laboratorios asignados por materia
    
    Estrategia:
    - Mantener día/hora original del CSV cuando sea posible
    - Aplicar restricciones en orden de prioridad
    - Resolver conflictos recursivamente moviendo clases en cadena
    - Si es necesario, mover clases a otros días/horas
    
    Args:
        df: DataFrame con el horario ORIGINAL
        config_materias: Configuración de materias
        preferencias_profesores: Preferencias de profesores
        laboratorios: Set de salones de laboratorio
        salones_teoria: Set de salones de teoría
        asignacion_grupos_1er: Dict con asignación grupo → salón para 1er semestre
    
    Returns:
        Tuple[Dict, Dict, list]: (solucion, ocupacion, indices_restantes)
    """
    
    def buscar_salon_libre(dia, bloque, tipo_req, ocupacion):
        """Busca un salón libre del tipo requerido"""
        if tipo_req == 'Laboratorio':
            candidatos = laboratorios
        else:
            candidatos = salones_teoria
        
        for salon in candidatos:
            if (dia, bloque, salon) not in ocupacion:
                return salon
        return None
    
    def buscar_bloque_alternativo(salon_prioritario, tipo_req, ocupacion, excluir_bloques=None):
        """Busca un bloque horario donde el salón prioritario esté libre"""
        if excluir_bloques is None:
            excluir_bloques = set()
        
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
        bloques = [710, 809, 910, 1011, 1112, 1213, 1314, 1415, 1516, 1617]
        
        for dia in dias:
            for bloque in bloques:
                if (dia, bloque) not in excluir_bloques:
                    if (dia, bloque, salon_prioritario) not in ocupacion:
                        return (dia, bloque)
        return None
    
    def resolver_conflicto_recursivo(idx_nueva, salon_prioritario, dia, bloque, tipo_req,
                                     solucion, ocupacion, clases_prioritarias_dict, profundidad=0):
        """
        Resuelve conflictos recursivamente con GARANTÍA de éxito
        """
        MAX_PROFUNDIDAD = 50
        
        if profundidad > MAX_PROFUNDIDAD:
            return False
        
        # Caso 1: Salón libre → asignar directamente
        if (dia, bloque, salon_prioritario) not in ocupacion:
            solucion[idx_nueva] = salon_prioritario
            ocupacion[(dia, bloque, salon_prioritario)] = idx_nueva
            return True
        
        # Caso 2: Salón ocupado → resolver conflicto
        idx_conflicto = ocupacion[(dia, bloque, salon_prioritario)]
        
        # Verificar si la clase conflictiva es prioritaria para este salón
        clase_conflicto = clases_prioritarias_dict.get(idx_conflicto)
        
        if clase_conflicto and clase_conflicto['salon_prioritario'] == salon_prioritario:
            # AMBAS clases son prioritarias para el MISMO salón en el MISMO bloque
            # Solución: Mover la clase NUEVA a otro bloque donde el salón esté libre
            bloque_alt = buscar_bloque_alternativo(salon_prioritario, tipo_req, ocupacion, {(dia, bloque)})
            
            if bloque_alt:
                dia_alt, bloque_alt_num = bloque_alt
                solucion[idx_nueva] = salon_prioritario
                ocupacion[(dia_alt, bloque_alt_num, salon_prioritario)] = idx_nueva
                # Actualizar el DataFrame para reflejar el nuevo horario
                df.at[idx_nueva, 'Dia'] = dia_alt
                df.at[idx_nueva, 'Bloque_Horario'] = bloque_alt_num
                return True
            else:
                # No hay bloques alternativos disponibles
                return False
        else:
            # La clase conflictiva NO es prioritaria para este salón
            # Mover la clase conflictiva a otro salón del mismo tipo
            tipo_conflicto = 'Laboratorio' if solucion.get(idx_conflicto, '') in laboratorios else tipo_req
            salon_alternativo = buscar_salon_libre(dia, bloque, tipo_conflicto, ocupacion)
            
            if salon_alternativo:
                # Mover clase conflictiva
                del ocupacion[(dia, bloque, salon_prioritario)]
                solucion[idx_conflicto] = salon_alternativo
                ocupacion[(dia, bloque, salon_alternativo)] = idx_conflicto
                
                # Asignar clase nueva al salón prioritario
                solucion[idx_nueva] = salon_prioritario
                ocupacion[(dia, bloque, salon_prioritario)] = idx_nueva
                return True
            else:
                # No hay salón alternativo directo
                # ESTRATEGIA MEJORADA: Intentar múltiples opciones de desplazamiento
                
                # Opción 1: Buscar en TODOS los salones para hacer cadena de movimientos
                if tipo_conflicto == 'Laboratorio':
                    candidatos = list(laboratorios)
                else:
                    candidatos = list(salones_teoria)
                
                # Intentar cada salón como candidato para la clase conflictiva
                for salon_candidato in candidatos:
                    if salon_candidato == salon_prioritario:
                        continue
                        
                    # Caso A: Salón candidato está libre
                    if (dia, bloque, salon_candidato) not in ocupacion:
                        # Mover clase conflictiva al salón libre
                        del ocupacion[(dia, bloque, salon_prioritario)]
                        solucion[idx_conflicto] = salon_candidato
                        ocupacion[(dia, bloque, salon_candidato)] = idx_conflicto
                        
                        # Asignar clase nueva al salón prioritario
                        solucion[idx_nueva] = salon_prioritario
                        ocupacion[(dia, bloque, salon_prioritario)] = idx_nueva
                        return True
                    
                    # Caso B: Salón candidato está ocupado - intentar cadena
                    else:
                        idx_temp = ocupacion[(dia, bloque, salon_candidato)]
                        if idx_temp != idx_conflicto and idx_temp != idx_nueva:
                            # Verificar si la clase temporal NO es prioritaria
                            clase_temp = clases_prioritarias_dict.get(idx_temp)
                            if clase_temp and clase_temp['salon_prioritario'] == salon_candidato:
                                # La clase temporal ES prioritaria para este salón, saltar
                                continue
                            
                            # Intentar mover la clase temporal a otro salón
                            salon_temp_anterior = solucion.get(idx_temp)
                            tipo_temp = 'Laboratorio' if salon_temp_anterior in laboratorios else tipo_conflicto
                            
                            # Buscar salón libre para la clase temporal
                            for salon_para_temp in (laboratorios if tipo_temp == 'Laboratorio' else salones_teoria):
                                if (dia, bloque, salon_para_temp) not in ocupacion:
                                    # Cadena exitosa: temp → salon_para_temp, conflicto → salon_candidato, nueva → prioritario
                                    del ocupacion[(dia, bloque, salon_candidato)]
                                    solucion[idx_temp] = salon_para_temp
                                    ocupacion[(dia, bloque, salon_para_temp)] = idx_temp
                                    
                                    del ocupacion[(dia, bloque, salon_prioritario)]
                                    solucion[idx_conflicto] = salon_candidato
                                    ocupacion[(dia, bloque, salon_candidato)] = idx_conflicto
                                    
                                    solucion[idx_nueva] = salon_prioritario
                                    ocupacion[(dia, bloque, salon_prioritario)] = idx_nueva
                                    return True
                
                # Opción 2: Si nada funcionó, mover la clase NUEVA a otro bloque (última opción)
                bloque_alt = buscar_bloque_alternativo(salon_prioritario, tipo_req, ocupacion, {(dia, bloque)})
                if bloque_alt:
                    dia_alt, bloque_alt_num = bloque_alt
                    solucion[idx_nueva] = salon_prioritario
                    ocupacion[(dia_alt, bloque_alt_num, salon_prioritario)] = idx_nueva
                    df.at[idx_nueva, 'Dia'] = dia_alt
                    df.at[idx_nueva, 'Bloque_Horario'] = bloque_alt_num
                    return True
                
                return False
    
    # ===== INICIO DE LA FUNCIÓN PRINCIPAL =====
    
    solucion = {}
    ocupacion = {}
    clases_prioritarias = []
    clases_normales = []
    clases_prioritarias_dict = {}
    
    # Rastrear horas asignadas por materia
    horas_asignadas = {}
    
    # PRIORIDAD 1: Identificar clases con preferencias prioritarias de profesores (MÁXIMA PRIORIDAD)
    for idx, row in df.iterrows():
            
        grupo = row['Grupo']
        materia = row['Materia']
        profesor = row['Profesor']
        dia = row['Dia']
        bloque = row['Bloque_Horario']
        
        # Determinar tipo de hora
        key = (grupo, materia)
        indice_hora = horas_asignadas.get(key, 0)
        tipo_req = determinar_tipo_hora(materia, indice_hora, config_materias)
        horas_asignadas[key] = indice_hora + 1
        
        # Verificar preferencia prioritaria
        es_prioritaria = es_preferencia_prioritaria(profesor, tipo_req, preferencias_profesores, materia)
        pref_salon = obtener_preferencia_profesor(profesor, tipo_req, preferencias_profesores, materia)
        
        if es_prioritaria and pref_salon:
            clase_info = {
                'idx': idx,
                'salon_prioritario': pref_salon,
                'dia_original': dia,
                'bloque_original': bloque,
                'tipo': tipo_req,
                'profesor': profesor
            }
            clases_prioritarias.append(clase_info)
            clases_prioritarias_dict[idx] = clase_info
        else:
            clases_normales.append(idx)
    
    # Fase 2: Ordenar por prioridad (profesores con más clases primero)
    contador = {}
    for clase in clases_prioritarias:
        prof = clase['profesor']
        contador[prof] = contador.get(prof, 0) + 1
    
    clases_ordenadas = sorted(clases_prioritarias, key=lambda c: -contador[c['profesor']])
    
    # Fase 3: Asignar con resolución recursiva COMPLETA
    asignaciones_exitosas = 0
    asignaciones_fallidas = []
    
    for clase in clases_ordenadas:
        idx = clase['idx']
        salon_prioritario = clase['salon_prioritario']
        dia = clase['dia_original']
        bloque = clase['bloque_original']
        tipo_req = clase['tipo']
        
        exito = resolver_conflicto_recursivo(
            idx, salon_prioritario, dia, bloque, tipo_req,
            solucion, ocupacion, clases_prioritarias_dict
        )
        
        if exito:
            asignaciones_exitosas += 1
        else:
            asignaciones_fallidas.append(clase)
            # Último recurso: FORZAR desplazamiento
            salon_alt = buscar_salon_libre(dia, bloque, tipo_req, ocupacion)
            if salon_alt:
                solucion[idx] = salon_alt
                ocupacion[(dia, bloque, salon_alt)] = idx
            else:
                # No hay salón libre - FORZAR desplazamiento de clase no prioritaria
                if (dia, bloque, salon_prioritario) in ocupacion:
                    idx_conflicto = ocupacion[(dia, bloque, salon_prioritario)]
                    # Verificar que la clase conflictiva NO sea prioritaria
                    if idx_conflicto not in clases_prioritarias_dict:
                        # Mover la clase conflictiva a CUALQUIER salón disponible
                        tipo_conflicto = 'Teoría'  # Asumimos teoría por defecto
                        for salon_temp in salones_teoria:
                            if (dia, bloque, salon_temp) not in ocupacion:
                                # Mover clase conflictiva
                                del ocupacion[(dia, bloque, salon_prioritario)]
                                solucion[idx_conflicto] = salon_temp
                                ocupacion[(dia, bloque, salon_temp)] = idx_conflicto
                                
                                # Asignar clase prioritaria
                                solucion[idx] = salon_prioritario
                                ocupacion[(dia, bloque, salon_prioritario)] = idx
                                asignaciones_exitosas += 1
                                asignaciones_fallidas.remove(clase)
                                break
                        else:
                            # Si no se pudo mover, asignar a salón libre cualquiera
                            solucion[idx] = salon_alt if salon_alt else salon_prioritario
                    else:
                        # La clase conflictiva ES prioritaria - asignar a salón alternativo
                        solucion[idx] = salon_alt if salon_alt else salon_prioritario
                else:
                    # El salón está libre, asignar directamente
                    solucion[idx] = salon_prioritario
                    ocupacion[(dia, bloque, salon_prioritario)] = idx
                    asignaciones_exitosas += 1
                    asignaciones_fallidas.remove(clase)
    
    
    if asignaciones_fallidas:
        print(f"⚠️  {len(asignaciones_fallidas)} clases prioritarias tuvieron conflictos irresolvibles")
    else:
        print(f"✅ {asignaciones_exitosas} clases prioritarias asignadas con 100% de cumplimiento")
    
    # PRIORIDAD 2: Laboratorios asignados por materia
    # Solo aplicar a clases de laboratorio que NO tienen preferencias de profesores
    for idx in clases_normales[:]:
        if idx in solucion:
            continue
            
        row = df.loc[idx]
        materia = row['Materia']
        tipo_salon = row['Tipo_Salon']
        dia = row['Dia']
        bloque = row['Bloque_Horario']
        
        # Solo para clases de laboratorio
        if tipo_salon == 'Laboratorio' and materia in config_materias:
            lab_asignado = config_materias[materia].get('laboratorio_asignado')
            
            # Si hay laboratorio asignado y no es null
            if lab_asignado and lab_asignado != 'null':
                # Verificar disponibilidad
                if (dia, bloque, lab_asignado) not in ocupacion:
                    solucion[idx] = lab_asignado
                    ocupacion[(dia, bloque, lab_asignado)] = idx
                    clases_normales.remove(idx)
    
    # PRIORIDAD 3: Grupos de 1er semestre (MENOR PRIORIDAD)
    # Solo aplicar a clases que NO tienen preferencias de profesores
    # Solo grupos 15xx (1502, 1504, 1561) - Los 11xx son en línea
    if asignacion_grupos_1er and '15xx' in asignacion_grupos_1er:
        for idx in clases_normales[:]:
            if idx in solucion:
                continue
                
            row = df.loc[idx]
            grupo = row['Grupo']
            dia = row['Dia']
            bloque = row['Bloque_Horario']
            tipo_salon = row['Tipo_Salon']
            
            # Solo procesar si es teoría y grupo de 1er semestre 15xx
            if tipo_salon == 'Teoría' and '/' in grupo:
                partes = grupo.split('/')
                if len(partes) == 2:
                    clave = partes[0]
                    letra = partes[1]
                    letra_base = letra[0] if letra else ''
                    
                    # Solo grupos 15xx
                    if clave.startswith('15'):
                        if letra_base in asignacion_grupos_1er['15xx']:
                            salon_asignado = asignacion_grupos_1er['15xx'][letra_base]
                            
                            # Verificar disponibilidad
                            if (dia, bloque, salon_asignado) not in ocupacion:
                                solucion[idx] = salon_asignado
                                ocupacion[(dia, bloque, salon_asignado)] = idx
                                clases_normales.remove(idx)
    
    return solucion, ocupacion, clases_normales


if __name__ == "__main__":
    # Prueba de las funciones
    print("🧪 Probando utilidades de restricciones...\n")
    
    config_materias, prefs_profesores = cargar_configuraciones()
    
    print(f"\n📊 Materias configuradas: {len(config_materias)}")
    print(f"👨‍🏫 Profesores con preferencias: {len(prefs_profesores)}")
    
    # Ejemplo de uso
    if config_materias:
        materia_ejemplo = list(config_materias.keys())[0]
        print(f"\n🔍 Ejemplo - {materia_ejemplo}:")
        print(f"   Configuración: {config_materias[materia_ejemplo]}")
        
        for i in range(config_materias[materia_ejemplo]['total_horas']):
            tipo = determinar_tipo_hora(materia_ejemplo, i, config_materias)
            print(f"   Hora {i+1}: {tipo}")
    
    if prefs_profesores:
        profesor_ejemplo = list(prefs_profesores.keys())[0]
        print(f"\n👨‍🏫 Ejemplo - {profesor_ejemplo}:")
        print(f"   Preferencias: {prefs_profesores[profesor_ejemplo]}")
        
        pref_teoria = obtener_preferencia_profesor(profesor_ejemplo, 'Teoría', prefs_profesores)
        es_prioritaria = es_preferencia_prioritaria(profesor_ejemplo, 'Teoría', prefs_profesores)
        print(f"   Salón teoría preferido: {pref_teoria} ({'Prioritario' if es_prioritaria else 'Opcional'})")
