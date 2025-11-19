<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <NavbarPublico />

    <div class="w-full p-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="mb-8 text-center">
          <h2 class="text-3xl font-black text-gray-900 dark:text-gray-100">
            Reportes Públicos
          </h2>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Transparencia y datos abiertos sobre las denuncias ciudadanas
          </p>
        </header>

        <!-- Tabs -->
        <div class="flex flex-wrap gap-2 justify-center mb-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-4 py-2 rounded-full text-sm font-medium border transition-colors"
            :class="activeTab === tab.id
              ? 'bg-primary text-white border-primary'
              : 'bg-white dark:bg-[#131b1f] text-gray-700 dark:text-gray-200 border-gray-200 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-900'"
          >
            <span class="material-symbols-outlined text-sm mr-1 align-middle">{{ tab.icon }}</span>
            <span class="align-middle">{{ tab.label }}</span>
          </button>
        </div>

        <!-- Contenido por pestaña -->
        <div v-if="activeTab === 'dashboards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          <div
            v-for="db in dashboards"
            :key="db.codigo_dashboard"
            class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-5 flex flex-col justify-between"
          >
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-1">
                {{ db.nombre }}
              </h3>
              <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-2">
                {{ db.tipo_dashboard }} · Actualización {{ db.frecuencia_actualizacion.toLowerCase() }}
              </p>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-3">
                {{ db.descripcion || 'Panel de visualización de indicadores públicos.' }}
              </p>
            </div>
            <button
              @click="selectDashboard(db)"
              class="mt-2 inline-flex items-center justify-center gap-1 text-sm font-semibold text-primary hover:text-primary/80"
            >
              Ver indicadores
              <span class="material-symbols-outlined text-sm">chevron_right</span>
            </button>
          </div>
        </div>

        <div v-else-if="activeTab === 'reportes'" class="mb-8">
          <div class="flex flex-wrap gap-3 items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">description</span>
              Reportes descargables
            </h3>
            <div class="flex flex-wrap gap-2 text-xs text-gray-500 dark:text-gray-400">
              <span>Filtrados por tipo y formato próximamente</span>
            </div>
          </div>

          <div class="overflow-x-auto bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-slate-800 text-sm">
              <thead class="bg-gray-50 dark:bg-slate-900/60">
                <tr>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Nombre</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Tipo</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Periodo</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Formato</th>
                  <th class="px-4 py-3"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-slate-800">
                <tr v-for="rpt in reportes" :key="rpt.codigo_reporte" class="hover:bg-gray-50 dark:hover:bg-slate-900/60">
                  <td class="px-4 py-3">
                    <p class="font-semibold text-gray-900 dark:text-gray-100">{{ rpt.nombre }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">{{ rpt.descripcion }}</p>
                  </td>
                  <td class="px-4 py-3 text-xs text-gray-700 dark:text-gray-200">{{ rpt.tipo_reporte }}</td>
                  <td class="px-4 py-3 text-xs text-gray-700 dark:text-gray-200">
                    <span v-if="rpt.fecha_inicio && rpt.fecha_fin">{{ formatFecha(rpt.fecha_inicio) }} - {{ formatFecha(rpt.fecha_fin) }}</span>
                    <span v-else>—</span>
                  </td>
                  <td class="px-4 py-3 text-xs">
                    <span class="inline-flex items-center px-2 py-1 rounded-full bg-primary/10 text-primary font-semibold uppercase">
                      {{ rpt.formato_exportacion }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-right">
                    <button
                      class="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:text-primary/80 disabled:opacity-40"
                      disabled
                    >
                      Descargar
                      <span class="material-symbols-outlined text-xs">download</span>
                    </button>
                  </td>
                </tr>
                <tr v-if="!loading && reportes.length === 0">
                  <td colspan="5" class="px-4 py-6 text-center text-sm text-gray-500 dark:text-gray-400">
                    No hay reportes públicos disponibles por el momento.
                  </td>
                </tr>
                <tr v-if="loading">
                  <td colspan="5" class="px-4 py-6 text-center text-sm text-gray-500 dark:text-gray-400">
                    Cargando reportes públicos...
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else-if="activeTab === 'tendencias'" class="mb-8">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">map</span>
            Tendencias geográficas
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="t in tendencias"
              :key="t.codigo_tendencia"
              class="p-4 bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 rounded-xl shadow"
            >
              <div class="flex items-center justify-between mb-2">
                <div>
                  <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ t.distrito }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ t.zona }}</p>
                </div>
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold"
                  :class="badgeCriticidadClass(t.nivel_criticidad)">
                  {{ t.nivel_criticidad }}
                </span>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">Periodo: {{ t.periodo_analisis }}</p>
              <p class="text-xs text-gray-600 dark:text-gray-300 mb-1">
                Denuncias: <span class="font-bold">{{ t.cantidad_denuncias }}</span>
              </p>
              <p class="text-xs text-gray-600 dark:text-gray-300 mb-1">
                Categoría más frecuente: <span class="font-bold">{{ t.categoria_mas_frecuente }}</span>
              </p>
              <p class="text-xs text-gray-600 dark:text-gray-300">
                Tasa de resolución: <span class="font-bold">{{ t.tasa_resolucion }}%</span>
              </p>
            </div>
          </div>
          <p v-if="!loading && tendencias.length === 0" class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
            Aún no hay tendencias geográficas registradas.
          </p>
        </div>

        <div v-else-if="activeTab === 'ranking'" class="mb-8">
          <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
            <span class="material-symbols-outlined text-primary">leaderboard</span>
            Ranking de áreas responsables
          </h3>
          <div class="overflow-x-auto bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-slate-800 text-sm">
              <thead class="bg-gray-50 dark:bg-slate-900/60">
                <tr>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Posición</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Área</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Puntaje</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Denuncias</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Tasa resolución</th>
                  <th class="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-200">Tiempo promedio</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 dark:divide-slate-800">
                <tr v-for="r in ranking" :key="r.codigo_ranking" class="hover:bg-gray-50 dark:hover:bg-slate-900/60">
                  <td class="px-4 py-3 text-sm font-bold text-gray-900 dark:text-gray-100">#{{ r.posicion }}</td>
                  <td class="px-4 py-3 text-sm text-gray-800 dark:text-gray-100">{{ r.area }}</td>
                  <td class="px-4 py-3 text-sm text-gray-800 dark:text-gray-100">{{ r.puntaje_total }}</td>
                  <td class="px-4 py-3 text-sm text-gray-800 dark:text-gray-100">{{ r.denuncias_atendidas }}</td>
                  <td class="px-4 py-3 text-sm text-gray-800 dark:text-gray-100">{{ r.tasa_resolucion_area }}%</td>
                  <td class="px-4 py-3 text-sm text-gray-800 dark:text-gray-100">{{ r.tiempo_promedio_area }}</td>
                </tr>
                <tr v-if="!loading && ranking.length === 0">
                  <td colspan="6" class="px-4 py-6 text-center text-sm text-gray-500 dark:text-gray-400">
                    No hay datos de ranking disponibles todavía.
                  </td>
                </tr>
                <tr v-if="loading">
                  <td colspan="6" class="px-4 py-6 text-center text-sm text-gray-500 dark:text-gray-400">
                    Cargando ranking público de desempeño...
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavbarPublico from '@/components/NavbarPublico.vue'
import {
  fetchPublicReportes,
  fetchPublicDashboards,
  fetchPublicTendencias,
  fetchPublicRankingAreas,
} from '@/services/publicReportes'

const tabs = [
  { id: 'dashboards', label: 'Dashboards', icon: 'insights' },
  { id: 'reportes', label: 'Reportes', icon: 'description' },
  { id: 'tendencias', label: 'Tendencias geográficas', icon: 'map' },
  { id: 'ranking', label: 'Ranking de áreas', icon: 'leaderboard' },
]

const activeTab = ref('dashboards')
const loading = ref(false)

const dashboards = ref([])
const reportes = ref([])
const tendencias = ref([])
const ranking = ref([])

const loadData = async () => {
  loading.value = true
  try {
    const [dbResp, rptResp, tenResp, rankResp] = await Promise.all([
      fetchPublicDashboards(),
      fetchPublicReportes(),
      fetchPublicTendencias(),
      fetchPublicRankingAreas(),
    ])

    dashboards.value = dbResp?.results || []
    reportes.value = rptResp?.results || []
    tendencias.value = tenResp?.results || []
    ranking.value = rankResp?.results || []
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Error cargando reportes públicos', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})

const selectDashboard = (db) => {
  // En esta versión solo mostramos la tarjeta; en el futuro se puede abrir detalle/gráficos
  activeTab.value = 'dashboards'
}

const formatFecha = (isoDate) => {
  if (!isoDate) return ''
  try {
    const d = new Date(isoDate)
    return d.toLocaleDateString()
  } catch {
    return isoDate
  }
}

const badgeCriticidadClass = (nivel) => {
  switch (nivel) {
    case 'Crítico':
      return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
    case 'Alto':
      return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300'
    case 'Medio':
      return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'
    default:
      return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
