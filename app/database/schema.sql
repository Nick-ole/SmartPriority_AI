-- ==========================================
-- BASE DE DATOS: SmartPriority AI
-- Sistema Inteligente de Priorización de Tickets
-- PostgreSQL
-- ==========================================

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('Administrador', 'Operador', 'Técnico', 'Supervisor')),
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE areas (
    id_area SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    id_area INTEGER NOT NULL REFERENCES areas(id_area),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE prioridades (
    id_prioridad SERIAL PRIMARY KEY,
    nombre VARCHAR(20) UNIQUE NOT NULL,
    nivel INTEGER UNIQUE NOT NULL,
    color VARCHAR(20) NOT NULL,
    descripcion TEXT
);

CREATE TABLE sla_configuracion (
    id_sla SERIAL PRIMARY KEY,
    id_prioridad INTEGER UNIQUE NOT NULL REFERENCES prioridades(id_prioridad),
    tiempo_minutos INTEGER NOT NULL,
    descripcion TEXT
);

CREATE TABLE tickets (
    id_ticket SERIAL PRIMARY KEY,
    codigo_ticket VARCHAR(20) GENERATED ALWAYS AS ('TK-' || LPAD(id_ticket::TEXT, 5, '0')) STORED,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cierre TIMESTAMP,
    vencimiento_sla TIMESTAMP,
    estado VARCHAR(40) DEFAULT 'Pendiente' CHECK (
        estado IN (
            'Pendiente', 'Registrado', 'Analizado por IA', 'Clasificado', 'Asignado',
            'Validado', 'En Proceso', 'Resuelto', 'Cerrado', 'Cancelado'
        )
    ),
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_area INTEGER NOT NULL REFERENCES areas(id_area),
    id_prioridad INTEGER NOT NULL REFERENCES prioridades(id_prioridad)
);

CREATE TABLE analisis_ia (
    id_analisis SERIAL PRIMARY KEY,
    id_ticket INTEGER NOT NULL REFERENCES tickets(id_ticket) ON DELETE CASCADE,
    palabras_clave TEXT,
    prioridad_sugerida VARCHAR(20),
    area_sugerida VARCHAR(100),
    equipo_sugerido VARCHAR(100),
    porcentaje_confianza DECIMAL(5,2),
    modelo_utilizado VARCHAR(100) DEFAULT 'SmartPriority NLP v1.0',
    estado_validacion VARCHAR(30) DEFAULT 'Pendiente' CHECK (estado_validacion IN ('Pendiente', 'Aprobado', 'Rechazado', 'Modificado')),
    observacion_operador TEXT,
    fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE asignaciones (
    id_asignacion SERIAL PRIMARY KEY,
    id_ticket INTEGER NOT NULL REFERENCES tickets(id_ticket) ON DELETE CASCADE,
    id_tecnico INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_equipo INTEGER REFERENCES equipos(id_equipo),
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE historial (
    id_historial SERIAL PRIMARY KEY,
    id_ticket INTEGER NOT NULL REFERENCES tickets(id_ticket) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    accion VARCHAR(120) NOT NULL,
    estado_anterior VARCHAR(40),
    estado_nuevo VARCHAR(40),
    observacion TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reportes (
    id_reporte SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generado_por INTEGER REFERENCES usuarios(id_usuario)
);

CREATE TABLE actividad_tiempo_real (
    id_actividad SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    tipo VARCHAR(50),
    id_ticket INTEGER REFERENCES tickets(id_ticket) ON DELETE SET NULL,
    id_usuario INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE configuracion_sistema (
    id_configuracion SERIAL PRIMARY KEY,
    nombre_configuracion VARCHAR(100) UNIQUE NOT NULL,
    valor VARCHAR(255),
    descripcion TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_fecha_ticket
BEFORE UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion();

INSERT INTO prioridades (nombre, nivel, color, descripcion) VALUES
('Crítica', 1, '#EF4444', 'Incidencia que afecta servicios críticos o producción'),
('Alta', 2, '#F59E0B', 'Incidencia importante con alto impacto operativo'),
('Media', 3, '#2563EB', 'Incidencia moderada que no detiene el servicio'),
('Baja', 4, '#22C55E', 'Solicitud o incidencia de bajo impacto');

INSERT INTO sla_configuracion (id_prioridad, tiempo_minutos, descripcion) VALUES
(1, 30, 'Atención máxima para prioridad crítica'),
(2, 120, 'Atención máxima para prioridad alta'),
(3, 480, 'Atención máxima para prioridad media'),
(4, 1440, 'Atención máxima para prioridad baja');

INSERT INTO areas (nombre, descripcion) VALUES
('Soporte Técnico', 'Atención de incidencias generales de usuarios'),
('Redes', 'Problemas de conectividad, internet, VPN y red interna'),
('Desarrollo', 'Errores del sistema, aplicaciones y módulos internos'),
('Infraestructura', 'Servidores, equipos físicos y servicios críticos'),
('Base de Datos', 'Administración, consultas y problemas de bases de datos');

INSERT INTO equipos (nombre, descripcion, id_area) VALUES
('Mesa de Ayuda', 'Primer nivel de atención al usuario', 1),
('Equipo de Redes', 'Especialistas en conectividad y comunicaciones', 2),
('Soporte Aplicaciones', 'Equipo encargado de sistemas internos', 3),
('NOC Nivel 2', 'Equipo especializado en infraestructura crítica', 4),
('DBA Team', 'Administradores de base de datos', 5);

INSERT INTO usuarios (nombre, apellido, correo, contrasena, rol) VALUES
('Administrador', 'Sistema', 'admin@empresa.com', '123456', 'Administrador'),
('Juan', 'Pérez', 'jperez@empresa.com', '123456', 'Técnico'),
('María', 'López', 'mlopez@empresa.com', '123456', 'Operador'),
('Carlos', 'Ramírez', 'cramirez@empresa.com', '123456', 'Supervisor'),
('Ana', 'Torres', 'atorres@empresa.com', '123456', 'Técnico');

INSERT INTO tickets (titulo, descripcion, estado, id_usuario, id_area, id_prioridad, vencimiento_sla) VALUES
('Error al iniciar sesión', 'El usuario no puede acceder al sistema corporativo. Aparece mensaje de credenciales inválidas.', 'Pendiente', 3, 1, 2, CURRENT_TIMESTAMP + INTERVAL '120 minutes'),
('Servidor principal sin conexión', 'El servidor principal dejó de responder y varios servicios internos no están disponibles.', 'En Proceso', 3, 4, 1, CURRENT_TIMESTAMP + INTERVAL '30 minutes'),
('Lentitud en la aplicación CRM', 'Los usuarios reportan lentitud al cargar clientes y oportunidades en el sistema CRM.', 'Analizado por IA', 3, 3, 3, CURRENT_TIMESTAMP + INTERVAL '480 minutes'),
('Problema de conexión VPN', 'Un usuario remoto no puede conectarse a la VPN corporativa desde su laptop.', 'Asignado', 3, 2, 2, CURRENT_TIMESTAMP + INTERVAL '120 minutes'),
('Consulta sobre actualización de contraseña', 'El usuario solicita información para cambiar su contraseña del sistema.', 'Cerrado', 3, 1, 4, CURRENT_TIMESTAMP + INTERVAL '1440 minutes');

INSERT INTO analisis_ia (id_ticket, palabras_clave, prioridad_sugerida, area_sugerida, equipo_sugerido, porcentaje_confianza, modelo_utilizado, estado_validacion, observacion_operador) VALUES
(1, 'inicio sesión, credenciales, acceso, sistema corporativo', 'Alta', 'Soporte Técnico', 'Mesa de Ayuda', 88.50, 'SmartPriority NLP v1.0', 'Pendiente', 'Pendiente de validación por operador'),
(2, 'servidor, sin conexión, servicios internos, caída', 'Crítica', 'Infraestructura', 'NOC Nivel 2', 96.80, 'SmartPriority NLP v1.0', 'Aprobado', 'Prioridad crítica validada'),
(3, 'lentitud, aplicación, CRM, clientes, oportunidades', 'Media', 'Desarrollo', 'Soporte Aplicaciones', 79.30, 'SmartPriority NLP v1.0', 'Pendiente', 'Requiere revisión funcional'),
(4, 'VPN, conexión, usuario remoto, laptop', 'Alta', 'Redes', 'Equipo de Redes', 91.20, 'SmartPriority NLP v1.0', 'Aprobado', 'Derivación correcta al área de redes'),
(5, 'contraseña, consulta, cambio, usuario', 'Baja', 'Soporte Técnico', 'Mesa de Ayuda', 72.00, 'SmartPriority NLP v1.0', 'Aprobado', 'Solicitud simple resuelta');

INSERT INTO asignaciones (id_ticket, id_tecnico, id_equipo) VALUES
(1, 2, 1),
(2, 2, 4),
(3, 5, 3),
(4, 2, 2),
(5, 5, 1);

INSERT INTO historial (id_ticket, id_usuario, accion, estado_anterior, estado_nuevo, observacion) VALUES
(1, 3, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado correctamente'),
(1, 3, 'Análisis IA', 'Pendiente', 'Analizado por IA', 'La IA sugirió prioridad Alta'),
(2, 3, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado correctamente'),
(2, 4, 'Validación del operador', 'Analizado por IA', 'Validado', 'Se validó prioridad crítica'),
(2, 2, 'Asignación técnica', 'Validado', 'En Proceso', 'Asignado al técnico Juan Pérez'),
(3, 3, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado correctamente'),
(3, 3, 'Análisis IA', 'Pendiente', 'Analizado por IA', 'La IA detectó posible problema en CRM'),
(4, 3, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado correctamente'),
(4, 4, 'Asignación inteligente', 'Analizado por IA', 'Asignado', 'Derivado automáticamente al equipo de redes'),
(5, 3, 'Creación de ticket', NULL, 'Pendiente', 'Ticket registrado correctamente'),
(5, 5, 'Cierre de ticket', 'Resuelto', 'Cerrado', 'Solicitud atendida correctamente');

INSERT INTO reportes (nombre, descripcion, tipo, generado_por) VALUES
('Reporte General de Incidencias', 'Reporte mensual con resumen de tickets registrados, resueltos y pendientes', 'General', 1),
('Reporte de Cumplimiento SLA', 'Reporte de cumplimiento de tiempos de atención según prioridad', 'SLA', 1),
('Reporte de Análisis IA', 'Reporte de confianza y clasificación automática de tickets', 'IA', 1);

INSERT INTO actividad_tiempo_real (descripcion, tipo, id_ticket, id_usuario) VALUES
('Nuevo ticket registrado: Error al iniciar sesión', 'Ticket', 1, 3),
('IA analizó el ticket Servidor principal sin conexión con 96.80% de confianza', 'IA', 2, 1),
('Ticket crítico asignado al equipo NOC Nivel 2', 'Asignación', 2, 2),
('Ticket de VPN derivado al área de redes', 'Derivación', 4, 4),
('Ticket de consulta sobre contraseña cerrado correctamente', 'Cierre', 5, 5);

INSERT INTO configuracion_sistema (nombre_configuracion, valor, descripcion) VALUES
('clasificacion_automatica', 'true', 'Permite que la IA sugiera prioridad automáticamente'),
('derivacion_inteligente', 'true', 'Permite que la IA sugiera área y equipo responsable'),
('umbral_confianza_ia', '80', 'Porcentaje mínimo de confianza recomendado para aprobar sugerencias IA'),
('notificaciones_sla', 'true', 'Activa alertas cuando un ticket está cerca de vencer su SLA'),
('nombre_sistema', 'SmartPriority AI', 'Nombre visible de la plataforma');

CREATE INDEX idx_usuarios_correo ON usuarios(correo);
CREATE INDEX idx_tickets_estado ON tickets(estado);
CREATE INDEX idx_tickets_usuario ON tickets(id_usuario);
CREATE INDEX idx_tickets_area ON tickets(id_area);
CREATE INDEX idx_tickets_prioridad ON tickets(id_prioridad);
CREATE INDEX idx_tickets_fecha_registro ON tickets(fecha_registro);
CREATE INDEX idx_analisis_ticket ON analisis_ia(id_ticket);
CREATE INDEX idx_asignaciones_ticket ON asignaciones(id_ticket);
CREATE INDEX idx_historial_ticket ON historial(id_ticket);
CREATE INDEX idx_actividad_fecha ON actividad_tiempo_real(fecha);

CREATE OR REPLACE VIEW vista_tickets AS
SELECT
    t.id_ticket,
    t.codigo_ticket,
    t.titulo,
    t.descripcion,
    t.estado,
    t.fecha_registro,
    t.fecha_actualizacion,
    t.fecha_cierre,
    t.vencimiento_sla,
    u.nombre || ' ' || u.apellido AS solicitante,
    u.correo AS correo_solicitante,
    a.nombre AS area,
    p.nombre AS prioridad,
    p.nivel AS nivel_prioridad,
    p.color AS color_prioridad,
    COALESCE(ai.porcentaje_confianza, 0) AS porcentaje_confianza,
    ai.prioridad_sugerida,
    ai.area_sugerida,
    ai.equipo_sugerido,
    ai.estado_validacion
FROM tickets t
INNER JOIN usuarios u ON t.id_usuario = u.id_usuario
INNER JOIN areas a ON t.id_area = a.id_area
INNER JOIN prioridades p ON t.id_prioridad = p.id_prioridad
LEFT JOIN analisis_ia ai ON t.id_ticket = ai.id_ticket;

CREATE OR REPLACE VIEW vista_dashboard AS
SELECT
    COUNT(*) AS total_tickets,
    COUNT(*) FILTER (WHERE estado NOT IN ('Cerrado', 'Cancelado')) AS tickets_activos,
    COUNT(*) FILTER (WHERE estado = 'Cerrado') AS tickets_cerrados,
    COUNT(*) FILTER (WHERE id_prioridad = 1 AND estado NOT IN ('Cerrado', 'Cancelado')) AS tickets_criticos,
    COUNT(*) FILTER (WHERE vencimiento_sla < CURRENT_TIMESTAMP AND estado NOT IN ('Cerrado', 'Cancelado')) AS tickets_sla_vencido,
    ROUND(COALESCE(AVG(ai.porcentaje_confianza), 0), 2) AS confianza_promedio_ia
FROM tickets t
LEFT JOIN analisis_ia ai ON t.id_ticket = ai.id_ticket;

CREATE OR REPLACE VIEW vista_rendimiento_equipos AS
SELECT
    e.nombre AS equipo,
    COUNT(a.id_ticket) AS tickets_asignados,
    COUNT(t.id_ticket) FILTER (WHERE t.estado IN ('Resuelto', 'Cerrado')) AS tickets_resueltos,
    ROUND(COALESCE(AVG(ai.porcentaje_confianza), 0), 2) AS confianza_promedio
FROM equipos e
LEFT JOIN asignaciones a ON e.id_equipo = a.id_equipo
LEFT JOIN tickets t ON a.id_ticket = t.id_ticket
LEFT JOIN analisis_ia ai ON t.id_ticket = ai.id_ticket
GROUP BY e.id_equipo, e.nombre
ORDER BY tickets_asignados DESC;

-- Consultas rápidas de prueba:
SELECT * FROM vista_tickets ORDER BY fecha_registro DESC;
SELECT * FROM vista_dashboard;
