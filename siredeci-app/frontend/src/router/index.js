import { createRouter, createWebHistory } from 'vue-router'

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
    component: () => import('../views/admin/DashboardAdmin.vue')
  },
  {
    path: '/admin/analisis-geografico',
    name: 'admin-analisis-geografico',
    component: () => import('../views/admin/AnalisisGeografico.vue')
  },
  {
    path: '/admin/indicadores',
    name: 'admin-indicadores',
    component: () => import('../views/admin/Indicadores.vue')
  },
  {
    path: '/admin/desempeno',
    name: 'admin-desempeno',
    component: () => import('../views/admin/RankingDesempeno.vue')
  },
  {
    path: '/admin/reportes',
    name: 'admin-reportes',
    component: () => import('../views/admin/ReportesHub.vue')
  },
  {
    path: '/admin/generador-reportes',
    name: 'admin-generador-reportes',
    component: () => import('../views/admin/GeneradorReportes.vue')
  },
  {
    path: '/admin/seleccion-datos-reportes',
    name: 'admin-seleccion-datos-reportes',
    component: () => import('../views/admin/SeleccionDatosReportes.vue')
  },
  {
    path: '/admin/vista-previa-reportes',
    name: 'admin-vista-previa-reportes',
    component: () => import('../views/admin/VistaPreviaReportes.vue')
  },
  {
    path: '/municipal/dashboard',
    name: 'municipal-dashboard',
    component: () => import('../views/personal_municipal/DashboardArea.vue')
  },
  {
    path: '/municipal/mi-area',
    name: 'municipal-mi-area',
    component: () => import('../views/personal_municipal/MiAreaAsignadas.vue')
  },
  {
    path: '/municipal/mi-area/:id',
    name: 'municipal-detalle-asignada',
    component: () => import('../views/personal_municipal/DetalleDenunciaAsignada.vue')
  },
  {
    path: '/municipal/pendientes-asignar',
    name: 'municipal-pendientes-asignar',
    component: () => import('../views/personal_municipal/PendientesAsignar.vue')
  },
  {
    path: '/municipal/duplicadas',
    name: 'municipal-duplicadas-vinculadas',
    component: () => import('../views/personal_municipal/DuplicadasVinculadas.vue')
  },
  {
    path: '/ciudadano/login',
    name: 'ciudadano-login',
    component: () => import('../views/ciudadano/LoginCiudadano.vue')
  },
  {
    path: '/ciudadano/dashboard',
    name: 'ciudadano-dashboard',
    component: () => import('../views/ciudadano/DashboardCiudadano.vue')
  },
  {
    path: '/ciudadano/mis-denuncias',
    name: 'ciudadano-mis-denuncias',
    component: () => import('../views/ciudadano/MisDenuncias.vue')
  },
  {
    path: '/ciudadano/registrar-denuncia',
    name: 'ciudadano-registrar-denuncia',
    component: () => import('../views/ciudadano/RegistrarDenuncia.vue')
  },
  {
    path: '/ciudadano/denuncia-exitosa',
    name: 'ciudadano-denuncia-exitosa',
    component: () => import('../views/ciudadano/DenunciaExitosa.vue')
  },
  {
    path: '/ciudadano/denuncia/:id',
    name: 'ciudadano-detalle-denuncia',
    component: () => import('../views/ciudadano/DetalleDenuncia.vue')
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
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
