<template>
  <aside class="flex flex-col w-72 bg-[#041227] text-white shadow-xl">
    <!-- Branding -->
    <div class="flex items-center gap-3 px-5 py-4 border-b border-white/10">
      <div class="h-9 w-9 rounded-lg bg-white flex items-center justify-center">
        <img
          src="@/assets/android-chrome-192x192.png"
          alt="Municipalidad Logo"
          class="h-7 w-7 object-contain"
        />
      </div>
      <div class="flex flex-col">
        <span class="text-sm font-semibold leading-tight">SIREDECI</span>
        <span class="text-xs text-white/70 leading-tight">Gestión de denuncias</span>
      </div>
    </div>

    <!-- User info -->
    <div class="px-5 py-4 border-b border-white/10 flex items-center gap-3 bg-white/5">
      <div
        class="bg-center bg-no-repeat bg-cover rounded-full size-9 flex-shrink-0 ring-2 ring-white/20"
        :style="avatarStyle"
      ></div>
      <div class="flex flex-col min-w-0">
        <span class="text-sm font-semibold truncate">{{ displayName }}</span>
        <span class="text-xs text-white/70 truncate">{{ user?.email || 'Sin correo' }}</span>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
      <button
        v-for="item in visibleMenuItems"
        :key="item.to"
        @click="goTo(item.to)"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors"
        :class="isActive(item.to)
          ? 'bg-[#0ea5e9] text-white shadow-md'
          : 'bg-transparent text-white/80 hover:bg-white/10 hover:text-white'"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">
          {{ item.icon }}
        </span>
        <span class="truncate flex-1">{{ item.label }}</span>
        <span
          v-if="item.to === '/admin/notificaciones' && unreadNotificaciones > 0"
          class="inline-flex items-center justify-center min-w-[18px] h-5 px-1.5 rounded-full bg-red-500 text-white text-[11px] font-semibold"
        >
          {{ unreadNotificaciones > 9 ? '9+' : unreadNotificaciones }}
        </span>
      </button>
    </nav>

    <!-- Footer actions -->
    <div class="px-3 py-4 border-t border-white/10 flex flex-col gap-2">
      <button
        @click="goTo('/admin/perfil')"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium bg-white/5 text-white hover:bg-white/10 transition-colors"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">account_circle</span>
        <span>Mi perfil</span>
      </button>
      <button
        @click="logout"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold bg-transparent text-red-200 hover:bg-red-500/10 hover:text-white transition-colors"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">logout</span>
        <span>Cerrar sesión</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { isSuperAdmin, isAdmin, isJefeArea, isAuditor } from '@/utils/roles'

const router = useRouter()
const route = useRoute()

const unreadNotificaciones = ref(0)

const user = computed(() => {
  try {
    const raw = localStorage.getItem('admin_user')
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
})

const displayName = computed(() => {
  if (!user.value) return 'Usuario administrador'
  return user.value.nombre_usuario || user.value.email || 'Usuario administrador'
})

const avatarStyle = computed(() => {
  const name = encodeURIComponent(displayName.value || 'Usuario')
  const url = `https://ui-avatars.com/api/?name=${name}&background=0f5dd1&color=fff`
  return `background-image: url('${url}')`
})

const menuItems = computed(() => [
  { to: '/admin/dashboard', label: 'Dashboard', icon: 'dashboard', visible: true },
  { to: '/admin/analisis-geografico', label: 'Análisis geográfico', icon: 'map', visible: isSuperAdmin() || isAdmin() || isAuditor() },
  { to: '/admin/reportes', label: 'Reportes', icon: 'bar_chart', visible: isSuperAdmin() || isAdmin() || isJefeArea() || isAuditor() },
  { to: '/admin/desempeno', label: 'Desempeño', icon: 'leaderboard', visible: isSuperAdmin() || isAdmin() || isJefeArea() || isAuditor() },
  { to: '/admin/indicadores', label: 'Indicadores', icon: 'insights', visible: isSuperAdmin() || isAdmin() || isJefeArea() || isAuditor() },
  { to: '/admin/notificaciones', label: 'Notificaciones', icon: 'notifications', visible: isSuperAdmin() || isAdmin() || isJefeArea() || isAuditor() },
])

const visibleMenuItems = computed(() => menuItems.value.filter(m => m.visible))

const isActive = (path) => {
  try {
    return route.path === path || route.path.startsWith(path + '/')
  } catch {
    return false
  }
}

const goTo = (path) => {
  if (route.path !== path) {
    router.push(path)
  }
}

const cargarUnreadNotificaciones = async () => {
  try {
    const response = await axios.get('/api/notificaciones/usuario/')
    const items = response.data?.results || []
    unreadNotificaciones.value = items.filter((n) => n.estado_envio !== 'Leído').length
  } catch (error) {
    console.error('Error al cargar contador de notificaciones internas (admin):', error)
    unreadNotificaciones.value = 0
  }
}

onMounted(() => {
  cargarUnreadNotificaciones()
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('admin_user')
  localStorage.removeItem('admin_personal')
  delete axios.defaults.headers.common['Authorization']
  router.push({ name: 'admin-login' })
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
}
</style>
