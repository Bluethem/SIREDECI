-- ============================================
-- SISTEMA DE DENUNCIAS CIUDADANAS
-- Script de Creación de Base de Datos
-- Motor: PostgreSQL 14+
-- Fecha: 2025-01-10
-- ============================================

-- ============================================
-- MÓDULO 1: CIUDADANOS
-- ============================================

-- Tabla: Usuario (debe crearse primero por dependencias)
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    codigo_usuario VARCHAR(20) UNIQUE NOT NULL,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP,
    estado_cuenta VARCHAR(20) NOT NULL DEFAULT 'Activo',
    intentos_login INTEGER NOT NULL DEFAULT 0,
    fecha_bloqueo TIMESTAMP,
    requiere_mfa BOOLEAN NOT NULL DEFAULT FALSE,
    token_mfa VARCHAR(255),
    
    CONSTRAINT chk_estado_cuenta CHECK (estado_cuenta IN ('Activo', 'Inactivo', 'Suspendido', 'Bloqueado')),
    CONSTRAINT chk_intentos_login CHECK (intentos_login >= 0),
    CONSTRAINT chk_email_formato CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_usuario_estado ON Usuario(estado_cuenta);
CREATE INDEX idx_usuario_ultimo_acceso ON Usuario(ultimo_acceso);

COMMENT ON TABLE Usuario IS 'Entidad general que representa cualquier usuario del sistema';
COMMENT ON COLUMN Usuario.password_hash IS 'Contraseña encriptada con bcrypt';
COMMENT ON COLUMN Usuario.intentos_login IS 'Contador de intentos fallidos de login';

-- Tabla: Ciudadano
CREATE TABLE Ciudadano (
    id_ciudadano SERIAL PRIMARY KEY,
    codigo_ciudadano VARCHAR(20) UNIQUE NOT NULL,
    dni CHAR(8) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    direccion VARCHAR(200),
    fecha_emision_dni DATE NOT NULL,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    es_anonimo BOOLEAN NOT NULL DEFAULT FALSE,
    estado_cuenta VARCHAR(20) NOT NULL DEFAULT 'Activo',
    id_usuario INTEGER UNIQUE,
    
    CONSTRAINT fk_ciudadano_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    CONSTRAINT chk_dni_formato CHECK (dni ~ '^[0-9]{8}$'),
    CONSTRAINT chk_email_ciudadano CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_estado_ciudadano CHECK (estado_cuenta IN ('Activo', 'Inactivo', 'Suspendido'))
);

CREATE INDEX idx_ciudadano_dni ON Ciudadano(dni);
CREATE INDEX idx_ciudadano_estado ON Ciudadano(estado_cuenta);

COMMENT ON TABLE Ciudadano IS 'Registra la información de los ciudadanos que realizan denuncias';
COMMENT ON COLUMN Ciudadano.dni IS 'Documento Nacional de Identidad de 8 dígitos';
COMMENT ON COLUMN Ciudadano.es_anonimo IS 'Indica si el ciudadano registró denuncias anónimas';

-- Tabla: CiudadanoTelefono
CREATE TABLE CiudadanoTelefono (
    id_ciudadano_telefono SERIAL PRIMARY KEY,
    id_ciudadano INTEGER NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    es_principal BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT fk_ciudadano_telefono_ciudadano FOREIGN KEY (id_ciudadano) REFERENCES Ciudadano(id_ciudadano) ON DELETE CASCADE,
    CONSTRAINT uq_ciudadano_telefono UNIQUE (id_ciudadano, telefono),
    CONSTRAINT chk_telefono_formato CHECK (telefono ~ '^[0-9+\-\s()]{7,20}$')
);

CREATE INDEX idx_ciudadano_telefono_ciudadano ON CiudadanoTelefono(id_ciudadano);

COMMENT ON TABLE CiudadanoTelefono IS 'Números de teléfono asociados a ciudadanos (multivaluado)';

-- Tabla: AreaResponsable
CREATE TABLE AreaResponsable (
    id_area_responsable SERIAL PRIMARY KEY,
    codigo_area VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(500),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    capacidad_maxima INTEGER NOT NULL DEFAULT 50,
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE,
    id_jefe_area INTEGER,
    
    CONSTRAINT chk_capacidad_positiva CHECK (capacidad_maxima > 0),
    CONSTRAINT chk_email_area CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_area_nombre ON AreaResponsable(nombre);
CREATE INDEX idx_area_activo ON AreaResponsable(esta_activo);

COMMENT ON TABLE AreaResponsable IS 'Departamentos o áreas del municipio responsables de atender denuncias';

-- Tabla: Categoria
CREATE TABLE Categoria (
    id_categoria SERIAL PRIMARY KEY,
    codigo_categoria VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(500),
    color VARCHAR(7),
    icono VARCHAR(50),
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE,
    tiempo_respuesta_promedio INTEGER,
    id_area_responsable INTEGER NOT NULL,
    
    CONSTRAINT fk_categoria_area FOREIGN KEY (id_area_responsable) REFERENCES AreaResponsable(id_area_responsable),
    CONSTRAINT chk_color_formato CHECK (color IS NULL OR color ~ '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT chk_tiempo_positivo CHECK (tiempo_respuesta_promedio IS NULL OR tiempo_respuesta_promedio > 0)
);

CREATE INDEX idx_categoria_activo ON Categoria(esta_activo);
CREATE INDEX idx_categoria_area ON Categoria(id_area_responsable);

COMMENT ON TABLE Categoria IS 'Clasificación temática de las denuncias';
COMMENT ON COLUMN Categoria.tiempo_respuesta_promedio IS 'Tiempo promedio de atención en horas';

-- Tabla: Ubicacion
CREATE TABLE Ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    codigo_ubicacion VARCHAR(20) UNIQUE NOT NULL,
    latitud NUMERIC(10,8) NOT NULL,
    longitud NUMERIC(11,8) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    referencia VARCHAR(200),
    distrito VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10),
    
    CONSTRAINT chk_latitud_rango CHECK (latitud BETWEEN -90 AND 90),
    CONSTRAINT chk_longitud_rango CHECK (longitud BETWEEN -180 AND 180)
);

CREATE INDEX idx_ubicacion_distrito ON Ubicacion(distrito);
CREATE INDEX idx_ubicacion_coordenadas ON Ubicacion(latitud, longitud);

COMMENT ON TABLE Ubicacion IS 'Información geográfica de la denuncia';

-- Tabla: Denuncia
CREATE TABLE Denuncia (
    id_denuncia SERIAL PRIMARY KEY,
    codigo_denuncia VARCHAR(20) UNIQUE NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'Registrado',
    prioridad VARCHAR(20) NOT NULL DEFAULT 'Media',
    es_anonima BOOLEAN NOT NULL DEFAULT FALSE,
    numero_seguimiento VARCHAR(20) UNIQUE NOT NULL,
    requiere_validacion BOOLEAN NOT NULL DEFAULT TRUE,
    id_ciudadano INTEGER,
    id_categoria INTEGER NOT NULL,
    id_ubicacion INTEGER NOT NULL,
    
    CONSTRAINT fk_denuncia_ciudadano FOREIGN KEY (id_ciudadano) REFERENCES Ciudadano(id_ciudadano) ON DELETE SET NULL,
    CONSTRAINT fk_denuncia_categoria FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
    CONSTRAINT fk_denuncia_ubicacion FOREIGN KEY (id_ubicacion) REFERENCES Ubicacion(id_ubicacion),
    CONSTRAINT chk_estado_denuncia CHECK (estado IN ('Registrado', 'En revisión', 'Asignado', 'En proceso', 'Resuelta', 'Rechazada', 'Cerrada')),
    CONSTRAINT chk_prioridad_denuncia CHECK (prioridad IN ('Baja', 'Media', 'Alta', 'Urgente')),
    CONSTRAINT chk_fechas_denuncia CHECK (fecha_actualizacion >= fecha_registro)
);

CREATE INDEX idx_denuncia_estado ON Denuncia(estado);
CREATE INDEX idx_denuncia_prioridad ON Denuncia(prioridad);
CREATE INDEX idx_denuncia_fecha_registro ON Denuncia(fecha_registro);
CREATE INDEX idx_denuncia_ciudadano ON Denuncia(id_ciudadano);
CREATE INDEX idx_denuncia_categoria ON Denuncia(id_categoria);

COMMENT ON TABLE Denuncia IS 'Registro principal de denuncias realizadas por los ciudadanos';
COMMENT ON COLUMN Denuncia.numero_seguimiento IS 'Código público para seguimiento de la denuncia';

-- Tabla: Evidencia
CREATE TABLE Evidencia (
    id_evidencia SERIAL PRIMARY KEY,
    codigo_evidencia VARCHAR(20) UNIQUE NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_almacenamiento VARCHAR(500) UNIQUE NOT NULL,
    tipo_archivo VARCHAR(100) NOT NULL,
    tamaño_bytes BIGINT NOT NULL,
    fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hash_archivo VARCHAR(64) UNIQUE NOT NULL,
    esta_escaneado BOOLEAN NOT NULL DEFAULT FALSE,
    id_denuncia INTEGER NOT NULL,
    
    CONSTRAINT fk_evidencia_denuncia FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    CONSTRAINT chk_tamaño_positivo CHECK (tamaño_bytes > 0),
    CONSTRAINT chk_tipo_archivo CHECK (tipo_archivo IN ('image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'application/pdf'))
);

CREATE INDEX idx_evidencia_denuncia ON Evidencia(id_denuncia);
CREATE INDEX idx_evidencia_tipo ON Evidencia(tipo_archivo);

COMMENT ON TABLE Evidencia IS 'Archivos multimedia adjuntos a una denuncia (máximo 5 por denuncia)';
COMMENT ON COLUMN Evidencia.hash_archivo IS 'Hash SHA-256 para verificar integridad';

-- Tabla: Seguimiento
CREATE TABLE Seguimiento (
    id_seguimiento SERIAL PRIMARY KEY,
    codigo_seguimiento VARCHAR(20) UNIQUE NOT NULL,
    estado_anterior VARCHAR(20),
    estado_nuevo VARCHAR(20) NOT NULL,
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    es_visible BOOLEAN NOT NULL DEFAULT TRUE,
    id_denuncia INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    
    CONSTRAINT fk_seguimiento_denuncia FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    CONSTRAINT fk_seguimiento_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT chk_estado_seguimiento CHECK (estado_nuevo IN ('Registrado', 'En revisión', 'Asignado', 'En proceso', 'Resuelta', 'Rechazada', 'Cerrada'))
);

CREATE INDEX idx_seguimiento_denuncia ON Seguimiento(id_denuncia);
CREATE INDEX idx_seguimiento_fecha ON Seguimiento(fecha_hora);

COMMENT ON TABLE Seguimiento IS 'Registro inmutable de cambios de estado de la denuncia';

-- ============================================
-- MÓDULO 2: PERSONAL MUNICIPAL
-- ============================================

-- Tabla: PersonalMunicipal
CREATE TABLE PersonalMunicipal (
    id_personal SERIAL PRIMARY KEY,
    codigo_personal VARCHAR(20) UNIQUE NOT NULL,
    dni CHAR(8) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    estado_laboral VARCHAR(20) NOT NULL DEFAULT 'Activo',
    especialidad VARCHAR(100),
    id_area_responsable INTEGER NOT NULL,
    id_usuario INTEGER UNIQUE NOT NULL,
    
    CONSTRAINT fk_personal_area FOREIGN KEY (id_area_responsable) REFERENCES AreaResponsable(id_area_responsable),
    CONSTRAINT fk_personal_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT chk_dni_personal CHECK (dni ~ '^[0-9]{8}$'),
    CONSTRAINT chk_estado_laboral CHECK (estado_laboral IN ('Activo', 'Inactivo', 'Vacaciones', 'Licencia', 'Desvinculado')),
    CONSTRAINT chk_email_personal CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_personal_area ON PersonalMunicipal(id_area_responsable);
CREATE INDEX idx_personal_estado ON PersonalMunicipal(estado_laboral);

COMMENT ON TABLE PersonalMunicipal IS 'Empleados del municipio que gestionan las denuncias';

-- Agregar FK de jefe de área (se hace después de crear PersonalMunicipal)
ALTER TABLE AreaResponsable 
ADD CONSTRAINT fk_area_jefe FOREIGN KEY (id_jefe_area) REFERENCES PersonalMunicipal(id_personal);

-- Tabla: PersonalTelefono
CREATE TABLE PersonalTelefono (
    id_personal_telefono SERIAL PRIMARY KEY,
    id_personal INTEGER NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    es_principal BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT fk_personal_telefono_personal FOREIGN KEY (id_personal) REFERENCES PersonalMunicipal(id_personal) ON DELETE CASCADE,
    CONSTRAINT uq_personal_telefono UNIQUE (id_personal, telefono),
    CONSTRAINT chk_telefono_personal CHECK (telefono ~ '^[0-9+\-\s()]{7,20}$')
);

CREATE INDEX idx_personal_telefono_personal ON PersonalTelefono(id_personal);

COMMENT ON TABLE PersonalTelefono IS 'Números de teléfono asociados al personal municipal';

-- Tabla: Asignacion
CREATE TABLE Asignacion (
    id_asignacion SERIAL PRIMARY KEY,
    codigo_asignacion VARCHAR(20) UNIQUE NOT NULL,
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo_asignacion VARCHAR(500),
    es_activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_finalizacion TIMESTAMP,
    id_denuncia INTEGER NOT NULL,
    id_personal_asignado INTEGER NOT NULL,
    id_personal_asignador INTEGER NOT NULL,
    
    CONSTRAINT fk_asignacion_denuncia FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia),
    CONSTRAINT fk_asignacion_personal_asignado FOREIGN KEY (id_personal_asignado) REFERENCES PersonalMunicipal(id_personal),
    CONSTRAINT fk_asignacion_personal_asignador FOREIGN KEY (id_personal_asignador) REFERENCES PersonalMunicipal(id_personal),
    CONSTRAINT chk_fechas_asignacion CHECK (fecha_finalizacion IS NULL OR fecha_finalizacion >= fecha_asignacion)
);

CREATE INDEX idx_asignacion_denuncia ON Asignacion(id_denuncia);
CREATE INDEX idx_asignacion_activa ON Asignacion(es_activa);
CREATE INDEX idx_asignacion_personal ON Asignacion(id_personal_asignado);

COMMENT ON TABLE Asignacion IS 'Registro de asignación de denuncias al personal';

-- Tabla: Tramitacion
CREATE TABLE Tramitacion (
    id_tramitacion SERIAL PRIMARY KEY,
    codigo_tramitacion VARCHAR(20) UNIQUE NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_finalizacion TIMESTAMP,
    accion_realizada TEXT NOT NULL,
    observaciones TEXT,
    costo_estimado NUMERIC(10,2),
    estado_tramitacion VARCHAR(20) NOT NULL DEFAULT 'En proceso',
    id_asignacion INTEGER UNIQUE NOT NULL,
    
    CONSTRAINT fk_tramitacion_asignacion FOREIGN KEY (id_asignacion) REFERENCES Asignacion(id_asignacion),
    CONSTRAINT chk_estado_tramitacion CHECK (estado_tramitacion IN ('En proceso', 'Finalizado', 'Suspendido', 'Cancelado')),
    CONSTRAINT chk_fechas_tramitacion CHECK (fecha_finalizacion IS NULL OR fecha_finalizacion >= fecha_inicio),
    CONSTRAINT chk_costo_positivo CHECK (costo_estimado IS NULL OR costo_estimado >= 0)
);

CREATE INDEX idx_tramitacion_estado ON Tramitacion(estado_tramitacion);

COMMENT ON TABLE Tramitacion IS 'Proceso de gestión y resolución de una denuncia';

-- Tabla: EvidenciaResolucion
CREATE TABLE EvidenciaResolucion (
    id_evidencia_resolucion SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_almacenamiento VARCHAR(500) UNIQUE NOT NULL,
    tipo_archivo VARCHAR(100) NOT NULL,
    tamaño_bytes BIGINT NOT NULL,
    fecha_carga TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    hash_archivo VARCHAR(64) UNIQUE NOT NULL,
    id_tramitacion INTEGER NOT NULL,
    
    CONSTRAINT fk_evidencia_resolucion_tramitacion FOREIGN KEY (id_tramitacion) REFERENCES Tramitacion(id_tramitacion) ON DELETE CASCADE,
    CONSTRAINT chk_tamaño_resolucion CHECK (tamaño_bytes > 0),
    CONSTRAINT chk_tipo_resolucion CHECK (tipo_archivo IN ('image/jpeg', 'image/png', 'application/pdf'))
);

CREATE INDEX idx_evidencia_resolucion_tramitacion ON EvidenciaResolucion(id_tramitacion);

COMMENT ON TABLE EvidenciaResolucion IS 'Evidencias fotográficas de la resolución';

-- Tabla: Resolucion
CREATE TABLE Resolucion (
    id_resolucion SERIAL PRIMARY KEY,
    codigo_resolucion VARCHAR(20) UNIQUE NOT NULL,
    fecha_resolucion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_resolucion VARCHAR(20) NOT NULL,
    descripcion_resolucion TEXT NOT NULL,
    tiempo_total_horas INTEGER NOT NULL,
    calificacion_ciudadano INTEGER,
    comentario_ciudadano TEXT,
    id_tramitacion INTEGER UNIQUE NOT NULL,
    
    CONSTRAINT fk_resolucion_tramitacion FOREIGN KEY (id_tramitacion) REFERENCES Tramitacion(id_tramitacion),
    CONSTRAINT chk_tipo_resolucion CHECK (tipo_resolucion IN ('Resuelta', 'Rechazada', 'Duplicada', 'No procede')),
    CONSTRAINT chk_tiempo_positivo_resolucion CHECK (tiempo_total_horas > 0),
    CONSTRAINT chk_calificacion_rango CHECK (calificacion_ciudadano IS NULL OR (calificacion_ciudadano BETWEEN 1 AND 5))
);

CREATE INDEX idx_resolucion_tipo ON Resolucion(tipo_resolucion);
CREATE INDEX idx_resolucion_fecha ON Resolucion(fecha_resolucion);

COMMENT ON TABLE Resolucion IS 'Resultado final de la atención de una denuncia';
COMMENT ON COLUMN Resolucion.calificacion_ciudadano IS 'Calificación de 1 a 5 estrellas';

-- Tabla: Comunicacion
CREATE TABLE Comunicacion (
    id_comunicacion SERIAL PRIMARY KEY,
    codigo_comunicacion VARCHAR(20) UNIQUE NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_remitente VARCHAR(20) NOT NULL,
    es_leido BOOLEAN NOT NULL DEFAULT FALSE,
    requiere_respuesta BOOLEAN NOT NULL DEFAULT FALSE,
    id_denuncia INTEGER NOT NULL,
    id_usuario_remitente INTEGER NOT NULL,
    
    CONSTRAINT fk_comunicacion_denuncia FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    CONSTRAINT fk_comunicacion_usuario FOREIGN KEY (id_usuario_remitente) REFERENCES Usuario(id_usuario),
    CONSTRAINT chk_tipo_remitente CHECK (tipo_remitente IN ('Ciudadano', 'Personal', 'Sistema'))
);

CREATE INDEX idx_comunicacion_denuncia ON Comunicacion(id_denuncia);
CREATE INDEX idx_comunicacion_fecha ON Comunicacion(fecha_envio);
CREATE INDEX idx_comunicacion_leido ON Comunicacion(es_leido);

COMMENT ON TABLE Comunicacion IS 'Mensajes intercambiados entre personal y ciudadanos';

-- ============================================
-- MÓDULO 3: NOTIFICACIONES
-- ============================================

-- Tabla: PlantillaNotificacion
CREATE TABLE PlantillaNotificacion (
    id_plantilla SERIAL PRIMARY KEY,
    codigo_plantilla VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    tipo_evento VARCHAR(50) NOT NULL,
    asunto VARCHAR(200) NOT NULL,
    cuerpo_mensaje TEXT NOT NULL,
    variables TEXT,
    esta_activa BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT chk_tipo_evento CHECK (tipo_evento IN ('Registro', 'Actualización', 'Asignación', 'Resolución', 'Rechazo', 'Comentario'))
);

CREATE INDEX idx_plantilla_tipo_evento ON PlantillaNotificacion(tipo_evento);
CREATE INDEX idx_plantilla_activa ON PlantillaNotificacion(esta_activa);

COMMENT ON TABLE PlantillaNotificacion IS 'Plantilla predefinida para generar notificaciones';
COMMENT ON COLUMN PlantillaNotificacion.variables IS 'Variables disponibles en formato JSON';

-- Tabla: Notificacion
CREATE TABLE Notificacion (
    id_notificacion SERIAL PRIMARY KEY,
    codigo_notificacion VARCHAR(20) UNIQUE NOT NULL,
    tipo_notificacion VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_envio TIMESTAMP,
    canal_envio VARCHAR(20) NOT NULL,
    estado_envio VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    mensaje_personalizado TEXT NOT NULL,
    intento_envio INTEGER NOT NULL DEFAULT 1,
    id_denuncia INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_plantilla INTEGER NOT NULL,
    
    CONSTRAINT fk_notificacion_denuncia FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    CONSTRAINT fk_notificacion_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_notificacion_plantilla FOREIGN KEY (id_plantilla) REFERENCES PlantillaNotificacion(id_plantilla),
    CONSTRAINT chk_canal_envio CHECK (canal_envio IN ('Email', 'SMS', 'Push', 'Interno')),
    CONSTRAINT chk_estado_envio CHECK (estado_envio IN ('Pendiente', 'Enviado', 'Entregado', 'Fallido', 'Leído')),
    CONSTRAINT chk_intento_positivo CHECK (intento_envio > 0)
);

CREATE INDEX idx_notificacion_usuario ON Notificacion(id_usuario);
CREATE INDEX idx_notificacion_denuncia ON Notificacion(id_denuncia);
CREATE INDEX idx_notificacion_estado ON Notificacion(estado_envio);
CREATE INDEX idx_notificacion_canal ON Notificacion(canal_envio);

COMMENT ON TABLE Notificacion IS 'Mensaje enviado a usuarios sobre eventos del sistema';

-- Tabla: ConfiguracionNotificacion
CREATE TABLE ConfiguracionNotificacion (
    id_configuracion SERIAL PRIMARY KEY,
    codigo_configuracion VARCHAR(20) UNIQUE NOT NULL,
    recibir_email BOOLEAN NOT NULL DEFAULT TRUE,
    recibir_sms BOOLEAN NOT NULL DEFAULT FALSE,
    recibir_push BOOLEAN NOT NULL DEFAULT TRUE,
    frecuencia_resumen VARCHAR(20) NOT NULL DEFAULT 'Diario',
    horario_preferido VARCHAR(50),
    id_usuario INTEGER UNIQUE NOT NULL,
    
    CONSTRAINT fk_configuracion_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT chk_frecuencia_resumen CHECK (frecuencia_resumen IN ('Inmediato', 'Diario', 'Semanal', 'Ninguno'))
);

COMMENT ON TABLE ConfiguracionNotificacion IS 'Preferencias de notificación por usuario';

-- ============================================
-- MÓDULO 4: ADMINISTRATIVO
-- ============================================

-- Tabla: Rol
CREATE TABLE Rol (
    id_rol SERIAL PRIMARY KEY,
    codigo_rol VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(500),
    nivel INTEGER NOT NULL,
    es_sistema BOOLEAN NOT NULL DEFAULT TRUE,
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT chk_nivel_positivo CHECK (nivel > 0)
);

CREATE INDEX idx_rol_activo ON Rol(esta_activo);
CREATE INDEX idx_rol_nivel ON Rol(nivel);

COMMENT ON TABLE Rol IS 'Rol de usuario en el sistema con permisos específicos (RBAC)';

-- Tabla: Permiso
CREATE TABLE Permiso (
    id_permiso SERIAL PRIMARY KEY,
    codigo_permiso VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(500),
    modulo VARCHAR(50) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    recurso VARCHAR(50) NOT NULL,
    
    CONSTRAINT chk_accion_permiso CHECK (accion IN ('Crear', 'Leer', 'Actualizar', 'Eliminar', 'Ejecutar'))
);

CREATE INDEX idx_permiso_modulo ON Permiso(modulo);
CREATE INDEX idx_permiso_accion ON Permiso(accion);

COMMENT ON TABLE Permiso IS 'Permiso específico para realizar acciones en el sistema';

-- Tabla: UsuarioRol (Relación N:M)
CREATE TABLE UsuarioRol (
    id_usuario INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    es_activo BOOLEAN NOT NULL DEFAULT TRUE,
    
    CONSTRAINT pk_usuario_rol PRIMARY KEY (id_usuario, id_rol),
    CONSTRAINT fk_usuario_rol_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_usuario_rol_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE CASCADE
);

CREATE INDEX idx_usuario_rol_usuario ON UsuarioRol(id_usuario);
CREATE INDEX idx_usuario_rol_rol ON UsuarioRol(id_rol);

COMMENT ON TABLE UsuarioRol IS 'Relación entre usuarios y roles (N:M)';

-- Tabla: RolPermiso (Relación N:M)
CREATE TABLE RolPermiso (
    id_rol INTEGER NOT NULL,
    id_permiso INTEGER NOT NULL,
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_rol_permiso PRIMARY KEY (id_rol, id_permiso),
    CONSTRAINT fk_rol_permiso_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE CASCADE,
    CONSTRAINT fk_rol_permiso_permiso FOREIGN KEY (id_permiso) REFERENCES Permiso(id_permiso) ON DELETE CASCADE
);

CREATE INDEX idx_rol_permiso_rol ON RolPermiso(id_rol);
CREATE INDEX idx_rol_permiso_permiso ON RolPermiso(id_permiso);

COMMENT ON TABLE RolPermiso IS 'Relación entre roles y permisos (N:M)';

-- Tabla: Sesion
CREATE TABLE Sesion (
    id_sesion SERIAL PRIMARY KEY,
    codigo_sesion VARCHAR(20) UNIQUE NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    direccion_ip VARCHAR(45) NOT NULL,
    user_agent VARCHAR(500) NOT NULL,
    esta_activa BOOLEAN NOT NULL DEFAULT TRUE,
    ultima_actividad TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    
    CONSTRAINT fk_sesion_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT chk_fechas_sesion CHECK (fecha_expiracion > fecha_inicio)
);

CREATE INDEX idx_sesion_usuario ON Sesion(id_usuario);
CREATE INDEX idx_sesion_activa ON Sesion(esta_activa);
CREATE INDEX idx_sesion_expiracion ON Sesion(fecha_expiracion);

COMMENT ON TABLE Sesion IS 'Sesión activa de un usuario en el sistema';

-- Tabla: LogAuditoria
CREATE TABLE LogAuditoria (
    id_log SERIAL PRIMARY KEY,
    codigo_log VARCHAR(20) UNIQUE NOT NULL,
    tipo_accion VARCHAR(50) NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    entidad VARCHAR(50) NOT NULL,
    entidad_id VARCHAR(36) NOT NULL,
    fecha_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    direccion_ip VARCHAR(45) NOT NULL,
    datos_antes TEXT,
    datos_despues TEXT,
    resultado VARCHAR(20) NOT NULL,
    mensaje_error TEXT,
    id_usuario INTEGER NOT NULL,
    
    CONSTRAINT fk_log_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT chk_tipo_accion_log CHECK (tipo_accion IN ('CREAR', 'LEER', 'ACTUALIZAR', 'ELIMINAR', 'LOGIN', 'LOGOUT', 'CAMBIO_ESTADO')),
    CONSTRAINT chk_resultado_log CHECK (resultado IN ('Exitoso', 'Fallido', 'Advertencia'))
);

CREATE INDEX idx_log_usuario ON LogAuditoria(id_usuario);
CREATE INDEX idx_log_fecha ON LogAuditoria(fecha_hora);
CREATE INDEX idx_log_tipo_accion ON LogAuditoria(tipo_accion);
CREATE INDEX idx_log_modulo ON LogAuditoria(modulo);
CREATE INDEX idx_log_entidad ON LogAuditoria(entidad, entidad_id);

COMMENT ON TABLE LogAuditoria IS 'Registro inmutable de todas las acciones críticas (conservar 5+ años)';

-- ============================================
-- MÓDULO 5: REPORTES Y ESTADÍSTICAS
-- ============================================

-- Tabla: Reporte
CREATE TABLE Reporte (
    id_reporte SERIAL PRIMARY KEY,
    codigo_reporte VARCHAR(20) UNIQUE NOT NULL,
    tipo_reporte VARCHAR(50) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_generacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    formato_exportacion VARCHAR(10) NOT NULL,
    ruta_archivo VARCHAR(500) UNIQUE,
    es_publico BOOLEAN NOT NULL DEFAULT FALSE,
    id_usuario_generador INTEGER NOT NULL,
    
    CONSTRAINT fk_reporte_usuario FOREIGN KEY (id_usuario_generador) REFERENCES Usuario(id_usuario),
    CONSTRAINT chk_tipo_reporte CHECK (tipo_reporte IN ('Ejecutivo', 'Operativo', 'Estadístico', 'Auditoria')),
    CONSTRAINT chk_formato_exportacion CHECK (formato_exportacion IN ('PDF', 'Excel', 'CSV', 'JSON')),
    CONSTRAINT chk_fechas_reporte CHECK (fecha_fin >= fecha_inicio)
);

CREATE INDEX idx_reporte_tipo ON Reporte(tipo_reporte);
CREATE INDEX idx_reporte_fecha_generacion ON Reporte(fecha_generacion);
CREATE INDEX idx_reporte_periodo ON Reporte(fecha_inicio, fecha_fin);

COMMENT ON TABLE Reporte IS 'Documento que consolida información analítica del sistema';

-- Tabla: Estadistica
CREATE TABLE Estadistica (
    id_estadistica SERIAL PRIMARY KEY,
    codigo_estadistica VARCHAR(20) UNIQUE NOT NULL,
    tipo_metrica VARCHAR(50) NOT NULL,
    valor NUMERIC(10,2) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,
    periodo VARCHAR(20) NOT NULL,
    fecha_calculo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    categoria VARCHAR(100),
    area VARCHAR(100),
    zona VARCHAR(100),
    
    CONSTRAINT chk_periodo_estadistica CHECK (periodo IN ('Diario', 'Semanal', 'Mensual', 'Trimestral', 'Anual'))
);

CREATE INDEX idx_estadistica_tipo_metrica ON Estadistica(tipo_metrica);
CREATE INDEX idx_estadistica_periodo ON Estadistica(periodo);
CREATE INDEX idx_estadistica_fecha ON Estadistica(fecha_calculo);
CREATE INDEX idx_estadistica_categoria ON Estadistica(categoria);

COMMENT ON TABLE Estadistica IS 'Métricas y datos estadísticos del sistema (KPIs)';

-- Tabla: Indicador
CREATE TABLE Indicador (
    id_indicador SERIAL PRIMARY KEY,
    codigo_indicador VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    formula VARCHAR(500) NOT NULL,
    valor_minimo NUMERIC(10,2),
    valor_maximo NUMERIC(10,2),
    valor_actual NUMERIC(10,2),
    frecuencia_actualizacion VARCHAR(20) NOT NULL,
    tipo_visualizacion VARCHAR(20) NOT NULL,
    
    CONSTRAINT chk_frecuencia_indicador CHECK (frecuencia_actualizacion IN ('Tiempo real', 'Diario', 'Semanal', 'Mensual')),
    CONSTRAINT chk_tipo_visualizacion CHECK (tipo_visualizacion IN ('Gauge', 'LineChart', 'BarChart', 'PieChart', 'Number'))
);

CREATE INDEX idx_indicador_frecuencia ON Indicador(frecuencia_actualizacion);

COMMENT ON TABLE Indicador IS 'Indicador de desempeño o KPI del sistema';

-- Tabla: Dashboard
CREATE TABLE Dashboard (
    id_dashboard SERIAL PRIMARY KEY,
    codigo_dashboard VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    tipo_dashboard VARCHAR(50) NOT NULL,
    frecuencia_actualizacion VARCHAR(20) NOT NULL,
    es_publico BOOLEAN NOT NULL DEFAULT FALSE,
    orden_visualizacion INTEGER,
    
    CONSTRAINT chk_tipo_dashboard CHECK (tipo_dashboard IN ('Ejecutivo', 'Operativo', 'Ciudadano', 'Analítico')),
    CONSTRAINT chk_frecuencia_dashboard CHECK (frecuencia_actualizacion IN ('Tiempo real', 'Diario', 'Semanal'))
);

CREATE INDEX idx_dashboard_tipo ON Dashboard(tipo_dashboard);
CREATE INDEX idx_dashboard_publico ON Dashboard(es_publico);

COMMENT ON TABLE Dashboard IS 'Panel de control con visualización de indicadores';

-- Tabla: DashboardIndicador (Relación N:M)
CREATE TABLE DashboardIndicador (
    id_dashboard INTEGER NOT NULL,
    id_indicador INTEGER NOT NULL,
    orden INTEGER NOT NULL,
    tipo_visualizacion VARCHAR(20) NOT NULL,
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_dashboard_indicador PRIMARY KEY (id_dashboard, id_indicador),
    CONSTRAINT fk_dashboard_indicador_dashboard FOREIGN KEY (id_dashboard) REFERENCES Dashboard(id_dashboard) ON DELETE CASCADE,
    CONSTRAINT fk_dashboard_indicador_indicador FOREIGN KEY (id_indicador) REFERENCES Indicador(id_indicador) ON DELETE CASCADE,
    CONSTRAINT chk_orden_positivo CHECK (orden > 0)
);

CREATE INDEX idx_dashboard_indicador_dashboard ON DashboardIndicador(id_dashboard);
CREATE INDEX idx_dashboard_indicador_indicador ON DashboardIndicador(id_indicador);

COMMENT ON TABLE DashboardIndicador IS 'Relación entre dashboards e indicadores con configuración';

-- Tabla: TendenciaGeografica
CREATE TABLE TendenciaGeografica (
    id_tendencia SERIAL PRIMARY KEY,
    codigo_tendencia VARCHAR(20) UNIQUE NOT NULL,
    zona VARCHAR(100) NOT NULL,
    distrito VARCHAR(100) NOT NULL,
    cantidad_denuncias INTEGER NOT NULL,
    categoria_mas_frecuente VARCHAR(100) NOT NULL,
    tasa_resolucion NUMERIC(5,2) NOT NULL,
    tiempo_promedio_atencion NUMERIC(10,2) NOT NULL,
    periodo_analisis VARCHAR(20) NOT NULL,
    nivel_criticidad VARCHAR(20) NOT NULL,
    
    CONSTRAINT chk_cantidad_positiva CHECK (cantidad_denuncias >= 0),
    CONSTRAINT chk_tasa_resolucion_rango CHECK (tasa_resolucion BETWEEN 0 AND 100),
    CONSTRAINT chk_tiempo_promedio_positivo CHECK (tiempo_promedio_atencion >= 0),
    CONSTRAINT chk_nivel_criticidad CHECK (nivel_criticidad IN ('Bajo', 'Medio', 'Alto', 'Crítico'))
);

CREATE INDEX idx_tendencia_zona ON TendenciaGeografica(zona);
CREATE INDEX idx_tendencia_distrito ON TendenciaGeografica(distrito);
CREATE INDEX idx_tendencia_periodo ON TendenciaGeografica(periodo_analisis);
CREATE INDEX idx_tendencia_criticidad ON TendenciaGeografica(nivel_criticidad);

COMMENT ON TABLE TendenciaGeografica IS 'Análisis de tendencias por zona geográfica';

-- Tabla: RankingDesempeno
CREATE TABLE RankingDesempeno (
    id_ranking SERIAL PRIMARY KEY,
    codigo_ranking VARCHAR(20) UNIQUE NOT NULL,
    periodo_evaluacion VARCHAR(20) NOT NULL,
    posicion INTEGER NOT NULL,
    puntaje_total NUMERIC(5,2) NOT NULL,
    denuncias_atendidas INTEGER NOT NULL,
    tasa_resolucion_area NUMERIC(5,2) NOT NULL,
    tiempo_promedio_area NUMERIC(10,2) NOT NULL,
    calificacion_promedio NUMERIC(3,2),
    id_area_responsable INTEGER NOT NULL,
    
    CONSTRAINT fk_ranking_area FOREIGN KEY (id_area_responsable) REFERENCES AreaResponsable(id_area_responsable),
    CONSTRAINT uq_area_periodo UNIQUE (id_area_responsable, periodo_evaluacion),
    CONSTRAINT chk_posicion_positiva CHECK (posicion > 0),
    CONSTRAINT chk_puntaje_rango CHECK (puntaje_total BETWEEN 0 AND 100),
    CONSTRAINT chk_tasa_resolucion_ranking CHECK (tasa_resolucion_area BETWEEN 0 AND 100),
    CONSTRAINT chk_calificacion_ranking CHECK (calificacion_promedio IS NULL OR (calificacion_promedio BETWEEN 0 AND 5))
);

CREATE INDEX idx_ranking_periodo ON RankingDesempeno(periodo_evaluacion);
CREATE INDEX idx_ranking_posicion ON RankingDesempeno(posicion);

COMMENT ON TABLE RankingDesempeno IS 'Ranking de desempeño de áreas responsables';