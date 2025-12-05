<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex h-screen w-full">
    <SidebarAdmin />

    <!-- Main content -->
    <main class="flex flex-1 flex-col overflow-hidden">
      <div class="flex-1 overflow-y-auto p-6 lg:p-8">
        <div class="w-full max-w-7xl mx-auto">
        <header class="flex flex-wrap justify-between items-center gap-4 mb-6">
          <div>
            <p class="text-3xl font-black leading-tight tracking-[-0.033em]">Ranking de Desempeño por Área</p>
            <p class="text-gray-500 mt-1">Periodo de Evaluación: 01 Ene, 2024 - 31 Mar, 2024</p>
          </div>
          <div class="flex flex-1 gap-3 flex-wrap justify-end min-w-[200px]">
            <button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-white text-dark-blue text-sm font-bold border border-medium-gray">
              <span class="truncate">View History</span>
            </button>
            <button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-principal-blue text-white text-sm font-bold">
              <span class="truncate">Export Ranking</span>
            </button>
          </div>
        </header>

        <!-- Top 3 -->
        <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div class="flex flex-col gap-3 text-center p-6 bg-white rounded-xl border border-medium-gray transform hover:scale-105 transition-transform duration-300">
            <div class="px-4">
              <div class="w-24 h-24 mx-auto bg-center bg-no-repeat aspect-square bg-cover rounded-full border-4 border-slate-300" style="background-image:url('https://lh3.googleusercontent.com/aida-public/AB6AXuDyjT-KPizI9BgQT8DPhAyV1KmRgi1vjzpUxmtNzky_qK3GfBKEP3AR9eCcuYD7TjB-RbxRZsr69ZKFnklHLJ-NsWoZCBuptoNGOE5IuRt_hjg_ruTOlQNb9Y0yXJsX7VOHFDpWOfNuaMl_domvvfMml1rlb2O3_VjllWBS_F7qFafC3_QfutNVmFZSOjasckSD2k9p8ry4aW7tkRtB5nAoUBogS0dtUc_x-38WzlsmjV6wjcSCPlNcL_CYze5ySceZRFWVy7hNKbT0')"></div>
            </div>
            <div>
              <p class="text-lg font-bold">Área de Soporte Técnico</p>
              <p class="text-4xl font-black text-slate-500 my-2">95.2 <span class="text-xl">Pts</span></p>
              <p class="text-slate-500 text-lg font-medium">2nd Place</p>
            </div>
          </div>
          <div class="flex flex-col gap-3 text-center p-6 bg-white rounded-xl border-2 border-amber-400 transform scale-105 hover:scale-110 transition-transform duration-300 shadow-lg z-10">
            <div class="px-4">
              <div class="w-28 h-28 mx-auto bg-center bg-no-repeat aspect-square bg-cover rounded-full border-4 border-amber-400" style="background-image:url('https://lh3.googleusercontent.com/aida-public/AB6AXuDjGI1CRoB0IIPh4ZSYLnZ5AvVHzHdxhAL582oHjyp8W0_4pXKLB_o5ZrGZQYiUnJBaW2TceUa3to9xNQ5WRZ7HxtK81ynHWp6Sdo5p2PPCz9hGqSaleWqHQQU9wVIdJ4yYPRXu2mHmFQggtf_zDSpn3K4cctvLoiyxWjZ62hP5EqJ4u7kCQlf7Mu-A6FZSNtBZwU3ObE7JRx8cMor898c4slnDLRgYW78o95Ak4hsQmdfJl-4IFkJh_xQfjeeITbNETwPmJ-VvQ__k')"></div>
            </div>
            <div>
              <p class="text-xl font-bold">Área de Operaciones</p>
              <p class="text-5xl font-black text-amber-500 my-2">98.5 <span class="text-2xl">Pts</span></p>
              <p class="text-amber-500 text-xl font-medium">1st Place</p>
            </div>
          </div>
          <div class="flex flex-col gap-3 text-center p-6 bg-white rounded-xl border border-medium-gray transform hover:scale-105 transition-transform duration-300">
            <div class="px-4">
              <div class="w-24 h-24 mx-auto bg-center bg-no-repeat aspect-square bg-cover rounded-full border-4 border-[#cd7f32]" style="background-image:url('https://lh3.googleusercontent.com/aida-public/AB6AXuCWWYnAa9PmffjaUHx-6Pc8RPwM1wDzRbAIiqdoPi69bgUX6iTTZ9cNE31K-5VtlqrVFkvz3jL7890_dzT8-dyX7AsAyknLXIYHz7InN553clU4uiVOtSkeQ1CLmltzgoCqhBjdGJx33sVeqgsXDDn5ShTA9jatUJ0D2UyfblZJcCOOjcO2tz3tBmlbCCqUALWet4TR947v-3Lwv1PPv-TsRXk1HNfgm3ZUsEEQGZ8YKxlwmIASZrOx9ooHO--YApK7LmPTbUr22zbe')"></div>
            </div>
            <div>
              <p class="text-lg font-bold">Área de Logística</p>
              <p class="text-4xl font-black text-[#b87333] my-2">92.8 <span class="text-xl">Pts</span></p>
              <p class="text-[#b87333] text-lg font-medium">3rd Place</p>
            </div>
          </div>
        </section>

        <!-- Table controls -->
        <div class="bg-white rounded-xl border border-medium-gray overflow-hidden">
          <div class="p-4 border-b border-medium-gray flex justify-between items-center gap-4">
            <div class="flex w-full md:w-1/2 lg:w-1/3">
              <label class="flex flex-col w-full">
                <div class="flex w-full flex-1 items-stretch rounded-lg h-10">
                  <div class="text-dark-blue flex border border-medium-gray bg-light-blue items-center justify-center pl-3 pr-2 rounded-l-lg border-r-0">
                    <span class="material-symbols-outlined">search</span>
                  </div>
                  <input id="search-input" v-model="query" class="form-input flex w-full min-w-0 flex-1 rounded-r-lg text-dark-blue focus:outline-0 focus:ring-2 focus:ring-main-blue/50 border-medium-gray bg-white h-full placeholder:text-gray-500 px-3 text-base" placeholder="Buscar por área..." />
                </div>
              </label>
            </div>
            <div class="flex gap-2 items-center">
              <select id="pagination-select" v-model.number="limit" class="px-3 py-2 border border-medium-gray rounded-lg text-sm">
                <option :value="10">10 registros</option>
                <option :value="25">25 registros</option>
                <option :value="50">50 registros</option>
              </select>
              <div class="flex gap-2">
                <button id="prev-page" @click="goPrev" class="px-3 py-2 border border-medium-gray rounded-lg hover:bg-gray-100">←</button>
                <span id="page-info" class="px-3 py-2 text-sm">Página {{ page }} de {{ maxPages }}</span>
                <button id="next-page" @click="goNext" class="px-3 py-2 border border-medium-gray rounded-lg hover:bg-gray-100">→</button>
              </div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm text-left text-gray-500">
              <thead class="text-xs text-dark-blue uppercase bg-gray-50">
                <tr>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="rank"># <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="area">Área Responsable <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="puntaje">Puntaje Total <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="denuncias">Denuncias Atendidas <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="tasa">Tasa Resolución <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="tiempo">Tiempo Promedio <span>↕</span></th>
                  <th class="px-6 py-3 cursor-pointer sort-icon" data-column="calificacion">Calificación <span>↕</span></th>
                  <th class="px-6 py-3">Tendencia</th>
                  <th class="px-6 py-3">Acciones</th>
                </tr>
              </thead>
              <tbody id="table-body">
                <tr v-for="area in pageData" :key="area.area" class="bg-white border-b border-medium-gray hover:bg-gray-50 cursor-pointer" @click="openModal(area)">
                  <td class="px-6 py-4"><span :class="rankBadge(area.rank)" class="text-xs font-medium px-2.5 py-0.5 rounded-full">{{ area.rank }}</span></td>
                  <td class="px-6 py-4 font-medium text-dark-blue">{{ area.area }}</td>
                  <td class="px-6 py-4">
                    <div class="font-bold text-dark-blue">{{ area.puntaje }}</div>
                    <div class="progress-bar"><div class="progress-bar-fill" :style="{width: area.puntaje + '%'}"></div></div>
                  </td>
                  <td class="px-6 py-4">{{ area.denuncias }}</td>
                  <td class="px-6 py-4">
                    <div class="font-bold text-dark-blue">{{ area.tasa }}%</div>
                    <div class="progress-bar"><div class="progress-bar-fill" :style="{width: area.tasa + '%'}"></div></div>
                  </td>
                  <td class="px-6 py-4"><span class="badge-green text-xs px-2 py-1 rounded">{{ area.tiempo }}h</span></td>
                  <td class="px-6 py-4 text-amber-400">★★★★<span v-if="(area.calificacion||0) >= 4">★</span><span v-else class="text-gray-300">★</span></td>
                  <td class="px-6 py-4 text-gray-500">—</td>
                  <td class="px-6 py-4"><a class="font-medium text-main-blue hover:underline">Ver Detalle</a></td>
                </tr>
                <tr v-if="!loading && pageData.length===0"><td class="px-6 py-4" colspan="9">Sin datos</td></tr>
                <tr v-if="loading"><td class="px-6 py-4" colspan="9">Cargando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Charts -->
        <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl border border-medium-gray p-6">
            <h3 class="text-lg font-bold mb-4">Comparativa de Indicadores (Top 5)</h3>
            <canvas id="chart-radar"></canvas>
          </div>
          <div class="bg-white rounded-xl border border-medium-gray p-6">
            <h3 class="text-lg font-bold mb-4">Distribución de Desempeño</h3>
            <canvas id="chart-histogram"></canvas>
          </div>
          <div class="bg-white rounded-xl border border-medium-gray p-6 lg:col-span-2">
            <h3 class="text-lg font-bold mb-4">Evolución de Puntajes</h3>
            <canvas id="chart-evolution"></canvas>
          </div>
        </div>
      </div>
      <!-- Modal de detalle -->
      <div id="detail-modal" class="modal" @click.self="closeModal">
        <div class="modal-content">
          <div class="p-6 border-b border-gray-200 flex items-center justify-between">
            <h2 id="modal-title" class="text-xl font-bold text-gray-900">Detalle</h2>
            <button type="button" class="text-gray-500 hover:text-gray-700" @click="closeModal">✕</button>
          </div>
          <div class="p-6 space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-600">Jefe de Área</p>
                <p id="modal-jefe" class="text-lg font-bold">-</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Capacidad</p>
                <p id="modal-capacidad" class="text-lg font-bold">-</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Carga Actual</p>
                <p id="modal-carga" class="text-lg font-bold">-</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Eficiencia</p>
                <p id="modal-eficiencia" class="text-lg font-bold">-</p>
              </div>
            </div>
            <div>
              <h3 class="font-bold mb-3">Gráfico de Evolución Mensual</h3>
              <canvas id="modal-chart-evolution" style="max-height:300px;"></canvas>
            </div>
            <div>
              <h3 class="font-bold mb-3">Personal Asignado</h3>
              <div id="modal-staff" class="space-y-2"></div>
            </div>
            <div>
              <h3 class="font-bold mb-3">Observaciones</h3>
              <p id="modal-observations" class="text-gray-700">-</p>
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
import SidebarAdmin from '@/components/SidebarAdmin.vue'
export default {
  name: 'RankingDesempeno',
  components: { SidebarAdmin },
  data() {
    return {
      loading: false,
      // backend data
      ranking: [],
      total: 0,
      // ui state
      query: '',
      page: 1,
      limit: 10,
      sortColumn: 'rank',
      sortOrder: 'asc',
      charts: {},
    }
  },
  computed: {
    maxPages() { return Math.max(1, Math.ceil(this.total / this.limit)) },
    offset() { return (this.page - 1) * this.limit },
    pageData() { return this.ranking },
  },
  watch: {
    limit() { this.page = 1; this.fetchRanking() },
    query() { this.fetchRankingDebounced() },
  },
  mounted() {
    const token = localStorage.getItem('access_token')
    if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    this.loadChartJs().then(() => this.fetchRanking())
  },
  methods: {
    async loadChartJs() {
      if (window.Chart) return
      await new Promise((resolve, reject) => {
        const s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js'; s.onload = resolve; s.onerror = reject; document.head.appendChild(s)
      })
    },
    setupEventListeners() {
      document.querySelectorAll('.sort-icon').forEach(header => {
        header.addEventListener('click', () => {
          const column = header.getAttribute('data-column')
          if (this.sortColumn === column) this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
          else { this.sortColumn = column; this.sortOrder = 'asc' }
          document.querySelectorAll('.sort-icon').forEach(h => h.classList.remove('active'))
          header.classList.add('active')
          this.ranking.sort((a, b) => {
            let av = a[column], bv = b[column]
            if (typeof av === 'string') av = av.toLowerCase(); if (typeof bv === 'string') bv = bv.toLowerCase()
            return this.sortOrder === 'asc' ? (av < bv ? -1 : 1) : (av > bv ? -1 : 1)
          })
          this.page = 1
        })
      })
    },
    fetchRankingDebounced: (()=>{ let t; return function(){ clearTimeout(t); t=setTimeout(()=>this.fetchRanking(), 300) } })(),
    async fetchRanking() {
      try {
        this.loading = true
        const params = { limit: this.limit, offset: this.offset }
        if (this.query && this.query.trim()) params.q = this.query.trim() // future backend support
        const { data } = await axios.get('/reportes/desempeno/ranking/', { params })
        this.total = data.count || 0
        // apply client-side filter by query until backend supports it
        let rows = data.results || []
        if (this.query && this.query.trim()) {
          const q = this.query.trim().toLowerCase()
          rows = rows.filter(r => (r.area||'').toLowerCase().includes(q))
        }
        this.ranking = rows
        this.renderCharts(true)
        this.setupEventListeners()
      } catch (e) {
        console.error('Error cargando ranking', e)
        this.ranking = []
      } finally {
        this.loading = false
      }
    },
    goPrev() { if (this.page > 1) { this.page--; this.fetchRanking() } },
    goNext() { if (this.page < this.maxPages) { this.page++; this.fetchRanking() } },
    rankBadge(rank){ return rank<=3 ? (rank===1?'bg-amber-100 text-amber-800': rank===2?'bg-slate-200 text-slate-800':'bg-orange-200 text-orange-800') : 'bg-gray-200 text-gray-800' },
    renderCharts(reset=false) {
      if (!window.Chart) return
      const top5 = this.ranking.slice(0, 5)
      // radar
      const radarCtx = document.getElementById('chart-radar')?.getContext('2d')
      if (this.charts.radar && reset) { this.charts.radar.destroy(); this.charts.radar = null }
      if (radarCtx && !this.charts.radar) {
        this.charts.radar = new Chart(radarCtx, {
          type: 'radar',
          data: { labels: top5.map(a => a.area), datasets: [
            { label: 'Tasa Resolución %', data: top5.map(a => a.tasa), borderColor: '#2A7DBD', backgroundColor: 'rgba(42,125,189,0.1)', tension: 0.4 },
            { label: 'Calificación (0-5)', data: top5.map(a => (a.calificacion||0) * 20), borderColor: '#0B4A72', backgroundColor: 'rgba(11,74,114,0.1)', tension: 0.4 },
          ]}, options: { responsive:true, plugins:{ legend:{ position:'bottom' } }, scales:{ r:{ beginAtZero:true, max:100 } } }
        })
      }
      // histogram
      const histCtx = document.getElementById('chart-histogram')?.getContext('2d')
      if (this.charts.histogram && reset) { this.charts.histogram.destroy(); this.charts.histogram = null }
      const dist = { Excelente: this.ranking.filter(a=>a.puntaje>=90).length, Bueno: this.ranking.filter(a=>a.puntaje>=70&&a.puntaje<90).length, Regular: this.ranking.filter(a=>a.puntaje>=50&&a.puntaje<70).length, Bajo: this.ranking.filter(a=>a.puntaje<50).length }
      if (histCtx && !this.charts.histogram) {
        this.charts.histogram = new Chart(histCtx, { type:'bar', data:{ labels:Object.keys(dist), datasets:[{ label:'Cantidad de Áreas', data:Object.values(dist), backgroundColor:['#10b981','#f59e0b','#ef4444','#dc2626'], borderRadius:4 }] }, options:{ responsive:true, plugins:{ legend:{ display:false } }, scales:{ y:{ beginAtZero:true } } } })
      }
      // evolution
      const evoCtx = document.getElementById('chart-evolution')?.getContext('2d')
      if (this.charts.evolution && reset) { this.charts.evolution.destroy(); this.charts.evolution = null }
      const months = ['Ene','Feb','Mar','Abr','May','Jun']
      if (evoCtx && !this.charts.evolution) {
        this.charts.evolution = new Chart(evoCtx, { type:'line', data:{ labels:months, datasets: top5.map((a,i)=>({ label:a.area, data:[75+i*2,76+i*2,80+i*2,85+i*2,90+i*2,a.puntaje], borderColor:['#2A7DBD','#0B4A72','#AFCFE3','#87CEEB','#4682B4'][i], fill:false, tension:0.4 })) }, options:{ responsive:true, plugins:{ legend:{ position:'bottom' } }, scales:{ y:{ beginAtZero:true, max:100 } } } })
      }
    },
    openModal(area) {
      const modal = document.getElementById('detail-modal')
      // Título con nombre de área
      document.getElementById('modal-title').textContent = `Detalle: ${area.area}`

      // Datos básicos usando la información del ranking
      // Por ahora no tenemos jefe ni capacidad desde backend, se muestra leyenda informativa
      document.getElementById('modal-jefe').textContent = 'No configurado en el sistema'

      const capacidadTexto = `${area.denuncias} denuncias atendidas en el período`
      document.getElementById('modal-capacidad').textContent = capacidadTexto

      const cargaTexto = `${area.tiempo} h promedio de atención`
      document.getElementById('modal-carga').textContent = cargaTexto

      const eficienciaTexto = `${area.tasa}% tasa de resolución`
      document.getElementById('modal-eficiencia').textContent = eficienciaTexto

      const calificacion = area.calificacion != null ? area.calificacion.toFixed(2) : 'Sin dato'
      document.getElementById('modal-observations').textContent = `Calificación promedio de ciudadanía: ${calificacion} / 5`
      if (this.charts.modalEvolution) this.charts.modalEvolution.destroy()
      const ctx = document.getElementById('modal-chart-evolution').getContext('2d')

      // Gráfico simple de evolución utilizando el puntaje total como valor final
      this.charts.modalEvolution = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
          datasets: [
            {
              label: area.area,
              data: [
                Math.max(0, area.puntaje - 20),
                Math.max(0, area.puntaje - 15),
                Math.max(0, area.puntaje - 10),
                Math.max(0, area.puntaje - 5),
                Math.max(0, area.puntaje - 2),
                area.puntaje
              ],
              borderColor: '#2A7DBD',
              backgroundColor: 'rgba(42,125,189,0.1)',
              fill: true,
              tension: 0.4
            }
          ]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, max: 100 } }
        }
      })
      modal.classList.add('active')
    },
    closeModal() {
      document.getElementById('detail-modal')?.classList.remove('active')
    }
  }
}
</script>

<style scoped>
.modal{ display:none; position:fixed; z-index:1000; left:0; top:0; width:100%; height:100%; background-color: rgba(0,0,0,0.5); animation: fadeIn .3s ease-in }
.modal.active{ display:flex; align-items:center; justify-content:center }
.modal-content{ background-color:#fff; border-radius:12px; width:90%; max-width:900px; max-height:90vh; overflow-y:auto; box-shadow:0 10px 40px rgba(0,0,0,0.2); animation: slideUp .3s ease-out }
@keyframes fadeIn{ from{opacity:0} to{opacity:1} }
@keyframes slideUp{ from{ transform: translateY(20px); opacity:0 } to{ transform: translateY(0); opacity:1 } }
.sort-icon span{ display:inline-block; width:12px; opacity:.4; font-size:12px }
.sort-icon.active span{ opacity:1 }
.progress-bar{ height:6px; background-color:#e5e7eb; border-radius:3px; overflow:hidden; margin-top:4px }
.progress-bar-fill{ height:100%; background: linear-gradient(90deg,#0B4A72,#2A7DBD); border-radius:3px; transition: width .3s ease }
.material-symbols-outlined{ font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24 }
</style>
