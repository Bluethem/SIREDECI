# SIREDECI - Sistema de Denuncias Ciudadanas

Sistema web para el registro, gestión y seguimiento de denuncias ciudadanas, desarrollado con enfoque en seguridad, privacidad y resiliencia.

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **Base de Datos**: PostgreSQL 14+
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Documentación API**: drf-yasg (Swagger)

### Frontend
- **Framework**: Vue.js 3.5.24
- **Build Tool**: Vite 7.2.2
- **UI Framework**: Tailwind CSS (via CDN)
- **Estado**: Pinia 3.0.4
- **Router**: Vue Router 4.6.3
- **HTTP Client**: Axios 1.13.2
- **Mapas**: Leaflet 1.9.4

## 📋 Requisitos Previos

- Python 3.10 o superior
- Node.js 18 o superior
- PostgreSQL 14 o superior
- npm o yarn

## 🚀 Instalación y Configuración

### 1. Base de Datos

```bash
# Crear la base de datos en PostgreSQL
createdb siredeci_db

# Ejecutar los scripts DDL y DML
psql -U postgres -d siredeci_db -f scripts/ddl/scriptDDL.sql
psql -U postgres -d siredeci_db -f scripts/dml/scriptDML.sql
```

### 2. Backend (Django)

```bash
# Navegar a la carpeta del backend
cd siredeci-app/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Editar .env con tus configuraciones
# Ejemplo:
# SECRET_KEY=tu-secret-key-super-secreta
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
# DB_NAME=siredeci_db
# DB_USER=postgres
# DB_PASSWORD=tu_password
# DB_HOST=localhost
# DB_PORT=5432
# CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
# JWT_ACCESS_TOKEN_LIFETIME=60
# JWT_REFRESH_TOKEN_LIFETIME=1440

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`
Panel de administración: `http://localhost:8000/admin`

### 3. Frontend (Vue.js)

```bash
# Navegar a la carpeta del frontend
cd siredeci-app/frontend

# Instalar dependencias
npm install

# Crear archivo de variables de entorno
copy .env.development.example .env.development  # Windows
# cp .env.development.example .env.development  # Linux/Mac

# Editar .env.development
# VITE_API_URL=http://localhost:8000/api

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📱 Módulo de Ciudadanos - Pantallas Implementadas

### 1. Login de Ciudadano
**Ruta**: `/ciudadano/login`

**Características**:
- Autenticación con DNI (8 dígitos)
- Fecha de emisión del DNI
- Validación de formulario
- Botones de acceso público:
  - Consultar Denuncia Pública
  - Ver Estadísticas Públicas

### 2. Dashboard del Ciudadano
**Ruta**: `/ciudadano/dashboard`

**Características**:
- Mensaje de bienvenida personalizado
- Botones de acción:
  - Consultar mis Denuncias
  - Registrar Nueva Denuncia
  - Ver Estadísticas Públicas
  - Consultar Denuncia Pública
- Opción de cerrar sesión

### 3. Mis Denuncias
**Ruta**: `/ciudadano/mis-denuncias`

**Características**:
- Lista de denuncias del ciudadano
- Tarjetas de estadísticas (Total, Resueltas, Pendientes)
- Filtros de búsqueda por código o título
- Filtro por estado
- Visualización de estado y prioridad con colores
- Botón para ver detalle de cada denuncia

### 4. Consulta Pública
**Ruta**: `/public/consulta`

**Características**:
- Búsqueda por código de seguimiento público
- Sin autenticación requerida
- Visualización del estado y prioridad
- Información detallada de la denuncia
- Historial de seguimiento
- Navegación a Estadísticas Públicas o Login

### 5. Estadísticas Públicas
**Ruta**: `/public/estadisticas`

**Características**:
- Dashboard público sin autenticación
- Tarjetas de resumen (Total, Resueltas, En Proceso, Tiempo Promedio)
- Gráficos de barras por categoría
- Estado de denuncias
- Denuncias por distrito
- Navegación a Consulta Pública o Login

## 🗄️ Modelos Implementados

### Módulo de Usuarios
- **Usuario**: Modelo de autenticación personalizado (AbstractBaseUser)

### Módulo de Ciudadanos
- **Ciudadano**: Información de ciudadanos
- **CiudadanoTelefono**: Teléfonos de contacto (multivaluado)

### Módulo de Categorías
- **AreaResponsable**: Áreas municipales
- **Categoria**: Clasificación de denuncias

### Módulo de Denuncias
- **Ubicacion**: Geolocalización de denuncias
- **Denuncia**: Registro principal de denuncias
- **Evidencia**: Archivos adjuntos (máx. 5 por denuncia)
- **Seguimiento**: Historial inmutable de cambios de estado

### Módulo de Personal
- **PersonalMunicipal**: Empleados municipales

## 🎨 Diseño y UI

- **Fuente**: Public Sans (Google Fonts)
- **Iconos**: Material Symbols Outlined
- **Framework CSS**: Tailwind CSS
- **Colores**:
  - Primary: `#2e87ad`
  - Background Light: `#f6f7f8`
  - Background Dark: `#131b1f`
- **Modo Oscuro**: Soporte completo con `dark:` classes

## 📝 Próximos Pasos

### Backend
1. Crear serializers para todos los modelos
2. Implementar ViewSets y APIs RESTful
3. Configurar autenticación JWT
4. Implementar permisos y RBAC
5. Crear endpoints de login con DNI
6. Implementar sistema de archivos (evidencias)
7. Crear tests unitarios

### Frontend
1. Implementar servicio de API (axios)
2. Crear store de Pinia para gestión de estado
3. Implementar formulario de nueva denuncia
4. Agregar mapa con Leaflet
5. Implementar vista de detalle de denuncia
6. Agregar sistema de notificaciones
7. Implementar validación de formularios

### Integración
1. Conectar login con backend
2. Integrar gestión de denuncias
3. Implementar carga de evidencias
4. Conectar estadísticas con datos reales
5. Implementar sistema de notificaciones en tiempo real

## 🔐 Seguridad

- Autenticación JWT
- Validación de DNI y fecha de emisión
- CORS configurado
- CSRF protection
- SQL Injection prevention (ORM Django)
- XSS protection
- Rate limiting (pendiente)
- Encriptación de datos sensibles (pendiente)

## 👥 Autores

- David Luza Ccorimanya - Módulo de Ciudadanos
- Rafael Adriano Olivos Gallardo - Módulo de Notificaciones

## 📄 Licencia

Este proyecto es parte de un trabajo académico.
