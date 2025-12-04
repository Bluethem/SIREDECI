<template>
  <aside class="flex flex-col h-screen w-64 bg-[#041836] text-white shadow-lg">
    <div class="flex items-center gap-3 px-5 py-4 border-b border-white/10">
      <div class="h-9 w-9 rounded-lg bg-white flex items-center justify-center">
        <img
          src="@/assets/android-chrome-192x192.png"
          alt="Municipalidad Logo"
          class="h-7 w-7 object-contain"
        />
      </div>
      <div class="flex flex-col">
        <span class="text-sm font-semibold leading-tight">Municipalidad</span>
        <span class="text-xs text-white/70 leading-tight">Gestión de Denuncias</span>
      </div>
    </div>

    <div class="px-5 py-4 border-b border-white/10 flex items-center gap-3">
      <div
        class="bg-center bg-no-repeat bg-cover rounded-full size-9 flex-shrink-0 ring-2 ring-white/20"
        style="background-image: url('https://ui-avatars.com/api/?name=Usuario&background=0f5dd1&color=fff')"
      ></div>
      <div class="flex flex-col min-w-0">
        <span class="text-sm font-medium truncate">Usuario</span>
        <span class="text-xs text-white/70 truncate">Área de Fiscalización</span>
      </div>
    </div>

    <nav class="flex-1 px-3 py-4 space-y-2 overflow-y-auto">
      <button
        v-for="item in menuItems"
        :key="item.to"
        @click="goTo(item.to)"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors shadow-sm"
        :class="isActive(item.to)
          ? 'bg-[#0ea5e9] text-white'
          : 'bg-[#041836] text-white/80 hover:bg-[#0ea5e9] hover:text-white'"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">
          {{ item.icon }}
        </span>
        <span class="truncate flex-1">{{ item.label }}</span>
        <span
          v-if="item.to === '/municipal/notificaciones' && unreadNotificaciones > 0"
          class="inline-flex items-center justify-center min-w-[18px] h-5 px-1.5 rounded-full bg-red-500 text-white text-[11px] font-semibold"
        >
          {{ unreadNotificaciones > 9 ? '9+' : unreadNotificaciones }}
        </span>
      </button>
    </nav>

    <div class="px-3 py-4 border-t border-white/10">
      <button
        @click="goTo('/municipal/perfil')"
        class="w-full flex items-center gap-3 px-3 py-2.5 mb-2 rounded-xl text-sm font-medium bg-white/5 text-white hover:bg-white/10 transition-colors"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">account_circle</span>
        <span>Mi perfil</span>
      </button>
      <button
        @click="logout"
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold bg-[#041836] text-red-200 hover:bg-[#0ea5e9] hover:text-white transition-colors shadow-sm"
      >
        <span class="material-symbols-outlined text-[20px] leading-none">logout</span>
        <span>Cerrar Sesión</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const unreadNotificaciones = ref(0)

const menuItems = computed(() => [
  {
    to: '/municipal/dashboard',
    label: 'Dashboard',
    icon: 'dashboard'
  },
  {
    to: '/municipal/mi-area',
    label: 'Mi Área (Asignadas)',
    icon: 'group'
  },
  {
    to: '/municipal/pendientes-asignar',
    label: 'Pendientes de Asignar',
    icon: 'assignment'
  },
  {
    to: '/municipal/duplicadas',
    label: 'Duplicadas/Vinculadas',
    icon: 'link'
  },
  {
    to: '/municipal/notificaciones',
    label: 'Notificaciones',
    icon: 'notifications'
  }
])

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
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
    console.error('Error al cargar contador de notificaciones internas (municipal):', error)
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
