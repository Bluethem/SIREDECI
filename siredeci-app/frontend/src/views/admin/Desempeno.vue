<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex h-screen w-full">
    <SidebarAdmin />

    <main class="flex h-screen flex-1 flex-col overflow-hidden">
      <!-- Top bar -->
      <header class="flex w-full flex-shrink-0 items-center justify-between border-b border-theme-medium-gray/50 bg-theme-white px-6 py-3 dark:border-gray-700 dark:bg-background-dark">
        <div class="flex flex-col">
          <h2 class="text-lg font-bold text-theme-dark-blue dark:text-white">Desempeño por Área Responsable</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Ranking de desempeño de áreas según denuncias atendidas.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <select
            v-model="filters.periodo"
            class="h-9 rounded-lg border border-theme-medium-gray bg-white px-3 text-xs font-medium text-theme-dark-blue focus:border-theme-main-blue focus:outline-none focus:ring-1 focus:ring-theme-main-blue dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100"
            @change="loadRanking"
          >
            <option value="">Todos los periodos</option>
            <option value="Diario">Diario</option>
            <option value="Semanal">Semanal</option>
            <option value="Mensual">Mensual</option>
            <option value="Trimestral">Trimestral</option>
            <option value="Anual">Anual</option>
          </select>

          <select
            v-model="filters.order"
            class="h-9 rounded-lg border border-theme-medium-gray bg-white px-3 text-xs font-medium text-theme-dark-blue focus:border-theme-main-blue focus:outline-none focus:ring-1 focus:ring-theme-main-blue dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100"
            @change="applyOrder"
          >
            <option value="rank">Orden: Ranking</option>
            <option value="puntaje_desc">Puntaje ↓</option>
            <option value="tasa_desc">Tasa resolución ↓</option>
            <option value="tiempo_asc">Tiempo promedio ↑</option>
            <option value="calificacion_desc">Calificación ↓</option>
          </select>

          <button
            class="flex h-9 min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg bg-theme-light-blue/60 px-4 text-xs font-bold text-theme-dark-blue hover:bg-theme-light-blue dark:bg-primary/20 dark:text-white dark:hover:bg-primary/30"
            @click="loadRanking"
          >
            <span class="material-symbols-outlined text-sm">refresh</span>
            Actualizar
          </button>
        </div>
      </header>

      <!-- Contenido -->
      <div class="flex flex-1 overflow-hidden">
        <div class="flex flex-1 flex-col overflow-y-auto p-6 gap-6">
          <!-- Resumen -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="rounded-xl bg-theme-white p-4 shadow-sm border border-theme-medium-gray/60 dark:bg-background-dark dark:border-gray-700">
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400">Áreas evaluadas</p>
              <p class="mt-1 text-2xl font-bold text-theme-dark-blue dark:text-white">{{ resumen.areas }}</p>
            </div>
            <div class="rounded-xl bg-theme-white p-4 shadow-sm border border-theme-medium-gray/60 dark:bg-background-dark dark:border-gray-700">
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400">Puntaje promedio</p>
              <p class="mt-1 text-2xl font-bold text-theme-dark-blue dark:text-white">{{ resumen.puntaje_promedio }}</p>
            </div>
            <div class="rounded-xl bg-theme-white p-4 shadow-sm border border-theme-medium-gray/60 dark:bg-background-dark dark:border-gray-700">
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400">Tasa resolución media</p>
              <p class="mt-1 text-2xl font-bold text-theme-dark-blue dark:text-white">{{ resumen.tasa_promedio }}%</p>
            </div>
            <div class="rounded-xl bg-theme-white p-4 shadow-sm border border-theme-medium-gray/60 dark:bg-background-dark dark:border-gray-700">
              <p class="text-xs font-medium text-gray-500 dark:text-gray-400">Calificación promedio</p>
              <p class="mt-1 text-2xl font-bold text-theme-dark-blue dark:text-white">{{ resumen.calificacion_promedio }}</p>
            </div>
          </div>

          <!-- Tabla de ranking -->
          <div class="flex-1 rounded-xl bg-theme-white shadow-sm border border-theme-medium-gray/60 overflow-hidden dark:bg-background-dark dark:border-gray-700">
            <div class="flex items-center justify-between px-4 py-3 border-b border-theme-medium-gray/60 bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
              <h3 class="text-sm font-semibold text-theme-dark-blue dark:text-white">Ranking de Desempeño</h3>
              <p class="text-[11px] text-gray-500 dark:text-gray-400">Ordenado por {{ labelOrden }}</p>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-sm text-left text-gray-700 dark:text-gray-200">
                <thead class="text-xs uppercase bg-gray-50 text-gray-600 border-b border-theme-medium-gray/60 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700">
                  <tr>
                    <th class="px-4 py-2">#</th>
                    <th class="px-4 py-2">Área responsable</th>
                    <th class="px-4 py-2">Puntaje</th>
                    <th class="px-4 py-2">Denuncias atendidas</th>
                    <th class="px-4 py-2">Tasa resolución</th>
                    <th class="px-4 py-2">Tiempo prom. (h)</th>
                    <th class="px-4 py-2">Calificación</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loading" class="border-t border-theme-medium-gray/60 bg-white dark:bg-background-dark">
                    <td colspan="7" class="px-4 py-3 text-xs text-gray-500 dark:text-gray-400">
                      Cargando ranking de desempeño...
                    </td>
                  </tr>
                  <tr
                    v-if="!loading && filasOrdenadas.length === 0"
                    class="border-t border-theme-medium-gray/60 bg-white dark:bg-background-dark"
                  >
                    <td colspan="7" class="px-4 py-3 text-xs text-gray-500 dark:text-gray-400">
                      No hay datos de desempeño para el periodo seleccionado.
                    </td>
                  </tr>
                  <tr
                    v-for="row in filasOrdenadas"
                    :key="row.area + '-' + row.rank"
                    class="border-t border-theme-medium-gray/40 bg-white hover:bg-gray-50 dark:bg-background-dark dark:hover:bg-gray-800 dark:border-gray-700"
                  >
                    <td class="px-4 py-2 font-semibold">
                      <span
                        class="inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold"
                        :class="rankBadgeClass(row.rank)"
                      >
                        {{ row.rank }}
                      </span>
                    </td>
                    <td class="px-4 py-2 font-medium text-theme-dark-blue dark:text-white">{{ row.area }}</td>
                    <td class="px-4 py-2 text-xs">{{ row.puntaje.toFixed(2) }}</td>
                    <td class="px-4 py-2 text-xs">{{ row.denuncias }}</td>
                    <td class="px-4 py-2 text-xs">{{ row.tasa.toFixed(1) }}%</td>
                    <td class="px-4 py-2 text-xs">{{ row.tiempo.toFixed(1) }}</td>
                    <td class="px-4 py-2 text-xs">
                      <span v-if="row.calificacion != null" class="inline-flex items-center gap-1">
                        <span class="material-symbols-outlined text-amber-400 text-base">star</span>
                        {{ row.calificacion.toFixed(2) }}
                      </span>
                      <span v-else class="text-gray-400">—</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'

const filas = ref([])
const loading = ref(false)

const filters = ref({
  periodo: '',
  order: 'rank',
})

const resumen = computed(() => {
  if (!filas.value.length) {
    return {
      areas: 0,
      puntaje_promedio: '0.0',
      tasa_promedio: '0.0',
      calificacion_promedio: '0.0',
    }
  }
  const n = filas.value.length
  const puntaje = filas.value.reduce((s, r) => s + (r.puntaje || 0), 0) / n
  const tasa = filas.value.reduce((s, r) => s + (r.tasa || 0), 0) / n
  const calVals = filas.value.filter((r) => r.calificacion != null)
  const cal = calVals.length
    ? calVals.reduce((s, r) => s + (r.calificacion || 0), 0) / calVals.length
    : 0
  return {
    areas: n,
    puntaje_promedio: puntaje.toFixed(1),
    tasa_promedio: tasa.toFixed(1),
    calificacion_promedio: cal.toFixed(1),
  }
})

const filasOrdenadas = computed(() => {
  const arr = [...filas.value]
  switch (filters.value.order) {
    case 'puntaje_desc':
      return arr.sort((a, b) => b.puntaje - a.puntaje)
    case 'tasa_desc':
      return arr.sort((a, b) => b.tasa - a.tasa)
    case 'tiempo_asc':
      return arr.sort((a, b) => a.tiempo - b.tiempo)
    case 'calificacion_desc':
      return arr.sort((a, b) => (b.calificacion || 0) - (a.calificacion || 0))
    default:
      return arr.sort((a, b) => a.rank - b.rank)
  }
})

const labelOrden = computed(() => {
  switch (filters.value.order) {
    case 'puntaje_desc':
      return 'puntaje de desempeño (mayor a menor)'
    case 'tasa_desc':
      return 'tasa de resolución (mayor a menor)'
    case 'tiempo_asc':
      return 'tiempo promedio de atención (menor a mayor)'
    case 'calificacion_desc':
      return 'calificación ciudadana (mayor a menor)'
    default:
      return 'posición de ranking'
  }
})

const rankBadgeClass = (rank) => {
  if (rank === 1) return 'bg-yellow-300 text-yellow-900'
  if (rank === 2) return 'bg-gray-200 text-gray-800'
  if (rank === 3) return 'bg-amber-500/80 text-white'
  return 'bg-theme-light-blue text-theme-dark-blue dark:bg-gray-700 dark:text-gray-100'
}

const loadRanking = async () => {
  try {
    loading.value = true
    const params = {}
    if (filters.value.periodo) params.periodo = filters.value.periodo

    const token = localStorage.getItem('access_token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }

    const { data } = await axios.get('/api/reportes/desempeno/ranking/', { params })
    filas.value = (data.results || []).map((r) => ({
      rank: r.rank,
      area: r.area,
      puntaje: r.puntaje,
      denuncias: r.denuncias,
      tasa: r.tasa,
      tiempo: r.tiempo,
      calificacion: r.calificacion,
    }))
  } catch (e) {
    console.error('Error cargando ranking de desempeño', e)
    filas.value = []
  } finally {
    loading.value = false
  }
}

const applyOrder = () => {
  filas.value = [...filas.value]
}

onMounted(() => {
  loadRanking()
})
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>