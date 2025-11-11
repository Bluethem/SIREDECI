# Sistema de Denuncias Ciudadanas - Documentación Completa

## Tabla de Contenido

---

### FASE 1: REQUISITOS

- [1. Descripción del Proyecto](./1-requisitos/1.1-descripcion.md)
  - [1.1. Introducción](./1-requisitos/1.1-descripcion.md#introduccion)
  - [1.2. Objetivos del Sistema](./1-requisitos/1.1-descripcion.md#objetivos)
  - [1.3. Alcance del Proyecto](./1-requisitos/1.1-descripcion.md#alcance)
  - [1.4. Stakeholders](./1-requisitos/1.1-descripcion.md#stakeholders)
- [2. Requerimientos Funcionales](./1-requisitos/1.2-requisitos-funcionales.md)
- [3. Requerimientos No Funcionales](./1-requisitos/1.3-requisitos-no-funcionales.md)
- [4. Requerimientos de Seguridad](./1-requisitos/1.4-requisitos-seguridad.md)
- [5. Requerimientos Regulatorios y Legales](./1-requisitos/1.5-requisitos-legales.md)

---

### FASE 2: DISEÑO DEL SISTEMA

- [6. Arquitectura del Sistema](./2-diseno/2.1-arquitectura.md)
- [7. Diseño Conceptual](./2-diseno/2.2-diseno-conceptual.md)
- [8. Modelo Relacional](./2-diseno/2.3-modelo-er.md)
- [9. Diseño de Interfaz de Usuario (Mockups)](./2-diseno/2.4-diseno-ui.md)
- [10. Diagramas UML](./2-diseno/2.5-diagramas-uml.md)
  - [10.1. Diagrama de Clases](./2-diseno/2.5-diagramas-uml.md#diagrama-clases)
  - [10.2. Diagrama de Secuencia](./2-diseno/2.5-diagramas-uml.md#diagrama-secuencia)
  - [10.3. Diagrama de Actividades](./2-diseno/2.5-diagramas-uml.md#diagrama-actividades)
  - [10.4. Diagrama de Estados](./2-diseno/2.5-diagramas-uml.md#diagrama-estados)
  - [10.5. Diagrama de Componentes](./2-diseno/2.5-diagramas-uml.md#diagrama-componentes)
  - [10.6. Diagrama de Despliegue](./2-diseno/2.5-diagramas-uml.md#diagrama-despliegue)
- [11. Diseño de Seguridad](./2-diseno/2.6-diseno-seguridad.md)
  - [11.1. Arquitectura de Seguridad](./2-diseno/2.6-diseno-seguridad.md#arquitectura-seguridad)
  - [11.2. Flujo de Autenticación](./2-diseno/2.6-diseno-seguridad.md#autenticacion)
  - [11.3. Sistema de Autorización RBAC](./2-diseno/2.6-diseno-seguridad.md#rbac)
  - [11.4. Encriptación de Datos](./2-diseno/2.6-diseno-seguridad.md#encriptacion)
  - [11.5. Gestión de Sesiones](./2-diseno/2.6-diseno-seguridad.md#sesiones)
  - [11.6. Auditoría y Logs](./2-diseno/2.6-diseno-seguridad.md#auditoria)

---

### FASE 3: IMPLEMENTACIÓN

- [12. Stack Tecnológico](./3-implementacion/3.1-stack-tecnologico.md)
  - [12.1. Frontend](./3-implementacion/3.1-stack-tecnologico.md#frontend)
  - [12.2. Backend](./3-implementacion/3.1-stack-tecnologico.md#backend)
  - [12.3. Base de Datos](./3-implementacion/3.1-stack-tecnologico.md#base-datos)
  - [12.4. Infraestructura](./3-implementacion/3.1-stack-tecnologico.md#infraestructura)
- [13. Configuración del Entorno](./3-implementacion/3.2-configuracion-entorno.md)
  - [13.1. Entorno de Desarrollo](./3-implementacion/3.2-configuracion-entorno.md#desarrollo)
  - [13.2. Entorno de Testing](./3-implementacion/3.2-configuracion-entorno.md#testing)
  - [13.3. Entorno de Staging](./3-implementacion/3.2-configuracion-entorno.md#staging)
  - [13.4. Entorno de Producción](./3-implementacion/3.2-configuracion-entorno.md#produccion)
  - [13.5. Variables de Entorno](./3-implementacion/3.2-configuracion-entorno.md#variables)
- [14. Implementación de Módulos](./3-implementacion/3.3-implementacion-modulos.md)
  - [14.1. Autenticación](./3-implementacion/3.3-implementacion-modulos.md#autenticacion)
  - [14.2. Ciudadanos](./3-implementacion/3.3-implementacion-modulos.md#ciudadanos)
  - [14.3. Personal Municipal](./3-implementacion/3.3-implementacion-modulos.md#personal)
  - [14.4. Notificaciones](./3-implementacion/3.3-implementacion-modulos.md#notificaciones)
  - [14.5. Administrativo](./3-implementacion/3.3-implementacion-modulos.md#administrativo)
  - [14.6. Reportes](./3-implementacion/3.3-implementacion-modulos.md#reportes)
- [15. Scripts SQL](./3-implementacion/3.4-scripts-sql.md)
  - [15.1. Scripts de Creación](./3-implementacion/3.4-scripts-sql.md#creacion)
  - [15.2. Scripts de Datos Iniciales](./3-implementacion/3.4-scripts-sql.md#datos-iniciales)
- [16. Implementación de Seguridad](./3-implementacion/3.5-implementacion-seguridad.md)
  - [16.1. Autenticación JWT](./3-implementacion/3.5-implementacion-seguridad.md#jwt)
  - [16.2. Doble Factor (2FA)](./3-implementacion/3.5-implementacion-seguridad.md#2fa)
  - [16.3. RBAC - Control de Acceso](./3-implementacion/3.5-implementacion-seguridad.md#rbac)
  - [16.4. Encriptación de Datos](./3-implementacion/3.5-implementacion-seguridad.md#encriptacion)
  - [16.5. Protección CSRF/XSS](./3-implementacion/3.5-implementacion-seguridad.md#proteccion-web)
  - [16.6. Rate Limiting](./3-implementacion/3.5-implementacion-seguridad.md#rate-limiting)
  - [16.7. Sistema de Auditoría](./3-implementacion/3.5-implementacion-seguridad.md#auditoria)
- [17. Documentación del Código](./3-implementacion/3.6-documentacion-codigo.md)
  - [17.1. README y Guías](./3-implementacion/3.6-documentacion-codigo.md#readme)

---

### FASE 4: PRUEBAS

- [18. Plan de Pruebas](./4-pruebas/4.1-plan-pruebas.md)
  - [18.1. Estrategia de Pruebas](./4-pruebas/4.1-plan-pruebas.md#estrategia)
  - [18.2. Tipos de Pruebas](./4-pruebas/4.1-plan-pruebas.md#tipos)
  - [18.3. Alcance de Pruebas](./4-pruebas/4.1-plan-pruebas.md#alcance)
- [19. Pruebas Unitarias](./4-pruebas/4.2-pruebas-unitarias.md)
  - [19.1. Configuración de Frameworks](./4-pruebas/4.2-pruebas-unitarias.md#configuracion)
  - [19.2. Backend](./4-pruebas/4.2-pruebas-unitarias.md#backend)
  - [19.3. Frontend](./4-pruebas/4.2-pruebas-unitarias.md#frontend)
  - [19.4. Cobertura de Código](./4-pruebas/4.2-pruebas-unitarias.md#cobertura)
  - [19.5. Mocks y Stubs](./4-pruebas/4.2-pruebas-unitarias.md#mocks)
- [20. Pruebas Funcionales](./4-pruebas/4.3-pruebas-funcionales.md)
  - [20.1. Casos de Prueba por Módulo](./4-pruebas/4.3-pruebas-funcionales.md#casos-prueba)
  - [20.2. Validación de Requerimientos](./4-pruebas/4.3-pruebas-funcionales.md#validacion)
  - [20.3. Flujos de Usuario](./4-pruebas/4.3-pruebas-funcionales.md#flujos)
  - [20.4. Matriz de Trazabilidad](./4-pruebas/4.3-pruebas-funcionales.md#trazabilidad)
- [21. Pruebas de Seguridad](./4-pruebas/4.4-pruebas-seguridad.md)
  - [21.1. Penetración](./4-pruebas/4.4-pruebas-seguridad.md#penetracion)
  - [21.2. Vulnerabilidades](./4-pruebas/4.4-pruebas-seguridad.md#vulnerabilidades)
  - [21.3. Autenticación](./4-pruebas/4.4-pruebas-seguridad.md#autenticacion)
  - [21.4. Autorización](./4-pruebas/4.4-pruebas-seguridad.md#autorizacion)
  - [21.5. Encriptación](./4-pruebas/4.4-pruebas-seguridad.md#encriptacion)
  - [21.6. OWASP Top 10](./4-pruebas/4.4-pruebas-seguridad.md#owasp)

---

### FASE 5: DESPLIEGUE

- [22. Estrategia de Despliegue](./5-despliegue/5.1-estrategia-despliegue.md)
  - [22.1. Metodología](./5-despliegue/5.1-estrategia-despliegue.md#metodologia)
  - [22.2. Calendario](./5-despliegue/5.1-estrategia-despliegue.md#calendario)
  - [22.3. Roles y Responsabilidades](./5-despliegue/5.1-estrategia-despliegue.md#roles)
  - [22.4. Plan de Rollback](./5-despliegue/5.1-estrategia-despliegue.md#rollback)

---

### FASE 6: MANTENIMIENTO

- [23. Plan de Mantenimiento](./6-mantenimiento/6.1-plan-mantenimiento.md)
  - [23.1. Tipos](./6-mantenimiento/6.1-plan-mantenimiento.md#tipos)
  - [23.2. Calendario](./6-mantenimiento/6.1-plan-mantenimiento.md#calendario)
  - [23.3. Ventanas](./6-mantenimiento/6.1-plan-mantenimiento.md#ventanas)
  - [23.4. Procedimientos](./6-mantenimiento/6.1-plan-mantenimiento.md#procedimientos)
- [24. Gestión de Versiones](./6-mantenimiento/6.2-gestion-versiones.md)
  - [24.1. Control de Versiones](./6-mantenimiento/6.2-gestion-versiones.md#control)
  - [24.2. Release Notes](./6-mantenimiento/6.2-gestion-versiones.md#release-notes)
  - [24.3. Versionado Semántico](./6-mantenimiento/6.2-gestion-versiones.md#semantico)
  - [24.4. Changelog](./6-mantenimiento/6.2-gestion-versiones.md#changelog)