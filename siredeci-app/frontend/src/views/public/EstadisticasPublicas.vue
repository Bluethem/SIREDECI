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

        <!-- Filtros de fecha -->
        <div class="flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
          <div class="flex items-center gap-3 w-full md:w-auto">
            <div class="flex flex-col text-sm text-gray-700 dark:text-gray-300">
              <span class="font-medium mb-1">Rango de fechas</span>
              <div class="flex flex-col sm:flex-row gap-2">
                <input
                  v-model="fromDate"
                  type="date"
                  class="border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-sm bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100"
                />
                <input
                  v-model="toDate"
                  type="date"
                  class="border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-sm bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100"
                />
              </div>
            </div>
          </div>
          <button
            @click="aplicarFiltros"
            class="inline-flex items-center justify-center h-10 px-4 rounded-lg bg-primary text-white text-sm font-semibold hover:bg-primary/90 transition-colors"
          >
            <span class="material-symbols-outlined text-sm mr-1">refresh</span>
            Actualizar estadísticas
          </button>
        </div>

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

      <!-- Denuncias por Distrito + Ranking de Áreas -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Denuncias por Distrito -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">location_on</span>
            Denuncias por Distrito
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
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

        <!-- Ranking de Áreas -->
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">leaderboard</span>
            Ranking de Áreas Responsables
          </h3>
          <div class="space-y-3">
            <div
              v-for="(area, index) in rankingAreas"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-900/50 rounded-lg"
            >
              <div class="flex items-center gap-3">
                <span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-primary/10 text-primary text-sm font-bold">
                  {{ area.posicion }}
                </span>
                <div>
                  <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ area.area }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ area.periodo_evaluacion }} · {{ area.denuncias_atendidas }} denuncias atendidas
                  </p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-bold text-primary">{{ area.puntaje_total }} pts</p>
                <p class="text-[11px] text-gray-500 dark:text-gray-400">
                  {{ area.tasa_resolucion_area }}% resueltas · {{ area.tiempo_promedio_area }}h prom.
                </p>
              </div>
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
import axios from 'axios'
import NavbarPublico from '@/components/NavbarPublico.vue'

const router = useRouter()

const stats = ref({
  total: 0,
  resueltas: 0,
  enProceso: 0,
  tiempoPromedio: 0
})

const categorias = ref([])
const estados = ref([])
const distritos = ref([])
const rankingAreas = ref([])

const fromDate = ref('')
const toDate = ref('')

const mapEstadoColor = (nombre) => {
  const map = {
    Resuelta: '#10b981',
    'En proceso': '#f59e0b',
    'En revisión': '#3b82f6',
    Asignado: '#6366f1',
    Registrado: '#6b7280',
    Rechazada: '#ef4444',
    Cerrada: '#0f766e'
  }
  return map[nombre] || '#6b7280'
}

const mapCategoriaColor = (index) => {
  const palette = ['#3b82f6', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#14b8a6']
  return palette[index % palette.length]
}

const loadEstadisticas = async () => {
  try {
    const params = {}
    if (fromDate.value) params.from = fromDate.value
    if (toDate.value) params.to = toDate.value
    const response = await axios.get('/public/reportes/estadisticas/denuncias-resumen/', { params })
    const data = response.data || {}

    const backendStats = data.stats || {}
    stats.value = {
      total: backendStats.total || 0,
      resueltas: backendStats.resueltas || 0,
      enProceso: backendStats.en_proceso || 0,
      tiempoPromedio: backendStats.tiempo_promedio_horas || 0
    }

    categorias.value = (data.categorias || []).map((cat, index) => ({
      nombre: cat.nombre,
      cantidad: cat.cantidad,
      porcentaje: cat.porcentaje,
      color: mapCategoriaColor(index)
    }))

    estados.value = (data.estados || []).map((e) => ({
      nombre: e.nombre,
      cantidad: e.cantidad,
      color: mapEstadoColor(e.nombre)
    }))

    distritos.value = data.distritos || []
  } catch (error) {
    console.error('Error al cargar estadísticas públicas:', error)
  }
}

const loadTendencias = async () => {
  try {
    const response = await axios.get('/public/reportes/tendencias-geograficas/')
    const data = response.data || {}
    const results = data.results || []

    // Mapear TendenciaGeografica a la estructura usada en "Denuncias por Distrito"
    distritos.value = results.map((t) => ({
      nombre: t.distrito,
      cantidad: t.cantidad_denuncias,
      tasa_resolucion: t.tasa_resolucion
    }))
  } catch (error) {
    console.error('Error al cargar tendencias geográficas:', error)
  }
}

const loadRankingAreas = async () => {
  try {
    const response = await axios.get('/public/reportes/ranking-areas/')
    const data = response.data || {}
    rankingAreas.value = data.results || []
  } catch (error) {
    console.error('Error al cargar ranking de áreas:', error)
  }
}

onMounted(() => {
  loadEstadisticas()
  loadTendencias()
  loadRankingAreas()
})

const aplicarFiltros = () => {
  loadEstadisticas()
}

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
