# Preguntas Frecuentes (FAQ)

## General

### ¿Qué es el Sistema de Asignación de Salones ISC?

Es un sistema de optimización que asigna automáticamente salones a clases del programa de Ingeniería en Sistemas Computacionales del Instituto Tecnológico de Ciudad Madero, minimizando movimientos de profesores y garantizando cumplimiento de preferencias prioritarias.

### ¿Por qué necesitamos este sistema?

La asignación manual de 680+ clases a 21 salones es:
- **Tiempo intensiva**: Horas o días de trabajo manual
- **Propensa a errores**: Conflictos temporales, preferencias olvidadas
- **Subóptima**: No considera todas las optimizaciones posibles
- **Difícil de actualizar**: Cambios requieren rehacer todo

### ¿Qué problemas resuelve?

1. **Garantiza 100% cumplimiento** de preferencias prioritarias de profesores
2. **Minimiza movimientos** de profesores entre salones
3. **Reduce cambios de piso** (menos fatiga)
4. **Optimiza distancias** recorridas
5. **Genera reportes** automáticos y comparativos

## Instalación y Configuración

### ¿Qué necesito para instalar el sistema?

**Requisitos:**
- Python 3.8 o superior
- pip (gestor de paquetes)
- ~100 MB de espacio en disco
- Sistema operativo: Windows, macOS, o Linux

**Instalación:**
```bash
pip install pandas openpyxl matplotlib seaborn scikit-learn
```

### ¿Cómo configuro las preferencias de profesores?

1. Ejecutar `python3 configurador_materias.py`
2. Ir a pestaña "Preferencias de Profesores"
3. Seleccionar profesor y materia
4. Configurar:
   - Salón preferido (Teoría/Laboratorio)
   - Prioridad (Prioritario/Normal/Sin preferencia)
5. Guardar configuración

### ¿Dónde se guardan las configuraciones?

- `preferencias_profesores.json`: Preferencias de profesores
- `configuracion_materias.json`: Configuración de materias
- `asignacion_grupos_1er_semestre.json`: Grupos de primer semestre

## Uso del Sistema

### ¿Cómo ejecuto el sistema completo?

**Opción 1 (Recomendada):**
```bash
python3 ejecutar_todos.py
```

**Opción 2 (Manual):**
```bash
python3 pre_asignar_p1.py
python3 optimizador_greedy.py
python3 corregir_prioridades.py datos_estructurados/04_Horario_Optimizado_Greedy.csv
# ... etc
```

### ¿Cuánto tiempo tarda?

| Componente | Tiempo |
|------------|--------|
| Pre-asignación | ~0.3s |
| Greedy | ~30s |
| ML | ~16s |
| Genético | ~74s |
| Corrección | ~0.2s cada uno |
| Comparativas | ~5s |
| **Total** | **~2-3 minutos** |

### ¿Qué optimizador debo usar?

| Optimizador | Cuándo usar |
|-------------|-------------|
| **Greedy** | Balance ideal velocidad/calidad, uso general |
| **ML** | Máxima velocidad, buena calidad |
| **Genético** | Mejor exploración, tiempo no crítico |
| **Todos** | Comparar y elegir mejor resultado |

## Prioridades

### ¿Qué significa PRIORIDAD 1?

**PRIORIDAD 1** son preferencias de salón de profesores marcadas como "Prioritario". El sistema **garantiza 100%** de cumplimiento.

**Ejemplo:**
- PROFESOR 3 quiere FFA para Lenguajes y Autómatas I (Teoría)
- Prioridad: Prioritario
- **Garantía**: Todas sus clases estarán en FFA

### ¿Qué pasa si dos profesores quieren el mismo salón al mismo tiempo?

**Durante configuración:**
- El sistema detecta el conflicto
- Solicita resolver manualmente
- Opciones: Cambiar horario o salón de uno

**Durante optimización:**
- Pre-asignación resuelve automáticamente
- Desplaza clases no-prioritarias
- Si ambas son P1: Requiere intervención manual

### ¿Qué son PRIORIDAD 2 y 3?

**PRIORIDAD 2**: Consistencia de grupos
- Objetivo: Mantener grupos en mismo salón
- **No garantizado**, se optimiza cuando es posible

**PRIORIDAD 3**: Grupos de primer semestre
- Objetivo: Asignar grupos 15xx a salones específicos
- **No garantizado**, mejor esfuerzo

**Estado actual**: P2 y P3 en desarrollo (v2.1.0)

## Resultados

### ¿Dónde encuentro los resultados?

**Horarios optimizados:**
- `datos_estructurados/04_Horario_Optimizado_Greedy.csv`
- `datos_estructurados/05_Horario_Optimizado_ML.csv`
- `datos_estructurados/06_Horario_Optimizado_Genetico.csv`

**Excels formateados:**
- `comparativas/04_inicial_vs_greedy/Horario_Optimizado_Greedy.xlsx`
- `comparativas/02_inicial_vs_ml/Horario_Optimizado_ML.xlsx`
- `comparativas/03_inicial_vs_genetico/Horario_Optimizado_Genetico.xlsx`

**Excel comparativo:**
- `comparativas/final/Comparativa_Todos_Optimizadores.xlsx`

**Gráficos:**
- `comparativas/final/graficos/`

### ¿Cómo interpreto los resultados?

**Métricas clave:**

1. **Cumplimiento P1**: Debe ser 100%
2. **Movimientos**: Menor es mejor (ideal < 320)
3. **Cambios piso**: Menor es mejor (ideal < 210)
4. **Distancia**: Menor es mejor (ideal < 2000)

**Comparación:**
- Ver `Comparativa_Todos_Optimizadores.xlsx`
- Comparar grupo por grupo
- Elegir optimizador con mejores métricas globales

### ¿Qué hago si PRIORIDAD 1 no está al 100%?

**Esto NO debería pasar**, pero si ocurre:

1. Ejecutar corrección:
   ```bash
   python3 corregir_prioridades.py datos_estructurados/XX_Horario.csv
   ```

2. Si persiste:
   - Verificar `preferencias_profesores.json`
   - Revisar conflictos irresolvables
   - Contactar soporte técnico

## Problemas Comunes

### Error: "No se encontró el archivo"

**Causa**: Archivo de entrada no existe

**Solución**:
```bash
# Verificar archivos
ls datos_estructurados/01_Horario_Inicial.csv

# Si no existe, generarlo o copiarlo
```

### Error: "PRIORIDAD 1 no al 100%"

**Causa**: Conflictos en preferencias o salones insuficientes

**Solución**:
1. Ejecutar `corregir_prioridades.py`
2. Verificar preferencias
3. Revisar disponibilidad de salones

### El optimizador es muy lento

**Causa**: Parámetros muy altos (especialmente Genético)

**Solución**:
Editar parámetros en el optimizador:
```python
# optimizador_genetico.py
optimizador = OptimizadorGenetico(
    tam_poblacion=50,      # Reducir de 150
    num_generaciones=200,  # Reducir de 500
)
```

### Los resultados varían entre ejecuciones

**Causa**: Aleatoriedad en algoritmos (especialmente Genético)

**Solución**:
Fijar semilla aleatoria:
```python
import random
random.seed(42)
```

## Personalización

### ¿Puedo cambiar los pesos de optimización?

Sí, editar en cada optimizador:

```python
# optimizador_greedy.py
self.pesos = {
    'movimientos': 10,      # Aumentar para priorizar
    'cambios_piso': 5,
    'distancia': 3,
}
```

### ¿Puedo agregar nuevas restricciones?

Sí:

1. Definir en `utils_restricciones.py`:
   ```python
   def verificar_nueva_restriccion(clase, salon):
       # Lógica
   ```

2. Integrar en función objetivo
3. Actualizar documentación

### ¿Puedo usar el sistema para otro campus?

Sí, pero requiere:

1. Actualizar lista de salones
2. Configurar nuevas materias
3. Definir preferencias de profesores
4. Ajustar parámetros si es necesario

## Desarrollo y Contribución

### ¿Cómo contribuyo al proyecto?

1. Fork el repositorio
2. Crear branch para tu feature
3. Implementar con tests
4. Documentar cambios
5. Pull request para revisión

### ¿Dónde reporto bugs?

- GitHub Issues (preferido)
- Email a equipo de desarrollo
- Slack interno (si aplica)

### ¿Hay tests automatizados?

**Estado actual**: Tests básicos de validación

**Roadmap**: Suite completa de tests (v2.1.0)

## Aplicación Web

### ¿Hay una aplicación web?

**Estado**: BETA - En desarrollo

**Funcionalidades actuales**:
- Visualización básica de horarios
- Filtros simples
- Exportación a PDF básica

**Limitaciones**:
- Sin autenticación
- No optimizado
- No lista para producción

Ver `docs/WEB_APP_BETA.md` para detalles.

### ¿Cuándo estará lista la app web?

**Estimado**: v2.1.0 (Q1 2026)

**Prioridades**:
1. Seguridad (autenticación, autorización)
2. Funcionalidad core (integración con optimizadores)
3. Rendimiento
4. UX/UI profesional

## Soporte

### ¿Dónde encuentro más documentación?

- `README.md`: Descripción general
- `docs/GUIA_USO.md`: Guía completa de usuario
- `docs/00_CONTEXTO_PROBLEMA.md`: Contexto matemático
- `docs/02-04_ALGORITMO_*.md`: Detalles de algoritmos
- `docs/07_ARQUITECTURA_CODIGO.md`: Arquitectura

### ¿A quién contacto para soporte?

- **Email**: sistemas@cdmadero.tecnm.mx
- **GitHub**: [@lic-ing-jesusolvera](https://github.com/lic-ing-jesusolvera)
- **Issues**: https://github.com/lic-ing-jesusolvera/Sistema-Salones-ISC/issues
- **Interno**: Coordinación académica ISC - ITCM

### ¿El sistema tiene licencia?

**Licencia**: Uso académico - Tecnológico Nacional de México

**Restricciones**:
- Uso educativo e institucional
- No comercial sin autorización
- Atribución requerida

## Rendimiento

### ¿Cuántas clases puede manejar?

**Probado con**: 680 clases, 21 salones

**Escalabilidad**:
- Hasta ~1000 clases: Sin problemas
- 1000-2000 clases: Posible, tiempos mayores
- >2000 clases: Requiere optimización adicional

### ¿Funciona en tiempo real?

**No**, es un sistema de optimización offline.

**Tiempo típico**: 2-3 minutos para generar horarios completos

**Uso recomendado**: Ejecutar al inicio de semestre o cuando hay cambios

## Futuro

### ¿Qué viene en próximas versiones?

**v2.1.0** (Próximo):
- PRIORIDAD 2 y 3 implementadas
- App web mejorada
- API REST
- Más formatos de exportación

**v3.0.0** (Futuro):
- Soporte multi-campus
- Optimización de horarios (no solo salones)
- Dashboard interactivo
- Integración institucional

Ver `CHANGELOG.md` para roadmap completo.

### ¿Puedo sugerir nuevas funcionalidades?

¡Sí! 

- GitHub Issues con etiqueta "enhancement"
- Email a equipo de desarrollo
- Discusión en reuniones de coordinación

---

**¿No encuentras tu pregunta?**

Consulta la documentación completa en `docs/` o contacta al equipo de desarrollo.

**Última actualización**: 2025-12-21  
**Versión**: 2.0.0
