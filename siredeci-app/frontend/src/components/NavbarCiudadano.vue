<template>
  <header class="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 sm:px-4 py-2.5 shadow-sm">
    <div class="flex items-center gap-2 text-black dark:text-white min-w-0 flex-shrink-0">
      <router-link 
        to="/ciudadano/dashboard" 
        class="flex items-center gap-2 hover:text-cyan-400 transition-colors duration-200"
      >
        <img 
          src="@/assets/android-chrome-192x192.png" 
          alt="SIREDECI Logo"
          class="h-8 w-8 object-contain flex-shrink-0"
        />
        <h2 class="text-sm sm:text-base font-bold leading-tight tracking-tight whitespace-nowrap">
          SIREDECI
        </h2>
      </router-link>
    </div>

    <div class="flex items-center gap-2 min-w-0 flex-shrink-0">
      <nav class="hidden lg:flex items-center gap-3 mr-2">
        <router-link to="/ciudadano/dashboard" 
                     class="text-gray-600 dark:text-gray-300 hover:text-primary text-sm font-medium whitespace-nowrap"
                     :class="{ 'text-primary font-bold': $route.path === '/ciudadano/dashboard' }">
          Dashboard
        </router-link>
        <router-link to="/ciudadano/mis-denuncias" 
                     class="text-gray-600 dark:text-gray-300 hover:text-primary text-sm font-medium whitespace-nowrap"
                     :class="{ 'text-primary font-bold': $route.path.includes('/mis-denuncias') || $route.path.includes('/denuncia/') }">
          Mis Denuncias
        </router-link>
        <router-link to="/ciudadano/registrar-denuncia" 
                     class="text-gray-600 dark:text-gray-300 hover:text-primary text-sm font-medium whitespace-nowrap"
                     :class="{ 'text-primary font-bold': $route.path === '/ciudadano/registrar-denuncia' }">
          Crear Denuncia
        </router-link>
      </nav>
      <div class="flex items-center gap-2 flex-shrink-0">
        <button
          class="relative flex items-center justify-center w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          @click="goToNotificaciones"
        >
          <span class="material-symbols-outlined text-[20px] leading-none">notifications</span>
          <span
            v-if="unreadCount > 0"
            class="absolute -top-0.5 -right-0.5 inline-flex items-center justify-center min-w-[16px] h-4 px-1 rounded-full bg-red-500 text-white text-[10px] font-semibold"
          >
            {{ unreadCount > 9 ? '9+' : unreadCount }}
          </span>
        </button>
        
        <!-- Settings dropdown with Dark Mode toggle -->
        <div class="relative" ref="settingsRef">
          <button @click="toggleSettings"
                  class="flex items-center justify-center w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
            <span class="material-symbols-outlined text-[20px] leading-none">settings</span>
          </button>
          
          <!-- Dropdown menu -->
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div v-if="showSettings"
              @click.stop
              class="absolute top-full right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-2xl border border-gray-200 dark:border-gray-700 py-1 z-[9999] origin-top-right">

              <!-- Botón modo oscuro / claro -->
              <button @click="toggleTheme"
                      type="button"
                      class="w-full flex items-center justify-between px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors cursor-pointer">
                <div class="flex items-center gap-2.5">
                  <span class="material-symbols-outlined text-[20px] leading-none">
                    {{ isDark ? 'dark_mode' : 'light_mode' }}
                  </span>
                  <span class="font-medium">{{ isDark ? 'Modo Oscuro' : 'Modo Claro' }}</span>
                </div>
                <div :class="[
                  'relative inline-flex h-5 w-9 items-center rounded-full transition-colors flex-shrink-0',
                  isDark ? 'bg-primary' : 'bg-gray-300'
                ]">
                  <span :class="[
                    'inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow-sm transition-transform',
                    isDark ? 'translate-x-4.5' : 'translate-x-0.5'
                  ]"></span>
                </div>
              </button>

              <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>

              <!-- Botón cerrar sesión -->
              <button @click="logout"
                      type="button"
                      class="w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors cursor-pointer">
                <span class="material-symbols-outlined text-[20px] leading-none">logout</span>
                <span class="font-medium">Cerrar Sesión</span>
              </button>
            </div>
          </transition>
        </div>
        
        <div
          class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-9 flex-shrink-0 ring-2 ring-white dark:ring-gray-700 cursor-pointer"
          :style="avatarStyle"
          @click="goToPerfil"
        ></div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/stores/theme'
import api from '@/services/api'
import authService from '@/services/auth'

const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const showSettings = ref(false)
const unreadCount = ref(0)

// Toggle del dropdown
const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

// Cerrar dropdown al hacer clic fuera
const settingsRef = ref(null)

const handleClickOutside = (event) => {
  if (!showSettings.value) return

  const el = settingsRef.value
  if (el && !el.contains(event.target)) {
    showSettings.value = false
  }
}

const cargarUnread = async () => {
  try {
    const user = authService.getCurrentUser()
    if (!user || !user.id_usuario) {
      unreadCount.value = 0
      return
    }
    const response = await api.get('/ciudadanos/notificaciones/', {
      params: { id_usuario: user.id_usuario }
    })
    const items = response.data?.results || []
    unreadCount.value = items.filter((n) => n.estado_envio !== 'Leído').length
  } catch (error) {
    console.error('Error al cargar contador de notificaciones de ciudadano:', error)
    unreadCount.value = 0
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  cargarUnread()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const logout = () => {
  authService.logout()
  router.push('/ciudadano/login')
}

const goToNotificaciones = () => {
  router.push({ name: 'ciudadano-notificaciones' })
}

const goToPerfil = () => {
  router.push({ name: 'ciudadano-perfil' })
}

const avatarStyle = computed(() => {
  const user = authService.getCurrentUser()
  const name = encodeURIComponent(
    user && (user.nombre || user.apellido)
      ? `${user.nombre || ''} ${user.apellido || ''}`.trim()
      : 'Usuario'
  )
  const url = `https://ui-avatars.com/api/?name=${name}&background=2e87ad&color=fff`
  return `background-image: url('${url}')`
})
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

/* Custom translate for toggle */
.translate-x-4\.5 {
  transform: translateX(1.125rem);
}
</style>
