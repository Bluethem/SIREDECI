import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/ciudadano/login'
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
