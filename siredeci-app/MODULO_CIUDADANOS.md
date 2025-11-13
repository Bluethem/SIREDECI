# Módulo de Ciudadanos - Implementación Completa

## 📋 Resumen

Se ha implementado el **Módulo de Ciudadanos** completo para el sistema SIREDECI, incluyendo:

1. ✅ **Backend (Django)**: Modelos, administración y estructura base
2. ✅ **Frontend (Vue.js)**: 5 pantallas completamente funcionales
3. ✅ **Routing**: Sistema de navegación configurado
4. ✅ **Diseño UI/UX**: Interfaz moderna con Tailwind CSS y modo oscuro

---

## 🎨 Pantallas Implementadas

### 1. Login de Ciudadano (`/ciudadano/login`)

**Características**:
- ✅ Formulario de autenticación con DNI (8 dígitos)
- ✅ Campo de fecha de emisión del DNI
- ✅ Validación de campos en tiempo real
- ✅ Mensajes de error descriptivos
- ✅ Botón para "Consultar Denuncia Pública"
- ✅ Botón para "Ver Estadísticas Públicas"
- ✅ Estados de carga (loading)
- ✅ Diseño responsive

**Vista previa**:
```
┌─────────────────────────────────────┐
│   SIREDECI - Iniciar Sesión         │
│                                     │
│   DNI: [________]                   │
│   Fecha Emisión: [__/__/____]       │
│                                     │
│   [   Iniciar Sesión   ]            │
│                                     │
│   ──── o ────                       │
│                                     │
│   [ Consultar Denuncia Pública ]    │
│   [ Ver Estadísticas Públicas  ]    │
└─────────────────────────────────────┘
```

---

### 2. Dashboard del Ciudadano (`/ciudadano/dashboard`)

**Características**:
- ✅ Mensaje de bienvenida personalizado
- ✅ 4 botones principales de acción
- ✅ Navegación fluida entre secciones
- ✅ Opción de cerrar sesión

**Botones**:
1. 🔍 **Consultar mis Denuncias** → Redirige a la lista de denuncias
2. ➕ **Registrar Nueva Denuncia** → (Pendiente implementar)
3. 📊 **Ver Estadísticas Públicas** → Redirige a estadísticas
4. 🌐 **Consultar Denuncia Pública** → Redirige a consulta pública
5. 🚪 **Cerrar Sesión** → Vuelve al login

---

### 3. Mis Denuncias (`/ciudadano/mis-denuncias`)

**Características**:
- ✅ Lista de todas las denuncias del ciudadano
- ✅ Tarjetas de estadísticas:
  - Total de denuncias
  - Denuncias resueltas
  - Denuncias pendientes
- ✅ **Filtros de búsqueda**:
  - Por código o título (búsqueda en tiempo real)
  - Por estado (dropdown)
- ✅ **Información de cada denuncia**:
  - Título y descripción
  - Código y fecha de registro
  - Estado con colores distintivos
  - Prioridad
  - Categoría
  - Distrito
- ✅ Botón "Ver Detalle" en cada denuncia
- ✅ Estados vacíos (cuando no hay denuncias)

**Estados de Denuncia** (con colores):
- 🔵 Registrado (azul)
- 🟡 En revisión (amarillo)
- 🟣 Asignado (morado)
- 🟠 En proceso (naranja)
- 🟢 Resuelta (verde)
- 🔴 Rechazada (rojo)
- ⚫ Cerrada (gris)

---

### 4. Consulta Pública (`/public/consulta`)

**Características**:
- ✅ **Sin autenticación requerida** (acceso público)
- ✅ Búsqueda por código de seguimiento
- ✅ Visualización completa de la denuncia:
  - Título y descripción
  - Estado y prioridad
  - Categoría
  - Ubicación
  - Fecha de registro
- ✅ **Historial de seguimiento**:
  - Línea de tiempo visual
  - Comentarios de cada cambio
  - Fechas y horas
- ✅ Navegación a estadísticas o login
- ✅ Mensajes de error si no se encuentra

---

### 5. Estadísticas Públicas (`/public/estadisticas`)

**Características**:
- ✅ **Sin autenticación requerida** (dashboard público)
- ✅ **4 Tarjetas de KPIs**:
  - Total de denuncias
  - Denuncias resueltas (con porcentaje)
  - Denuncias en proceso (con porcentaje)
  - Tiempo promedio de resolución
- ✅ **Gráfico de Denuncias por Categoría**:
  - Barras de progreso con colores
  - Porcentajes calculados
  - Top 5 categorías
- ✅ **Gráfico de Estados**:
  - Distribución por estado
  - Contadores por cada estado
- ✅ **Denuncias por Distrito**:
  - Grid responsive
  - Tasa de resolución por distrito
  - Cantidad de denuncias
- ✅ Navegación a consulta pública o login

---

## 🗄️ Modelos de Base de Datos (Backend)

### 1. **Usuario** (`apps/usuarios/models.py`)
```python
class Usuario(AbstractBaseUser, PermissionsMixin):
    - id_usuario
    - codigo_usuario (auto-generado: USU-00001)
    - nombre_usuario (único)
    - email (único)
    - password_hash
    - fecha_creacion
    - ultimo_acceso
    - estado_cuenta (Activo, Inactivo, Suspendido, Bloqueado)
    - intentos_login
    - fecha_bloqueo
    - requiere_mfa
    - token_mfa
```

### 2. **Ciudadano** (`apps/ciudadanos/models.py`)
```python
class Ciudadano:
    - id_ciudadano
    - codigo_ciudadano (auto-generado: CIU-00001)
    - dni (8 dígitos, único)
    - nombre
    - apellido
    - email (único, opcional)
    - direccion
    - fecha_emision_dni
    - fecha_registro
    - es_anonimo
    - estado_cuenta
    - id_usuario (FK a Usuario)
```

### 3. **CiudadanoTelefono** (`apps/ciudadanos/models.py`)
```python
class CiudadanoTelefono:
    - id_ciudadano_telefono
    - id_ciudadano (FK)
    - telefono
    - es_principal
```

### 4. **AreaResponsable** (`apps/categorias/models.py`)
```python
class AreaResponsable:
    - id_area_responsable
    - codigo_area (auto-generado: ARE-001)
    - nombre (único)
    - descripcion
    - email (único)
    - telefono
    - capacidad_maxima
    - esta_activo
    - id_jefe_area (FK a PersonalMunicipal)
```

### 5. **Categoria** (`apps/categorias/models.py`)
```python
class Categoria:
    - id_categoria
    - codigo_categoria (auto-generado: CAT-001)
    - nombre (único)
    - descripcion
    - color (hexadecimal)
    - icono
    - esta_activo
    - tiempo_respuesta_promedio (horas)
    - id_area_responsable (FK)
```

### 6. **Ubicacion** (`apps/denuncias/models.py`)
```python
class Ubicacion:
    - id_ubicacion
    - codigo_ubicacion (auto-generado: UBI-00001)
    - latitud (-90 a 90)
    - longitud (-180 a 180)
    - direccion
    - referencia
    - distrito
    - codigo_postal
```

### 7. **Denuncia** (`apps/denuncias/models.py`)
```python
class Denuncia:
    - id_denuncia
    - codigo_denuncia (auto-generado: DEN-2025-00001)
    - titulo (max 100 caracteres)
    - descripcion (texto largo)
    - fecha_registro
    - fecha_actualizacion
    - estado (Registrado, En revisión, etc.)
    - prioridad (Baja, Media, Alta, Urgente)
    - es_anonima
    - numero_seguimiento (auto-generado: SEG-A3F5D8C9)
    - requiere_validacion
    - id_ciudadano (FK, nullable)
    - id_categoria (FK)
    - id_ubicacion (FK)
```

### 8. **Evidencia** (`apps/denuncias/models.py`)
```python
class Evidencia:
    - id_evidencia
    - codigo_evidencia (auto-generado: EVI-00001)
    - nombre_archivo
    - ruta_almacenamiento (única)
    - tipo_archivo (JPEG, PNG, GIF, MP4, PDF)
    - tamaño_bytes
    - fecha_carga
    - hash_archivo (SHA-256, único)
    - esta_escaneado
    - id_denuncia (FK)
```

### 9. **Seguimiento** (`apps/denuncias/models.py`)
```python
class Seguimiento:
    - id_seguimiento
    - codigo_seguimiento (auto-generado: SEG-00001)
    - estado_anterior (opcional)
    - estado_nuevo
    - fecha_hora
    - comentario
    - es_visible (para ciudadano)
    - id_denuncia (FK)
    - id_usuario (FK)
```

### 10. **PersonalMunicipal** (`apps/personal/models.py`)
```python
class PersonalMunicipal:
    - id_personal
    - codigo_personal (auto-generado: PER-00001)
    - dni (8 dígitos, único)
    - nombre
    - apellido
    - email (único)
    - cargo
    - fecha_ingreso
    - estado_laboral (Activo, Inactivo, etc.)
    - especialidad
    - id_area_responsable (FK)
    - id_usuario (FK, único)
```

---

## 🎨 Diseño y Estilos

### Colores
```css
--primary: #2e87ad
--background-light: #f6f7f8
--background-dark: #131b1f
```

### Tipografía
- **Fuente**: Public Sans (Google Fonts)
- **Tamaños**: 32px (títulos), 24px (subtítulos), 16px (texto)

### Iconos
- **Library**: Material Symbols Outlined
- **Estilo**: Outlined, peso 400

### Modo Oscuro
- ✅ Completamente soportado
- ✅ Classes `dark:` de Tailwind
- ✅ Contraste mejorado para accesibilidad

---

## 🔧 Configuración Técnica

### Rutas del Frontend
```javascript
/                          → Redirige a /ciudadano/login
/ciudadano/login           → Login de ciudadano
/ciudadano/dashboard       → Dashboard principal
/ciudadano/mis-denuncias   → Lista de denuncias
/public/consulta           → Consulta pública
/public/estadisticas       → Estadísticas públicas
```

### Estructura de Carpetas (Backend)
```
backend/
├── apps/
│   ├── usuarios/       → Autenticación
│   ├── ciudadanos/     → Gestión de ciudadanos
│   ├── denuncias/      → Denuncias y seguimiento
│   ├── categorias/     → Categorías y áreas
│   └── personal/       → Personal municipal
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
└── manage.py
```

### Estructura de Carpetas (Frontend)
```
frontend/
├── src/
│   ├── views/
│   │   ├── ciudadano/
│   │   │   ├── LoginCiudadano.vue
│   │   │   ├── DashboardCiudadano.vue
│   │   │   └── MisDenuncias.vue
│   │   └── public/
│   │       ├── ConsultaPublica.vue
│   │       └── EstadisticasPublicas.vue
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
└── index.html
```

---

## 📝 Próximos Pasos

### Prioridad Alta
1. **Serializers del Backend**
   - Crear serializers para todos los modelos
   - Implementar validaciones personalizadas

2. **ViewSets y APIs**
   - Implementar ViewSets de DRF
   - Configurar endpoints RESTful
   - Documentar con Swagger

3. **Autenticación**
   - Endpoint de login con DNI + fecha emisión
   - Generación de tokens JWT
   - Refresh token

4. **Formulario de Nueva Denuncia**
   - Componente Vue.js
   - Selector de categoría
   - Mapa con Leaflet para ubicación
   - Carga de evidencias (máx. 5 archivos)

### Prioridad Media
5. **Detalle de Denuncia**
   - Vista completa con timeline
   - Comentarios y actualizaciones
   - Descarga de evidencias

6. **Integración Backend-Frontend**
   - Servicio de API con Axios
   - Interceptores para JWT
   - Manejo de errores

7. **Estado Global**
   - Store de Pinia para usuario
   - Store para denuncias
   - Persistencia en localStorage

### Prioridad Baja
8. **Notificaciones en Tiempo Real**
   - WebSockets o Server-Sent Events
   - Alertas de cambio de estado

9. **Tests**
   - Tests unitarios en Django
   - Tests de componentes en Vue
   - Tests E2E con Cypress

---

## ✅ Checklist de Implementación

### Backend
- [x] Modelos creados y documentados
- [x] Admin de Django configurado
- [x] Migraciones preparadas
- [x] AUTH_USER_MODEL configurado
- [ ] Serializers
- [ ] ViewSets
- [ ] Endpoints de API
- [ ] Autenticación JWT
- [ ] Tests

### Frontend
- [x] Router configurado
- [x] Login implementado
- [x] Dashboard implementado
- [x] Mis Denuncias implementado
- [x] Consulta Pública implementado
- [x] Estadísticas Públicas implementado
- [ ] Servicio de API
- [ ] Store de Pinia
- [ ] Nueva Denuncia
- [ ] Detalle de Denuncia
- [ ] Tests

---

## 🎓 Notas Importantes

1. **Códigos Auto-generados**: Todos los códigos (CIU-00001, DEN-2025-00001, etc.) se generan automáticamente en el método `save()` de cada modelo.

2. **Número de Seguimiento Público**: Se genera con UUID para ser único y seguro (`SEG-A3F5D8C9AB`).

3. **Validaciones**: Los campos tienen validadores de Django (RegexValidator para DNI, EmailValidator, etc.).

4. **Índices de BD**: Se han definido índices para optimizar consultas frecuentes.

5. **Relaciones**: Se usa `PROTECT` en FKs críticas y `CASCADE` donde es apropiado.

6. **Datos de Ejemplo**: Las pantallas tienen datos de prueba (mock data) que deben ser reemplazados por llamadas reales al API.

---

## 🚀 Para Ejecutar

```bash
# Backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Frontend (otra terminal)
cd frontend
npm run dev
```

Luego visita: `http://localhost:5173/ciudadano/login`

---

**Desarrollado por**: David Luza Ccorimanya  
**Fecha**: Enero 2025  
**Proyecto**: SIREDECI - Sistema de Denuncias Ciudadanas
