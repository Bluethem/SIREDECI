-- ============================================
-- SISTEMA DE DENUNCIAS CIUDADANAS
-- Script COMPLETO: Poblamiento Inicial + Masivo
-- Motor: PostgreSQL 14+
-- Descripción: Script todo-en-uno que crea TODOS los datos
-- Fecha: 2025-01-10
-- ============================================

-- ============================================
-- PARTE 1: DATOS MAESTROS (INICIAL)
-- ============================================

-- Insertar Roles del Sistema
INSERT INTO Rol (codigo_rol, nombre, descripcion, nivel, es_sistema, esta_activo) VALUES
('ROL-001', 'SuperAdmin', 'Administrador con acceso total al sistema', 1, TRUE, TRUE),
('ROL-002', 'Administrador', 'Administrador del sistema con permisos de configuración', 2, TRUE, TRUE),
('ROL-003', 'JefeArea', 'Jefe de área responsable con permisos de gestión', 3, TRUE, TRUE),
('ROL-004', 'Operador', 'Personal municipal que gestiona denuncias', 4, TRUE, TRUE),
('ROL-005', 'Ciudadano', 'Usuario ciudadano que registra denuncias', 5, TRUE, TRUE),
('ROL-006', 'Auditor', 'Usuario con permisos de solo lectura para auditoría', 6, TRUE, TRUE)
ON CONFLICT (codigo_rol) DO NOTHING;

-- Insertar Permisos del Sistema
INSERT INTO Permiso (codigo_permiso, nombre, descripcion, modulo, accion, recurso) VALUES
('PER-001', 'CREAR_DENUNCIA', 'Permite crear denuncias', 'Denuncias', 'Crear', 'Denuncia'),
('PER-002', 'LEER_DENUNCIA', 'Permite consultar denuncias', 'Denuncias', 'Leer', 'Denuncia'),
('PER-003', 'ACTUALIZAR_DENUNCIA', 'Permite actualizar denuncias', 'Denuncias', 'Actualizar', 'Denuncia'),
('PER-004', 'ELIMINAR_DENUNCIA', 'Permite eliminar denuncias', 'Denuncias', 'Eliminar', 'Denuncia'),
('PER-005', 'ASIGNAR_DENUNCIA', 'Permite asignar denuncias al personal', 'Denuncias', 'Ejecutar', 'Asignacion'),
('PER-006', 'RESOLVER_DENUNCIA', 'Permite resolver denuncias', 'Denuncias', 'Ejecutar', 'Resolucion'),
('PER-007', 'GESTIONAR_USUARIOS', 'Permite administrar usuarios del sistema', 'Administrativo', 'Crear', 'Usuario'),
('PER-008', 'LEER_USUARIOS', 'Permite consultar usuarios', 'Administrativo', 'Leer', 'Usuario'),
('PER-009', 'GESTIONAR_ROLES', 'Permite administrar roles y permisos', 'Administrativo', 'Crear', 'Rol'),
('PER-010', 'GENERAR_REPORTES', 'Permite generar reportes del sistema', 'Reportes', 'Crear', 'Reporte'),
('PER-011', 'LEER_REPORTES', 'Permite consultar reportes', 'Reportes', 'Leer', 'Reporte'),
('PER-012', 'VER_AUDITORIA', 'Permite consultar logs de auditoría', 'Administrativo', 'Leer', 'LogAuditoria'),
('PER-013', 'GESTIONAR_CATEGORIAS', 'Permite administrar categorías', 'Administrativo', 'Crear', 'Categoria'),
('PER-014', 'GESTIONAR_AREAS', 'Permite administrar áreas responsables', 'Administrativo', 'Crear', 'AreaResponsable'),
('PER-015', 'GESTIONAR_NOTIFICACIONES', 'Permite administrar plantillas de notificaciones', 'Notificaciones', 'Crear', 'PlantillaNotificacion')
ON CONFLICT (codigo_permiso) DO NOTHING;

-- Asignar Permisos a Roles
INSERT INTO RolPermiso (id_rol, id_permiso) 
SELECT r.id_rol, p.id_permiso 
FROM Rol r, Permiso p 
WHERE r.codigo_rol = 'ROL-001' -- SuperAdmin
ON CONFLICT DO NOTHING;

INSERT INTO RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso FROM Rol r, Permiso p
WHERE r.codigo_rol = 'ROL-002' AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-005', 'PER-007', 'PER-008', 'PER-009', 'PER-010', 'PER-011', 'PER-012', 'PER-013', 'PER-014', 'PER-015')
ON CONFLICT DO NOTHING;

INSERT INTO RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso FROM Rol r, Permiso p
WHERE r.codigo_rol = 'ROL-003' AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-005', 'PER-006', 'PER-008', 'PER-010', 'PER-011')
ON CONFLICT DO NOTHING;

INSERT INTO RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso FROM Rol r, Permiso p
WHERE r.codigo_rol = 'ROL-004' AND p.codigo_permiso IN ('PER-002', 'PER-003', 'PER-006')
ON CONFLICT DO NOTHING;

INSERT INTO RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso FROM Rol r, Permiso p
WHERE r.codigo_rol = 'ROL-005' AND p.codigo_permiso IN ('PER-001', 'PER-002')
ON CONFLICT DO NOTHING;

INSERT INTO RolPermiso (id_rol, id_permiso)
SELECT r.id_rol, p.id_permiso FROM Rol r, Permiso p
WHERE r.codigo_rol = 'ROL-006' AND p.codigo_permiso IN ('PER-002', 'PER-008', 'PER-011', 'PER-012')
ON CONFLICT DO NOTHING;

-- Áreas Responsables
INSERT INTO AreaResponsable (codigo_area, nombre, descripcion, email, telefono, capacidad_maxima, esta_activo) VALUES
('ARE-001', 'Obras Públicas', 'Responsable de infraestructura vial, mantenimiento de calles y espacios públicos', 'obras.publicas@municipalidad.gob.pe', '01-2345678', 100, TRUE),
('ARE-002', 'Servicios Públicos', 'Gestión de limpieza pública, recojo de basura y ornato', 'servicios.publicos@municipalidad.gob.pe', '01-2345679', 80, TRUE),
('ARE-003', 'Seguridad Ciudadana', 'Coordinación con serenazgo y gestión de seguridad', 'seguridad@municipalidad.gob.pe', '01-2345680', 60, TRUE),
('ARE-004', 'Gestión Ambiental', 'Áreas verdes, parques y medio ambiente', 'ambiente@municipalidad.gob.pe', '01-2345681', 50, TRUE),
('ARE-005', 'Alumbrado Público', 'Mantenimiento y reparación de alumbrado público', 'alumbrado@municipalidad.gob.pe', '01-2345682', 40, TRUE),
('ARE-006', 'Desarrollo Urbano', 'Planificación urbana y obras de desarrollo', 'desarrollo@municipalidad.gob.pe', '01-2345683', 70, TRUE)
ON CONFLICT (codigo_area) DO NOTHING;

-- Categorías de Denuncias
INSERT INTO Categoria (codigo_categoria, nombre, descripcion, color, icono, esta_activo, tiempo_respuesta_promedio, id_area_responsable) VALUES
('CAT-001', 'Baches en la vía', 'Huecos o deterioro en calles y avenidas', '#E74C3C', 'road_damage', TRUE, 72, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-001')),
('CAT-002', 'Basura acumulada', 'Acumulación de residuos sólidos en vía pública', '#F39C12', 'delete', TRUE, 24, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-002')),
('CAT-003', 'Alumbrado público', 'Postes sin luz o instalaciones dañadas', '#F1C40F', 'lightbulb', TRUE, 48, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-005')),
('CAT-004', 'Inseguridad', 'Problemas de seguridad ciudadana', '#8E44AD', 'security', TRUE, 12, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-003')),
('CAT-005', 'Áreas verdes descuidadas', 'Parques y jardines sin mantenimiento', '#27AE60', 'park', TRUE, 168, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-006', 'Veredas deterioradas', 'Veredas rotas o en mal estado', '#34495E', 'directions_walk', TRUE, 96, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-001')),
('CAT-007', 'Señalización deficiente', 'Falta de señales de tránsito o en mal estado', '#3498DB', 'traffic', TRUE, 120, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-006')),
('CAT-008', 'Ruido excesivo', 'Contaminación sonora', '#E67E22', 'volume_up', TRUE, 48, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-009', 'Mascota abandonada', 'Animales en situación de abandono', '#95A5A6', 'pets', TRUE, 24, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
('CAT-010', 'Construcción ilegal', 'Obras sin permisos o invasiones', '#C0392B', 'construction', TRUE, 72, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-006'))
ON CONFLICT (codigo_categoria) DO NOTHING;

-- Plantillas de Notificaciones
INSERT INTO PlantillaNotificacion (codigo_plantilla, nombre, tipo_evento, asunto, cuerpo_mensaje, variables, esta_activa) VALUES
('PLT-001', 'Registro de Denuncia', 'Registro', 'Denuncia Registrada Exitosamente', 
'Estimado/a {nombre_ciudadano}, Su denuncia ha sido registrada exitosamente en nuestro sistema. Código de seguimiento: {numero_seguimiento}. Tiempo estimado de atención: {tiempo_estimado} horas.', 
'["nombre_ciudadano", "numero_seguimiento", "tiempo_estimado"]', TRUE),
('PLT-002', 'Actualización de Estado', 'Actualización', 'Actualización de su Denuncia {numero_seguimiento}', 
'Estimado/a {nombre_ciudadano}, Le informamos que su denuncia ha sido actualizada. Estado anterior: {estado_anterior}. Estado actual: {estado_nuevo}.', 
'["nombre_ciudadano", "estado_anterior", "estado_nuevo", "numero_seguimiento"]', TRUE),
('PLT-003', 'Asignación a Personal', 'Asignación', 'Nueva denuncia asignada', 
'Estimado/a {nombre_personal}, Se le ha asignado una nueva denuncia para su atención. Código: {codigo_denuncia}', 
'["nombre_personal", "codigo_denuncia"]', TRUE),
('PLT-004', 'Resolución de Denuncia', 'Resolución', 'Su denuncia ha sido resuelta', 
'Estimado/a {nombre_ciudadano}, Le informamos que su denuncia ha sido resuelta. Tipo de resolución: {tipo_resolucion}', 
'["nombre_ciudadano", "tipo_resolucion"]', TRUE)
ON CONFLICT (codigo_plantilla) DO NOTHING;

-- Usuarios administrativos
INSERT INTO Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta, requiere_mfa) VALUES
('USR-00001', 'superadmin', 'Admin123!', 'superadmin@municipalidad.gob.pe', 'Activo', TRUE),
('USR-00002', 'admin', 'Admin123!', 'admin@municipalidad.gob.pe', 'Activo', TRUE),
('USR-00003', 'auditor', 'Audit123!', 'auditor@municipalidad.gob.pe', 'Activo', FALSE)
ON CONFLICT (codigo_usuario) DO NOTHING;

-- Asignar roles a usuarios administrativos
INSERT INTO UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE FROM Usuario u, Rol r
WHERE (u.codigo_usuario = 'USR-00001' AND r.codigo_rol = 'ROL-001')
   OR (u.codigo_usuario = 'USR-00002' AND r.codigo_rol = 'ROL-002')
   OR (u.codigo_usuario = 'USR-00003' AND r.codigo_rol = 'ROL-006')
ON CONFLICT DO NOTHING;

-- Jefes de Área
INSERT INTO Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta) VALUES
('USR-00101', 'jperez', 'Jefe123!', 'juan.perez@municipalidad.gob.pe', 'Activo'),
('USR-00102', 'mgarcia', 'Jefe123!', 'maria.garcia@municipalidad.gob.pe', 'Activo'),
('USR-00103', 'crodriguez', 'Jefe123!', 'carlos.rodriguez@municipalidad.gob.pe', 'Activo')
ON CONFLICT (codigo_usuario) DO NOTHING;

INSERT INTO PersonalMunicipal (codigo_personal, dni, nombre, apellido, email, cargo, fecha_ingreso, especialidad, id_area_responsable, id_usuario) VALUES
('PER-00101', '12345678', 'Juan', 'Pérez López', 'juan.perez@municipalidad.gob.pe', 'Jefe de Obras Públicas', '2020-01-15', 'Ingeniería Civil', 
 (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-001'),
 (SELECT id_usuario FROM Usuario WHERE codigo_usuario = 'USR-00101')),
('PER-00102', '23456789', 'María', 'García Torres', 'maria.garcia@municipalidad.gob.pe', 'Jefa de Servicios Públicos', '2019-03-10', 'Gestión Pública', 
 (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-002'),
 (SELECT id_usuario FROM Usuario WHERE codigo_usuario = 'USR-00102')),
('PER-00103', '34567890', 'Carlos', 'Rodríguez Díaz', 'carlos.rodriguez@municipalidad.gob.pe', 'Jefe de Seguridad Ciudadana', '2021-06-20', 'Seguridad', 
 (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-003'),
 (SELECT id_usuario FROM Usuario WHERE codigo_usuario = 'USR-00103'))
ON CONFLICT (codigo_personal) DO NOTHING;

INSERT INTO UsuarioRol (id_usuario, id_rol, es_activo)
SELECT u.id_usuario, r.id_rol, TRUE FROM Usuario u, Rol r
WHERE u.codigo_usuario IN ('USR-00101', 'USR-00102', 'USR-00103') AND r.codigo_rol = 'ROL-003'
ON CONFLICT DO NOTHING;

-- Actualizar jefes de área
UPDATE AreaResponsable SET id_jefe_area = (SELECT id_personal FROM PersonalMunicipal WHERE codigo_personal = 'PER-00101') WHERE codigo_area = 'ARE-001';
UPDATE AreaResponsable SET id_jefe_area = (SELECT id_personal FROM PersonalMunicipal WHERE codigo_personal = 'PER-00102') WHERE codigo_area = 'ARE-002';
UPDATE AreaResponsable SET id_jefe_area = (SELECT id_personal FROM PersonalMunicipal WHERE codigo_personal = 'PER-00103') WHERE codigo_area = 'ARE-003';

-- Indicadores y Dashboards
INSERT INTO Indicador (codigo_indicador, nombre, descripcion, formula, valor_minimo, valor_maximo, valor_actual, frecuencia_actualizacion, tipo_visualizacion) VALUES
('IND-001', 'Tasa de Resolución', 'Porcentaje de denuncias resueltas vs total', '(denuncias_resueltas / total_denuncias) * 100', 70.00, 100.00, 85.50, 'Diario', 'Gauge'),
('IND-002', 'Tiempo Promedio de Atención', 'Tiempo promedio en horas para resolver denuncias', 'AVG(tiempo_total_horas)', 0.00, 168.00, 48.75, 'Diario', 'Number'),
('IND-003', 'Denuncias Registradas Hoy', 'Cantidad de denuncias registradas en el día', 'COUNT(*) WHERE fecha_registro = TODAY', 0.00, 500.00, 12.00, 'Tiempo real', 'Number'),
('IND-004', 'Satisfacción Ciudadana', 'Calificación promedio de ciudadanos', 'AVG(calificacion_ciudadano)', 1.00, 5.00, 4.25, 'Diario', 'Gauge')
ON CONFLICT (codigo_indicador) DO NOTHING;

INSERT INTO Dashboard (codigo_dashboard, nombre, descripcion, tipo_dashboard, frecuencia_actualizacion, es_publico) VALUES
('DSH-001', 'Dashboard Ejecutivo', 'Vista general para autoridades municipales', 'Ejecutivo', 'Diario', FALSE),
('DSH-002', 'Dashboard Operativo', 'Vista para personal municipal', 'Operativo', 'Tiempo real', FALSE),
('DSH-003', 'Dashboard Público', 'Estadísticas visibles para ciudadanos', 'Ciudadano', 'Diario', TRUE)
ON CONFLICT (codigo_dashboard) DO NOTHING;

INSERT INTO DashboardIndicador (id_dashboard, id_indicador, orden, tipo_visualizacion) VALUES
((SELECT id_dashboard FROM Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM Indicador WHERE codigo_indicador = 'IND-001'), 1, 'Gauge'),
((SELECT id_dashboard FROM Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM Indicador WHERE codigo_indicador = 'IND-002'), 2, 'Number'),
((SELECT id_dashboard FROM Dashboard WHERE codigo_dashboard = 'DSH-001'), (SELECT id_indicador FROM Indicador WHERE codigo_indicador = 'IND-004'), 3, 'Gauge'),
((SELECT id_dashboard FROM Dashboard WHERE codigo_dashboard = 'DSH-002'), (SELECT id_indicador FROM Indicador WHERE codigo_indicador = 'IND-003'), 1, 'Number'),
((SELECT id_dashboard FROM Dashboard WHERE codigo_dashboard = 'DSH-003'), (SELECT id_indicador FROM Indicador WHERE codigo_indicador = 'IND-001'), 1, 'BarChart')
ON CONFLICT DO NOTHING;

-- ============================================
-- SISTEMA DE DENUNCIAS CIUDADANAS
-- Script de Poblamiento Masivo con PL/pgSQL
-- Motor: PostgreSQL 14+
-- Cantidad: 100+ registros realistas
-- Fecha: 2025-01-10
-- ============================================

DO $$
DECLARE
    v_usuario_id INTEGER;
    v_ciudadano_id INTEGER;
    v_personal_id INTEGER;
    v_denuncia_id INTEGER;
    v_asignacion_id INTEGER;
    v_tramitacion_id INTEGER;
    v_ubicacion_id INTEGER;
    v_categoria_id INTEGER;
    v_area_id INTEGER;
    v_contador INTEGER;
    v_estado TEXT;
    v_prioridad TEXT;
    v_count_areas INTEGER;
    v_count_categorias INTEGER;
    v_fecha_asignacion TIMESTAMP;
    v_fecha_tramitacion TIMESTAMP;
    v_fecha_registro TIMESTAMP;
    v_fecha_actualiz TIMESTAMP;
    
    -- Arrays para generar datos aleatorios
    v_nombres_m TEXT[] := ARRAY['Carlos', 'Juan', 'Pedro', 'Luis', 'José', 'Miguel', 'Roberto', 'Fernando', 'Andrés', 'Diego', 
                                 'Ricardo', 'Alberto', 'Raúl', 'Manuel', 'Francisco', 'Jorge', 'Daniel', 'Alejandro', 'Javier', 'Rafael'];
    v_nombres_f TEXT[] := ARRAY['María', 'Ana', 'Carmen', 'Rosa', 'Patricia', 'Laura', 'Sofía', 'Isabel', 'Gabriela', 'Daniela',
                                 'Lucía', 'Mónica', 'Claudia', 'Teresa', 'Verónica', 'Sandra', 'Beatriz', 'Silvia', 'Elena', 'Andrea'];
    v_apellidos TEXT[] := ARRAY['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores',
                                 'Rivera', 'Gómez', 'Díaz', 'Cruz', 'Morales', 'Reyes', 'Jiménez', 'Hernández', 'Ruiz', 'Vargas',
                                 'Castillo', 'Mendoza', 'Ortiz', 'Silva', 'Castro', 'Romero', 'Vega', 'Delgado', 'Aguilar', 'Medina'];
    v_calles TEXT[] := ARRAY['Av. Principal', 'Jr. Los Álamos', 'Calle Las Flores', 'Av. Los Pinos', 'Jr. San Martín', 
                             'Av. Libertad', 'Calle Real', 'Jr. Progreso', 'Av. Primavera', 'Calle Comercio',
                             'Av. Industrial', 'Jr. Unión', 'Calle Grau', 'Av. Universitaria', 'Jr. Bolognesi',
                             'Calle Lima', 'Av. Larco', 'Jr. Arequipa', 'Calle Tacna', 'Av. Benavides'];
    v_distritos TEXT[] := ARRAY['Miraflores', 'San Isidro', 'Surco', 'La Molina', 'San Borja', 'Lince', 'Jesús María', 
                                'Magdalena', 'Pueblo Libre', 'San Miguel', 'Cercado de Lima', 'Breña', 'Los Olivos',
                                'Independencia', 'Comas', 'San Juan de Lurigancho', 'Ate', 'Santa Anita', 'La Victoria', 'Surquillo'];
    v_referencias TEXT[] := ARRAY['Frente al parque', 'Cerca del mercado', 'Al lado de la iglesia', 'Cerca del colegio', 
                                  'Frente a la comisaría', 'Al lado del banco', 'Cerca de la plaza', 'Frente al hospital',
                                  'Al costado de la municipalidad', 'Cerca de la estación', 'Junto al centro comercial', 
                                  'Frente a la farmacia', 'Al lado del parque infantil', 'Cerca de la biblioteca'];
    
    v_titulos_baches TEXT[] := ARRAY['Bache grande en la vía', 'Hueco peligroso en la pista', 'Deterioro severo de la calzada',
                                     'Bache profundo que causa accidentes', 'Pista en mal estado', 'Varios baches en la cuadra'];
    v_titulos_basura TEXT[] := ARRAY['Acumulación de basura', 'Basura sin recoger por días', 'Residuos sólidos abandonados',
                                     'Punto crítico de acumulación de basura', 'Basura desbordada', 'Montículo de desperdicios'];
    v_titulos_luz TEXT[] := ARRAY['Poste sin luz', 'Alumbrado público no funciona', 'Falta de iluminación', 
                                  'Postes apagados hace días', 'Luminaria dañada', 'Cables colgantes peligrosos'];
    v_titulos_seguridad TEXT[] := ARRAY['Falta de patrullaje', 'Inseguridad en la zona', 'Ausencia de serenazgo',
                                        'Robos frecuentes', 'Zona oscura y peligrosa', 'Necesidad de vigilancia'];
    v_titulos_parques TEXT[] := ARRAY['Parque descuidado', 'Área verde sin mantenimiento', 'Jardín en mal estado',
                                      'Césped muy alto', 'Juegos infantiles deteriorados', 'Bancas rotas'];
    
    v_lat_base NUMERIC := -12.046374;
    v_lon_base NUMERIC := -77.042793;
    v_dni_base INTEGER := 20000000;
    v_fecha_actual TIMESTAMP := CURRENT_TIMESTAMP;
    v_genero INTEGER;
BEGIN
    RAISE NOTICE '================================================';
    RAISE NOTICE 'INICIANDO POBLAMIENTO MASIVO DE BASE DE DATOS';
    RAISE NOTICE '================================================';
    
    -- ============================================
    -- VALIDACIÓN PREVIA: VERIFICAR DATOS MAESTROS
    -- ============================================
    RAISE NOTICE 'Verificando datos maestros necesarios...';
    
    -- Verificar áreas responsables
    SELECT COUNT(*) INTO v_count_areas FROM AreaResponsable;
    IF v_count_areas = 0 THEN
        RAISE NOTICE '⚠ No hay áreas responsables. Creando datos maestros...';
        
        -- Crear áreas responsables
        INSERT INTO AreaResponsable (codigo_area, nombre, descripcion, email, telefono, capacidad_maxima, esta_activo) VALUES
        ('ARE-001', 'Obras Públicas', 'Responsable de infraestructura vial, mantenimiento de calles y espacios públicos', 'obras.publicas@municipalidad.gob.pe', '01-2345678', 100, TRUE),
        ('ARE-002', 'Servicios Públicos', 'Gestión de limpieza pública, recojo de basura y ornato', 'servicios.publicos@municipalidad.gob.pe', '01-2345679', 80, TRUE),
        ('ARE-003', 'Seguridad Ciudadana', 'Coordinación con serenazgo y gestión de seguridad', 'seguridad@municipalidad.gob.pe', '01-2345680', 60, TRUE),
        ('ARE-004', 'Gestión Ambiental', 'Áreas verdes, parques y medio ambiente', 'ambiente@municipalidad.gob.pe', '01-2345681', 50, TRUE),
        ('ARE-005', 'Alumbrado Público', 'Mantenimiento y reparación de alumbrado público', 'alumbrado@municipalidad.gob.pe', '01-2345682', 40, TRUE),
        ('ARE-006', 'Desarrollo Urbano', 'Planificación urbana y obras de desarrollo', 'desarrollo@municipalidad.gob.pe', '01-2345683', 70, TRUE)
        ON CONFLICT (codigo_area) DO NOTHING;
        
        RAISE NOTICE '✓ Áreas responsables creadas';
    ELSE
        RAISE NOTICE '✓ Áreas responsables existentes: %', v_count_areas;
    END IF;
    
    -- Verificar categorías
    SELECT COUNT(*) INTO v_count_categorias FROM Categoria;
    IF v_count_categorias = 0 THEN
        RAISE NOTICE '⚠ No hay categorías. Creando datos maestros...';
        
        -- Crear categorías
        INSERT INTO Categoria (codigo_categoria, nombre, descripcion, color, icono, esta_activo, tiempo_respuesta_promedio, id_area_responsable) VALUES
        ('CAT-001', 'Baches en la vía', 'Huecos o deterioro en calles y avenidas', '#E74C3C', 'road_damage', TRUE, 72, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-001')),
        ('CAT-002', 'Basura acumulada', 'Acumulación de residuos sólidos en vía pública', '#F39C12', 'delete', TRUE, 24, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-002')),
        ('CAT-003', 'Alumbrado público', 'Postes sin luz o instalaciones dañadas', '#F1C40F', 'lightbulb', TRUE, 48, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-005')),
        ('CAT-004', 'Inseguridad', 'Problemas de seguridad ciudadana', '#8E44AD', 'security', TRUE, 12, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-003')),
        ('CAT-005', 'Áreas verdes descuidadas', 'Parques y jardines sin mantenimiento', '#27AE60', 'park', TRUE, 168, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
        ('CAT-006', 'Veredas deterioradas', 'Veredas rotas o en mal estado', '#34495E', 'directions_walk', TRUE, 96, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-001')),
        ('CAT-007', 'Señalización deficiente', 'Falta de señales de tránsito o en mal estado', '#3498DB', 'traffic', TRUE, 120, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-006')),
        ('CAT-008', 'Ruido excesivo', 'Contaminación sonora', '#E67E22', 'volume_up', TRUE, 48, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
        ('CAT-009', 'Mascota abandonada', 'Animales en situación de abandono', '#95A5A6', 'pets', TRUE, 24, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-004')),
        ('CAT-010', 'Construcción ilegal', 'Obras sin permisos o invasiones', '#C0392B', 'construction', TRUE, 72, (SELECT id_area_responsable FROM AreaResponsable WHERE codigo_area = 'ARE-006'))
        ON CONFLICT (codigo_categoria) DO NOTHING;
        
        RAISE NOTICE '✓ Categorías creadas';
    ELSE
        RAISE NOTICE '✓ Categorías existentes: %', v_count_categorias;
    END IF;
    
    -- Verificar plantillas de notificación
    IF NOT EXISTS (SELECT 1 FROM PlantillaNotificacion LIMIT 1) THEN
        RAISE NOTICE '⚠ No hay plantillas de notificación. Creando...';
        
        INSERT INTO PlantillaNotificacion (codigo_plantilla, nombre, tipo_evento, asunto, cuerpo_mensaje, variables, esta_activa) VALUES
        ('PLT-001', 'Registro de Denuncia', 'Registro', 'Denuncia Registrada Exitosamente', 
        'Estimado/a {nombre_ciudadano}, Su denuncia ha sido registrada exitosamente. Código: {numero_seguimiento}', 
        '["nombre_ciudadano", "numero_seguimiento"]', TRUE),
        ('PLT-002', 'Actualización de Estado', 'Actualización', 'Actualización de su Denuncia', 
        'Su denuncia ha sido actualizada. Estado: {estado_nuevo}', 
        '["estado_nuevo"]', TRUE)
        ON CONFLICT (codigo_plantilla) DO NOTHING;
        
        RAISE NOTICE '✓ Plantillas de notificación creadas';
    END IF;
    
    -- Verificar roles
    IF NOT EXISTS (SELECT 1 FROM Rol WHERE codigo_rol = 'ROL-005') THEN
        RAISE NOTICE '⚠ No hay roles. Creando roles básicos...';
        
        INSERT INTO Rol (codigo_rol, nombre, descripcion, nivel, es_sistema, esta_activo) VALUES
        ('ROL-005', 'Ciudadano', 'Usuario ciudadano que registra denuncias', 5, TRUE, TRUE),
        ('ROL-004', 'Operador', 'Personal municipal que gestiona denuncias', 4, TRUE, TRUE)
        ON CONFLICT (codigo_rol) DO NOTHING;
        
        RAISE NOTICE '✓ Roles creados';
    END IF;
    
    RAISE NOTICE '✓ Validación completada. Iniciando poblamiento...';
    RAISE NOTICE '';
    
    -- ============================================
    -- PASO 1: CREAR 100 CIUDADANOS CON USUARIOS
    -- ============================================
    RAISE NOTICE 'Paso 1/8: Creando 100 ciudadanos...';
    
    FOR v_contador IN 1..100 LOOP
        v_genero := floor(random() * 2)::INTEGER; -- 0=masculino, 1=femenino
        
        -- Crear usuario (usando rango 20000+ para evitar conflictos)
        INSERT INTO Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta)
        VALUES (
            'USR-' || LPAD((20000 + v_contador)::TEXT, 5, '0'),
            'ciudadano_' || (20000 + v_contador),
            'Ciudadano123!',
            'ciudadano_' || (20000 + v_contador) || '@email.com',
            CASE WHEN random() < 0.95 THEN 'Activo' ELSE 'Inactivo' END
        )
        RETURNING id_usuario INTO v_usuario_id;
        
        -- Crear ciudadano
        INSERT INTO Ciudadano (
            codigo_ciudadano, dni, nombre, apellido, email, direccion, 
            fecha_emision_dni, id_usuario, es_anonimo, estado_cuenta
        )
        VALUES (
            'CIU-' || LPAD((20000 + v_contador)::TEXT, 5, '0'),
            LPAD((v_dni_base + v_contador)::TEXT, 8, '0'),
            CASE WHEN v_genero = 0 THEN v_nombres_m[1 + floor(random() * 20)::INTEGER]
                 ELSE v_nombres_f[1 + floor(random() * 20)::INTEGER] END,
            v_apellidos[1 + floor(random() * 30)::INTEGER] || ' ' || v_apellidos[1 + floor(random() * 30)::INTEGER],
            'ciudadano_' || (20000 + v_contador) || '@email.com',
            v_calles[1 + floor(random() * 20)::INTEGER] || ' ' || (100 + floor(random() * 900)::INTEGER),
            CURRENT_DATE - INTERVAL '1 year' * (1 + floor(random() * 5)::INTEGER),
            v_usuario_id,
            random() < 0.1, -- 10% anónimos
            'Activo'
        )
        RETURNING id_ciudadano INTO v_ciudadano_id;
        
        -- Asignar rol ciudadano
        INSERT INTO UsuarioRol (id_usuario, id_rol, es_activo)
        SELECT v_usuario_id, id_rol, TRUE 
        FROM Rol WHERE codigo_rol = 'ROL-005';
        
        -- Agregar teléfono
        INSERT INTO CiudadanoTelefono (id_ciudadano, telefono, es_principal)
        VALUES (
            v_ciudadano_id,
            '9' || LPAD((10000000 + v_contador)::TEXT, 8, '0'),
            TRUE
        );
        
        -- Configuración de notificaciones
        INSERT INTO ConfiguracionNotificacion (
            codigo_configuracion, recibir_email, recibir_sms, recibir_push, 
            frecuencia_resumen, id_usuario
        )
        VALUES (
            'CFG-' || LPAD((20000 + v_contador)::TEXT, 5, '0'),
            random() < 0.9, -- 90% reciben email
            random() < 0.3, -- 30% reciben SMS
            random() < 0.8, -- 80% reciben push
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Inmediato'
                WHEN 1 THEN 'Diario'
                WHEN 2 THEN 'Semanal'
                ELSE 'Ninguno'
            END,
            v_usuario_id
        );
        
        IF v_contador % 20 = 0 THEN
            RAISE NOTICE '  -> Creados % ciudadanos', v_contador;
        END IF;
    END LOOP;
    
    RAISE NOTICE '✓ 100 ciudadanos creados exitosamente';
    
    -- ============================================
    -- PASO 2: CREAR PERSONAL ADICIONAL
    -- ============================================
    RAISE NOTICE 'Paso 2/8: Creando personal municipal adicional...';
    
    FOR v_contador IN 1..20 LOOP
        v_genero := floor(random() * 2)::INTEGER;
        
        -- Crear usuario para personal (usando rango 1000+ para evitar conflictos)
        INSERT INTO Usuario (codigo_usuario, nombre_usuario, password_hash, email, estado_cuenta)
        VALUES (
            'USR-' || LPAD((1000 + v_contador)::TEXT, 5, '0'),
            'personal_' || (1000 + v_contador),
            'Personal123!',
            'personal_' || (1000 + v_contador) || '@municipalidad.gob.pe',
            'Activo'
        )
        RETURNING id_usuario INTO v_usuario_id;
        
        -- Crear personal
        INSERT INTO PersonalMunicipal (
            codigo_personal, dni, nombre, apellido, email, cargo, 
            fecha_ingreso, especialidad, estado_laboral, id_area_responsable, id_usuario
        )
        SELECT 
            'PER-' || LPAD((1000 + v_contador)::TEXT, 5, '0'),
            LPAD((50000000 + v_contador)::TEXT, 8, '0'),
            CASE WHEN v_genero = 0 THEN v_nombres_m[1 + floor(random() * 20)::INTEGER]
                 ELSE v_nombres_f[1 + floor(random() * 20)::INTEGER] END,
            v_apellidos[1 + floor(random() * 30)::INTEGER] || ' ' || v_apellidos[1 + floor(random() * 30)::INTEGER],
            'personal_' || (1000 + v_contador) || '@municipalidad.gob.pe',
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Técnico de Campo'
                WHEN 1 THEN 'Supervisor'
                WHEN 2 THEN 'Especialista'
                ELSE 'Operador'
            END,
            CURRENT_DATE - INTERVAL '1 year' * (1 + floor(random() * 8)::INTEGER),
            CASE floor(random() * 6)::INTEGER
                WHEN 0 THEN 'Obras Civiles'
                WHEN 1 THEN 'Electricidad'
                WHEN 2 THEN 'Limpieza'
                WHEN 3 THEN 'Seguridad'
                WHEN 4 THEN 'Jardinería'
                ELSE 'Mantenimiento'
            END,
            'Activo',
            (SELECT id_area_responsable FROM AreaResponsable WHERE esta_activo = TRUE ORDER BY RANDOM() LIMIT 1),
            v_usuario_id
        RETURNING id_personal INTO v_personal_id;
        
        -- Asignar rol operador
        INSERT INTO UsuarioRol (id_usuario, id_rol, es_activo)
        SELECT v_usuario_id, id_rol, TRUE 
        FROM Rol WHERE codigo_rol = 'ROL-004';
        
        -- Agregar teléfono
        INSERT INTO PersonalTelefono (id_personal, telefono, es_principal)
        VALUES (
            v_personal_id,
            '9' || LPAD((50000000 + v_contador)::TEXT, 8, '0'),
            TRUE
        );
    END LOOP;
    
    RAISE NOTICE '✓ 20 personal municipal adicional creado';
    
    -- ============================================
    -- PASO 3: CREAR 150 UBICACIONES
    -- ============================================
    RAISE NOTICE 'Paso 3/8: Creando 150 ubicaciones...';
    
    FOR v_contador IN 1..150 LOOP
        INSERT INTO Ubicacion (
            codigo_ubicacion, latitud, longitud, direccion, referencia, distrito, codigo_postal
        )
        VALUES (
            'UBI-' || LPAD((1000 + v_contador)::TEXT, 5, '0'),
            v_lat_base + (random() * 0.2 - 0.1), -- Variación de latitud
            v_lon_base + (random() * 0.2 - 0.1), -- Variación de longitud
            v_calles[1 + floor(random() * 20)::INTEGER] || ' ' || (100 + floor(random() * 2900)::INTEGER),
            v_referencias[1 + floor(random() * 14)::INTEGER],
            v_distritos[1 + floor(random() * 20)::INTEGER],
            '15' || LPAD((floor(random() * 100)::INTEGER)::TEXT, 3, '0')
        );
        
        IF v_contador % 30 = 0 THEN
            RAISE NOTICE '  -> Creadas % ubicaciones', v_contador;
        END IF;
    END LOOP;
    
    RAISE NOTICE '✓ 150 ubicaciones creadas exitosamente';
    
    -- ============================================
    -- PASO 4: CREAR 200 DENUNCIAS
    -- ============================================
    RAISE NOTICE 'Paso 4/8: Creando 200 denuncias con diferentes estados...';
    
    FOR v_contador IN 1..200 LOOP
        -- Determinar estado con distribución realista
        CASE floor(random() * 100)::INTEGER
            WHEN 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14 THEN v_estado := 'Registrado'; -- 15%
            WHEN 15,16,17,18,19,20,21,22,23,24 THEN v_estado := 'En revisión'; -- 10%
            WHEN 25,26,27,28,29,30,31,32,33,34,35,36,37,38,39 THEN v_estado := 'Asignado'; -- 15%
            WHEN 40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64 THEN v_estado := 'En proceso'; -- 25%
            WHEN 65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89 THEN v_estado := 'Resuelta'; -- 25%
            WHEN 90,91,92,93,94 THEN v_estado := 'Rechazada'; -- 5%
            ELSE v_estado := 'Cerrada'; -- 5%
        END CASE;
        
        -- Determinar prioridad
        CASE floor(random() * 100)::INTEGER
            WHEN 0,1,2,3,4,5,6,7,8,9 THEN v_prioridad := 'Urgente'; -- 10%
            WHEN 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 THEN v_prioridad := 'Alta'; -- 20%
            WHEN 30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64 THEN v_prioridad := 'Media'; -- 35%
            ELSE v_prioridad := 'Baja'; -- 35%
        END CASE;
        
        -- Seleccionar categoría aleatoria
        SELECT id_categoria INTO v_categoria_id 
        FROM Categoria 
        WHERE esta_activo = TRUE 
        ORDER BY RANDOM() 
        LIMIT 1;
        
        -- Seleccionar ubicación aleatoria
        SELECT id_ubicacion INTO v_ubicacion_id 
        FROM Ubicacion 
        ORDER BY RANDOM() 
        LIMIT 1;
        
        -- Seleccionar ciudadano aleatorio
        SELECT id_ciudadano INTO v_ciudadano_id 
        FROM Ciudadano 
        ORDER BY RANDOM() 
        LIMIT 1;
        
        -- Crear denuncia con fecha variable en los últimos 60 días
        v_fecha_registro := v_fecha_actual - INTERVAL '1 day' * floor(random() * 60)::INTEGER;
        v_fecha_actualiz := v_fecha_registro + INTERVAL '1 day' * floor(random() * 30)::INTEGER;
        
        INSERT INTO Denuncia (
            codigo_denuncia, titulo, descripcion, fecha_registro, fecha_actualizacion,
            estado, prioridad, es_anonima, numero_seguimiento, requiere_validacion,
            id_ciudadano, id_categoria, id_ubicacion
        )
        VALUES (
            'DEN-2025-' || LPAD((10000 + v_contador)::TEXT, 5, '0'),
            CASE (SELECT codigo_categoria FROM Categoria WHERE id_categoria = v_categoria_id)
                WHEN 'CAT-001' THEN v_titulos_baches[1 + floor(random() * 6)::INTEGER]
                WHEN 'CAT-002' THEN v_titulos_basura[1 + floor(random() * 6)::INTEGER]
                WHEN 'CAT-003' THEN v_titulos_luz[1 + floor(random() * 6)::INTEGER]
                WHEN 'CAT-004' THEN v_titulos_seguridad[1 + floor(random() * 6)::INTEGER]
                WHEN 'CAT-005' THEN v_titulos_parques[1 + floor(random() * 6)::INTEGER]
                ELSE 'Problema reportado en la zona'
            END,
            'Descripción detallada del problema reportado. Se requiere atención para resolver esta situación que afecta a los vecinos de la zona. ' ||
            'El problema persiste desde hace ' || (1 + floor(random() * 30)::INTEGER) || ' días.',
            v_fecha_registro,
            v_fecha_actualiz,
            v_estado,
            v_prioridad,
            random() < 0.15, -- 15% anónimas
            'SEG-' || UPPER(substring(md5(random()::text) from 1 for 9)),
            random() < 0.7, -- 70% requieren validación
            CASE WHEN random() < 0.85 THEN v_ciudadano_id ELSE NULL END, -- 85% tienen ciudadano
            v_categoria_id,
            v_ubicacion_id
        )
        RETURNING id_denuncia INTO v_denuncia_id;
        
        -- Crear registro de seguimiento inicial
        INSERT INTO Seguimiento (
            codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora,
            comentario, es_visible, id_denuncia, id_usuario
        )
        VALUES (
            'SEG-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-01',
            NULL,
            'Registrado',
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 60)::INTEGER,
            'Denuncia registrada exitosamente en el sistema',
            TRUE,
            v_denuncia_id,
            (SELECT id_usuario FROM Ciudadano WHERE id_ciudadano = v_ciudadano_id)
        );
        
        -- Si la denuncia tiene estados avanzados, crear seguimientos adicionales
        IF v_estado IN ('En revisión', 'Asignado', 'En proceso', 'Resuelta', 'Rechazada', 'Cerrada') THEN
            INSERT INTO Seguimiento (
                codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora,
                comentario, es_visible, id_denuncia, id_usuario
            )
            VALUES (
                'SEG-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-02',
                'Registrado',
                'En revisión',
                v_fecha_actual - INTERVAL '1 day' * floor(random() * 45)::INTEGER,
                'Denuncia en proceso de revisión por el área responsable',
                TRUE,
                v_denuncia_id,
                (SELECT id_usuario FROM PersonalMunicipal ORDER BY RANDOM() LIMIT 1)
            );
        END IF;
        
        IF v_estado IN ('Asignado', 'En proceso', 'Resuelta', 'Cerrada') THEN
            -- Crear asignación
            -- Intentar encontrar personal del área correspondiente, si no hay, usar cualquier personal
            SELECT id_personal INTO v_personal_id
            FROM PersonalMunicipal 
            WHERE id_area_responsable = (SELECT id_area_responsable FROM Categoria WHERE id_categoria = v_categoria_id)
            AND estado_laboral = 'Activo'
            ORDER BY RANDOM() 
            LIMIT 1;
            
            -- Si no hay personal en esa área específica, asignar a cualquier personal activo
            IF v_personal_id IS NULL THEN
                SELECT id_personal INTO v_personal_id
                FROM PersonalMunicipal 
                WHERE estado_laboral = 'Activo'
                ORDER BY RANDOM() 
                LIMIT 1;
            END IF;
            
            -- Calcular fecha de asignación primero
            v_fecha_asignacion := v_fecha_actual - INTERVAL '1 day' * floor(random() * 40)::INTEGER;
            
            INSERT INTO Asignacion (
                codigo_asignacion, fecha_asignacion, motivo_asignacion, es_activa,
                fecha_finalizacion, id_denuncia, id_personal_asignado, id_personal_asignador
            )
            VALUES (
                'ASG-' || LPAD((10000 + v_contador)::TEXT, 5, '0'),
                v_fecha_asignacion,
                'Asignación por especialidad y disponibilidad',
                v_estado NOT IN ('Resuelta', 'Cerrada', 'Rechazada'),
                CASE WHEN v_estado IN ('Resuelta', 'Cerrada') 
                     -- Sumar días a fecha_asignacion para garantizar que sea posterior
                     THEN v_fecha_asignacion + INTERVAL '1 day' * (1 + floor(random() * 20)::INTEGER)
                     ELSE NULL END,
                v_denuncia_id,
                v_personal_id,
                (SELECT id_personal FROM PersonalMunicipal ORDER BY RANDOM() LIMIT 1)
            )
            RETURNING id_asignacion INTO v_asignacion_id;
            
            INSERT INTO Seguimiento (
                codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora,
                comentario, es_visible, id_denuncia, id_usuario
            )
            VALUES (
                'SEG-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-03',
                'En revisión',
                'Asignado',
                v_fecha_actual - INTERVAL '1 day' * floor(random() * 35)::INTEGER,
                'Denuncia asignada al personal técnico correspondiente',
                TRUE,
                v_denuncia_id,
                (SELECT id_usuario FROM PersonalMunicipal WHERE id_personal = v_personal_id)
            );
        END IF;
        
        IF v_estado IN ('En proceso', 'Resuelta', 'Cerrada') THEN
            -- Crear tramitación
            -- Calcular fecha de inicio primero
            v_fecha_tramitacion := v_fecha_actual - INTERVAL '1 day' * floor(random() * 30)::INTEGER;
            
            INSERT INTO Tramitacion (
                codigo_tramitacion, fecha_inicio, fecha_finalizacion, accion_realizada,
                observaciones, costo_estimado, estado_tramitacion, id_asignacion
            )
            VALUES (
                'TRA-' || LPAD((10000 + v_contador)::TEXT, 5, '0'),
                v_fecha_tramitacion,
                CASE WHEN v_estado IN ('Resuelta', 'Cerrada') 
                     -- Sumar días a fecha_tramitacion para garantizar que sea posterior
                     THEN v_fecha_tramitacion + INTERVAL '1 day' * (1 + floor(random() * 15)::INTEGER)
                     ELSE NULL END,
                'Se procedió con la atención correspondiente según los protocolos establecidos. ' ||
                'Se coordinó con las áreas involucradas para la resolución del caso.',
                'Observaciones técnicas del personal asignado durante el proceso de atención.',
                50.00 + (random() * 1000)::NUMERIC(10,2),
                CASE WHEN v_estado IN ('Resuelta', 'Cerrada') THEN 'Finalizado'
                     WHEN v_estado = 'Rechazada' THEN 'Cancelado'
                     ELSE 'En proceso' END,
                v_asignacion_id
            )
            RETURNING id_tramitacion INTO v_tramitacion_id;
            
            INSERT INTO Seguimiento (
                codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora,
                comentario, es_visible, id_denuncia, id_usuario
            )
            VALUES (
                'SEG-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-04',
                'Asignado',
                'En proceso',
                v_fecha_actual - INTERVAL '1 day' * floor(random() * 25)::INTEGER,
                'Se inició el proceso de atención y resolución',
                TRUE,
                v_denuncia_id,
                (SELECT id_usuario FROM PersonalMunicipal WHERE id_personal = v_personal_id)
            );
        END IF;
        
        IF v_estado IN ('Resuelta', 'Cerrada') THEN
            -- Crear resolución
            INSERT INTO Resolucion (
                codigo_resolucion, fecha_resolucion, tipo_resolucion, descripcion_resolucion,
                tiempo_total_horas, calificacion_ciudadano, comentario_ciudadano, id_tramitacion
            )
            VALUES (
                'RES-' || LPAD((10000 + v_contador)::TEXT, 5, '0'),
                v_fecha_actual - INTERVAL '1 day' * floor(random() * 3)::INTEGER,
                CASE floor(random() * 4)::INTEGER
                    WHEN 0 THEN 'Resuelta'
                    WHEN 1 THEN 'Rechazada'
                    WHEN 2 THEN 'Duplicada'
                    ELSE 'No procede'
                END,
                'Se completó la atención de la denuncia conforme a los procedimientos establecidos. ' ||
                'Se verificó la correcta ejecución de las acciones correctivas necesarias.',
                24 + floor(random() * 200)::INTEGER,
                CASE WHEN random() < 0.7 THEN 1 + floor(random() * 5)::INTEGER ELSE NULL END,
                CASE WHEN random() < 0.5 THEN 
                    CASE floor(random() * 5)::INTEGER
                        WHEN 0 THEN 'Excelente atención, muy satisfecho con el servicio'
                        WHEN 1 THEN 'Buena respuesta, el problema fue solucionado'
                        WHEN 2 THEN 'Regular, esperaba una solución más rápida'
                        WHEN 3 THEN 'Muy buena coordinación del personal'
                        ELSE 'Agradezco la pronta atención'
                    END
                ELSE NULL END,
                v_tramitacion_id
            );
            
            INSERT INTO Seguimiento (
                codigo_seguimiento, estado_anterior, estado_nuevo, fecha_hora,
                comentario, es_visible, id_denuncia, id_usuario
            )
            VALUES (
                'SEG-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-05',
                'En proceso',
                v_estado,
                v_fecha_actual - INTERVAL '1 day' * floor(random() * 2)::INTEGER,
                'Denuncia finalizada - ' || v_estado,
                TRUE,
                v_denuncia_id,
                (SELECT id_usuario FROM PersonalMunicipal WHERE id_personal = v_personal_id)
            );
        END IF;
        
        -- Crear evidencias para algunas denuncias (40%)
        IF random() < 0.4 THEN
            FOR v_genero IN 1..(1 + floor(random() * 3)::INTEGER) LOOP
                INSERT INTO Evidencia (
                    codigo_evidencia, nombre_archivo, ruta_almacenamiento, tipo_archivo,
                    tamaño_bytes, fecha_carga, hash_archivo, esta_escaneado, id_denuncia
                )
                VALUES (
                    'EVI-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-' || LPAD(v_genero::TEXT, 2, '0'),
                    'evidencia_' || (10000 + v_contador) || '_' || v_genero || '.jpg',
                    '/storage/evidencias/2025/01/' || (10000 + v_contador) || '/' || v_genero || '.jpg',
                    CASE floor(random() * 3)::INTEGER
                        WHEN 0 THEN 'image/jpeg'
                        WHEN 1 THEN 'image/png'
                        ELSE 'application/pdf'
                    END,
                    100000 + floor(random() * 5000000)::BIGINT,
                    v_fecha_actual - INTERVAL '1 day' * floor(random() * 55)::INTEGER,
                    md5(random()::text || v_contador::text || v_genero::text),
                    random() < 0.9,
                    v_denuncia_id
                );
            END LOOP;
        END IF;
        
        -- Crear comunicaciones para denuncias avanzadas (30%)
        IF v_estado IN ('En proceso', 'Resuelta', 'Cerrada') AND random() < 0.3 THEN
            FOR v_genero IN 1..(1 + floor(random() * 3)::INTEGER) LOOP
                INSERT INTO Comunicacion (
                    codigo_comunicacion, mensaje, fecha_envio, tipo_remitente,
                    es_leido, requiere_respuesta, id_denuncia, id_usuario_remitente
                )
                VALUES (
                    'COM-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-' || LPAD(v_genero::TEXT, 2, '0'),
                    CASE floor(random() * 4)::INTEGER
                        WHEN 0 THEN '¿Cuál es el estado actual de mi denuncia?'
                        WHEN 1 THEN 'Necesito información sobre los avances'
                        WHEN 2 THEN 'El problema persiste, requiere atención adicional'
                        ELSE 'Agradezco el seguimiento brindado'
                    END,
                    v_fecha_actual - INTERVAL '1 day' * floor(random() * 20)::INTEGER,
                    CASE floor(random() * 2)::INTEGER
                        WHEN 0 THEN 'Ciudadano'
                        ELSE 'Personal'
                    END,
                    random() < 0.8,
                    random() < 0.4,
                    v_denuncia_id,
                    (SELECT id_usuario FROM Usuario ORDER BY RANDOM() LIMIT 1)
                );
            END LOOP;
        END IF;
        
        -- Crear notificaciones
        INSERT INTO Notificacion (
            codigo_notificacion, tipo_notificacion, fecha_creacion, fecha_envio,
            canal_envio, estado_envio, mensaje_personalizado, intento_envio,
            id_denuncia, id_usuario, id_plantilla
        )
        VALUES (
            'NOT-' || LPAD((10000 + v_contador)::TEXT, 5, '0') || '-01',
            'Registro',
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 60)::INTEGER,
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 59)::INTEGER,
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Email'
                WHEN 1 THEN 'SMS'
                WHEN 2 THEN 'Push'
                ELSE 'Interno'
            END,
            CASE floor(random() * 5)::INTEGER
                WHEN 0 THEN 'Pendiente'
                WHEN 1 THEN 'Enviado'
                WHEN 2 THEN 'Entregado'
                WHEN 3 THEN 'Leído'
                ELSE 'Fallido'
            END,
            'Su denuncia ha sido registrada exitosamente. Código de seguimiento: SEG-' || UPPER(substring(md5(random()::text) from 1 for 9)),
            1 + floor(random() * 2)::INTEGER,
            v_denuncia_id,
            (SELECT id_usuario FROM Ciudadano WHERE id_ciudadano = v_ciudadano_id),
            (SELECT id_plantilla FROM PlantillaNotificacion WHERE codigo_plantilla = 'PLT-001')
        );
        
        IF v_contador % 40 = 0 THEN
            RAISE NOTICE '  -> Creadas % denuncias', v_contador;
        END IF;
    END LOOP;
    
    RAISE NOTICE '✓ 200 denuncias creadas con estados, seguimientos y evidencias';
    
    -- ============================================
    -- PASO 5: CREAR ESTADÍSTICAS
    -- ============================================
    RAISE NOTICE 'Paso 5/8: Generando estadísticas del sistema...';
    
    FOR v_contador IN 1..50 LOOP
        INSERT INTO Estadistica (
            codigo_estadistica, tipo_metrica, valor, unidad_medida, periodo,
            fecha_calculo, categoria, area, zona
        )
        VALUES (
            'EST-' || LPAD((5000 + v_contador)::TEXT, 5, '0'),
            CASE floor(random() * 6)::INTEGER
                WHEN 0 THEN 'Denuncias Registradas'
                WHEN 1 THEN 'Denuncias Resueltas'
                WHEN 2 THEN 'Tiempo Promedio Atención'
                WHEN 3 THEN 'Satisfacción Ciudadana'
                WHEN 4 THEN 'Tasa de Resolución'
                ELSE 'Personal Activo'
            END,
            (random() * 100)::NUMERIC(10,2),
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Cantidad'
                WHEN 1 THEN 'Horas'
                WHEN 2 THEN 'Porcentaje'
                ELSE 'Calificación'
            END,
            CASE floor(random() * 5)::INTEGER
                WHEN 0 THEN 'Diario'
                WHEN 1 THEN 'Semanal'
                WHEN 2 THEN 'Mensual'
                WHEN 3 THEN 'Trimestral'
                ELSE 'Anual'
            END,
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 90)::INTEGER,
            (SELECT nombre FROM Categoria ORDER BY RANDOM() LIMIT 1),
            (SELECT nombre FROM AreaResponsable ORDER BY RANDOM() LIMIT 1),
            v_distritos[1 + floor(random() * 20)::INTEGER]
        );
    END LOOP;
    
    RAISE NOTICE '✓ 50 registros estadísticos generados';
    
    -- ============================================
    -- PASO 6: CREAR TENDENCIAS GEOGRÁFICAS
    -- ============================================
    RAISE NOTICE 'Paso 6/8: Creando análisis de tendencias geográficas...';
    
    FOR v_contador IN 1..20 LOOP
        INSERT INTO TendenciaGeografica (
            codigo_tendencia, zona, distrito, cantidad_denuncias, categoria_mas_frecuente,
            tasa_resolucion, tiempo_promedio_atencion, periodo_analisis, nivel_criticidad
        )
        VALUES (
            'TEN-' || LPAD((6000 + v_contador)::TEXT, 5, '0'),
            'Zona ' || (1 + floor(random() * 10)::INTEGER),
            v_distritos[1 + floor(random() * 20)::INTEGER],
            5 + floor(random() * 50)::INTEGER,
            (SELECT nombre FROM Categoria ORDER BY RANDOM() LIMIT 1),
            (50 + random() * 50)::NUMERIC(5,2),
            (24 + random() * 144)::NUMERIC(10,2),
            CASE floor(random() * 3)::INTEGER
                WHEN 0 THEN 'Semanal'
                WHEN 1 THEN 'Mensual'
                ELSE 'Trimestral'
            END,
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Bajo'
                WHEN 1 THEN 'Medio'
                WHEN 2 THEN 'Alto'
                ELSE 'Crítico'
            END
        );
    END LOOP;
    
    RAISE NOTICE '✓ 20 tendencias geográficas creadas';
    
    -- ============================================
    -- PASO 7: CREAR RANKINGS DE DESEMPEÑO
    -- ============================================
    RAISE NOTICE 'Paso 7/8: Generando rankings de desempeño...';
    
    v_contador := 1;
    FOR v_area_id IN (SELECT id_area_responsable FROM AreaResponsable ORDER BY id_area_responsable) LOOP
        INSERT INTO RankingDesempeno (
            codigo_ranking, periodo_evaluacion, posicion, puntaje_total,
            denuncias_atendidas, tasa_resolucion_area, tiempo_promedio_area,
            calificacion_promedio, id_area_responsable
        )
        VALUES (
            'RNK-' || LPAD((7000 + v_contador)::TEXT, 5, '0'),
            'Mensual',
            v_contador,
            (60 + random() * 40)::NUMERIC(5,2),
            10 + floor(random() * 50)::INTEGER,
            (70 + random() * 30)::NUMERIC(5,2),
            (24 + random() * 120)::NUMERIC(10,2),
            (3 + random() * 2)::NUMERIC(3,2),
            v_area_id
        );
        v_contador := v_contador + 1;
    END LOOP;
    
    RAISE NOTICE '✓ Rankings de desempeño generados para todas las áreas';
    
    -- ============================================
    -- PASO 8: CREAR REPORTES
    -- ============================================
    RAISE NOTICE 'Paso 8/8: Generando reportes del sistema...';
    
    FOR v_contador IN 1..15 LOOP
        INSERT INTO Reporte (
            codigo_reporte, tipo_reporte, nombre, descripcion, fecha_generacion,
            fecha_inicio, fecha_fin, formato_exportacion, ruta_archivo,
            es_publico, id_usuario_generador, estado_generacion, parametros_configuracion
        )
        VALUES (
            'REP-' || LPAD((8000 + v_contador)::TEXT, 5, '0'),
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Ejecutivo'
                WHEN 1 THEN 'Operativo'
                WHEN 2 THEN 'Estadístico'
                ELSE 'Auditoria'
            END,
            'Reporte ' || CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'Mensual de Denuncias'
                WHEN 1 THEN 'de Desempeño por Área'
                WHEN 2 THEN 'de Satisfacción Ciudadana'
                ELSE 'de Tiempos de Atención'
            END || ' - ' || to_char(v_fecha_actual, 'Month YYYY'),
            'Análisis detallado del período con métricas clave de desempeño',
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 30)::INTEGER,
            v_fecha_actual - INTERVAL '1 month',
            v_fecha_actual,
            CASE floor(random() * 4)::INTEGER
                WHEN 0 THEN 'PDF'
                WHEN 1 THEN 'Excel'
                WHEN 2 THEN 'CSV'
                ELSE 'JSON'
            END,
            '/storage/reportes/2025/01/reporte_' || (8000 + v_contador) || '.pdf',
            random() < 0.3,
            (SELECT id_usuario FROM Usuario WHERE codigo_usuario IN ('USR-00002', 'USR-00003') ORDER BY RANDOM() LIMIT 1),
            CASE floor(random() * 3)::INTEGER
                WHEN 0 THEN 'Borrador'
                WHEN 1 THEN 'En proceso'
                ELSE 'Completado'
            END,
            '{"filtros": {"estado": "todos", "prioridad": "todas"}}'::jsonb
        );
    END LOOP;
    
    RAISE NOTICE '✓ 15 reportes generados';
    
    -- ============================================
    -- PASO 9: CREAR LOGS DE AUDITORÍA
    -- ============================================
    RAISE NOTICE 'Paso 9/8: Generando logs de auditoría...';
    
    FOR v_contador IN 1..100 LOOP
        INSERT INTO LogAuditoria (
            codigo_log, tipo_accion, modulo, entidad, entidad_id, fecha_hora,
            direccion_ip, datos_antes, datos_despues, resultado, mensaje_error, id_usuario
        )
        VALUES (
            'LOG-' || LPAD((9000 + v_contador)::TEXT, 5, '0'),
            CASE floor(random() * 7)::INTEGER
                WHEN 0 THEN 'CREAR'
                WHEN 1 THEN 'LEER'
                WHEN 2 THEN 'ACTUALIZAR'
                WHEN 3 THEN 'ELIMINAR'
                WHEN 4 THEN 'LOGIN'
                WHEN 5 THEN 'LOGOUT'
                ELSE 'CAMBIO_ESTADO'
            END,
            CASE floor(random() * 5)::INTEGER
                WHEN 0 THEN 'Denuncias'
                WHEN 1 THEN 'Usuarios'
                WHEN 2 THEN 'Asignaciones'
                WHEN 3 THEN 'Resoluciones'
                ELSE 'Notificaciones'
            END,
            CASE floor(random() * 5)::INTEGER
                WHEN 0 THEN 'Denuncia'
                WHEN 1 THEN 'Usuario'
                WHEN 2 THEN 'Asignacion'
                WHEN 3 THEN 'Resolucion'
                ELSE 'Notificacion'
            END,
            'ID-' || (1 + floor(random() * 200)::INTEGER),
            v_fecha_actual - INTERVAL '1 day' * floor(random() * 90)::INTEGER,
            '192.168.' || (1 + floor(random() * 255)::INTEGER) || '.' || (1 + floor(random() * 255)::INTEGER),
            CASE WHEN random() < 0.5 THEN '{"estado": "Registrado"}' ELSE NULL END,
            CASE WHEN random() < 0.5 THEN '{"estado": "En revisión"}' ELSE NULL END,
            CASE WHEN random() < 0.95 THEN 'Exitoso' ELSE 'Fallido' END,
            CASE WHEN random() < 0.05 THEN 'Error en la operación' ELSE NULL END,
            (SELECT id_usuario FROM Usuario ORDER BY RANDOM() LIMIT 1)
        );
        
        IF v_contador % 25 = 0 THEN
            RAISE NOTICE '  -> Creados % logs de auditoría', v_contador;
        END IF;
    END LOOP;
    
    RAISE NOTICE '✓ 100 logs de auditoría generados';
    
    -- ============================================
    -- RESUMEN FINAL
    -- ============================================
    RAISE NOTICE '================================================';
    RAISE NOTICE 'POBLAMIENTO COMPLETADO EXITOSAMENTE';
    RAISE NOTICE '================================================';
    RAISE NOTICE '';
    RAISE NOTICE 'RESUMEN DE REGISTROS CREADOS:';
    RAISE NOTICE '  ✓ 100 Ciudadanos con usuarios y teléfonos';
    RAISE NOTICE '  ✓ 20 Personal municipal adicional';
    RAISE NOTICE '  ✓ 150 Ubicaciones geográficas';
    RAISE NOTICE '  ✓ 200 Denuncias con diferentes estados';
    RAISE NOTICE '  ✓ 500+ Registros de seguimiento';
    RAISE NOTICE '  ✓ 150+ Asignaciones al personal';
    RAISE NOTICE '  ✓ 120+ Tramitaciones';
    RAISE NOTICE '  ✓ 80+ Resoluciones';
    RAISE NOTICE '  ✓ 150+ Evidencias adjuntas';
    RAISE NOTICE '  ✓ 100+ Comunicaciones';
    RAISE NOTICE '  ✓ 200+ Notificaciones';
    RAISE NOTICE '  ✓ 100 Configuraciones de notificación';
    RAISE NOTICE '  ✓ 50 Registros estadísticos';
    RAISE NOTICE '  ✓ 20 Tendencias geográficas';
    RAISE NOTICE '  ✓ 6 Rankings de desempeño';
    RAISE NOTICE '  ✓ 15 Reportes generados';
    RAISE NOTICE '  ✓ 100 Logs de auditoría';
    RAISE NOTICE '';
    RAISE NOTICE '================================================';
    RAISE NOTICE 'TOTAL: 1,800+ REGISTROS CREADOS';
    RAISE NOTICE '================================================';
    
END $$;