# 🚀 Guía de Publicación en GitHub

## Paso 1: Inicializar Git

```bash
cd "/Users/lic.ing.jesusolvera/Documents/PROYECTOS PERSONALES/Sistema-Salones-ISC"

# Inicializar repositorio
git init

# Añadir archivos
git add .

# Primer commit
git commit -m "feat: initial commit - Sistema de Optimización de Salones ISC"
```

## Paso 2: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `Sistema-Salones-ISC`
3. Descripción: `Sistema inteligente de optimización de horarios con múltiples algoritmos`
4. Público o Privado (tu elección)
5. **NO** inicializar con README (ya lo tienes)
6. Click en "Create repository"

## Paso 3: Conectar con GitHub

```bash
# Añadir remote (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/Sistema-Salones-ISC.git

# Renombrar rama a main
git branch -M main

# Push inicial
git push -u origin main
```

## Paso 4: Configurar GitHub (Opcional)

### Añadir Topics

En GitHub, ve a tu repositorio y añade topics:
- `python`
- `optimization`
- `scheduling`
- `flask`
- `machine-learning`
- `genetic-algorithm`
- `education`

### Crear Releases

```bash
# Crear tag para primera versión
git tag -a v1.0.0 -m "Primera versión estable"
git push origin v1.0.0
```

Luego en GitHub:
1. Ve a "Releases"
2. Click "Create a new release"
3. Selecciona tag `v1.0.0`
4. Título: `v1.0.0 - Primera Versión Estable`
5. Descripción: Resumen de características
6. Publish release

### Añadir Screenshots (Recomendado)

```bash
# Crear carpeta para screenshots
mkdir -p docs/screenshots

# Añadir tus capturas de pantalla:
# - main.png (interfaz principal)
# - results.png (página de resultados)
# - comparison.png (gráficos comparativos)

git add docs/screenshots/
git commit -m "docs: add screenshots"
git push
```

## Paso 5: Actualizar README con tu Info

Edita `README.md` y reemplaza:

```markdown
- **Jesús Olvera** - *Desarrollo inicial* - [GitHub](https://github.com/TU-USUARIO)

## 📞 Contacto

- Email: TU-EMAIL@example.com
- GitHub: [@TU-USUARIO](https://github.com/TU-USUARIO)
```

Luego:

```bash
git add README.md
git commit -m "docs: update contact information"
git push
```

## Paso 6: Proteger Datos Sensibles

Verifica que `.gitignore` esté funcionando:

```bash
# Ver qué archivos se subirán
git status

# Si ves archivos .csv o .xlsx, añádelos a .gitignore
echo "*.csv" >> .gitignore
echo "*.xlsx" >> .gitignore

git add .gitignore
git commit -m "chore: update gitignore"
git push
```

## 📋 Checklist Pre-Publicación

- [ ] README.md completo y actualizado
- [ ] LICENSE añadida
- [ ] .gitignore configurado
- [ ] Sin datos sensibles
- [ ] requirements.txt actualizado
- [ ] Código comentado y documentado
- [ ] Tests funcionando (si los hay)
- [ ] Screenshots añadidas
- [ ] Información de contacto actualizada

## 🎉 ¡Listo!

Tu repositorio está ahora en GitHub. Comparte el link:

```
https://github.com/TU-USUARIO/Sistema-Salones-ISC
```

## 📈 Siguientes Pasos

1. **Añadir GitHub Actions** para CI/CD
2. **Crear Wiki** con documentación extendida
3. **Issues Templates** para bugs y features
4. **Pull Request Template**
5. **GitHub Pages** para demo online

## 🔄 Workflow Diario

```bash
# Hacer cambios
git add .
git commit -m "tipo: descripción del cambio"
git push

# Crear nueva feature
git checkout -b feature/nueva-feature
# ... hacer cambios ...
git add .
git commit -m "feat: nueva feature"
git push origin feature/nueva-feature
# Luego crear Pull Request en GitHub
```

---

**¿Necesitas ayuda?** Abre un issue en el repositorio.
