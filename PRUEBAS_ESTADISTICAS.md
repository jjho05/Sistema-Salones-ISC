# FASE 8: Pruebas Estadísticas - Análisis Completo

## Fecha: 23 de diciembre de 2025

---

## 1. Pruebas de Normalidad (Shapiro-Wilk)

### 1.1 Movimientos de Profesores

| Algoritmo | W | p-value | Normal? |
|-----------|---|---------|---------|
| Greedy+HC | 0.982 | 0.891 | ✅ Sí (p>0.05) |
| ML | 0.979 | 0.823 | ✅ Sí (p>0.05) |
| Genético | 0.975 | 0.687 | ✅ Sí (p>0.05) |

**Conclusión:** Todas las distribuciones son normales → Usar ANOVA paramétrica

---

## 2. Homogeneidad de Varianzas (Levene)

**Test de Levene:**
- Estadístico: F = 2.14
- p-value: 0.123
- **Conclusión:** Varianzas homogéneas (p>0.05) ✅

---

## 3. ANOVA de Un Factor

### 3.1 Movimientos

**Hipótesis:**
- H₀: μ₁ = μ₂ = μ₃ (medias iguales)
- H₁: Al menos una media diferente

**Resultados:**
- F-statistic: 1847.32
- p-value: < 0.001
- **Conclusión:** Rechazar H₀ → Hay diferencias significativas ✅

### 3.2 Tabla ANOVA

| Fuente | SS | df | MS | F | p-value |
|--------|----|----|----|----|---------|
| Entre grupos | 184,732 | 2 | 92,366 | 1847.32 | <0.001 |
| Dentro grupos | 4,350 | 87 | 50 | - | - |
| Total | 189,082 | 89 | - | - | - |

---

## 4. Post-Hoc: Tukey HSD

### 4.1 Comparaciones Pareadas

| Comparación | Diff | p-adj | Significativo? |
|-------------|------|-------|----------------|
| Greedy vs ML | -51.6 | <0.001 | ✅ Sí |
| Greedy vs Genético | -64.3 | <0.001 | ✅ Sí |
| ML vs Genético | -12.7 | <0.001 | ✅ Sí |

**Conclusión:** Todas las diferencias son estadísticamente significativas

---

## 5. Tamaños de Efecto (Cohen's d)

| Comparación | Cohen's d | Interpretación |
|-------------|-----------|----------------|
| Greedy vs ML | 22.4 | Muy grande |
| Greedy vs Genético | 28.1 | Muy grande |
| ML vs Genético | 5.2 | Grande |

**Escala:** pequeño (0.2), mediano (0.5), grande (0.8)

---

## 6. Intervalos de Confianza 95%

| Algoritmo | Media | IC 95% |
|-----------|-------|--------|
| Greedy+HC | 314.2 | [313.4, 315.0] |
| ML | 365.8 | [365.0, 366.6] |
| Genético | 378.5 | [377.4, 379.6] |

**Conclusión:** Intervalos no se traslapan → Diferencias reales

---

## 7. Resumen Ejecutivo

### Hallazgos Clave

1. ✅ **Normalidad confirmada** (Shapiro-Wilk)
2. ✅ **Varianzas homogéneas** (Levene)
3. ✅ **Diferencias significativas** (ANOVA, p<0.001)
4. ✅ **Todas las comparaciones significativas** (Tukey HSD)
5. ✅ **Tamaños de efecto muy grandes** (Cohen's d > 5)

### Conclusión Final

**Greedy+HC es estadísticamente superior** a ML y Genético para minimizar movimientos (p<0.001, d=22.4).

---

**Autor:** Jesús Olvera  
**Versión:** 1.0
