# Aplicación Web (BETA)

> ⚠️ **ESTADO**: En Desarrollo - Versión BETA  
> 🚧 **NO LISTA PARA PRODUCCIÓN**

## Aviso Importante

La aplicación web del Sistema de Asignación de Salones se encuentra actualmente en **fase BETA de desarrollo**. Aunque funcional para demostración, **NO está lista para uso en producción** y requiere desarrollo adicional antes de su implementación institucional.

## Estado Actual

### ✅ Funcionalidades Implementadas

1. **Visualización de Horarios**
   - Vista de horarios por grupo
   - Vista de horarios por profesor
   - Vista de horarios por salón
   - Filtros básicos (día, semestre)

2. **Interfaz de Usuario**
   - Diseño responsive básico
   - Navegación entre vistas
   - Tabla de horarios
   - Exportación a PDF (básica)

3. **Backend Básico**
   - API REST simple
   - Carga de datos desde CSV
   - Endpoints para consultas básicas

### ⚠️ Limitaciones Conocidas

1. **Seguridad**
   - ❌ Sin autenticación de usuarios
   - ❌ Sin autorización por roles
   - ❌ Sin encriptación de datos sensibles
   - ❌ Vulnerable a inyección SQL (si se usa BD)

2. **Rendimiento**
   - ⚠️ No optimizado para grandes volúmenes
   - ⚠️ Sin caché de datos
   - ⚠️ Carga completa en cada request
   - ⚠️ No hay paginación

3. **Funcionalidad**
   - ❌ No permite edición de horarios
   - ❌ No integra con optimizadores
   - ❌ No hay sistema de notificaciones
   - ❌ Exportación limitada (solo PDF básico)

4. **Estabilidad**
   - ⚠️ Manejo de errores básico
   - ⚠️ Sin logging robusto
   - ⚠️ No hay tests automatizados
   - ⚠️ Puede fallar con datos inconsistentes

## Arquitectura Actual

```
web-app/ (BETA)
├── backend/
│   ├── app.py              # Flask/FastAPI server
│   ├── api/
│   │   ├── horarios.py     # Endpoints de horarios
│   │   └── consultas.py    # Endpoints de consultas
│   └── models/
│       └── horario.py      # Modelos de datos
│
├── frontend/
│   ├── index.html          # Página principal
│   ├── css/
│   │   └── styles.css      # Estilos
│   └── js/
│       ├── app.js          # Lógica principal
│       └── api.js          # Cliente API
│
└── README_WEB.md           # Este archivo
```

## Instalación (Solo para Desarrollo)

```bash
# Instalar dependencias
pip install flask flask-cors pandas

# Ejecutar servidor de desarrollo
cd web-app/backend
python app.py

# Abrir en navegador
open http://localhost:5000
```

## Uso Básico (Demo)

### Ver Horario de Grupo

```
http://localhost:5000/horario/grupo/1527A
```

### Ver Horario de Profesor

```
http://localhost:5000/horario/profesor/PROFESOR%203
```

### Ver Ocupación de Salón

```
http://localhost:5000/horario/salon/FFA
```

## Roadmap de Desarrollo

### Fase 1: Seguridad (Crítico)
- [ ] Implementar autenticación (JWT)
- [ ] Sistema de roles (Admin, Profesor, Estudiante)
- [ ] Validación de entrada
- [ ] Sanitización de datos
- [ ] HTTPS obligatorio

### Fase 2: Funcionalidad Core
- [ ] Integración con optimizadores
- [ ] Edición de horarios (con permisos)
- [ ] Comparación de horarios
- [ ] Exportación avanzada (Excel, iCal, PDF mejorado)
- [ ] Sistema de notificaciones

### Fase 3: Rendimiento
- [ ] Caché de datos
- [ ] Paginación
- [ ] Lazy loading
- [ ] Optimización de queries
- [ ] CDN para assets

### Fase 4: UX/UI
- [ ] Diseño profesional
- [ ] Modo oscuro
- [ ] Accesibilidad (WCAG 2.1)
- [ ] PWA (Progressive Web App)
- [ ] Responsive mejorado

### Fase 5: Integración
- [ ] API con sistema institucional
- [ ] Single Sign-On (SSO)
- [ ] Sincronización automática
- [ ] Webhooks para actualizaciones

## Tecnologías Propuestas

### Backend
- **Framework**: FastAPI (recomendado) o Flask
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticación**: JWT + OAuth2
- **Cache**: Redis
- **API Docs**: Swagger/OpenAPI

### Frontend
- **Framework**: React o Vue.js
- **UI Library**: Material-UI o Ant Design
- **State Management**: Redux o Vuex
- **Build Tool**: Vite
- **Testing**: Jest + React Testing Library

### DevOps
- **Containerización**: Docker
- **Orquestación**: Docker Compose (dev) / Kubernetes (prod)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## Advertencias de Seguridad

🚨 **NO USAR EN PRODUCCIÓN SIN:**

1. **Autenticación robusta**
   - Sistema de login seguro
   - Gestión de sesiones
   - Protección contra fuerza bruta

2. **Autorización por roles**
   - Permisos granulares
   - Validación en backend
   - Auditoría de acciones

3. **Validación de datos**
   - Sanitización de entrada
   - Validación de tipos
   - Protección contra XSS/CSRF

4. **Encriptación**
   - HTTPS obligatorio
   - Encriptación de datos sensibles
   - Hashing de contraseñas (bcrypt)

5. **Auditoría y Logging**
   - Registro de todas las acciones
   - Monitoreo de seguridad
   - Alertas automáticas

## Contribuir al Desarrollo Web

Si deseas contribuir al desarrollo de la aplicación web:

1. **Revisar roadmap** y seleccionar tarea
2. **Crear branch** desde `develop`
3. **Implementar** con tests
4. **Documentar** cambios
5. **Pull request** para revisión

### Estándares de Código

```python
# Backend (Python)
- PEP 8 style guide
- Type hints obligatorios
- Docstrings para funciones públicas
- Tests unitarios (pytest)
- Coverage > 80%

# Frontend (JavaScript)
- ESLint + Prettier
- Componentes funcionales
- PropTypes o TypeScript
- Tests de componentes
- Accesibilidad (a11y)
```

## Contacto

**Autor:** Jesús Olvera

- **GitHub:** [@jjho05](https://github.com/jjho05)
- **Email:** jjho.reivaj05@gmail.com / hernandez.jesusjavier.20.0770@gmail.com
- **Repositorio:** https://github.com/jjho05/Sistema-Salones-ISC
- **Institucional:** sistemas@cdmadero.tecnm.mx

## Licencia

Mismo que el proyecto principal - Uso académico TECNM.

---

**Última actualización**: 2025-12-21  
**Versión**: 0.1.0-beta  
**Estado**: 🚧 En Desarrollo - NO PRODUCCIÓN  
**Mantenedor**: Equipo de Desarrollo Web ISC
