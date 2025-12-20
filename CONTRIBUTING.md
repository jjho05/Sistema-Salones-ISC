# Contribuir al Sistema de Optimización de Salones ISC

¡Gracias por tu interés en contribuir! 🎉

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado antes
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Versión de Python y OS

### Sugerir Mejoras

1. Abre un issue describiendo:
   - La mejora propuesta
   - Por qué sería útil
   - Ejemplos de uso

### Pull Requests

1. Fork el repositorio
2. Crea una rama desde `main`:
   ```bash
   git checkout -b feature/mi-nueva-feature
   ```
3. Haz tus cambios siguiendo las guías de estilo
4. Escribe tests si aplica
5. Commit con mensajes descriptivos:
   ```bash
   git commit -m "feat: añade detección de columnas mejorada"
   ```
6. Push a tu fork:
   ```bash
   git push origin feature/mi-nueva-feature
   ```
7. Abre un Pull Request

## 📝 Guías de Estilo

### Python

- Seguir PEP 8
- Docstrings para funciones y clases
- Type hints cuando sea posible
- Nombres descriptivos

### Commits

Usar conventional commits:
- `feat:` nueva característica
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` formato, sin cambios de código
- `refactor:` refactorización
- `test:` añadir tests
- `chore:` mantenimiento

### Código

```python
def optimizar_horario(df: pd.DataFrame, metodo: str = 'greedy') -> pd.DataFrame:
    """
    Optimiza el horario usando el método especificado.
    
    Args:
        df: DataFrame con horario inicial
        metodo: Método a usar ('greedy', 'ml', 'genetic')
    
    Returns:
        DataFrame con horario optimizado
    """
    # Implementación
    pass
```

## 🧪 Tests

```bash
# Ejecutar tests
python -m pytest tests/

# Con coverage
python -m pytest --cov=. tests/
```

## 📚 Documentación

- Actualizar README.md si añades features
- Documentar nuevos métodos en `documentacion_metodos/`
- Añadir ejemplos de uso

## ❓ Preguntas

Si tienes preguntas, abre un issue con la etiqueta `question`.

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo MIT License.
