<template>
  <div class="font-display bg-very-light-gray text-dark-blue flex min-h-screen w-full">
    <SidebarAdmin />

    <!-- Main content -->
    <main class="flex-1 p-6 lg:p-8">
      <div class="w-full max-w-5xl mx-auto">
        <header class="mb-8">
          <h1 class="text-3xl font-black leading-tight tracking-[-0.033em]">Reportes</h1>
          <p class="text-gray-500 mt-1">Selecciona una opción para continuar</p>
        </header>

        <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            v-if="canGenerateReports"
            @click="$router.push('/admin/generador-reportes')"
            class="group flex flex-col items-center justify-center p-8 bg-white rounded-xl border border-medium-gray hover:border-principal-blue hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-principal-blue/50"
          >
            <span class="material-symbols-outlined text-5xl text-principal-blue mb-4 group-hover:scale-110 transition-transform">description</span>
            <h2 class="text-xl font-bold text-dark-blue mb-2">Generación y exportación de reportes</h2>
            <p class="text-sm text-gray-500 text-center">Crea y exporta nuevos reportes según los criterios que necesites</p>
          </button>

          <button class="group flex flex-col items-center justify-center p-8 bg-white rounded-xl border border-medium-gray hover:border-principal-blue hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-principal-blue/50">
            <span class="material-symbols-outlined text-5xl text-principal-blue mb-4 group-hover:scale-110 transition-transform">history</span>
            <h2 class="text-xl font-bold text-dark-blue mb-2">Historial de reportes</h2>
            <p class="text-sm text-gray-500 text-center">Consulta y descarga reportes generados anteriormente</p>
          </button>
        </section>

        <!-- Historial de reportes recientes -->
        <section class="mt-10 bg-white rounded-xl border border-medium-gray shadow-sm overflow-hidden">
          <div class="flex items-center justify-between px-4 py-3 border-b border-medium-gray bg-gray-50">
            <h3 class="text-sm font-semibold text-dark-blue">Historial reciente</h3>
            <button
              class="flex items-center gap-1 text-xs font-medium text-principal-blue hover:underline"
              @click="fetchReportes"
            >
              <span class="material-symbols-outlined text-base">refresh</span>
              Actualizar
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm text-left text-gray-600">
              <thead class="text-xs uppercase bg-gray-50 text-gray-700">
                <tr>
                  <th class="px-4 py-2">Nombre</th>
                  <th class="px-4 py-2">Tipo</th>
                  <th class="px-4 py-2">Rango</th>
                  <th class="px-4 py-2">Formato</th>
                  <th class="px-4 py-2">Estado</th>
                  <th class="px-4 py-2">Generado</th>
                  <th class="px-4 py-2">Acción</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading" class="border-t border-medium-gray/60 bg-white">
                  <td colspan="7" class="px-4 py-3 text-xs text-gray-500">Cargando historial de reportes...</td>
                </tr>
                <tr v-if="!loading && reportes.length === 0" class="border-t border-medium-gray/60 bg-white">
                  <td colspan="7" class="px-4 py-3 text-xs text-gray-500">Aún no se han generado reportes.</td>
                </tr>
                <tr
                  v-for="r in reportes"
                  :key="r.codigo_reporte"
                  class="border-t border-medium-gray/60 bg-white hover:bg-gray-50"
                >
                  <td class="px-4 py-2 font-medium text-dark-blue">{{ r.nombre }}</td>
                  <td class="px-4 py-2 text-xs">{{ r.tipo_reporte }}</td>
                  <td class="px-4 py-2 text-xs">
                    <span v-if="r.fecha_inicio && r.fecha_fin">{{ r.fecha_inicio }} → {{ r.fecha_fin }}</span>
                    <span v-else>—</span>
                  </td>
                  <td class="px-4 py-2 text-xs">{{ r.formato_exportacion }}</td>
                  <td class="px-4 py-2 text-xs">
                    <span
                      class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                      :class="estadoPillClass(r.estado_generacion)"
                    >
                      {{ r.estado_generacion }}
                    </span>
                  </td>
                  <td class="px-4 py-2 text-xs">{{ r.fecha_generacion || '—' }}</td>
                  <td class="px-4 py-2 text-xs">
                    <button
                      class="flex items-center gap-1 text-xs font-medium text-principal-blue hover:underline disabled:text-gray-400 disabled:cursor-not-allowed"
                      :disabled="r.estado_generacion !== 'Completado'"
                      @click="downloadReporte(r.codigo_reporte)"
                    >
                      <span class="material-symbols-outlined text-sm">download</span>
                      Descargar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  </div>
 </template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'
import { isSuperAdmin, isAdmin } from '@/utils/roles'

const canGenerateReports = computed(() => isSuperAdmin() || isAdmin())

const reportes = ref([])
const loading = ref(false)

const ensureAuthHeader = () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

const fetchReportes = async () => {
  try {
    loading.value = true
    const { data } = await axios.get('/api/reportes/reportes/')
    reportes.value = data.results || []
  } catch (e) {
    console.error('Error cargando historial de reportes', e)
    reportes.value = []
  } finally {
    loading.value = false
  }
}

const downloadReporte = (codigo) => {
  if (!codigo) return
  const url = `/api/reportes/reportes/${encodeURIComponent(codigo)}/download/`
  window.open(url, '_blank')
}

const estadoPillClass = (estado) => {
  const v = (estado || '').toLowerCase()
  if (v === 'completado') return 'bg-green-100 text-green-700 border border-green-200'
  if (v === 'en progreso') return 'bg-blue-100 text-blue-700 border border-blue-200'
  if (v === 'fallido') return 'bg-red-100 text-red-700 border border-red-200'
  return 'bg-gray-100 text-gray-700 border border-gray-200'
}

onMounted(() => {
  ensureAuthHeader()
  fetchReportes()
})
</script>

<script>
export default {
  name: 'ReportesHub'
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
