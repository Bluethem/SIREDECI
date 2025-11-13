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
      <nav class="hidden md:flex items-center gap-3 mr-2">
        <router-link to="/public/consulta" 
                     class="text-gray-600 dark:text-gray-300 hover:text-primary text-sm font-medium whitespace-nowrap"
                     :class="{ 'text-primary font-bold': $route.path === '/public/consulta' }">
          Consultar Denuncia
        </router-link>
        <router-link to="/public/estadisticas" 
                     class="text-gray-600 dark:text-gray-300 hover:text-primary text-sm font-medium whitespace-nowrap"
                     :class="{ 'text-primary font-bold': $route.path === '/public/estadisticas' }">
          Estadísticas
        </router-link>
      </nav>
      
      <div class="flex items-center gap-2 flex-shrink-0">
        <!-- Dark Mode Toggle -->
        <button @click="toggleTheme"
                class="flex items-center justify-center w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
          <span class="material-symbols-outlined text-[20px] leading-none">
            {{ isDark ? 'dark_mode' : 'light_mode' }}
          </span>
        </button>
        
        <!-- Botón de volver al dashboard (solo si está logueado) -->
        <router-link v-if="isLoggedIn" 
                     to="/ciudadano/dashboard"
                     class="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-bold hover:bg-primary/90 transition-colors whitespace-nowrap">
          <span class="material-symbols-outlined text-lg">dashboard</span>
          <span class="hidden sm:inline">Mi Dashboard</span>
        </router-link>
        
        <!-- Botón de iniciar sesión (solo si NO está logueado) -->
        <router-link v-else
                     to="/ciudadano/login"
                     class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 border-primary text-primary text-sm font-bold hover:bg-primary hover:text-white transition-colors whitespace-nowrap">
          <span class="material-symbols-outlined text-lg">login</span>
          <span class="hidden sm:inline">Iniciar Sesión</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/stores/theme'

const { isDark, toggleTheme } = useTheme()

// Verificar si el usuario está logueado
const isLoggedIn = computed(() => {
  // Verificar si hay datos de ciudadano en localStorage
  const ciudadano = localStorage.getItem('ciudadano')
  return ciudadano !== null && ciudadano !== undefined
})

onMounted(() => {
  console.log('Usuario logueado:', isLoggedIn.value)
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
</style>
