<template>
  <header class="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 sm:px-4 py-2.5 shadow-sm">
    <div class="flex items-center gap-2 text-black dark:text-white min-w-0 flex-shrink-0">
      <router-link 
        to="/" 
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
import authService from '@/services/auth'

const { isDark, toggleTheme } = useTheme()

// Verificar si el usuario está logueado
const isLoggedIn = computed(() => {
  return authService.isAuthenticated()
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
