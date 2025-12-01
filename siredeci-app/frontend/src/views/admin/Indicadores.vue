<template>
  <div class="font-display bg-background-light dark:bg-background-dark flex h-screen w-full text-gray-900 dark:text-white">
    <SidebarAdmin />

    <!-- Main content -->
    <main class="flex-1 flex overflow-hidden">
      <div class="flex-1 p-6 lg:p-8 overflow-y-auto">
      <!-- Heading -->
      <header class="mb-6">
        <h1 class="text-3xl md:text-4xl font-black leading-tight tracking-[-0.02em]">Indicadores y Métricas Personalizadas</h1>
        <p class="text-gray-600 dark:text-gray-400 text-base mt-2">Explore, busque y gestione todos los indicadores disponibles.</p>
      </header>

      <!-- Search and Filters -->
      <div class="flex flex-col sm:flex-row gap-4 mb-6">
        <div class="flex-grow">
          <label class="flex flex-col w-full">
            <div class="flex w-full items-stretch rounded-lg h-12 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
              <div class="text-gray-500 dark:text-gray-400 flex items-center justify-center pl-4">
                <span class="material-symbols-outlined">search</span>
              </div>
              <input v-model="query" class="flex w-full min-w-0 flex-1 rounded-r-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-0 border-none bg-transparent h-full placeholder:text-gray-500 dark:placeholder:text-gray-400 pl-2 text-base" placeholder="Buscar por nombre..." />
            </div>
          </label>
        </div>
        <div class="flex gap-2 flex-wrap items-center">
          <div>
            <label class="sr-only" for="filterType">Tipo de visualización</label>
            <select v-model="type" class="h-12 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 text-sm text-gray-800 dark:text-gray-200">
              <option value="all">Todos los tipos</option>
              <option value="barchart">BarChart</option>
              <option value="gauge">Gauge</option>
              <option value="number">Number</option>
              <option value="piechart">PieChart</option>
              <option value="linechart">LineChart</option>
            </select>
          </div>
          <div>
            <label class="sr-only" for="filterFreq">Frecuencia</label>
            <select v-model="freq" class="h-12 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 text-sm text-gray-800 dark:text-gray-200">
              <option value="all">Todas las frecuencias</option>
              <option value="diaria">Diaria</option>
              <option value="semanal">Semanal</option>
              <option value="mensual">Mensual</option>
              <option value="tiempo_real">Tiempo real</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Indicators Grid -->
      <div id="indicatorsGrid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="item in filtered" :key="item.codigo" class="flex flex-col bg-white dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 p-5 gap-4 transition-shadow hover:shadow-lg">
          <div class="flex flex-col">
            <p class="text-base font-medium">{{ item.nombre }}</p>
            <p class="text-gray-500 dark:text-gray-400 text-sm">{{ item.descripcion }}</p>
          </div>
          <div class="text-center my-4">
            <p class="text-primary text-4xl md:text-5xl font-bold">{{ item.valor_actual ?? '—' }}<span v-if="item.tipo==='number'" class="text-3xl text-gray-400"></span></p>
          </div>
          <div class="flex flex-col text-xs text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-4 gap-2">
            <div class="flex justify-between">
              <span><strong class="text-gray-700 dark:text-gray-300">Tipo:</strong> {{ displayType(item.tipo) }}</span>
              <span><strong class="text-gray-700 dark:text-gray-300">Frecuencia:</strong> {{ displayFreq(item.frecuencia) }}</span>
            </div>
            <div class="flex justify-between">
              <span>Min: <strong class="text-gray-900 dark:text-white">{{ item.valor_min ?? '—' }}</strong></span>
              <span>Max: <strong class="text-gray-900 dark:text-white">{{ item.valor_max ?? '—' }}</strong></span>
              <span>Última: <strong class="text-gray-900 dark:text-white">{{ item.ultima_actualizacion ?? '—' }}</strong></span>
            </div>
          </div>
          <button class="w-full h-10 px-4 rounded-lg bg-primary/10 text-primary text-sm font-bold hover:bg-primary/20">Agregar al dashboard</button>
        </div>
        <div v-if="!loading && filtered.length===0" class="col-span-full text-sm text-gray-500">Sin indicadores para los filtros seleccionados.</div>
        <div v-if="loading" class="col-span-full text-sm text-gray-500">Cargando indicadores...</div>
      </div>

      <!-- Floating Action Button -->
      <button
        v-if="canCreateIndicator"
        class="fixed bottom-8 right-8 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary/90 transition-transform hover:scale-105"
        title="Crear nuevo indicador"
      >
        <span class="material-symbols-outlined text-3xl">add</span>
      </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'
import { isSuperAdmin, isAdmin } from '@/utils/roles'

const loading = ref(false)
const indicators = ref([])
const query = ref('')
const type = ref('all')
const freq = ref('all')

const filtered = computed(() => {
  // Los datos ya vienen filtrados del backend; retornamos tal cual
  return indicators.value
})

const canCreateIndicator = computed(() => isSuperAdmin() || isAdmin())

watch(query, () => fetchIndicatorsDebounced())
watch(type, () => fetchIndicators())
watch(freq, () => fetchIndicators())

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  fetchIndicators()
})

const fetchIndicatorsDebounced = (() => {
  let t
  return function() {
    clearTimeout(t)
    t = setTimeout(() => fetchIndicators(), 300)
  }
})()

async function fetchIndicators() {
  try {
    loading.value = true
    const params = {}
    if (query.value && query.value.trim()) params.q = query.value.trim()
    if (type.value && type.value !== 'all') params.type = type.value
    if (freq.value && freq.value !== 'all') params.freq = freq.value
    const { data } = await axios.get('/api/reportes/indicators/', { params })
    indicators.value = data.results || []
  } catch (e) {
    console.error('Error cargando indicadores', e)
    indicators.value = []
  } finally {
    loading.value = false
  }
}

function displayType(t) {
  return ({ barchart:'BarChart', gauge:'Gauge', number:'Number', piechart:'PieChart', linechart:'LineChart' }[t] || t)
}

function displayFreq(f) {
  return ({ tiempo_real:'Tiempo real', diaria:'Diaria', semanal:'Semanal', mensual:'Mensual' }[f] || f)
}
</script>

<style scoped>
.material-symbols-outlined{ font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24 }
</style>
