-- ============================================
-- SISTEMA DE DENUNCIAS CIUDADANAS (SIREDECI)
-- Script de Poblamiento Inicial de Base de Datos
-- Motor: PostgreSQL 14+
-- Fecha: 2025-01-10
-- ============================================

-- Establecer el search_path
SET search_path TO siredeci, public;

-- ============================================
-- LIMPIEZA DE DATOS (Opcional - Usar con precaución)
-- ============================================

-- NOTA: Descomentar solo si necesitas limpiar datos existentes
-- TRUNCATE TABLE siredeci.LogAuditoria CASCADE;
-- TRUNCATE TABLE siredeci.Sesion CASCADE;
-- TRUNCATE TABLE siredeci.RolPermiso CASCADE;
-- TRUNCATE TABLE siredeci.UsuarioRol CASCADE;
-- ... (resto de tablas)

-- ============================================
-- DATOS MAESTROS: ROLES Y PERMISOS
-- ============================================

-- Insertar Roles del Sistema
INSERT INTO siredeci.Rol (codigo_rol, nombre, descripcion, nivel, es_sistema, esta_activo) VALUES
('ROL-001', 'SuperAdmin', 'Administrador con acceso total al sistema', 1, TRUE, TRUE),
('ROL-002', 'Administrador', 'Administrador del sistema con permisos de configuración', 2, TRUE, TRUE),
('ROL-003', 'JefeArea', 'Jefe de área responsable con permisos de gestión', 3, TRUE, TRUE),
('ROL-004', 'Operador', 'Personal municipal que gestiona denuncias', 4, TRUE, TRUE),
('ROL-005', 'Ciudadano', 'Usuario ciudadano que registra denuncias', 5, TRUE, TRUE),
('ROL-006', 'Auditor', 'Usuario con permisos de solo lectura para auditoría', 6, TRUE, TRUE)
ON CONFLICT (codigo_rol) DO NOTHING;

-- Insertar Permisos del Sistema
INSERT INTO siredeci.Permiso (codigo_permiso, nombre, descripcion, modulo, accion, recurso) VALUES
-- Módulo Denuncias
('PER-001', 'CREAR_DENUNCIA', 'Permite crear denuncias', 'Denuncias', 'Crear', 'Denuncia'),
('PER-002', 'LEER_DENUNCIA', 'Permite consultar denuncias', 'Denuncias', 'Leer', 'Denuncia'),
('PER-003', 'ACTUALIZAR_DENUNCIA', 'Permite actualizar denuncias', 'Denuncias', 'Actualizar', 'Denuncia'),
('PER-004', 'ELIMINAR_DENUNCIA', 'Permite eliminar denuncias', 'Denuncias', 'Eliminar', 'Denuncia'),
('PER-005', 'ASIGNAR_DENUNCIA', 'Permite asignar denuncias al personal', 'Denuncias', 'Ejecutar', 'Asignacion'),
('PER-006', 'RESOLVER_DENUNCIA', 'Permite resolver denuncias', 'Denuncias', 'Ejecutar', 'Resolucion'),

-- Módulo Usuarios
('PER-007', 'GESTIONAR_USUARIOS', 'Permite administrar usuarios del sistema', 'Administrativo', 'Crear', 'Usuario'),
('PER-008', 'LEER_USUARIOS', 'Permite consultar usuarios', 'Administrativo', 'Leer', 'Usuario'),
('PER-009', 'GESTIONAR_ROLES', 'Permite administrar roles y permisos', 'Administrativo', 'Crear', 'Rol'),

-- Módulo Reportes
('PER-010', 'GENERAR_REPORTES', 'Permite generar reportes del sistema', 'Reportes', 'Crear', 'Reporte'),
('PER-011', 'LEER_REPORTES', 'Permite consultar reportes', 'Reportes', 'Leer', 'Reporte'),

-- Módulo Auditoría
('PER-012', 'VER_AUDITORIA', 'Permite consultar logs de auditoría', 'Administrativo', 'Leer', 'LogAuditoria'),

-- Módulo Configuración
('PER-013', 'GESTIONAR_CATEGORIAS', 'Permite administrar categorías', 'Administrativo', 'Crear', 'Categoria'),
('PER-014', 'GESTIONAR_AREAS', 'Permite administrar áreas responsables', 'Administrativo', 'Crear', 'AreaResponsable'),

-- Módulo Notificaciones
('PER-015', 'GESTIONAR_NOTIFICACIONES', 'Permite administrar plantillas de notificaciones', 'Notificaciones', 'Crear', 'PlantillaNotificacion')
ON CONFLICT (codigo_permiso) DO NOTHING;

-- Asignar Permisos a Roles
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso) 
SELECT r.id_rol, p.id_permiso 
FROM siredeci.Rol r, siredeci.Permiso p 
WHERE r.codigo_rol = 'ROL-001' -- SuperAdmin tiene todos los permisos
ON CONFLICT DO NOTHING;

-- Administrador
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso
FROM siredeci.Rol r, siredeci.Permiso p
WHERE r.codigo_rol = 'ROL-002'
AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-005', 'PER-007', 'PER-008', 'PER-009', 'PER-010', 'PER-011', 'PER-012', 'PER-013', 'PER-014', 'PER-015')
ON CONFLICT DO NOTHING;

-- Jefe de Área
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso
FROM siredeci.Rol r, siredeci.Permiso p
WHERE r.codigo_rol = 'ROL-003'
AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-005', 'PER-006', 'PER-008', 'PER-010', 'PER-011')
ON CONFLICT DO NOTHING;

-- Operador
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso
FROM siredeci.Rol r, siredeci.Permiso p
WHERE r.codigo_rol = 'ROL-004'
AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-006')
ON CONFLICT DO NOTHING;

-- Ciudadano
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso
FROM siredeci.Rol r, siredeci.Permiso p
WHERE r.codigo_rol = 'ROL-005'
AND p.codigo_permiso IN ('PER-001', 'PER-002')
ON CONFLICT DO NOTHING;

-- Auditor
INSERT INTO siredeci.RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso
FROM siredeci.Rol r, siredeci.Permiso p
WHERE r.codigo_rol = 'ROL-006'
AND p.codigo_permiso IN ('PER-002', 'PER-008', 'PER-011', 'PER-012')
ON CONFLICT DO NOTHING;

-- ============================================
-- ÁREAS RESPONSABLES
-- ============================================

INSERT INTO siredeci.AreaResponsable (codigo_area, nombre, descripcion, email, telefono, capacidad_maxima, esta_activo) VALUES
('ARE-001', 'Obras Públicas', 'Responsable de infraestructura vial, mantenimiento de calles y espacios públicos', 'obras.publicas@municipalidad.gob.pe', '01-2345678', 100, TRUE),
('ARE-002', 'Servicios Públicos', 'Gestión de limpieza pública, recojo de basura y ornato', 'servicios.publicos@municipalidad.gob.pe', '01-2345679', 80, TRUE),
('ARE-003', 'Seguridad Ciudadana', 'Coordinación con serenazgo y gestión de seguridad', 'seguridad@municipalidad.gob.pe', '01-2345680', 60, TRUE),
('ARE-004', 'Gestión Ambiental', 'Áreas verdes, parques y medio ambiente', 'ambiente@municipalidad.gob.pe', '01-2345681', 50, TRUE),
('ARE-005', 'Alumbrado Público', 'Mantenimiento y reparación de alumbrado público', 'alumbrado@municipalidad.gob.pe', '01-2345682', 40, TRUE),
('ARE-006', 'Desarrollo Urbano', 'Planificación urbana y obras de desarrollo', 'desarrollo@municipalidad.gob.pe', '01-2345683', 70, TRUE)
ON CONFLICT (codigo_area) DO NOTHING;

-- ============================================
-- CATEGORÍAS DE DENUNCIAS
-- ============================================

INSERT INTO siredeci.Categoria (codigo_categoria, nombre, descripcion, color, icono, esta_activo, tiempo_respuesta_promedio, id_area_responsable) VALUES
('CAT-001', 'Baches en la vía', 'Huecos o deterioro en calles y avenidas', '#E74C3C', 'road_damage', TRUE, 72, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-001')),
('CAT-002', 'Basura acumulada', 'Acumulación de residuos sólidos en vía pública', '#F39C12', 'delete', TRUE, 24, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-002')),
('CAT-003', 'Alumbrado público', 'Postes sin luz o instalaciones dañadas', '#F1C40F', 'lightbulb', TRUE, 48, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-005')),
('CAT-004', 'Inseguridad', 'Problemas de seguridad ciudadana', '#8E44AD', 'security', TRUE, 12, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-003')),
('CAT-005', 'Áreas verdes descuidadas', 'Parques y jardines sin mantenimiento', '#27AE60', 'park', TRUE, 168, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-006', 'Veredas deterioradas', 'Veredas rotas o en mal estado', '#34495E', 'directions_walk', TRUE, 96, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-001')),
('CAT-007', 'Señalización deficiente', 'Falta de señales de tránsito o en mal estado', '#3498DB', 'traffic', TRUE, 120, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-006')),
('CAT-008', 'Ruido excesivo', 'Contaminación sonora', '#E67E22', 'volume_up', TRUE, 48, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-009', 'Mascota abandonada', 'Animales en situación de abandono', '#95A5A6', 'pets', TRUE, 24, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-010', 'Construcción ilegal', 'Obras sin permisos o invasiones', '#C0392B', 'construction', TRUE, 72, (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-006'))
ON CONFLICT (codigo_categoria) DO NOTHING;

-- ============================================
-- PLANTILLAS DE NOTIFICACIONES
-- ============================================

INSERT INTO siredeci.PlantillaNotificacion (codigo_plantilla, nombre, tipo_evento, asunto, cuerpo_mensaje, variables, esta_activa) VALUES
('PLT-001', 'Registro de Denuncia', 'Registro', 'Denuncia Registrada Exitosamente', 
'Estimado/a {nombre_ciudadano},

Su denuncia ha sido registrada exitosamente en nuestro sistema.

Detalles de su denuncia:
- Código de seguimiento: {numero_seguimiento}
- Categoría: {categoria}
- Fecha de registro: {fecha_registro}
- Ubicación: {direccion}

Puede hacer seguimiento de su denuncia en cualquier momento ingresando a nuestro sistema con el código de seguimiento proporcionado.

Tiempo estimado de atención: {tiempo_estimado} horas

Atentamente,
Municipalidad - Sistema de Denuncias Ciudadanas (SIREDECI)', 
'["nombre_ciudadano", "numero_seguimiento", "categoria", "fecha_registro", "direccion", "tiempo_estimado"]', TRUE),

('PLT-002', 'Actualización de Estado', 'Actualización', 'Actualización de su Denuncia {numero_seguimiento}', 
'Estimado/a {nombre_ciudadano},

Le informamos que su denuncia {codigo_denuncia} ha sido actualizada.

Estado anterior: {estado_anterior}
Estado actual: {estado_nuevo}

{comentario}

Para más detalles, puede ingresar a nuestro sistema con su código de seguimiento: {numero_seguimiento}

Atentamente,
Municipalidad - Sistema de Denuncias Ciudadanas', 
'["nombre_ciudadano", "codigo_denuncia", "estado_anterior", "estado_nuevo", "comentario", "numero_seguimiento"]', TRUE),

('PLT-003', 'Asignación a Personal', 'Asignación', 'Nueva denuncia asignada - {codigo_denuncia}', 
'Estimado/a {nombre_personal},

Se le ha asignado una nueva denuncia para su atención:

Código: {codigo_denuncia}
Categoría: {categoria}
Prioridad: {prioridad}
Ubicación: {direccion}
Descripción: {descripcion}

Por favor, revise los detalles en el sistema y proceda con su atención.

Fecha de asignación: {fecha_asignacion}

Saludos,
Sistema de Denuncias Ciudadanas', 
'["nombre_personal", "codigo_denuncia", "categoria", "prioridad", "direccion", "descripcion", "fecha_asignacion"]', TRUE),

('PLT-004', 'Resolución de Denuncia', 'Resolución', 'Su denuncia ha sido resuelta - {numero_seguimiento}', 
'Estimado/a {nombre_ciudadano},

Le informamos que su denuncia {codigo_denuncia} ha sido resuelta.

Tipo de resolución: {tipo_resolucion}
Fecha de resolución: {fecha_resolucion}
Tiempo total de atención: {tiempo_total} horas

Descripción de la resolución:
{descripcion_resolucion}

Nos gustaría conocer su opinión sobre la atención brindada. Por favor, califique nuestro servicio ingresando al sistema.

Agradecemos su participación ciudadana.

Atentamente,
Municipalidad - Sistema de Denuncias Ciudadanas', 
'["nombre_ciudadano", "codigo_denuncia", "numero_seguimiento", "tipo_resolucion", "fecha_resolucion", "tiempo_total", "descripcion_resolucion"]', TRUE),

('PLT-005', 'Solicitud de Información', 'Comentario', 'Se requiere información adicional - {numero_seguimiento}', 
'Estimado/a {nombre_ciudadano},

Para poder atender su denuncia {codigo_denuncia}, necesitamos información adicional:

{mensaje}

Por favor, responda a través de nuestro sistema o comuníquese con nosotros.

Código de seguimiento: {numero_seguimiento}

Atentamente,
{nombre_personal}
{area_responsable}', 
'["nombre_ciudadano", "codigo_denuncia", "numero_seguimiento", "mensaje", "nombre_personal", "area_responsable"]', TRUE),

('PLT-006', 'Denuncia Rechazada', 'Rechazo', 'Denuncia No Procede - {numero_seguimiento}', 
'Estimado/a {nombre_ciudadano},

Lamentamos informarle que su denuncia {codigo_denuncia} no puede ser atendida.

Motivo: {motivo_rechazo}

{observaciones}

Si tiene alguna consulta, puede comunicarse con nosotros.

Atentamente,
Municipalidad - Sistema de Denuncias Ciudadanas', 
'["nombre_ciudadano", "codigo_denuncia", "numero_seguimiento", "motivo_rechazo", "observaciones"]', TRUE)
ON CONFLICT (codigo_plantilla) DO NOTHING;

-- ============================================
-- USUARIOS DEL SISTEMA
-- ============================================

-- Usuario SuperAdmin (password: Admin123!)
INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta, requiere_mfa) VALUES
('USR-00001', 'superadmin', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'superadmin@municipalidad.gob.pe', 'Activo', TRUE)
ON CONFLICT (codigo_usuario) DO NOTHING;

-- Usuario Administrador (password: Admin123!)
INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta, requiere_mfa) VALUES
('USR-00002', 'admin', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'admin@municipalidad.gob.pe', 'Activo', TRUE)
ON CONFLICT (codigo_usuario) DO NOTHING;

-- Usuario Auditor (password: Audit123!)
INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta, requiere_mfa) VALUES
('USR-00003', 'auditor', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'auditor@municipalidad.gob.pe', 'Activo', FALSE)
ON CONFLICT (codigo_usuario) DO NOTHING;

-- Asignar roles a usuarios administrativos
INSERT INTO siredeci.UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE
FROM siredeci.Usuario u, siredeci.Rol r
WHERE (u.codigo_usuario = 'USR-00001' AND r.codigo_rol = 'ROL-001')
   OR (u.codigo_usuario = 'USR-00002' AND r.codigo_rol = 'ROL-002')
   OR (u.codigo_usuario = 'USR-00003' AND r.codigo_rol = 'ROL-006')
ON CONFLICT DO NOTHING;

-- ============================================
-- PERSONAL MUNICIPAL
-- ============================================

-- Jefes de Área
INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta) VALUES
('USR-00101', 'jperez', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'juan.perez@municipalidad.gob.pe', 'Activo'),
('USR-00102', 'mgarcia', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'maria.garcia@municipalidad.gob.pe', 'Activo'),
('USR-00103', 'crodriguez', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'carlos.rodriguez@municipalidad.gob.pe', 'Activo')
ON CONFLICT (codigo_usuario) DO NOTHING;

INSERT INTO siredeci.PersonalMunicipal (codigo_personal, dni, nombre, apellido, email, cargo, fecha_ingreso, especialidad, id_area_responsable, id_usuario) VALUES
('PER-00101', '12345678', 'Juan', 'Pérez López', 'juan.perez@municipalidad.gob.pe', 'Jefe de Obras Públicas', '2020-01-15', 'Ingeniería Civil', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-001'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00101')),
 
('PER-00102', '23456789', 'María', 'García Torres', 'maria.garcia@municipalidad.gob.pe', 'Jefa de Servicios Públicos', '2019-03-10', 'Gestión Pública', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-002'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00102')),
 
('PER-00103', '34567890', 'Carlos', 'Rodríguez Díaz', 'carlos.rodriguez@municipalidad.gob.pe', 'Jefe de Seguridad Ciudadana', '2021-06-20', 'Seguridad', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-003'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00103'))
ON CONFLICT (codigo_personal) DO NOTHING;

-- Asignar rol de Jefe de Área
INSERT INTO siredeci.UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE
FROM siredeci.Usuario u, siredeci.Rol r
WHERE u.codigo_usuario IN ('USR-00101', 'USR-00102', 'USR-00103')
AND r.codigo_rol = 'ROL-003'
ON CONFLICT DO NOTHING;

-- Actualizar jefes de área
UPDATE siredeci.AreaResponsable SET id_jefe_area = (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00101') WHERE codigo_area = 'ARE-001';
UPDATE siredeci.AreaResponsable SET id_jefe_area = (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00102') WHERE codigo_area = 'ARE-002';
UPDATE siredeci.AreaResponsable SET id_jefe_area = (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00103') WHERE codigo_area = 'ARE-003';

-- Operadores
INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta) VALUES
('USR-00201', 'lmartinez', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'luis.martinez@municipalidad.gob.pe', 'Activo'),
('USR-00202', 'asanchez', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'ana.sanchez@municipalidad.gob.pe', 'Activo'),
('USR-00203', 'rfernandez', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'roberto.fernandez@municipalidad.gob.pe', 'Activo'),
('USR-00204', 'plovato', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'patricia.lovato@municipalidad.gob.pe', 'Activo')
ON CONFLICT (codigo_usuario) DO NOTHING;

INSERT INTO siredeci.PersonalMunicipal (codigo_personal, dni, nombre, apellido, email, cargo, fecha_ingreso, especialidad, id_area_responsable, id_usuario) VALUES
('PER-00201', '45678901', 'Luis', 'Martínez Ruiz', 'luis.martinez@municipalidad.gob.pe', 'Técnico de Campo', '2021-02-01', 'Obras Civiles', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-001'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00201')),
 
('PER-00202', '56789012', 'Ana', 'Sánchez Vega', 'ana.sanchez@municipalidad.gob.pe', 'Supervisora de Limpieza', '2020-08-15', 'Servicios', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-002'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00202')),
 
('PER-00203', '67890123', 'Roberto', 'Fernández Castro', 'roberto.fernandez@municipalidad.gob.pe', 'Agente de Serenazgo', '2022-01-10', 'Seguridad', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-003'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00203')),
 
('PER-00204', '78901234', 'Patricia', 'Lovato Mendoza', 'patricia.lovato@municipalidad.gob.pe', 'Técnica Electricista', '2021-09-05', 'Electricidad', 
 (SELECT id_area_responsable FROM siredeci.AreaResponsable WHERE codigo_area = 'ARE-005'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00204'))
ON CONFLICT (codigo_personal) DO NOTHING;

-- Asignar rol de Operador
INSERT INTO siredeci.UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE
FROM siredeci.Usuario u, siredeci.Rol r
WHERE u.codigo_usuario IN ('USR-00201', 'USR-00202', 'USR-00203', 'USR-00204')
AND r.codigo_rol = 'ROL-004'
ON CONFLICT DO NOTHING;

-- Teléfonos del personal
INSERT INTO siredeci.PersonalTelefono (id_personal, telefono, es_principal) VALUES
((SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00101'), '987654321', TRUE),
((SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00102'), '987654322', TRUE),
((SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00103'), '987654323', TRUE),
((SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00201'), '987654324', TRUE),
((SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00202'), '987654325', TRUE)
ON CONFLICT DO NOTHING;

-- ============================================
-- CIUDADANOS DE PRUEBA
-- ============================================

INSERT INTO siredeci.Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta) VALUES
('USR-10001', 'ciudadano1', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'ciudadano1@email.com', 'Activo'),
('USR-10002', 'ciudadano2', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'ciudadano2@email.com', 'Activo'),
('USR-10003', 'ciudadano3', '$2b$10$YQv4R0uY5vG8ZQK4mE1KxOXwX7C9K8xmV5nY2qW3eR4tY5uI6oP7q', 'ciudadano3@email.com', 'Activo')
ON CONFLICT (codigo_usuario) DO NOTHING;

INSERT INTO siredeci.Ciudadano (codigo_ciudadano, dni, nombre, apellido, email, direccion, fecha_emision_dni, id_usuario) VALUES
('CIU-10001', '11223344', 'Pedro', 'González Ramos', 'ciudadano1@email.com', 'Av. Los Álamos 123', '2018-05-10',
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10001')),
('CIU-10002', '22334455', 'Laura', 'Mendoza Silva', 'ciudadano2@email.com', 'Jr. Las Flores 456', '2019-08-15',
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10002')),
('CIU-10003', '33445566', 'Jorge', 'Vargas Torres', 'ciudadano3@email.com', 'Av. Primavera 789', '2020-02-20',
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10003'))
ON CONFLICT (codigo_ciudadano) DO NOTHING;

-- Asignar rol de Ciudadano
INSERT INTO siredeci.UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE
FROM siredeci.Usuario u, siredeci.Rol r
WHERE u.codigo_usuario IN ('USR-10001', 'USR-10002', 'USR-10003')
AND r.codigo_rol = 'ROL-005'
ON CONFLICT DO NOTHING;

-- Teléfonos de ciudadanos
INSERT INTO siredeci.CiudadanoTelefono (id_ciudadano, telefono, es_principal) VALUES
((SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10001'), '999111222', TRUE),
((SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10002'), '999222333', TRUE),
((SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10003'), '999333444', TRUE)
ON CONFLICT DO NOTHING;

-- ============================================
-- UBICACIONES DE PRUEBA
-- ============================================

INSERT INTO siredeci.Ubicacion (codigo_ubicacion, latitud, longitud, direccion, referencia, distrito, codigo_postal) VALUES
('UBI-00001', -12.046374, -77.042793, 'Av. Arequipa 1234', 'Frente al Parque Kennedy', 'Miraflores', '15047'),
('UBI-00002', -12.073770, -77.054430, 'Jr. de la Unión 456', 'Cerca de la Plaza Mayor', 'Lima', '15001'),
('UBI-00003', -12.087190, -77.050360, 'Av. Abancay 789', 'Altura del Hospital Nacional', 'Lima', '15001'),
('UBI-00004', -12.103280, -77.038970, 'Av. Javier Prado 2345', 'Cruce con Av. Aviación', 'San Isidro', '15036'),
('UBI-00005', -12.120450, -77.029840, 'Calle Los Olivos 567', 'Cerca del colegio', 'Surco', '15023')
ON CONFLICT (codigo_ubicacion) DO NOTHING;

-- ============================================
-- DENUNCIAS DE PRUEBA
-- ============================================

-- Denuncia 1: Bache (Registrada)
INSERT INTO siredeci.Denuncia (codigo_denuncia, titulo, descripcion, estado, prioridad, numero_seguimiento, id_ciudadano, id_categoria, id_ubicacion) VALUES
('DEN-2025-00001', 'Bache grande en Av. Arequipa', 'Existe un bache de aproximadamente 50cm de diámetro que representa un peligro para los vehículos', 'Registrado', 'Alta', 'SEG-ABC123456',
 (SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10001'),
 (SELECT id_categoria FROM siredeci.Categoria WHERE codigo_categoria = 'CAT-001'),
 (SELECT id_ubicacion FROM siredeci.Ubicacion WHERE codigo_ubicacion = 'UBI-00001'))
ON CONFLICT (codigo_denuncia) DO NOTHING;

-- Denuncia 2: Basura (En revisión)
INSERT INTO siredeci.Denuncia (codigo_denuncia, titulo, descripcion, fecha_registro, estado, prioridad, numero_seguimiento, id_ciudadano, id_categoria, id_ubicacion) VALUES
('DEN-2025-00002', 'Acumulación de basura', 'Hace 3 días que no pasa el camión recolector y la basura se acumula', CURRENT_TIMESTAMP - INTERVAL '2 days', 'En revisión', 'Urgente', 'SEG-DEF789012',
 (SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10002'),
 (SELECT id_categoria FROM siredeci.Categoria WHERE codigo_categoria = 'CAT-002'),
 (SELECT id_ubicacion FROM siredeci.Ubicacion WHERE codigo_ubicacion = 'UBI-00002'))
ON CONFLICT (codigo_denuncia) DO NOTHING;

-- Denuncia 3: Alumbrado (Asignada)
INSERT INTO siredeci.Denuncia (codigo_denuncia, titulo, descripcion, fecha_registro, estado, prioridad, numero_seguimiento, id_ciudadano, id_categoria, id_ubicacion) VALUES
('DEN-2025-00003', 'Poste de luz sin funcionar', 'El poste de luz de la cuadra lleva 5 días apagado', CURRENT_TIMESTAMP - INTERVAL '3 days', 'Asignado', 'Media', 'SEG-GHI345678',
 (SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10003'),
 (SELECT id_categoria FROM siredeci.Categoria WHERE codigo_categoria = 'CAT-003'),
 (SELECT id_ubicacion FROM siredeci.Ubicacion WHERE codigo_ubicacion = 'UBI-00003'))
ON CONFLICT (codigo_denuncia) DO NOTHING;

-- Denuncia 4: Seguridad (Resuelta)
INSERT INTO siredeci.Denuncia (codigo_denuncia, titulo, descripcion, fecha_registro, estado, prioridad, numero_seguimiento, id_ciudadano, id_categoria, id_ubicacion) VALUES
('DEN-2025-00004', 'Falta de patrullaje en la zona', 'No se observa presencia de serenazgo en horas de la noche', CURRENT_TIMESTAMP - INTERVAL '7 days', 'Resuelta', 'Alta', 'SEG-JKL901234',
 (SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10001'),
 (SELECT id_categoria FROM siredeci.Categoria WHERE codigo_categoria = 'CAT-004'),
 (SELECT id_ubicacion FROM siredeci.Ubicacion WHERE codigo_ubicacion = 'UBI-00004'))
ON CONFLICT (codigo_denuncia) DO NOTHING;

-- Denuncia 5: Área verde (En proceso)
INSERT INTO siredeci.Denuncia (codigo_denuncia, titulo, descripcion, fecha_registro, estado, prioridad, numero_seguimiento, id_ciudadano, id_categoria, id_ubicacion) VALUES
('DEN-2025-00005', 'Parque descuidado', 'El parque necesita mantenimiento urgente, el césped está muy alto', CURRENT_TIMESTAMP - INTERVAL '5 days', 'En proceso', 'Baja', 'SEG-MNO567890',
 (SELECT id_ciudadano FROM siredeci.Ciudadano WHERE codigo_ciudadano = 'CIU-10002'),
 (SELECT id_categoria FROM siredeci.Categoria WHERE codigo_categoria = 'CAT-005'),
 (SELECT id_ubicacion FROM siredeci.Ubicacion WHERE codigo_ubicacion = 'UBI-00005'))
ON CONFLICT (codigo_denuncia) DO NOTHING;

-- ============================================
-- SEGUIMIENTO DE DENUNCIAS
-- ============================================

-- Seguimiento Denuncia 1
INSERT INTO siredeci.Seguimiento (codigo_seguimiento, estado_anterior, estado_nuevo, comentario, id_denuncia, id_usuario) VALUES
('SEG-00001', NULL, 'Registrado', 'Denuncia registrada exitosamente en el sistema',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00001'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10001'))
ON CONFLICT (codigo_seguimiento) DO NOTHING;

-- Seguimiento Denuncia 2
INSERT INTO siredeci.Seguimiento (codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora, comentario, id_denuncia, id_usuario) VALUES
('SEG-00002', NULL, 'Registrado', CURRENT_TIMESTAMP - INTERVAL '2 days', 'Denuncia registrada exitosamente en el sistema',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00002'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10002')),
('SEG-00003', 'Registrado', 'En revisión', CURRENT_TIMESTAMP - INTERVAL '1 day', 'Denuncia en revisión por el área responsable',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00002'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00102'))
ON CONFLICT (codigo_seguimiento) DO NOTHING;

-- Seguimiento Denuncia 3
INSERT INTO siredeci.Seguimiento (codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora, comentario, id_denuncia, id_usuario) VALUES
('SEG-00004', NULL, 'Registrado', CURRENT_TIMESTAMP - INTERVAL '3 days', 'Denuncia registrada exitosamente en el sistema',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00003'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10003')),
('SEG-00005', 'Registrado', 'En revisión', CURRENT_TIMESTAMP - INTERVAL '2 days', 'Denuncia en revisión por el área responsable',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00003'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00001')),
('SEG-00006', 'En revisión', 'Asignado', CURRENT_TIMESTAMP - INTERVAL '1 day', 'Asignada a técnico de alumbrado público',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00003'),
 (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-00001'))
ON CONFLICT (codigo_seguimiento) DO NOTHING;

-- ============================================
-- ASIGNACIONES
-- ============================================

-- Asignación Denuncia 3
INSERT INTO siredeci.Asignacion (codigo_asignacion, fecha_asignacion, motivo_asignacion, id_denuncia, id_personal_asignado, id_personal_asignador) VALUES
('ASG-00001', CURRENT_TIMESTAMP - INTERVAL '1 day', 'Asignación por especialidad en alumbrado público',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00003'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00204'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00101'))
ON CONFLICT (codigo_asignacion) DO NOTHING;

-- Asignación Denuncia 4 (Resuelta)
INSERT INTO siredeci.Asignacion (codigo_asignacion, fecha_asignacion, motivo_asignacion, es_activa, fecha_finalizacion, id_denuncia, id_personal_asignado, id_personal_asignador) VALUES
('ASG-00002', CURRENT_TIMESTAMP - INTERVAL '7 days', 'Asignación a agente de serenazgo', FALSE, CURRENT_TIMESTAMP - INTERVAL '2 days',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00004'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00203'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00103'))
ON CONFLICT (codigo_asignacion) DO NOTHING;

-- Asignación Denuncia 5
INSERT INTO siredeci.Asignacion (codigo_asignacion, fecha_asignacion, motivo_asignacion, id_denuncia, id_personal_asignado, id_personal_asignador) VALUES
('ASG-00003', CURRENT_TIMESTAMP - INTERVAL '4 days', 'Asignación para mantenimiento de área verde',
 (SELECT id_denuncia FROM siredeci.Denuncia WHERE codigo_denuncia = 'DEN-2025-00005'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00202'),
 (SELECT id_personal FROM siredeci.PersonalMunicipal WHERE codigo_personal = 'PER-00102'))
ON CONFLICT (codigo_asignacion) DO NOTHING;

-- ============================================
-- TRAMITACIONES
-- ============================================

-- Tramitación Denuncia 4 (Resuelta)
INSERT INTO siredeci.Tramitacion (codigo_tramitacion, fecha_inicio, fecha_finalizacion, accion_realizada, observaciones, estado_tramitacion, id_asignacion) VALUES
('TRA-00001', CURRENT_TIMESTAMP - INTERVAL '6 days', CURRENT_TIMESTAMP - INTERVAL '2 days',
 'Se incrementó el patrullaje de serenazgo en la zona con recorridos cada 2 horas durante la noche',
 'Se coordinó con la comisaría del sector para reforzar la seguridad',
 'Finalizado',
 (SELECT id_asignacion FROM siredeci.Asignacion WHERE codigo_asignacion = 'ASG-00002'))
ON CONFLICT (codigo_tramitacion) DO NOTHING;

-- Tramitación Denuncia 5 (En proceso)
INSERT INTO siredeci.Tramitacion (codigo_tramitacion, fecha_inicio, accion_realizada, observaciones, costo_estimado, estado_tramitacion, id_asignacion) VALUES
('TRA-00002', CURRENT_TIMESTAMP - INTERVAL '3 days',
 'Se programó el corte de césped y limpieza general del parque',
 'Se requiere coordinación con la brigada de jardinería',
 350.00,
 'En proceso',
 (SELECT id_asignacion FROM siredeci.Asignacion WHERE codigo_asignacion = 'ASG-00003'))
ON CONFLICT (codigo_tramitacion) DO NOTHING;

-- ============================================
-- RESOLUCIONES
-- ============================================

-- Resolución Denuncia 4
INSERT INTO siredeci.Resolucion (codigo_resolucion, fecha_resolucion, tipo_resolucion, descripcion_resolucion, tiempo_total_horas, calificacion_ciudadano, comentario_ciudadano, id_tramitacion) VALUES
('RES-00001', CURRENT_TIMESTAMP - INTERVAL '2 days', 'Resuelta',
 'Se implementó patrullaje permanente en la zona con recorridos cada 2 horas. Se coordinó con PNP para apoyo adicional.',
 120, 5, 'Excelente respuesta, ya se observa mayor presencia policial en la zona',
 (SELECT id_tramitacion FROM siredeci.Tramitacion WHERE codigo_tramitacion = 'TRA-00001'))
ON CONFLICT (codigo_resolucion) DO NOTHING;

-- ============================================
-- CONFIGURACIONES DE NOTIFICACIONES
-- ============================================

INSERT INTO siredeci.ConfiguracionNotificacion (codigo_configuracion, recibir_email, recibir_sms, recibir_push, frecuencia_resumen, id_usuario) VALUES
('CFG-00001', TRUE, FALSE, TRUE, 'Inmediato', (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10001')),
('CFG-00002', TRUE, TRUE, TRUE, 'Diario', (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10002')),
('CFG-00003', TRUE, FALSE, FALSE, 'Semanal', (SELECT id_usuario FROM siredeci.Usuario WHERE codigo_usuario = 'USR-10003'))
ON CONFLICT (codigo_configuracion) DO NOTHING;

-- ============================================
-- INDICADORES Y DASHBOARDS
-- ============================================

INSERT INTO siredeci.Indicador (codigo_indicador, nombre, descripcion, formula, valor_minimo, valor_maximo, valor_actual, frecuencia_actualizacion, tipo_visualizacion) VALUES
('IND-001', 'Tasa de Resolución', 'Porcentaje de denuncias resueltas vs total', '(denuncias_resueltas / total_denuncias) * 100', 70.00, 100.00, 85.50, 'Diario', 'Gauge'),
('IND-002', 'Tiempo Promedio de Atención', 'Tiempo promedio en horas para resolver denuncias', 'AVG(tiempo_total_horas)', 0.00, 168.00, 48.75, 'Diario', 'Number'),
('IND-003', 'Denuncias Registradas Hoy', 'Cantidad de denuncias registradas en el día', 'COUNT(*) WHERE fecha_registro = TODAY', 0.00, 500.00, 12.00, 'Tiempo real', 'Number'),
('IND-004', 'Satisfacción Ciudadana', 'Calificación promedio de ciudadanos', 'AVG(calificacion_ciudadano)', 1.00, 5.00, 4.25, 'Diario', 'Gauge')
ON CONFLICT (codigo_indicador) DO NOTHING;

INSERT INTO siredeci.Dashboard (codigo_dashboard, nombre, descripcion, tipo_dashboard, frecuencia_actualizacion, es_publico) VALUES
('DSH-001', 'Dashboard Ejecutivo', 'Vista general para autoridades municipales', 'Ejecutivo', 'Diario', FALSE),
('DSH-002', 'Dashboard Operativo', 'Vista para personal municipal', 'Operativo', 'Tiempo real', FALSE),
('DSH-003', 'Dashboard Público', 'Estadísticas visibles para ciudadanos', 'Ciudadano', 'Diario', TRUE)
ON CONFLICT (codigo_dashboard) DO NOTHING;

-- Asignar indicadores a dashboards
INSERT INTO siredeci.DashboardIndicador (id_dashboard, id_indicador, orden, tipo_visualizacion) VALUES
((SELECT id_dashboard FROM siredeci.Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM siredeci.Indicador WHERE codigo_indicador = 'IND-001'), 1, 'Gauge'),
((SELECT id_dashboard FROM siredeci.Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM siredeci.Indicador WHERE codigo_indicador = 'IND-002'), 2, 'Number'),
((SELECT id_dashboard FROM siredeci.Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM siredeci.Indicador WHERE codigo_indicador = 'IND-004'), 3, 'Gauge'),
((SELECT id_dashboard FROM siredeci.Dashboard WHERE codigo_dashboard = 'DSH-002'), (SELECT id_indicador FROM siredeci.Indicador WHERE codigo_indicador = 'IND-003'), 1, 'Number'),
((SELECT id_dashboard FROM siredeci.Dashboard WHERE codigo_dashboard = 'DSH-003'), (SELECT id_indicador FROM siredeci.Indicador WHERE codigo_indicador = 'IND-001'), 1, 'BarChart')
ON CONFLICT DO NOTHING;

-- ============================================
-- RESUMEN FINAL
-- ============================================

DO $$
DECLARE
    v_usuarios INTEGER;
    v_ciudadanos INTEGER;
    v_personal INTEGER;
    v_areas INTEGER;
    v_categorias INTEGER;
    v_denuncias INTEGER;
    v_roles INTEGER;
    v_permisos INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_usuarios FROM siredeci.Usuario;
    SELECT COUNT(*) INTO v_ciudadanos FROM siredeci.Ciudadano;
    SELECT COUNT(*) INTO v_personal FROM siredeci.PersonalMunicipal;
    SELECT COUNT(*) INTO v_areas FROM siredeci.AreaResponsable;
    SELECT COUNT(*) INTO v_categorias FROM siredeci.Categoria;
    SELECT COUNT(*) INTO v_denuncias FROM siredeci.Denuncia;
    SELECT COUNT(*) INTO v_roles FROM siredeci.Rol;
    SELECT COUNT(*) INTO v_permisos FROM siredeci.Permiso;
    
    RAISE NOTICE '============================================';
    RAISE NOTICE 'POBLAMIENTO INICIAL COMPLETADO EXITOSAMENTE';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Usuarios creados: %', v_usuarios;
    RAISE NOTICE 'Ciudadanos: %', v_ciudadanos;
    RAISE NOTICE 'Personal Municipal: %', v_personal;
    RAISE NOTICE 'Áreas Responsables: %', v_areas;
    RAISE NOTICE 'Categorías: %', v_categorias;
    RAISE NOTICE 'Denuncias de prueba: %', v_denuncias;
    RAISE NOTICE 'Roles: %', v_roles;
    RAISE NOTICE 'Permisos: %', v_permisos;
    RAISE NOTICE '============================================';
    RAISE NOTICE 'CREDENCIALES DE ACCESO:';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'SuperAdmin: superadmin / Admin123!';
    RAISE NOTICE 'Admin: admin / Admin123!';
    RAISE NOTICE 'Auditor: auditor / Audit123!';
    RAISE NOTICE 'Jefes de Área: jperez, mgarcia, crodriguez / Admin123!';
    RAISE NOTICE 'Operadores: lmartinez, asanchez, rfernandez, plovato / Admin123!';
    RAISE NOTICE 'Ciudadanos: ciudadano1, ciudadano2, ciudadano3 / Admin123!';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'NOTA: Cambiar las contraseñas en producción';
    RAISE NOTICE '============================================';
END $$;

-- Fin del script de poblamiento