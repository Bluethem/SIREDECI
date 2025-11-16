<template>
  <div class="font-display bg-background-light dark:bg-background-dark flex min-h-screen w-full text-gray-900 dark:text-white">
    <!-- Sidebar identical to Dashboard -->
    <aside class="w-64 bg-white flex flex-col border-r border-medium-gray">
      <div class="flex flex-col h-full p-4">
        <div class="flex items-center gap-3 p-2 mb-4">
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
            data-alt="Company logo abstract shape"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBaXtYxFyHwjmkfzelKdSwckui0VVqBxvGCgbtXZGm7PLNonck59Pa-GNBQiIsq87W1Lh6EuZpvNHIl5ut6OMcMKYLyvJY29ahhMDpwOxBZPAlC0GJX4nsu6xBRTYFiYOiIbwJTgSuczE5rPIRwmep9qHnn0FoAzi8SzFgNs7b6pwFoWzm0BP_V813hr6YZomVQerH46whjBHv_QzMR-PdF8ZxV4zElToDiD0RtlSzhnMFiUQtPfDYTQ16z0SxPZYNRrHGjRBMPQV2U");'>
          </div>
          <div class="flex flex-col">
            <h1 class="text-base font-bold text-dark-blue">Plataforma de</h1>
            <p class="text-sm text-gray-500">Gestión</p>
          </div>
        </div>
        <nav class="flex flex-col gap-2">
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/dashboard') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/dashboard')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/dashboard') ? 'text-principal-blue' : '']">dashboard</span>
            <p class="text-sm font-medium leading-none">Dashboard</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/analisis-geografico') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/analisis-geografico')">
            <span class="material-symbols-outlined nofill">map</span>
            <p class="text-sm font-medium">Tendencias geograficas</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/reportes') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/reportes')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/reportes') ? 'text-principal-blue' : '']">bar_chart</span>
            <p class="text-sm font-medium leading-none">Reportes</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/indicadores') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/indicadores')">
            <span class="material-symbols-outlined nofill">insights</span>
            <p class="text-sm font-medium">Indicadores</p>
          </a>
        </nav>
        <div class="mt-auto">
          <a class="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg" href="#">
            <span class="material-symbols-outlined nofill">help</span>
            <p class="text-sm font-medium">Ayuda</p>
          </a>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 flex flex-col p-6 lg:p-8">
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
      <button class="fixed bottom-8 right-8 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-primary/90 transition-transform hover:scale-105" title="Crear nuevo indicador">
        <span class="material-symbols-outlined text-3xl">add</span>
      </button>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'IndicadoresAdmin',
  data() {
    return {
      loading: false,
      indicators: [],
      query: '',
      type: 'all',
      freq: 'all',
    }
  },
  computed: {
    filtered() {
      // Los datos ya vienen filtrados del backend; retornamos tal cual
      return this.indicators
    }
  },
  watch: {
    query() { this.fetchIndicatorsDebounced() },
    type() { this.fetchIndicators() },
    freq() { this.fetchIndicators() },
  },
  mounted() {
    const token = localStorage.getItem('access_token')
    if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    this.fetchIndicators()
  },
  methods: {
    fetchIndicatorsDebounced: (() => {
      let t
      return function() {
        clearTimeout(t)
        t = setTimeout(() => this.fetchIndicators(), 300)
      }
    })(),
    async fetchIndicators() {
      try {
        this.loading = true
        const params = {}
        if (this.query && this.query.trim()) params.q = this.query.trim()
        if (this.type && this.type !== 'all') params.type = this.type
        if (this.freq && this.freq !== 'all') params.freq = this.freq
        const { data } = await axios.get('/api/reportes/indicators/', { params })
        this.indicators = data.results || []
      } catch (e) {
        console.error('Error cargando indicadores', e)
        this.indicators = []
      } finally {
        this.loading = false
      }
    },
    displayType(t) {
      return ({ barchart:'BarChart', gauge:'Gauge', number:'Number', piechart:'PieChart', linechart:'LineChart' }[t] || t)
    },
    displayFreq(f) {
      return ({ tiempo_real:'Tiempo real', diaria:'Diaria', semanal:'Semanal', mensual:'Mensual' }[f] || f)
    },
    isActive(path) {
      try { return this.$route.path.startsWith(path) } catch { return false }
    }
  }
}
</script>

<style scoped>
.material-symbols-outlined{ font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24 }
</style>
