import { createRouter, createWebHistory } from 'vue-router'
import { hasAnyRole, getDefaultAdminRoute } from '@/utils/roles'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/public/LandingPage.vue')
  },
  {
    path: '/login',
    redirect: '/ciudadano/login'
  },
  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('../views/admin/LoginAdmin.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: () => import('../views/admin/DashboardAdmin.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-006'] }
  },
  {
    path: '/admin/analisis-geografico',
    name: 'admin-analisis-geografico',
    component: () => import('../views/admin/AnalisisGeografico.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-006'] }
  },
  {
    path: '/admin/indicadores',
    name: 'admin-indicadores',
    component: () => import('../views/admin/Indicadores.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-006'] }
  },
  {
    path: '/admin/desempeno',
    name: 'admin-desempeno',
    component: () => import('../views/admin/RankingDesempeno.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-006'] }
  },
  {
    path: '/admin/perfil',
    name: 'admin-perfil',
    component: () => import('../views/admin/PerfilUsuario.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-004', 'ROL-006'] }
  },
  {
    path: '/admin/notificaciones',
    name: 'admin-notificaciones',
    component: () => import('../views/admin/NotificacionesAdmin.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-004', 'ROL-006'] }
  },
  {
    path: '/admin/reportes',
    name: 'admin-reportes',
    component: () => import('../views/admin/ReportesHub.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-006'] }
  },
  {
    path: '/admin/generador-reportes',
    name: 'admin-generador-reportes',
    component: () => import('../views/admin/GeneradorReportes.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002'] }
  },
  {
    path: '/admin/seleccion-datos-reportes',
    name: 'admin-seleccion-datos-reportes',
    component: () => import('../views/admin/SeleccionDatosReportes.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002'] }
  },
  {
    path: '/admin/vista-previa-reportes',
    name: 'admin-vista-previa-reportes',
    component: () => import('../views/admin/VistaPreviaReportes.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-006'] }
  },
  {
    path: '/municipal/dashboard',
    name: 'municipal-dashboard',
    component: () => import('../views/personal_municipal/DashboardArea.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-004'] }
  },
  {
    path: '/municipal/mi-area',
    name: 'municipal-mi-area',
    component: () => import('../views/personal_municipal/MiAreaAsignadas.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-003', 'ROL-004', 'ROL-001', 'ROL-002'] }
  },
  {
    path: '/municipal/mi-area/:id',
    name: 'municipal-detalle-asignada',
    component: () => import('../views/personal_municipal/DetalleDenunciaAsignada.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-003', 'ROL-004', 'ROL-001', 'ROL-002'] }
  },
  {
    path: '/municipal/pendientes-asignar',
    name: 'municipal-pendientes-asignar',
    component: () => import('../views/personal_municipal/PendientesAsignar.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-003', 'ROL-001', 'ROL-002'] }
  },
  {
    path: '/municipal/duplicadas',
    name: 'municipal-duplicadas-vinculadas',
    component: () => import('../views/personal_municipal/DuplicadasVinculadas.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-003', 'ROL-004', 'ROL-001', 'ROL-002'] }
  },
  {
    path: '/municipal/notificaciones',
    name: 'municipal-notificaciones',
    component: () => import('../views/personal_municipal/NotificacionesMunicipal.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-004'] }
  },
  {
    path: '/municipal/perfil',
    name: 'municipal-perfil',
    component: () => import('../views/personal_municipal/PerfilMunicipal.vue'),
    meta: { requiresAdmin: true, allowedRoles: ['ROL-001', 'ROL-002', 'ROL-003', 'ROL-004'] }
  },
  {
    path: '/ciudadano/login',
    name: 'ciudadano-login',
    component: () => import('../views/ciudadano/LoginCiudadano.vue')
  },
  {
    path: '/ciudadano/dashboard',
    name: 'ciudadano-dashboard',
    component: () => import('../views/ciudadano/DashboardCiudadano.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/perfil',
    name: 'ciudadano-perfil',
    component: () => import('../views/ciudadano/PerfilCiudadano.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/notificaciones',
    name: 'ciudadano-notificaciones',
    component: () => import('../views/ciudadano/NotificacionesCiudadano.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/mis-denuncias',
    name: 'ciudadano-mis-denuncias',
    component: () => import('../views/ciudadano/MisDenuncias.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/registrar-denuncia',
    name: 'ciudadano-registrar-denuncia',
    component: () => import('../views/ciudadano/RegistrarDenuncia.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/denuncia-exitosa',
    name: 'ciudadano-denuncia-exitosa',
    component: () => import('../views/ciudadano/DenunciaExitosa.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/ciudadano/denuncia/:id',
    name: 'ciudadano-detalle-denuncia',
    component: () => import('../views/ciudadano/DetalleDenuncia.vue'),
    meta: { requiresCiudadano: true }
  },
  {
    path: '/public/consulta',
    name: 'consulta-publica',
    component: () => import('../views/public/ConsultaPublica.vue')
  },
  {
    path: '/public/estadisticas',
    name: 'estadisticas-publicas',
    component: () => import('../views/public/EstadisticasPublicas.vue')
  },
  {
    path: '/public/reportes',
    name: 'reportes-publicos',
    component: () => import('../views/public/ReportesPublicos.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isAdminLogged = !!localStorage.getItem('access_token') && !!localStorage.getItem('admin_user')

  const isCiudadanoLogged =
    !!localStorage.getItem('token') &&
    !!localStorage.getItem('user') &&
    localStorage.getItem('tipo_usuario') === 'ciudadano'

  if (to.meta?.requiresAdmin && !isAdminLogged) {
    return next({ name: 'admin-login' })
  }

  // Si ya hay sesión admin, no tiene sentido volver al login de admin
  if (to.name === 'admin-login' && isAdminLogged) {
    const fallback = getDefaultAdminRoute() || '/admin/dashboard'
    if (to.path !== fallback) {
      return next(fallback)
    }
  }

   // Validación por roles para rutas admin
   if (to.meta?.requiresAdmin && Array.isArray(to.meta.allowedRoles) && to.meta.allowedRoles.length > 0) {
     if (!hasAnyRole(to.meta.allowedRoles)) {
       const fallback = getDefaultAdminRoute()
       if (fallback && fallback !== to.path) {
         return next(fallback)
       }
       return next({ name: 'admin-login' })
     }
   }

  if (to.meta?.requiresCiudadano && !isCiudadanoLogged) {
    return next({ name: 'ciudadano-login' })
  }

  return next()
})

export default router
