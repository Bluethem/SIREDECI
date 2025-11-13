<template>
  <header class="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 sm:px-4 py-2.5 shadow-sm">
    <div class="flex items-center gap-2 text-gray-900 dark:text-white min-w-0 flex-shrink-0">
      <div class="size-5 text-primary flex-shrink-0">
        <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
          <g clip-path="url(#clip0_6_319)">
            <path d="M8.57829 8.57829C5.52816 11.6284 3.451 15.5145 2.60947 19.7452C1.76794 23.9758 2.19984 28.361 3.85056 32.3462C5.50128 36.3314 8.29667 39.7376 11.8832 42.134C15.4698 44.5305 19.6865 45.8096 24 45.8096C28.3135 45.8096 32.5302 44.5305 36.1168 42.134C39.7033 39.7375 42.4987 36.3314 44.1494 32.3462C45.8002 28.361 46.2321 23.9758 45.3905 19.7452C44.549 15.5145 42.4718 11.6284 39.4217 8.57829L24 24L8.57829 8.57829Z" fill="currentColor"/>
          </g>
          <defs>
            <clipPath id="clip0_6_319">
              <rect fill="white" height="48" width="48"/>
            </clipPath>
          </defs>
        </svg>
      </div>
      <h2 class="text-sm sm:text-base font-bold leading-tight tracking-tight whitespace-nowrap">SIREDECI</h2>
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
        <button class="flex items-center justify-center w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
          <span class="material-symbols-outlined text-[20px] leading-none">notifications</span>
        </button>
        
        <!-- Settings dropdown with Dark Mode toggle -->
        <div class="relative">
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
        
        <div class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-9 flex-shrink-0 ring-2 ring-white dark:ring-gray-700" 
             style="background-image: url('https://ui-avatars.com/api/?name=Usuario&background=2e87ad&color=fff')"></div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/stores/theme'

const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const showSettings = ref(false)

// Toggle del dropdown
const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

// Cerrar dropdown al hacer clic fuera
const handleClickOutside = (event) => {
  if (showSettings.value && !event.target.closest('.relative')) {
    showSettings.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const logout = () => {
  // TODO: Lógica de logout real
  localStorage.removeItem('ciudadano')
  router.push('/ciudadano/login')
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

/* Custom translate for toggle */
.translate-x-4\.5 {
  transform: translateX(1.125rem);
}
</style>
