<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex min-h-screen w-full">
    <SidebarAdmin />

    <main class="flex-1 p-6 lg:p-8 bg-background-light">
      <div class="max-w-7xl mx-auto">
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <h1 class="text-primary-dark dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Generador de Reportes</h1>
          <button class="flex items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-white dark:bg-gray-800 text-primary-dark dark:text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors border border-border-gray dark:border-gray-700 shadow-sm">
            <span class="material-symbols-outlined mr-2">bookmark</span>
            <span class="truncate">Mis reportes guardados</span>
          </button>
        </header>

        <div class="mb-8">
          <div class="flex h-12 flex-1 items-center justify-center rounded-lg bg-gray-200 dark:bg-gray-800 p-1.5">
            <label
              class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 dark:text-gray-400 text-sm font-medium leading-normal hover:text-principal-blue"
              @click.prevent="goTo('/admin/generador-reportes')"
            >
              <span class="truncate">1. Configuración</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="1" />
            </label>
            <label
              class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 dark:text-gray-400 text-sm font-medium leading-normal hover:text-principal-blue"
              @click.prevent="goTo('/admin/seleccion-datos-reportes')"
            >
              <span class="truncate">2. Selección de datos</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="2" />
            </label>
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 bg-white dark:bg-gray-900 shadow-[0_1px_3px_rgba(0,0,0,0.1)] text-primary text-sm font-bold leading-normal">
              <span class="truncate">3. Vista Previa y Generación</span>
              <input checked class="invisible w-0" name="wizard-step" type="radio" value="3" />
            </label>
          </div>
        </div>

        <section class="bg-white dark:bg-gray-900/50 p-6 sm:p-8 rounded-xl shadow-sm border border-border-gray dark:border-gray-800">
          <div class="space-y-10" id="step-3">
            <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              <div class="space-y-8 xl:col-span-2">
                <div>
                  <h2 class="text-primary-dark dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray dark:border-gray-700 mb-6">Vista Previa de Contenido</h2>
                  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-background-light dark:bg-background-dark p-4 rounded-lg">
                      <h3 class="font-bold text-primary-dark dark:text-white mb-3">Secciones seleccionadas</h3>
                      <ul class="space-y-1.5 text-sm text-gray-700 dark:text-gray-300">
                        <li v-for="item in previewSelections" :key="item" class="flex items-center">
                          <span class="material-symbols-outlined mr-2 text-primary" style="font-size: 16px;">check</span>
                          {{ item }}
                        </li>
                      </ul>
                    </div>
                    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-2 gap-4">
                      <div v-for="card in summaryCards" :key="card.label" class="bg-background-light dark:bg-background-dark p-4 rounded-lg text-center flex flex-col justify-center">
                        <p class="text-sm text-gray-500">{{ card.label }}</p>
                        <p class="text-2xl font-bold text-primary">{{ card.value }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h2 class="text-primary-dark dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray dark:border-gray-700 mb-6">Opciones Adicionales</h2>
                  <div class="space-y-4">
                    <label v-for="option in advancedOptions" :key="option.key" class="flex items-center space-x-3">
                      <input v-model="option.checked" type="checkbox" class="form-checkbox rounded text-primary focus:ring-primary/50" />
                      <span>{{ option.label }}</span>
                    </label>
                  </div>
                </div>

                <div class="mt-10 pt-6 border-t border-border-gray dark:border-gray-700 flex flex-wrap gap-3 justify-between">
                  <button class="flex items-center justify-center h-11 px-6 text-base font-bold rounded-lg bg-gray-200 dark:bg-gray-700 text-primary-dark dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors" @click="goTo('/admin/seleccion-datos-reportes')">
                    <span class="material-symbols-outlined mr-1">arrow_back</span>
                    Volver
                  </button>
                  <div class="flex flex-wrap gap-3 justify-end grow">
                    <button class="flex items-center justify-center h-11 px-6 text-base font-bold rounded-lg border border-primary text-primary hover:bg-primary/10 transition-colors" @click="guardarConfiguracion">
                      <span class="material-symbols-outlined mr-1">save</span>
                      Guardar configuración
                    </button>
                    <button class="flex-1 min-w-[180px] flex items-center justify-center h-11 px-6 text-base font-bold text-white bg-primary rounded-lg hover:bg-primary/90 transition-colors" @click="generarReporte">
                      <span class="material-symbols-outlined mr-1">analytics</span>
                      Generar reporte
                    </button>
                  </div>
                </div>
              </div>

              <div class="space-y-6 lg:row-span-2 xl:col-span-1">
                <div class="bg-background-light dark:bg-background-dark p-6 rounded-lg">
                  <h3 class="font-bold text-lg mb-4 text-primary-dark dark:text-white">Estado de Generación</h3>
                  <div class="space-y-3 text-sm">
                    <div v-for="step in statusSteps" :key="step.label" class="flex items-center gap-2" :class="statusTextClass(step.state)">
                      <template v-if="step.state === 'current'">
                        <div class="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                      </template>
                      <template v-else>
                        <span class="material-symbols-outlined" :class="step.state === 'done' ? 'text-green-500' : ''">{{ step.state === 'pending' ? 'pending' : 'check_circle' }}</span>
                      </template>
                      <span>{{ step.label }}</span>
                    </div>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-4">
                    <div class="bg-primary h-2.5 rounded-full" :style="{ width: progressPercent + '%' }"></div>
                  </div>
                  <div class="mt-6 text-center" v-if="progressPercent >= 100">
                    <span class="material-symbols-outlined text-green-500" style="font-size: 50px;">check_circle</span>
                    <p class="font-bold text-green-600 dark:text-green-400 mt-2">✓ Reporte generado exitosamente</p>
                  </div>
                </div>

                <div class="bg-background-light dark:bg-background-dark p-6 rounded-lg">
                  <h3 class="font-bold text-lg mb-4 text-primary-dark dark:text-white">Resultado Final</h3>
                  <div class="border-2 border-dashed border-border-gray dark:border-gray-700 rounded-lg h-48 flex items-center justify-center bg-white dark:bg-gray-800/50 p-4">
                    <p class="text-gray-500 dark:text-gray-400 text-sm text-center">Aquí se mostrará una vista previa del reporte en PDF.</p>
                  </div>
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
                    <button
                      v-for="action in resultActions"
                      :key="action.label"
                      class="w-full flex items-center justify-center h-10 px-4 text-sm font-bold rounded-lg transition-colors"
                      :class="action.variant === 'primary' ? 'text-white bg-primary hover:bg-primary/90' : 'border border-border-gray dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'"
                      @click="handleResultAction(action)"
                    >
                      <span class="material-symbols-outlined mr-1.5" style="font-size: 18px;">{{ action.icon }}</span>
                      {{ action.label }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'

export default {
  name: 'VistaPreviaReportes',
  components: { SidebarAdmin },
  data() {
    return {
      config: null,
      previewSelections: [],
      summaryCards: [
        { label: 'Secciones', value: '0' },
        { label: 'Páginas (PDF)', value: '~0' },
        { label: 'Tamaño aprox.', value: '—' }
      ],
      advancedOptions: [
        { key: 'charts', label: 'Incluir gráficos e imágenes', checked: true }
      ],
      statusSteps: [
        { label: 'Recopilando datos...', state: 'done' },
        { label: 'Procesando información...', state: 'done' },
        { label: 'Generando archivo...', state: 'pending' },
        { label: 'Listo para descargar', state: 'pending' }
      ],
      progressPercent: 0,
      resultActions: [
        { key: 'download', label: 'Descargar ahora', icon: 'download', variant: 'primary' }
      ],
      generatedReportCode: null,
      loadingGenerate: false
    }
  },
  created() {
    try {
      const raw = localStorage.getItem('admin_report_config')
      if (raw) {
        this.config = JSON.parse(raw)
      }
    } catch (e) {
      console.error('Error leyendo configuración de reporte', e)
      this.config = null
    }

    // Si no hay configuración básica, redirigir al primer paso del generador
    if (!this.config || !this.config.basic) {
      this.$router.replace('/admin/generador-reportes').catch(() => {})
      return
    }

    if (this.config && Array.isArray(this.config.selection)) {
      this.previewSelections = this.config.selection
    } else {
      this.previewSelections = []
    }

    const secciones = this.previewSelections.length
    this.summaryCards[0].value = String(secciones)
    this.summaryCards[1].value = secciones > 0 ? `~${Math.max(3, secciones * 2)}` : '~0'
    this.summaryCards[2].value = secciones > 0 ? '1-3 MB' : '—'

    const token = localStorage.getItem('access_token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  },
  methods: {
    isActive(path) {
      try {
        return this.$route.path.startsWith(path)
      } catch (error) {
        return false
      }
    },
    goTo(path) {
      this.$router.push(path).catch(() => {})
    },
    guardarConfiguracion() {
      console.log('Guardando configuración de vista previa...')
    },
    generarReporte() {
      if (this.loadingGenerate) return
      if (!this.config || !this.config.basic) {
        console.error('No hay configuración de reporte disponible')
        return
      }

      this.loadingGenerate = true
      this.progressPercent = 10
      this.statusSteps[2].state = 'current'

      const { basic, filters } = this.config

      // Parsear rango de fechas "DD/MM/YYYY - DD/MM/YYYY" a YYYY-MM-DD
      const parseRange = (value) => {
        if (!value || typeof value !== 'string') return { start: null, end: null }
        const parts = value.split('-')
        if (parts.length !== 2) return { start: null, end: null }
        const toIso = (s) => {
          const t = s.trim().split('/')
          if (t.length !== 3) return null
          const [dd, mm, yyyy] = t
          return `${yyyy}-${mm.padStart(2, '0')}-${dd.padStart(2, '0')}`
        }
        return { start: toIso(parts[0]), end: toIso(parts[1]) }
      }

      const { start, end } = parseRange(basic.rangoFechas || '')

      const payload = {
        nombre: basic.nombre,
        descripcion: basic.descripcion,
        tipo_reporte: basic.tipo,
        fecha_inicio: start,
        fecha_fin: end,
        formato_exportacion: basic.formato,
        parametros_configuracion: {
          secciones: this.previewSelections,
          filtros: {
            categorias: (filters && filters.categories) || [],
            estados: (filters && filters.states) || [],
            prioridades: (filters && filters.priorities) || []
          }
        }
      }

      axios
        .post('/api/reportes/reportes/generar/', payload)
        .then((response) => {
          const data = response.data || {}
          this.generatedReportCode = data.codigo_reporte || null
          this.progressPercent = 100
          this.statusSteps = [
            { label: 'Recopilando datos...', state: 'done' },
            { label: 'Procesando información...', state: 'done' },
            { label: 'Generando archivo...', state: 'done' },
            { label: 'Listo para descargar', state: 'current' }
          ]
        })
        .catch((error) => {
          console.error('Error generando reporte final', error)
          this.statusSteps = [
            { label: 'Error al generar el reporte', state: 'pending' },
            { label: 'Revisa los parámetros y vuelve a intentar', state: 'pending' },
            { label: '', state: 'pending' },
            { label: '', state: 'pending' }
          ]
          this.progressPercent = 0
        })
        .finally(() => {
          this.loadingGenerate = false
        })
    },
    statusTextClass(state) {
      if (state === 'done') return 'text-gray-400 dark:text-gray-500'
      if (state === 'current') return 'font-medium text-primary dark:text-primary-light'
      return 'text-gray-400 dark:text-gray-500 opacity-70'
    },
    async handleResultAction(action) {
      if (action.key === 'download') {
        if (!this.generatedReportCode) {
          console.warn('No hay reporte generado para descargar aún')
          return
        }
        const url = `/api/reportes/reportes/${encodeURIComponent(this.generatedReportCode)}/download/`
        // Usamos redirección simple del navegador para descarga
        window.open(url, '_blank')
      }
    }
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  font-size: 20px;
}
</style>
