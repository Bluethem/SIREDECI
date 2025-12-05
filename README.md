# Sistema de Denuncias Ciudadanas - Documentación Completa

## Tabla de Contenido

### Fase 1: Requisitos

- [1. Descripción del Proyecto](./1-requisitos/1.1-descripcion.md)
  - [1.1. Introducción](./1-requisitos/1.1-descripcion.md#introduccion)
  - [1.2. Objetivos del Sistema](./1-requisitos/1.1-descripcion.md#objetivos)
  - [1.3. Alcance del Proyecto](./1-requisitos/1.1-descripcion.md#alcance)
  - [1.4. Stakeholders](./1-requisitos/1.1-descripcion.md#stakeholders)
- [2. Requerimientos Funcionales](./1-requisitos/1.2-requisitos-funcionales.md)
- [3. Requerimientos No Funcionales](./1-requisitos/1.3-requisitos-no-funcionales.md)
- [4. Requerimientos de Seguridad](./1-requisitos/1.4-requisitos-seguridad.md)
- [5. Requerimientos Regulatorios y Legales](./1-requisitos/1.5-requisitos-legales.md)

### Fase 2: Diseño del Sistema

- [6. Arquitectura del Sistema](./2-diseno/2.1-arquitectura.md)
- [7. Diseño Conceptual](./2-diseno/2.2-diseno-conceptual.md)
- [8. Modelo Relacional](./2-diseno/2.3-modelo-er.md)
- [9. Diseño de Interfaz de Usuario (Mockups)](./2-diseno/2.4-diseno-ui.md)
- [10. Diagramas UML](./2-diseno/2.5-diagramas-uml.md)
  - [10.1. Diagrama de Clases](./2-diseno/2.5-diagramas-uml.md#diagrama-de-clases)
  - [10.2. Diagrama de Secuencia](./2-diseno/2.5-diagramas-uml.md#diagrama-de-secuencia)
  - [10.3. Diagrama de Actividades](./2-diseno/2.5-diagramas-uml.md#diagrama-de-actividades)
  - [10.4. Diagrama de Estados](./2-diseno/2.5-diagramas-uml.md#diagrama-de-estados)
  - [10.5. Diagrama de Componentes](./2-diseno/2.5-diagramas-uml.md#diagrama-de-componentes)
  - [10.6. Diagrama de Despliegue](./2-diseno/2.5-diagramas-uml.md#diagrama-de-despliegue)
- [11. Diseño de Seguridad](./2-diseno/2.6-diseno-seguridad.md)
  - [11.1. Arquitectura de Seguridad](./2-diseno/2.6-diseno-seguridad.md#arquitectura-seguridad)
  - [11.2. Flujo de Autenticación](./2-diseno/2.6-diseno-seguridad.md#autenticacion)
  - [11.3. Sistema de Autorización RBAC](./2-diseno/2.6-diseno-seguridad.md#rbac)
  - [11.4. Encriptación de Datos](./2-diseno/2.6-diseno-seguridad.md#encriptacion)
  - [11.5. Gestión de Sesiones](./2-diseno/2.6-diseno-seguridad.md#sesiones)
  - [11.6. Auditoría y Logs](./2-diseno/2.6-diseno-seguridad.md#auditoria)

### Fase 3: Implementación

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
- [17. Documentación del Código](./3-implementacion/3.6-documentacion-codigo.md)

### Fase 4: Pruebas

- [18. Plan de Pruebas](./4-pruebas/4.1-plan-pruebas.md)
  - [18.1. Estrategia de Pruebas](./4-pruebas/4.1-plan-pruebas.md#estrategia)
  - [18.2. Tipos de Pruebas](./4-pruebas/4.1-plan-pruebas.md#tipos)
  - [18.3. Alcance de Pruebas](./4-pruebas/4.1-plan-pruebas.md#alcance)
- [19. Pruebas Unitarias](./4-pruebas/4.2-pruebas-unitarias.md)
  - [19.1. Configuración de Frameworks](./4-pruebas/4.2-pruebas-unitarias.md#configuracion)
  - [19.2. Backend](./4-pruebas/4.2-pruebas-unitarias.md#backend)
  - [19.3. Frontend](./4-pruebas/4.2-pruebas-unitarias.md#frontend)

### Fase 5: Despliegue

- [20. Estrategia de Despliegue](./5-despliegue/5.1-estrategia-despliegue.md)
  - [20.1. Metodología](./5-despliegue/5.1-estrategia-despliegue.md#metodologia)
  - [20.2. Calendario](./5-despliegue/5.1-estrategia-despliegue.md#calendario)
  - [20.3. Roles y Responsabilidades](./5-despliegue/5.1-estrategia-despliegue.md#roles)
  - [20.4. Plan de Rollback](./5-despliegue/5.1-estrategia-despliegue.md#rollback)