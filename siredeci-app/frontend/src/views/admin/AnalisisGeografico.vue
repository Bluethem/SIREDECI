<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex h-screen w-full">
    <SidebarAdmin />

    <!-- Main -->
    <main class="flex h-screen flex-1 flex-col overflow-hidden">
      <!-- Top Bar -->
      <header class="flex w-full flex-shrink-0 items-center justify-between border-b border-theme-medium-gray/50 bg-theme-white px-6 py-3 dark:border-gray-700 dark:bg-background-dark">
        <div class="flex flex-col">
          <h2 class="text-lg font-bold text-theme-dark-blue dark:text-white">Análisis Geográfico de Denuncias</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Visualización de incidencias en el municipio.</p>
        </div>
        <div class="flex items-center gap-4">
          <button class="flex h-10 cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg bg-gray-100 px-4 text-sm font-medium text-theme-dark-blue hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700">
            <span class="material-symbols-outlined text-base">calendar_today</span>
            <span class="truncate">Periodo: Últimos 30 días</span>
          </button>
          <button id="export-map-btn" class="flex h-10 min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg bg-green-600 px-4 text-sm font-bold text-white hover:bg-green-700">
            <span class="material-symbols-outlined text-base">download</span>
            <span class="truncate">Descargar Mapa</span>
          </button>
          <button class="flex h-10 min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg bg-blue-400 px-4 text-sm font-bold text-white hover:bg-blue-500">
            <span class="material-symbols-outlined text-base">ios_share</span>
            <span class="truncate">Exportar Mapa</span>
          </button>
        </div>
      </header>

      <div class="flex flex-1 overflow-hidden">
        <!-- Left filters -->
        <div class="flex h-full w-80 flex-shrink-0 flex-col gap-4 border-r border-theme-medium-gray/50 bg-theme-white p-4 overflow-y-auto dark:border-gray-700 dark:bg-background-dark">
          <h3 class="text-base font-semibold text-theme-dark-blue dark:text-white">Filtros Geográficos</h3>

          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-gray-600 dark:text-gray-400" for="district-selector">Distrito</label>
            <select id="district-selector" class="w-full rounded-md border-theme-medium-gray text-sm focus:border-theme-main-blue focus:ring-theme-main-blue dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-primary">
              <option>Todos los distritos</option>
              <option>Distrito Centro</option>
              <option>Distrito Norte</option>
            </select>
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-gray-600 dark:text-gray-400" for="search-code">Búsqueda por Código</label>
            <input id="search-code" type="text" placeholder="Ej: DEN-001" class="w-full rounded-md border border-theme-medium-gray px-2 py-1 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:border-theme-main-blue focus:ring-theme-main-blue" />
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-gray-600 dark:text-gray-400" for="zone-selector">Zona</label>
            <select id="zone-selector" class="w-full rounded-md border-theme-medium-gray text-sm focus:border-theme-main-blue focus:ring-theme-main-blue dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-primary">
              <option>Todas las zonas</option>
              <option>Zona Comercial</option>
              <option>Zona Residencial</option>
            </select>
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Rango de Fechas</label>
            <div class="flex gap-2">
              <input id="date-from" type="date" placeholder="Desde" class="flex-1 rounded-md border border-theme-medium-gray px-2 py-1 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
              <input id="date-to" type="date" placeholder="Hasta" class="flex-1 rounded-md border border-theme-medium-gray px-2 py-1 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
            </div>
          </div>

          <details class="flex flex-col group" open>
            <summary class="flex cursor-pointer list-none items-center justify-between py-2">
              <p class="text-xs font-medium text-gray-600 dark:text-gray-400">Categorías</p>
              <span class="material-symbols-outlined text-lg text-gray-500 transition-transform group-open:rotate-180">expand_less</span>
            </summary>
            <div class="flex flex-col gap-2 pl-1">
              <label class="flex items-center gap-2"><input checked class="h-4 w-4 rounded border-gray-300 text-theme-main-blue focus:ring-theme-main-blue" type="checkbox" /> <span class="text-sm">Vandalismo</span></label>
              <label class="flex items-center gap-2"><input checked class="h-4 w-4 rounded border-gray-300 text-theme-main-blue focus:ring-theme-main-blue" type="checkbox" /> <span class="text-sm">Robo</span></label>
              <label class="flex items-center gap-2"><input class="h-4 w-4 rounded border-gray-300 text-theme-main-blue focus:ring-theme-main-blue" type="checkbox" /> <span class="text-sm">Ruido Excesivo</span></label>
              <label class="flex items-center gap-2"><input class="h-4 w-4 rounded border-gray-300 text-theme-main-blue focus:ring-theme-main-blue" type="checkbox" /> <span class="text-sm">Infraestructura</span></label>
            </div>
          </details>

          <div class="flex flex-col gap-2 pt-2">
            <label class="text-xs font-medium text-gray-600 dark:text-gray-400" for="radius-slider">Radio de Búsqueda (km)</label>
            <input id="radius-slider" type="range" min="1" max="10" value="5" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-theme-main-blue" />
            <div class="flex justify-between text-xs text-gray-500"><p>1 km</p><p>5 km</p><p>10 km</p></div>
          </div>

          <button id="apply-filters" class="mt-4 flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-theme-light-blue/50 text-theme-dark-blue hover:bg-theme-light-blue text-sm font-bold dark:bg-primary/20 dark:text-white dark:hover:bg-primary/30" @click="applyFilters">
            <span class="material-symbols-outlined">search</span>
            Aplicar Filtros
          </button>
        </div>

        <!-- Map and bottom panel -->
        <div class="flex flex-1 flex-col overflow-hidden p-6 gap-6">
          <div class="flex flex-1 flex-col gap-4 rounded-xl bg-theme-white dark:bg-background-dark overflow-hidden shadow-sm">
            <div class="flex items-center gap-3 border-b border-theme-medium-gray/50 px-4 py-2 dark:border-gray-700">
              <!-- Filtro categoría -->
              <div class="flex items-center gap-2">
                <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Categoría</label>
                <select
                  id="categoria-filter"
                  class="h-8 rounded-lg border border-theme-medium-gray bg-gray-100 px-2 text-xs text-theme-dark-blue dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
                >
                  <option value="">Todas</option>
                  <option value="Vandalismo">Vandalismo</option>
                  <option value="Robo">Robo</option>
                  <option value="Ruido Excesivo">Ruido Excesivo</option>
                  <option value="Infraestructura">Infraestructura</option>
                </select>
              </div>

              <!-- Filtro estado -->
              <div class="flex items-center gap-2">
                <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Estado</label>
                <select
                  id="estado-filter"
                  class="h-8 rounded-lg border border-theme-medium-gray bg-gray-100 px-2 text-xs text-theme-dark-blue dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
                >
                  <option value="">Todos</option>
                  <option value="Registrado">Registrado</option>
                  <option value="En revisión">En revisión</option>
                  <option value="Asignado">Asignado</option>
                  <option value="En proceso">En proceso</option>
                  <option value="Resuelta">Resuelta</option>
                  <option value="Rechazada">Rechazada</option>
                  <option value="Cerrada">Cerrada</option>
                </select>
              </div>

              <!-- Filtro prioridad -->
              <div class="flex items-center gap-2">
                <label class="text-xs font-medium text-gray-600 dark:text-gray-400">Prioridad</label>
                <select
                  id="prioridad-filter"
                  class="h-8 rounded-lg border border-theme-medium-gray bg-gray-100 px-2 text-xs text-theme-dark-blue dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
                >
                  <option value="">Todas</option>
                  <option value="Baja">Baja</option>
                  <option value="Media">Media</option>
                  <option value="Alta">Alta</option>
                  <option value="Urgente">Urgente</option>
                </select>
              </div>
            </div>
            <div class="flex-1 px-4 pb-4">
              <div id="map" class="relative h-full w-full rounded-lg bg-gray-100 dark:bg-gray-800" style="z-index:1;"></div>
            </div>
          </div>

          <div class="flex h-1/3 min-h-[300px] flex-col rounded-xl bg-theme-white dark:bg-background-dark shadow-sm">
            <div class="flex border-b border-theme-medium-gray/50 px-4 dark:border-gray-700">
              <button
                class="tab-btn px-3 py-2 text-sm"
                :class="activeTab === 'tabla'
                  ? 'border-b-2 border-theme-main-blue font-semibold text-theme-main-blue'
                  : 'border-b-2 border-transparent font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'"
                data-tab="tabla"
                @click="setActiveTab('tabla')"
              >
                Tabla de Tendencias
              </button>
              <button
                class="tab-btn px-3 py-2 text-sm"
                :class="activeTab === 'graficos'
                  ? 'border-b-2 border-theme-main-blue font-semibold text-theme-main-blue'
                  : 'border-b-2 border-transparent font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'"
                data-tab="graficos"
                @click="setActiveTab('graficos')"
              >
                Gráficos Complementarios
              </button>
            </div>
            <div id="tabla-tab" class="tab-content flex-1 overflow-x-auto" v-show="activeTab === 'tabla'">
              <table class="w-full min-w-[800px] text-left text-sm">
                <thead class="border-b border-theme-medium-gray/50 bg-gray-50 text-xs uppercase text-gray-700 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400">
                  <tr>
                    <th class="px-6 py-3" scope="col">Zona/Distrito</th>
                    <th class="px-6 py-3" scope="col">Total Denuncias</th>
                    <th class="px-6 py-3" scope="col">Categoría Frecuente</th>
                    <th class="px-6 py-3" scope="col">Tasa Resolución</th>
                    <th class="px-6 py-3" scope="col">Tiempo Prom. (h)</th>
                    <th class="px-6 py-3" scope="col">Nivel Crítico</th>
                    <th class="px-6 py-3" scope="col">vs Periodo Ant.</th>
                    <th class="px-6 py-3" scope="col">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="row in tendencias"
                    :key="row.codigo_tendencia"
                    class="border-b bg-theme-white hover:bg-gray-50 dark:border-gray-700 dark:bg-background-dark dark:hover:bg-gray-800"
                  >
                    <td class="px-6 py-3 font-medium text-theme-dark-blue dark:text-white">
                      {{ row.zona || row.distrito || 'Sin zona' }}
                    </td>
                    <td class="px-6 py-3">{{ row.cantidad_denuncias }}</td>
                    <td class="px-6 py-3">{{ row.categoria_mas_frecuente || '—' }}</td>
                    <td class="px-6 py-3">{{ row.tasa_resolucion != null ? row.tasa_resolucion.toFixed(1) + '%' : '—' }}</td>
                    <td class="px-6 py-3">{{ row.tiempo_promedio_atencion != null ? row.tiempo_promedio_atencion.toFixed(1) : '—' }}</td>
                    <td class="px-6 py-3">
                      <span
                        class="px-2.5 py-0.5 text-xs font-medium rounded-full"
                        :class="nivelCriticoBadgeClass(row.nivel_criticidad)"
                      >
                        {{ row.nivel_criticidad || 'Sin dato' }}
                      </span>
                    </td>
                    <td class="px-6 py-3 text-gray-500 flex items-center gap-1">
                      <span>—</span>
                    </td>
                    <td class="px-6 py-3">
                      <button
                        type="button"
                        class="font-medium text-theme-main-blue hover:underline text-sm"
                        @click="openTrendDetail(row)"
                      >
                        Ver Detalle
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!loadingTendencias && tendencias.length === 0">
                    <td class="px-6 py-4 text-sm text-gray-500" colspan="8">Sin datos para los filtros seleccionados.</td>
                  </tr>
                  <tr v-if="loadingTendencias">
                    <td class="px-6 py-4 text-sm text-gray-500" colspan="8">Cargando tendencias geográficas...</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div id="graficos-tab" class="tab-content flex-1 overflow-auto p-4" v-show="activeTab === 'graficos'">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
                <div class="flex flex-col rounded-lg bg-gray-50 p-4 dark:bg-gray-800">
                  <h4 class="mb-2 text-sm font-semibold text-theme-dark-blue dark:text-white">Top 10 Zonas con Mayor Incidencia</h4>
                  <canvas id="chart-top-zonas"></canvas>
                </div>
                <div class="flex flex-col rounded-lg bg-gray-50 p-4 dark:bg-gray-800">
                  <h4 class="mb-2 text-sm font-semibold text-theme-dark-blue dark:text-white">Evolución por Distrito</h4>
                  <canvas id="chart-evolucion"></canvas>
                </div>
                <div class="flex flex-col rounded-lg bg-gray-50 p-4 dark:bg-gray-800 lg:col-span-2">
                  <h4 class="mb-2 text-sm font-semibold text-theme-dark-blue dark:text-white">Mapa de Calor Temporal (Últimos 7 días)</h4>
                  <canvas id="chart-heatmap"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Detalle Tendencia -->
    <div
      v-if="showTrendModal && selectedTendencia"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="bg-white dark:bg-background-dark rounded-xl shadow-xl max-w-xl w-full mx-4 overflow-hidden">
        <div class="flex items-center justify-between border-b border-theme-medium-gray/50 px-5 py-3 dark:border-gray-700">
          <h3 class="text-lg font-bold text-theme-dark-blue dark:text-white">
            Detalle de Zona: {{ selectedTendencia.zona || selectedTendencia.distrito || 'Sin zona' }}
          </h3>
          <button
            type="button"
            class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 text-xl"
            @click="closeTrendDetail"
          >
            ×
          </button>
        </div>
        <div class="px-5 py-4 space-y-3 text-sm">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Distrito</p>
              <p class="font-medium text-theme-dark-blue dark:text-white">{{ selectedTendencia.distrito || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Zona</p>
              <p class="font-medium text-theme-dark-blue dark:text-white">{{ selectedTendencia.zona || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Total denuncias</p>
              <p class="font-medium">{{ selectedTendencia.cantidad_denuncias }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Categoría más frecuente</p>
              <p class="font-medium">{{ selectedTendencia.categoria_mas_frecuente || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Tasa de resolución</p>
              <p class="font-medium">{{ selectedTendencia.tasa_resolucion != null ? selectedTendencia.tasa_resolucion.toFixed(1) + '%' : '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Tiempo promedio atención (h)</p>
              <p class="font-medium">{{ selectedTendencia.tiempo_promedio_atencion != null ? selectedTendencia.tiempo_promedio_atencion.toFixed(1) : '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Nivel crítico</p>
              <p class="font-medium">
                <span
                  class="px-2.5 py-0.5 text-xs font-medium rounded-full"
                  :class="nivelCriticoBadgeClass(selectedTendencia.nivel_criticidad)"
                >
                  {{ selectedTendencia.nivel_criticidad || 'Sin dato' }}
                </span>
              </p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Periodo de análisis</p>
              <p class="font-medium">{{ selectedTendencia.periodo_analisis || '—' }}</p>
            </div>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Los datos provienen de la tabla de tendencias geográficas agregadas del sistema.
          </p>
        </div>
        <div class="flex justify-end gap-2 border-t border-theme-medium-gray/50 px-5 py-3 dark:border-gray-700">
          <button
            type="button"
            class="h-9 px-4 rounded-lg border border-medium-gray text-xs font-medium text-gray-700 hover:bg-gray-50 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-800"
            @click="closeTrendDetail"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow
})

const activeTab = ref('tabla')

let map = null
let markersLayer = null

const charts = {
  topZonas: null,
  evolucion: null,
  heatmap: null
}

const tendencias = ref([])
const loadingTendencias = ref(false)
const selectedTendencia = ref(null)
const showTrendModal = ref(false)

const ensureAuthHeader = () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

const loadTendencias = async () => {
  try {
    loadingTendencias.value = true
    const baseParams = buildParams()
    const params = {}
    if (baseParams.district) params.distrito = baseParams.district
    if (baseParams.from || baseParams.to) {
      // Si se diera el caso de mapear el rango a un periodo_analisis textual, se podra hacer aqu.
    }
    const { data } = await axios.get('/api/public/reportes/tendencias-geograficas/', { params })
    tendencias.value = data.results || []
  } catch (e) {
    console.error('Error cargando tendencias geogrficas', e)
    tendencias.value = []
  } finally {
    loadingTendencias.value = false
  }
}

const openTrendDetail = (row) => {
  selectedTendencia.value = row
  showTrendModal.value = true
}

const closeTrendDetail = () => {
  showTrendModal.value = false
  selectedTendencia.value = null
}

const loadChartJs = async () => {
  if (window.Chart) return
  await new Promise((resolve, reject) => {
    const s = document.createElement('script')
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js'
    s.onload = resolve
    s.onerror = reject
    document.head.appendChild(s)
  })
}

const setActiveTab = (tab) => {
  activeTab.value = tab
}

const nivelCriticoBadgeClass = (nivel) => {
  const value = (nivel || '').toLowerCase()
  if (value === 'alto' || value === 'crtico' || value === 'crtica') {
    return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  if (value === 'medio' || value === 'moderado') {
    return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  }
  if (value === 'bajo') {
    return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300'
  }
  return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
}

const buildParams = () => {
  const params = {}

  const districtEl = document.getElementById('district-selector')
  if (districtEl && districtEl.value && districtEl.value !== 'Todos los distritos') {
    params.district = districtEl.value
  }

  const codeEl = document.getElementById('search-code')
  if (codeEl && codeEl.value) {
    params.code = codeEl.value.trim()
  }

  const categoriaEl = document.getElementById('categoria-filter')
  if (categoriaEl && categoriaEl.value) {
    params.categoria = categoriaEl.value
  }

  const estadoEl = document.getElementById('estado-filter')
  if (estadoEl && estadoEl.value) {
    params.estado = estadoEl.value
  }

  const prioridadEl = document.getElementById('prioridad-filter')
  if (prioridadEl && prioridadEl.value) {
    params.prioridad = prioridadEl.value
  }

  const fromEl = document.getElementById('date-from')
  const toEl = document.getElementById('date-to')
  if (fromEl && fromEl.value) {
    params.from = fromEl.value
  }
  if (toEl && toEl.value) {
    params.to = toEl.value
  }

  return params
}

const initMap = () => {
  const mapElement = document.getElementById('map')
  if (!mapElement || map) return

  const defaultLat = -12.0464
  const defaultLng = -77.0428

  map = L.map('map', {
    center: [defaultLat, defaultLng],
    zoom: 12,
    zoomControl: true
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
}

const renderPointsOnMap = (points) => {
  if (!map || !markersLayer) return

  markersLayer.clearLayers()

  if (!points || !points.length) return

  const bounds = []

  points.forEach((p) => {
    if (typeof p.lat !== 'number' || typeof p.lng !== 'number') return
    const marker = L.marker([p.lat, p.lng])
    const popup = `
      <div>
        <strong>${p.codigo || ''}</strong><br/>
        ${p.titulo || ''}<br/>
        <span>Categoría: ${p.categoria || '—'}</span><br/>
        <span>Estado: ${p.estado || '—'}</span><br/>
        <span>Prioridad: ${p.prioridad || '—'}</span><br/>
        <span>Distrito: ${p.distrito || '—'}</span>
      </div>
    `
    marker.bindPopup(popup)
    marker.addTo(markersLayer)
    bounds.push([p.lat, p.lng])
  })

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40] })
  }
}

const loadGeoPoints = async () => {
  try {
    const params = buildParams()
    const { data } = await axios.get('/api/reportes/geo/points/', { params })
    renderPointsOnMap(data.points || [])
  } catch (e) {
    console.error('Error cargando puntos geográficos', e)
  }
}

const renderTopZonasChart = (items) => {
  if (!window.Chart) return
  const canvas = document.getElementById('chart-top-zonas')
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (charts.topZonas) {
    charts.topZonas.destroy()
    charts.topZonas = null
  }

  const labels = items.map((i) => i.zona)
  const values = items.map((i) => i.denuncias)

  charts.topZonas = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Denuncias',
          data: values,
          backgroundColor: '#2A7DBD',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}

const loadTopZonas = async () => {
  try {
    const baseParams = buildParams()
    const params = {}
    if (baseParams.from) params.from = baseParams.from
    if (baseParams.to) params.to = baseParams.to

    const { data } = await axios.get('/api/reportes/geo/top-zonas/', { params })
    renderTopZonasChart(data.top_zonas || [])
  } catch (e) {
    console.error('Error cargando top de zonas', e)
  }
}

const renderEvolucionChart = (labels, datasets) => {
  if (!window.Chart) return
  const canvas = document.getElementById('chart-evolucion')
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (charts.evolucion) {
    charts.evolucion.destroy()
    charts.evolucion = null
  }

  charts.evolucion = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: (datasets || []).map((ds, idx) => ({
        label: ds.label,
        data: ds.data,
        borderColor: ['#2A7DBD', '#0B4A72', '#AFCFE3', '#10B981', '#F59E0B'][idx % 5],
        backgroundColor: 'transparent',
        tension: 0.3
      }))
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}

const renderHeatmapChart = (labels, datasets) => {
  if (!window.Chart) return
  const canvas = document.getElementById('chart-heatmap')
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (charts.heatmap) {
    charts.heatmap.destroy()
    charts.heatmap = null
  }

  const totalPerDay = labels.map((_, idx) => {
    return (datasets || []).reduce((sum, ds) => sum + (ds.data[idx] || 0), 0)
  })

  charts.heatmap = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Denuncias por día',
          data: totalPerDay,
          backgroundColor: totalPerDay.map((v) => {
            if (v === 0) return '#E5E7EB'
            if (v < 3) return '#BFDBFE'
            if (v < 7) return '#60A5FA'
            return '#1D4ED8'
          }),
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}

const loadEvolucion = async () => {
  try {
    const { data } = await axios.get('/api/reportes/geo/evolucion/', {
      params: { days: 7 }
    })
    const labels = data.labels || []
    const datasets = data.datasets || []
    renderEvolucionChart(labels, datasets)
    renderHeatmapChart(labels, datasets)
  } catch (e) {
    console.error('Error cargando evolución geográfica', e)
  }
}

const applyFilters = async () => {
  await loadGeoPoints()
  await loadTopZonas()
  await loadEvolucion()
   await loadTendencias()
}

onMounted(async () => {
  ensureAuthHeader()
  initMap()
  try {
    await loadChartJs()
  } catch (e) {
    console.error('Error cargando librería Chart.js', e)
  }
  applyFilters()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
  markersLayer = null

  if (charts.topZonas) {
    charts.topZonas.destroy()
    charts.topZonas = null
  }
  if (charts.evolucion) {
    charts.evolucion.destroy()
    charts.evolucion = null
  }
  if (charts.heatmap) {
    charts.heatmap.destroy()
    charts.heatmap = null
  }
})
</script>

<style scoped>
:root {
  --theme-main-blue: #2A7DBD;
  --theme-light-blue: #AFCFE3;
  --theme-dark-blue: #0B4A72;
  --theme-white: #FFFFFF;
  --theme-light-gray: #F5F7F9;
  --theme-medium-gray: #D1D5DB;
}

.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
