---
marp: true
theme: default
paginate: true
math: mathjax
style: |
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap');
  
  :root {
    font-family: Outfit, Helvetica, Arial;
  }
  
  .MathJax, .MathJax_Display, mjx-container {
    font-family: 'Times New Roman', Times, serif !important;
  }
  
  section {
    background-color: #ffffff;
    background-image: linear-gradient(to bottom right, #cadaf7 5%, #87a7e4 95%);
  }
  
  h1, h2, h3, h4, h5, h6 {
    color: #214484;
    font-weight: 700;
  }
  
  a {
    color: #303ca6;
  }
  
  code {
    background-color: #ffffffad;
  }
  
  section::after {
    font-size: 0.75em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    color: #303ca6;
  }
---

<!-- _class: lead blue -->
# Sistema de Asignación de Salones ISC

**Optimización Inteligente de Espacios Académicos**

**Jesús Olvera**

Ingeniería en Sistemas Computacionales
Instituto Tecnológico de Ciudad Madero

---

## Contexto del Problema

**Desafío:** Asignar 680 clases a 21 salones minimizando movimientos de profesores

**Restricciones:**
- ✅ 100% cumplimiento de preferencias prioritarias (P1)
- ✅ Capacidad de salones
- ✅ Compatibilidad teoría/laboratorio
- ✅ Sin conflictos horarios

**Objetivo:** Minimizar movimientos, cambios de piso y distancia recorrida

---

## Estado del Arte - Enfoques Principales

| Enfoque | Ventaja | Limitación |
|---------|---------|------------|
| **Metaheurísticas** | Buena calidad | Tiempo alto |
| **Machine Learning** | Rápido | Necesita datos |
| **Programación Lineal** | Óptimo garantizado | No escala |
| **Híbridos** | Balance | Complejidad |

**Nuestra solución:** Enfoque híbrido con 4 algoritmos comparados

---

## Modelo Matemático

**Función Objetivo:**

$$
E(A) = 10 \cdot movimientos + 5 \cdot cambios\_piso + 1 \cdot distancia
$$

**Restricciones Duras:**
- Unicidad temporal
- Capacidad suficiente
- Tipo compatible

**Restricciones Suaves (Prioridades):**
- P1: Preferencias profesores (100% garantizado)
- P2: Consistencia de grupos
- P3: Primer semestre

---

## Algoritmos Implementados

### 1. Greedy + Hill Climbing
- Construcción voraz + refinamiento local
- Tiempo: ~30s
- **Mejor en movimientos** (314)

### 2. Machine Learning
- Random Forest para predicción
- Tiempo: ~16s
- **Más rápido**

### 3. Algoritmo Genético
- Búsqueda evolutiva
- Tiempo: ~74s
- Exploración amplia

---

## Ejemplo Didáctico: Greedy + HC

**Problema simplificado:** 10 clases, 4 salones, 4 profesores

**Algoritmo:**
1. Construcción voraz (asignar clase por clase)
2. Hill Climbing (mejorar iterativamente)

**Resultado:**
- Inicial: 6 movimientos
- Final: 3 movimientos
- **Mejora: 50%**

---

## Resultados Experimentales

**30 corridas por algoritmo:**

| Algoritmo | Movimientos | Cambios Piso | Distancia | Tiempo |
|-----------|-------------|--------------|-----------|--------|
| Inicial | 357 | 287 | 2847 | - |
| **Greedy+HC** | **314** | **206** | 1951 | 30s |
| ML | 366 | 223 | **1821** | **16s** |
| Genético | 379 | 286 | 2413 | 74s |

**Ganador:** Greedy+HC (mejor balance calidad/tiempo)

---

## Pruebas Estadísticas

**ANOVA:** F = 1847, p < 0.001 ✅

**Tukey HSD:** Todas las diferencias significativas

**Cohen's d:** 
- Greedy vs ML: d = 22.4 (muy grande)
- Greedy vs Genético: d = 28.1 (muy grande)

**Conclusión:** Greedy+HC es **estadísticamente superior** (p<0.001)

---

## Implementación

**Arquitectura:**
```
pre_asignar_p1.py → optimizador_*.py → corregir_prioridades.py
```

**Ejecución:**
```bash
python3 ejecutar_todos.py  # Todo automático
```

**Salidas:**
- Horarios optimizados (CSV/Excel)
- Comparativas y gráficos
- Reportes detallados

---

## Conclusiones

### Logros
✅ **314 movimientos** vs 357 inicial (-12%)
✅ **206 cambios de piso** vs 287 inicial (-28%)
✅ **100% cumplimiento P1** garantizado
✅ **Validación estadística** rigurosa

### Recomendación
**Greedy + Hill Climbing** para producción:
- Mejor calidad en métricas principales
- Tiempo aceptable (~30s)
- Resultados consistentes

---

## Trabajo Futuro

**Corto plazo:**
- Implementar P2 y P3 completamente
- Optimizar tiempos de ejecución
- App web mejorada

**Largo plazo:**
- Soporte multi-campus
- Optimización de horarios (no solo salones)
- Integración institucional

---

<!-- _class: lead blue -->
# ¡Gracias!

---

## Contacto

**Jesús Olvera**

- **GitHub:** [@jjho05](https://github.com/jjho05)
- **Email:** jjho.reivaj05@gmail.com
- **Institución:** Instituto Tecnológico de Ciudad Madero

**Repositorio:**
https://github.com/jjho05/Sistema-Salones-ISC

---

<!-- _class: lead blue -->

# "Por mi patria y por mi bien"

**Orgullo Tec Madero**

🎓
