<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex h-screen w-full">
    <!-- Sidebar (identical to Dashboard Ejecutivo) -->
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
          <a class="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg" href="#">
            <span class="material-symbols-outlined nofill">leaderboard</span>
            <p class="text-sm font-medium">Desempeño</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/indicadores') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/indicadores')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/indicadores') ? 'text-principal-blue' : '']">insights</span>
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
          <button class="flex h-10 min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg bg-theme-main-blue px-4 text-sm font-bold text-white hover:bg-theme-main-blue/90">
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

          <button id="apply-filters" class="mt-4 flex h-10 w-full items-center justify-center gap-2 rounded-lg bg-theme-light-blue/50 text-theme-dark-blue hover:bg-theme-light-blue text-sm font-bold dark:bg-primary/20 dark:text-white dark:hover:bg-primary/30">
            <span class="material-symbols-outlined">search</span>
            Aplicar Filtros
          </button>
        </div>

        <!-- Map and bottom panel -->
        <div class="flex flex-1 flex-col overflow-hidden p-6 gap-6">
          <div class="flex flex-1 flex-col gap-4 rounded-xl bg-theme-white dark:bg-background-dark overflow-hidden shadow-sm">
            <div class="flex items-center gap-3 border-b border-theme-medium-gray/50 px-4 py-2 dark:border-gray-700">
              <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-gray-100 pl-3 pr-2 dark:bg-gray-800">
                <p class="text-sm font-medium text-theme-dark-blue dark:text-gray-200">Categoría</p>
                <span class="material-symbols-outlined text-lg">arrow_drop_down</span>
              </button>
              <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-gray-100 pl-3 pr-2 dark:bg-gray-800">
                <p class="text-sm font-medium text-theme-dark-blue dark:text-gray-200">Estado</p>
                <span class="material-symbols-outlined text-lg">arrow_drop_down</span>
              </button>
              <button class="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg bg-gray-100 pl-3 pr-2 dark:bg-gray-800">
                <p class="text-sm font-medium text-theme-dark-blue dark:text-gray-200">Prioridad</p>
                <span class="material-symbols-outlined text-lg">arrow_drop_down</span>
              </button>
            </div>
            <div class="flex-1 px-4 pb-4">
              <div id="map" class="relative h-full w-full rounded-lg bg-gray-100 dark:bg-gray-800" style="z-index:1;"></div>
            </div>
          </div>

          <div class="flex h-1/3 min-h-[300px] flex-col rounded-xl bg-theme-white dark:bg-background-dark shadow-sm">
            <div class="flex border-b border-theme-medium-gray/50 px-4 dark:border-gray-700">
              <button class="tab-btn border-b-2 border-theme-main-blue px-3 py-2 text-sm font-semibold text-theme-main-blue" data-tab="tabla">Tabla de Tendencias</button>
              <button class="tab-btn border-b-2 border-transparent px-3 py-2 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300" data-tab="graficos">Gráficos Complementarios</button>
            </div>
            <div id="tabla-tab" class="tab-content flex-1 overflow-x-auto block">
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
                  <tr class="border-b bg-theme-white hover:bg-gray-50 dark:border-gray-700 dark:bg-background-dark dark:hover:bg-gray-800">
                    <td class="px-6 py-3 font-medium text-theme-dark-blue dark:text-white">Distrito Centro</td>
                    <td class="px-6 py-3">152</td>
                    <td class="px-6 py-3">Vandalismo</td>
                    <td class="px-6 py-3">85%</td>
                    <td class="px-6 py-3">48</td>
                    <td class="px-6 py-3"><span class="rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800">Medio</span></td>
                    <td class="px-6 py-3 text-red-600 flex items-center gap-1"><span>↑</span> 12%</td>
                    <td class="px-6 py-3"><a class="font-medium text-theme-main-blue hover:underline" href="#">Ver Detalle</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div id="graficos-tab" class="tab-content hidden flex-1 overflow-auto p-4">
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
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AnalisisGeografico',
  mounted() {
    const loadScript = (src) => new Promise((resolve, reject) => {
      const s = document.createElement('script'); s.src = src; s.onload = resolve; s.onerror = reject; document.head.appendChild(s);
    });
    const loadStyle = (href) => { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l) }

    // Material Symbols (if not globally present)
    if (!document.querySelector('link[href*="fonts.googleapis.com/css2?family=Material+Symbols+Outlined"]')) {
      const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined'; document.head.appendChild(l);
    }

    // Leaflet CSS
    if (!document.querySelector('link[href*="leaflet.min.css"]')) {
      loadStyle('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css')
    }

    const init = async () => {
      const token = localStorage.getItem('access_token')
      if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      // Load libs
      if (!window.L) await loadScript('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js')
      if (!window.Chart) await loadScript('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js')
      if (!window.L.heatLayer) await loadScript('https://cdnjs.cloudflare.com/ajax/libs/leaflet-heat/0.2.0/leaflet-heat.js')

      // Init map
      this._map = window.L.map('map').setView([-12.0499, -76.9499], 13)
      window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors', maxZoom: 19
      }).addTo(this._map)
      this._markers = []
      this._heat = null

      // Charts
      const ctxTop = document.getElementById('chart-top-zonas').getContext('2d')
      this._chartTop = new window.Chart(ctxTop, {
        type: 'bar', data: { labels: [], datasets: [{ label: 'Cantidad de Denuncias', data: [], backgroundColor: '#2A7DBD' }] },
        options: { indexAxis: 'y', plugins:{legend:{display:false}}, responsive:true, maintainAspectRatio:true, scales:{ x:{ beginAtZero:true } } }
      })

      const ctxEvo = document.getElementById('chart-evolucion').getContext('2d')
      this._chartEvo = new window.Chart(ctxEvo, {
        type: 'line', data: { labels: [], datasets: [] },
        options: { responsive:true, maintainAspectRatio:true, scales:{ y:{ beginAtZero:true } } }
      })

      const ctxHeat = document.getElementById('chart-heatmap').getContext('2d')
      this._chartHeat = new window.Chart(ctxHeat, {
        type: 'bar', data: { labels: [], datasets: [] }, options:{ indexAxis:'x', responsive:true, maintainAspectRatio:true, scales:{ x:{ stacked:true }, y:{ stacked:true } }, plugins:{ legend:{ display:true } } }
      })

      // Tabs
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
          const tab = this.getAttribute('data-tab')
          document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'))
          document.getElementById(tab + '-tab').classList.remove('hidden')
          document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('border-theme-main-blue','text-theme-main-blue'))
          this.classList.add('border-theme-main-blue','text-theme-main-blue')
        })
      })

      // Fetch initial
      await this.applyFilters()
      // Wire apply filters button
      document.getElementById('apply-filters')?.addEventListener('click', this.applyFilters)
    }

    init().catch(e => console.error('Error inicializando análisis geográfico', e))
  },
  methods: {
    buildQueryParams() {
      const params = {}
      const d = document.getElementById('district-selector')?.value
      if (d && d !== 'Todos los distritos') params['district'] = d
      const z = document.getElementById('zone-selector')?.value
      // zona no disponible en BD; ignoramos por ahora o úsalo si existiera
      const code = document.getElementById('search-code')?.value?.trim()
      if (code) params['code'] = code
      const from = document.getElementById('date-from')?.value
      const to = document.getElementById('date-to')?.value
      if (from) params['from'] = from
      if (to) params['to'] = to
      return params
    },
    async applyFilters() {
      await Promise.all([
        this.fetchPoints(),
        this.updateTopZonas(),
        this.updateEvolucion(),
      ])
    },
    async fetchPoints() {
      try {
        const { data } = await axios.get('/api/reportes/geo/points/', { params: this.buildQueryParams() })
        const points = data.points || []
        // Clear markers
        this._markers.forEach(m => this._map.removeLayer(m))
        this._markers = []
        if (this._heat) { this._map.removeLayer(this._heat); this._heat = null }
        const heatData = []
        points.forEach(p => {
          const marker = window.L.marker([p.lat, p.lng]).addTo(this._map)
          marker.bindPopup(`<div style="min-width:200px;"><h4 style="margin:0 0 8px 0;font-weight:bold;color:#0B4A72;">${p.codigo}</h4><p style="margin:4px 0;font-size:12px;"><strong>${p.titulo||''}</strong></p><p style="margin:4px 0;font-size:11px;">Categoría: ${p.categoria||'-'}</p><p style=\"margin:4px 0;font-size:11px;\">Estado: ${p.estado}</p><p style=\"margin:4px 0;font-size:11px;\">Fecha: ${p.fecha?.slice(0,10)}</p></div>`)
          this._markers.push(marker)
          heatData.push([p.lat, p.lng, 1])
        })
        if (heatData.length) {
          this._heat = window.L.heatLayer(heatData, { radius: 30, blur: 25, maxZoom: 17 }).addTo(this._map)
          // Fit bounds
          const bounds = window.L.latLngBounds(heatData.map(h => [h[0], h[1]]))
          this._map.fitBounds(bounds, { maxZoom: 15 })
        }
        this.updateTableFromPoints(points)
      } catch (e) { console.error('Error geo points', e) }
    },
    async updateTopZonas() {
      try {
        const { data } = await axios.get('/api/reportes/geo/top-zonas/', { params: this.buildQueryParams() })
        const items = data.top_zonas || []
        this._chartTop.data.labels = items.map(i => i.zona)
        this._chartTop.data.datasets[0].data = items.map(i => i.denuncias)
        this._chartTop.update()
      } catch (e) { console.error('Error top zonas', e) }
    },
    async updateEvolucion() {
      try {
        const { data } = await axios.get('/api/reportes/geo/evolucion/', { params: { ...this.buildQueryParams(), days: 7 } })
        this._chartEvo.data.labels = data.labels || []
        const palette = ['#2A7DBD','#FF6B6B','#FFD93D','#10B981','#8B5CF6','#F59E0B']
        this._chartEvo.data.datasets = (data.datasets||[]).map((ds, idx) => ({
          label: ds.label,
          data: ds.data,
          borderColor: palette[idx % palette.length],
          backgroundColor: palette[idx % palette.length] + '33',
          tension: 0.3,
          borderWidth: 2,
          fill: true
        }))
        this._chartEvo.update()
        // Heat stacked demo from evolucion (aggregate by weekday)
        const weekday = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb']
        const agg = {}
        (data.labels||[]).forEach((lbl, i) => {
          const d = new Date(lbl); const w = weekday[d.getDay()]
          (data.datasets||[]).forEach(ds => { agg[w] = (agg[w]||0) + (ds.data[i]||0) })
        })
        this._chartHeat.data.labels = weekday
        this._chartHeat.data.datasets = [{ label: 'Incidencias', data: weekday.map(w => agg[w]||0), backgroundColor: '#2A7DBD' }]
        this._chartHeat.update()
      } catch (e) { console.error('Error evolucion', e) }
    },
    updateTableFromPoints(points) {
      try {
        const tbody = document.querySelector('#tabla-tab tbody')
        if (!tbody) return
        // Aggregate by distrito
        const byDist = {}
        points.forEach(p => {
          const key = p.distrito || 'Sin distrito'
          const obj = byDist[key] = byDist[key] || { total:0, cats:{} }
          obj.total += 1
          if (p.categoria) obj.cats[p.categoria] = (obj.cats[p.categoria]||0) + 1
        })
        const rows = Object.entries(byDist).slice(0, 5).map(([dist, v]) => {
          const catFreq = Object.entries(v.cats).sort((a,b)=>b[1]-a[1])[0]?.[0] || '-'
          const tasa = '—'
          const tiempo = '—'
          const nivel = v.total > 150 ? 'Alto' : v.total > 80 ? 'Medio' : 'Bajo'
          const nivelTag = nivel === 'Alto' ? 'bg-red-100 text-red-800' : nivel === 'Medio' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
          return `<tr class="border-b bg-theme-white hover:bg-gray-50 dark:border-gray-700 dark:bg-background-dark dark:hover:bg-gray-800">
            <td class="px-6 py-3 font-medium text-theme-dark-blue dark:text-white">${dist}</td>
            <td class="px-6 py-3">${v.total}</td>
            <td class="px-6 py-3">${catFreq}</td>
            <td class="px-6 py-3">${tasa}</td>
            <td class="px-6 py-3">${tiempo}</td>
            <td class="px-6 py-3"><span class="rounded-full px-2.5 py-0.5 text-xs font-medium ${nivelTag}">${nivel}</span></td>
            <td class="px-6 py-3 text-gray-600 flex items-center gap-1"><span>•</span> —</td>
            <td class="px-6 py-3"><a class="font-medium text-theme-main-blue hover:underline" href="#">Ver Detalle</a></td>
          </tr>`
        }).join('')
        tbody.innerHTML = rows || '<tr><td class="px-6 py-3" colspan="8">Sin datos</td></tr>'
      } catch (e) { console.error('Error tabla', e) }
    },
    isActive(path) {
      try { return this.$route.path.startsWith(path) } catch { return false }
    }
  }
}
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
.material-symbols-outlined{ font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24 }
</style>
