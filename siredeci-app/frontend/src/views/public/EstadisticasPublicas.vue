<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Navbar -->
    <NavbarPublico />
    
    <div class="w-full p-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="mb-8">
          <h2 class="text-3xl font-black text-gray-900 dark:text-gray-100 text-center">
            Estadísticas Públicas
          </h2>
          <p class="text-gray-600 dark:text-gray-400 text-center mt-2">
            Datos actualizados sobre las denuncias ciudadanas
          </p>
        </header>

        <!-- Stats Overview Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <!-- Total Denuncias -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Denuncias</p>
              <p class="text-3xl font-black text-gray-900 dark:text-gray-100">{{ stats.total }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-blue-600 dark:text-blue-400">description</span>
            </div>
          </div>
        </div>

        <!-- Resueltas -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Resueltas</p>
              <p class="text-3xl font-black text-green-600 dark:text-green-400">{{ stats.resueltas }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-green-600 dark:text-green-400">check_circle</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-2">
            {{ ((stats.resueltas / stats.total) * 100).toFixed(1) }}% del total
          </p>
        </div>

        <!-- En Proceso -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">En Proceso</p>
              <p class="text-3xl font-black text-orange-600 dark:text-orange-400">{{ stats.enProceso }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-orange-600 dark:text-orange-400">sync</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-2">
            {{ ((stats.enProceso / stats.total) * 100).toFixed(1) }}% del total
          </p>
        </div>

        <!-- Tiempo Promedio -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Tiempo Promedio</p>
              <p class="text-3xl font-black text-primary">{{ stats.tiempoPromedio }}h</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <span class="material-symbols-outlined text-primary">schedule</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-500 mt-2">
            De resolución
          </p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Denuncias por Categoría -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">category</span>
            Denuncias por Categoría
          </h3>
          <div class="space-y-3">
            <div v-for="(cat, index) in categorias" :key="index">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ cat.nombre }}</span>
                <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ cat.cantidad }}</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all duration-300"
                  :style="{ width: cat.porcentaje + '%', backgroundColor: cat.color }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Estado de Denuncias -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">pie_chart</span>
            Estado de Denuncias
          </h3>
          <div class="space-y-3">
            <div v-for="(estado, index) in estados" :key="index" class="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-900/50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: estado.color }"></div>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ estado.nombre }}</span>
              </div>
              <span class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ estado.cantidad }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Denuncias por Distrito -->
      <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6 mb-8">
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
          <span class="material-symbols-outlined text-primary">location_on</span>
          Denuncias por Distrito
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="(distrito, index) in distritos" :key="index" class="p-4 bg-gray-50 dark:bg-slate-900/50 rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <span class="font-semibold text-gray-900 dark:text-gray-100">{{ distrito.nombre }}</span>
              <span class="text-sm font-bold text-primary">{{ distrito.cantidad }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <span class="material-symbols-outlined text-xs">trending_up</span>
              <span>{{ distrito.tasa_resolucion }}% resueltas</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          @click="goToConsultaPublica"
          class="flex items-center justify-center gap-2 h-12 px-6 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 transition-colors duration-200"
        >
          <span class="material-symbols-outlined">search</span>
          <span>Consultar Denuncia</span>
        </button>
        <button
          @click="goToLogin"
          class="flex items-center justify-center gap-2 h-12 px-6 rounded-lg border border-primary text-primary hover:bg-primary/10 dark:hover:bg-primary/20 font-bold transition-colors duration-200"
        >
          <span class="material-symbols-outlined">login</span>
          <span>Iniciar Sesión</span>
        </button>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavbarPublico from '@/components/NavbarPublico.vue'

const router = useRouter()

const stats = ref({
  total: 1245,
  resueltas: 892,
  enProceso: 285,
  tiempoPromedio: 48
})

const categorias = ref([
  { nombre: 'Infraestructura Vial', cantidad: 342, porcentaje: 27.5, color: '#3b82f6' },
  { nombre: 'Alumbrado Público', cantidad: 287, porcentaje: 23.1, color: '#f59e0b' },
  { nombre: 'Limpieza y Residuos', cantidad: 245, porcentaje: 19.7, color: '#10b981' },
  { nombre: 'Seguridad Ciudadana', cantidad: 198, porcentaje: 15.9, color: '#ef4444' },
  { nombre: 'Áreas Verdes', cantidad: 173, porcentaje: 13.9, color: '#8b5cf6' }
])

const estados = ref([
  { nombre: 'Resueltas', cantidad: 892, color: '#10b981' },
  { nombre: 'En Proceso', cantidad: 285, color: '#f59e0b' },
  { nombre: 'En Revisión', cantidad: 52, color: '#3b82f6' },
  { nombre: 'Rechazadas', cantidad: 16, color: '#ef4444' }
])

const distritos = ref([
  { nombre: 'Miraflores', cantidad: 256, tasa_resolucion: 75 },
  { nombre: 'San Isidro', cantidad: 198, tasa_resolucion: 82 },
  { nombre: 'Surco', cantidad: 234, tasa_resolucion: 68 },
  { nombre: 'La Molina', cantidad: 187, tasa_resolucion: 71 },
  { nombre: 'San Borja', cantidad: 165, tasa_resolucion: 79 },
  { nombre: 'Barranco', cantidad: 205, tasa_resolucion: 73 }
])

onMounted(() => {
  // TODO: Cargar estadísticas desde el API
  // loadEstadisticas()
})

const goToConsultaPublica = () => {
  router.push({ name: 'consulta-publica' })
}

const goToLogin = () => {
  router.push({ name: 'ciudadano-login' })
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}
</style>
