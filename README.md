# Sistema de Denuncias Ciudadanas - Documentación Completa

## Tabla de Contenido

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
  - [7.1. Diagrama Conceptual General](./2-diseno/2.2-diseno-conceptual.md#diagrama-general)
  - [7.2. Entidades Principales](./2-diseno/2.2-diseno-conceptual.md#entidades)
  - [7.3. Relaciones entre Entidades](./2-diseno/2.2-diseno-conceptual.md#relaciones)

- [8. Modelo de Datos](./2-diseno/2.3-modelo-datos.md)
  - [8.1. Diccionario de Datos Completo](./2-diseno/2.3-modelo-datos.md#diccionario-completo)
  - [8.2. Módulos del Sistema](./2-diseno/2.3-modelo-datos.md#modulos)
    - [8.2.1. Ciudadanos](./2-diseno/2.3-modelo-datos.md#modulo-ciudadanos)
    - [8.2.2. Personal Municipal](./2-diseno/2.3-modelo-datos.md#modulo-personal)
    - [8.2.3. Notificaciones](./2-diseno/2.3-modelo-datos.md#modulo-notificaciones)
    - [8.2.4. Administrativo](./2-diseno/2.3-modelo-datos.md#modulo-administrativo)
    - [8.2.5. Reportes y Estadísticas](./2-diseno/2.3-modelo-datos.md#modulo-reportes)

- [9. Modelo Entidad-Relación](./2-diseno/2.4-modelo-er.md)
  - [9.1. Diagrama ER Completo](./2-diseno/2.4-modelo-er.md#diagrama-completo)
  - [9.2. Diagrama ER por Módulo](./2-diseno/2.4-modelo-er.md#por-modulo)

- [10. Modelo Relacional](./2-diseno/2.5-modelo-relacional.md)
- [11. Diseño de Interfaz de Usuario (mockups)](./2-diseno/2.6-diseno-ui.md)

- [12. Diagramas UML](./2-diseno/2.8-diagramas-uml.md)
  - [12.1. Diagrama de Clases](./2-diseno/2.8-diagramas-uml.md#diagrama-clases)
  - [12.2. Diagrama de Secuencia](./2-diseno/2.8-diagramas-uml.md#diagrama-secuencia)
  - [12.3. Diagrama de Actividades](./2-diseno/2.8-diagramas-uml.md#diagrama-actividades)
  - [12.4. Diagrama de Estados](./2-diseno/2.8-diagramas-uml.md#diagrama-estados)
  - [12.5. Diagrama de Componentes](./2-diseno/2.8-diagramas-uml.md#diagrama-componentes)
  - [12.6. Diagrama de Despliegue](./2-diseno/2.8-diagramas-uml.md#diagrama-despliegue)

- [13. Diseño de Seguridad](./2-diseno/2.9-diseno-seguridad.md)
  - [13.1. Arquitectura de Seguridad](./2-diseno/2.9-diseno-seguridad.md#arquitectura-seguridad)
  - [13.2. Flujo de Autenticación](./2-diseno/2.9-diseno-seguridad.md#autenticacion)
  - [13.3. Sistema de Autorización RBAC](./2-diseno/2.9-diseno-seguridad.md#rbac)
  - [13.4. Encriptación de Datos](./2-diseno/2.9-diseno-seguridad.md#encriptacion)
  - [13.5. Gestión de Sesiones](./2-diseno/2.9-diseno-seguridad.md#sesiones)
  - [13.6. Auditoría y Logs](./2-diseno/2.9-diseno-seguridad.md#auditoria)

---

### FASE 3: IMPLEMENTACIÓN

- [14. Stack Tecnológico](./3-implementacion/3.1-stack-tecnologico.md)
  - [14.1. Frontend](./3-implementacion/3.1-stack-tecnologico.md#frontend)
  - [14.2. Backend](./3-implementacion/3.1-stack-tecnologico.md#backend)
  - [14.3. Base de Datos](./3-implementacion/3.1-stack-tecnologico.md#base-datos)
  - [14.4. Infraestructura](./3-implementacion/3.1-stack-tecnologico.md#infraestructura)

- [15. Configuración del Entorno](./3-implementacion/3.2-configuracion-entorno.md)
  - [15.1. Entorno de Desarrollo](./3-implementacion/3.2-configuracion-entorno.md#desarrollo)
  - [15.2. Entorno de Testing](./3-implementacion/3.2-configuracion-entorno.md#testing)
  - [15.3. Entorno de Staging](./3-implementacion/3.2-configuracion-entorno.md#staging)
  - [15.4. Entorno de Producción](./3-implementacion/3.2-configuracion-entorno.md#produccion)
  - [15.5. Variables de Entorno](./3-implementacion/3.2-configuracion-entorno.md#variables)

- [16. Implementación de Módulos](./3-implementacion/3.4-implementacion-modulos.md)
  - [16.1. Autenticación](./3-implementacion/3.4-implementacion-modulos.md#autenticacion)
  - [16.2. Ciudadanos](./3-implementacion/3.4-implementacion-modulos.md#ciudadanos)
  - [16.3. Personal Municipal](./3-implementacion/3.4-implementacion-modulos.md#personal)
  - [16.4. Notificaciones](./3-implementacion/3.4-implementacion-modulos.md#notificaciones)
  - [16.5. Administrativo](./3-implementacion/3.4-implementacion-modulos.md#administrativo)
  - [16.6. Reportes](./3-implementacion/3.4-implementacion-modulos.md#reportes)

- [17. Scripts SQL](./3-implementacion/3.5-scripts-sql.md)
  - [17.1. Scripts de Creación](./3-implementacion/3.5-scripts-sql.md#creacion)
  - [17.2. Scripts de Datos Iniciales](./3-implementacion/3.5-scripts-sql.md#datos-iniciales)

- [18. Implementación de Seguridad](./3-implementacion/3.6-implementacion-seguridad.md)
  - [18.1. Autenticación JWT](./3-implementacion/3.6-implementacion-seguridad.md#jwt)
  - [18.2. Doble Factor (2FA)](./3-implementacion/3.6-implementacion-seguridad.md#2fa)
  - [18.3. RBAC - Control de Acceso](./3-implementacion/3.6-implementacion-seguridad.md#rbac)
  - [18.4. Encriptación de Datos](./3-implementacion/3.6-implementacion-seguridad.md#encriptacion)
  - [18.5. Protección CSRF/XSS](./3-implementacion/3.6-implementacion-seguridad.md#proteccion-web)
  - [18.6. Rate Limiting](./3-implementacion/3.6-implementacion-seguridad.md#rate-limiting)
  - [18.7. Sistema de Auditoría](./3-implementacion/3.6-implementacion-seguridad.md#auditoria)

- [19. Documentación del Código](./3-implementacion/3.8-documentacion-codigo.md)
  - [19.1. README y Guías](./3-implementacion/3.8-documentacion-codigo.md#readme)

---

### FASE 4: PRUEBAS

- [20. Plan de Pruebas](./4-pruebas/4.1-plan-pruebas.md)
  - [20.1. Estrategia de Pruebas](./4-pruebas/4.1-plan-pruebas.md#estrategia)
  - [20.2. Tipos de Pruebas](./4-pruebas/4.1-plan-pruebas.md#tipos)
  - [20.3. Alcance de Pruebas](./4-pruebas/4.1-plan-pruebas.md#alcance)

- [21. Pruebas Unitarias](./4-pruebas/4.2-pruebas-unitarias.md)
  - [21.1. Configuración de Frameworks](./4-pruebas/4.2-pruebas-unitarias.md#configuracion)
  - [21.2. Backend](./4-pruebas/4.2-pruebas-unitarias.md#backend)
  - [21.3. Frontend](./4-pruebas/4.2-pruebas-unitarias.md#frontend)
  - [21.4. Cobertura de Código](./4-pruebas/4.2-pruebas-unitarias.md#cobertura)
  - [21.5. Mocks y Stubs](./4-pruebas/4.2-pruebas-unitarias.md#mocks)

- [22. Pruebas Funcionales](./4-pruebas/4.4-pruebas-funcionales.md)
  - [22.1. Casos de Prueba por Módulo](./4-pruebas/4.4-pruebas-funcionales.md#casos-prueba)
  - [22.2. Validación de Requerimientos](./4-pruebas/4.4-pruebas-funcionales.md#validacion)
  - [22.3. Flujos de Usuario](./4-pruebas/4.4-pruebas-funcionales.md#flujos)
  - [22.4. Matriz de Trazabilidad](./4-pruebas/4.4-pruebas-funcionales.md#trazabilidad)

- [23. Pruebas de Seguridad](./4-pruebas/4.5-pruebas-seguridad.md)
  - [23.1. Penetración](./4-pruebas/4.5-pruebas-seguridad.md#penetracion)
  - [23.2. Vulnerabilidades](./4-pruebas/4.5-pruebas-seguridad.md#vulnerabilidades)
  - [23.3. Autenticación](./4-pruebas/4.5-pruebas-seguridad.md#autenticacion)
  - [23.4. Autorización](./4-pruebas/4.5-pruebas-seguridad.md#autorizacion)
  - [23.5. Encriptación](./4-pruebas/4.5-pruebas-seguridad.md#encriptacion)
  - [23.6. OWASP Top 10](./4-pruebas/4.5-pruebas-seguridad.md#owasp)

---

### FASE 5: DESPLIEGUE

- [24. Estrategia de Despliegue](./5-despliegue/5.1-estrategia-despliegue.md)
  - [24.1. Metodología](./5-despliegue/5.1-estrategia-despliegue.md#metodologia)
  - [24.2. Calendario](./5-despliegue/5.1-estrategia-despliegue.md#calendario)
  - [24.3. Roles y Responsabilidades](./5-despliegue/5.1-estrategia-despliegue.md#roles)
  - [24.4. Plan de Rollback](./5-despliegue/5.1-estrategia-despliegue.md#rollback)

---

### FASE 6: MANTENIMIENTO

- [25. Plan de Mantenimiento](./6-mantenimiento/6.1-plan-mantenimiento.md)
  - [25.1. Tipos](./6-mantenimiento/6.1-plan-mantenimiento.md#tipos)
  - [25.2. Calendario](./6-mantenimiento/6.1-plan-mantenimiento.md#calendario)
  - [25.3. Ventanas](./6-mantenimiento/6.1-plan-mantenimiento.md#ventanas)
  - [25.4. Procedimientos](./6-mantenimiento/6.1-plan-mantenimiento.md#procedimientos)

- [26. Gestión de Versiones](./6-mantenimiento/6.7-gestion-versiones.md)
  - [26.1. Control de Versiones](./6-mantenimiento/6.7-gestion-versiones.md#control)
  - [26.2. Release Notes](./6-mantenimiento/6.7-gestion-versiones.md#release-notes)
  - [26.3. Versionado Semántico](./6-mantenimiento/6.7-gestion-versiones.md#semantico)
  - [26.4. Changelog](./6-mantenimiento/6.7-gestion-versiones.md#changelog)
