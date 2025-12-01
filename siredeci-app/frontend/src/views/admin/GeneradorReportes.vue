<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex h-screen w-full">
    <SidebarAdmin />

    <!-- Main content -->
    <main class="flex h-screen flex-1 flex-col overflow-hidden">
      <div class="flex-1 overflow-y-auto p-6 lg:p-8">
        <div class="max-w-7xl mx-auto">
        <!-- PageHeading -->
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <h1 class="text-4xl font-black leading-tight tracking-\[-0.033em\]">Generador de Reportes</h1>
          <button class="flex items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-gray-200 text-gray-900 text-sm font-bold leading-normal tracking-\[0.015em\] hover:bg-gray-300 transition-colors">
            <span class="material-symbols-outlined mr-2">bookmark</span>
            <span class="truncate">Mis reportes guardados</span>
          </button>
        </header>

        <!-- SegmentedButtons as a horizontal stepper -->
        <div class="mb-8">
          <div class="flex h-12 flex-1 items-center justify-center rounded-lg bg-gray-200 p-1.5">
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 bg-white shadow-[0_1px_3px_rgba(0,0,0,0.1)] text-primary text-sm font-bold leading-normal">
              <span class="truncate">1. Configuración</span>
              <input checked class="invisible w-0" name="wizard-step" type="radio" value="1" />
            </label>
            <label
              class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 text-sm font-medium leading-normal hover:text-principal-blue"
              @click.prevent="siguientePaso"
            >
              <span class="truncate">2. Selección de datos</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="2" />
            </label>
            <label
              class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 text-sm font-medium leading-normal hover:text-principal-blue"
              @click.prevent="goTo('/admin/vista-previa-reportes')"
            >
              <span class="truncate">3. Vista Previa y Generación</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="3" />
            </label>
          </div>
        </div>

        <!-- Step 1: Report Configuration -->
        <section class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-gray-200">
          <div class="space-y-10">
            <!-- Section: Información Básica -->
            <div>
              <h2 class="text-\[22px\] font-bold leading-tight tracking-\[-0.015em\] pb-4 border-b border-gray-200 mb-6">Información Básica</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="flex flex-col gap-6">
                  <label class="flex flex-col flex-1">
                    <p class="text-base font-medium leading-normal pb-2">Nombre del reporte</p>
                    <input v-model="form.nombre" class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary\/50 border border-gray-300 bg-very-light-gray h-12 placeholder:text-gray-500 p-3 text-base font-normal leading-normal" placeholder="Ej: Reporte Mensual de Quejas" />
                  </label>
                  <label class="flex flex-col flex-1">
                    <p class="text-base font-medium leading-normal pb-2">Descripción (opcional)</p>
                    <textarea v-model="form.descripcion" class="form-textarea flex w-full min-w-0 flex-1 resize-y overflow-hidden rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary\/50 border border-gray-300 bg-very-light-gray min-h-32 placeholder:text-gray-500 p-3 text-base font-normal leading-normal" placeholder="Añade una breve descripción del contenido del reporte"></textarea>
                  </label>
                </div>
                <div class="flex flex-col">
                  <p class="text-base font-medium leading-normal pb-2">Tipo de reporte</p>
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <label class="flex items-center space-x-3 p-3 rounded-lg border border-gray-300 has-\[:checked\]:border-primary has-\[:checked\]:bg-primary\/10 cursor-pointer transition-colors">
                      <input v-model="form.tipo" class="form-radio text-primary focus:ring-primary\/50" name="report-type" type="radio" value="ejecutivo"/>
                      <span>Ejecutivo</span>
                    </label>
                    <label class="flex items-center space-x-3 p-3 rounded-lg border border-gray-300 has-\[:checked\]:border-primary has-\[:checked\]:bg-primary\/10 cursor-pointer transition-colors">
                      <input v-model="form.tipo" class="form-radio text-primary focus:ring-primary\/50" name="report-type" type="radio" value="operativo"/>
                      <span>Operativo</span>
                    </label>
                    <label class="flex items-center space-x-3 p-3 rounded-lg border border-gray-300 has-\[:checked\]:border-primary has-\[:checked\]:bg-primary\/10 cursor-pointer transition-colors">
                      <input v-model="form.tipo" class="form-radio text-primary focus:ring-primary\/50" name="report-type" type="radio" value="estadistico"/>
                      <span>Estadístico</span>
                    </label>
                    <label class="flex items-center space-x-3 p-3 rounded-lg border border-gray-300 has-\[:checked\]:border-primary has-\[:checked\]:bg-primary\/10 cursor-pointer transition-colors">
                      <input v-model="form.tipo" class="form-radio text-primary focus:ring-primary\/50" name="report-type" type="radio" value="auditoria"/>
                      <span>Auditoría</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section: Periodo del Reporte -->
            <div>
              <h2 class="text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-gray-200 mb-6">Periodo del Reporte</h2>
              <div class="space-y-3">
                <div>
                  <p class="text-base font-medium leading-normal pb-2">Rango de fechas</p>
                  <div class="relative flex items-center">
                    <input
                      v-model="form.rangoFechas"
                      class="form-input w-full rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 bg-very-light-gray h-12 placeholder:text-gray-500 p-3 text-base font-normal"
                      type="text"
                      placeholder="Selecciona un rango de fechas o usa los accesos rápidos"
                    />
                    <span class="material-symbols-outlined absolute right-3 text-gray-500">calendar_today</span>
                  </div>
                </div>
                <div class="flex flex-wrap gap-2">
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-full text-xs font-medium border border-border-gray bg-white hover:bg-gray-100"
                    @click="setQuickRange('hoy')"
                  >
                    Hoy
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-full text-xs font-medium border border-border-gray bg-white hover:bg-gray-100"
                    @click="setQuickRange('ultima-semana')"
                  >
                    Últimos 7 días
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-full text-xs font-medium border border-border-gray bg-white hover:bg-gray-100"
                    @click="setQuickRange('ultimo-mes')"
                  >
                    Último mes
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-full text-xs font-medium border border-border-gray bg-white hover:bg-gray-100"
                    @click="setQuickRange('ultimo-trimestre')"
                  >
                    Último trimestre
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-full text-xs font-medium border border-border-gray bg-white hover:bg-gray-100"
                    @click="setQuickRange('ultimo-ano')"
                  >
                    Último año
                  </button>
                </div>
              </div>
            </div>

            <!-- Section: Formato de Exportación -->
            <div>
              <h2 class="text-\[22px\] font-bold leading-tight tracking-\[-0.015em\] pb-4 border-b border-gray-200 mb-6">Formato de Exportación</h2>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <label class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-colors" :class="form.formato === 'pdf' ? 'border-primary bg-primary\/10' : 'border-gray-300 hover:border-primary\/50 cursor-pointer'">
                  <input v-model="form.formato" class="sr-only" name="export-format" type="radio" value="pdf"/>
                  <span class="material-symbols-outlined text-4xl mb-2" :class="form.formato === 'pdf' ? 'text-primary' : 'text-gray-600'" style="font-size: 40px;">picture_as_pdf</span>
                  <span class="font-bold">PDF</span>
                </label>
                <label class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-colors" :class="form.formato === 'excel' ? 'border-primary bg-primary\/10' : 'border-gray-300 hover:border-primary\/50 cursor-pointer'">
                  <input v-model="form.formato" class="sr-only" name="export-format" type="radio" value="excel"/>
                  <span class="material-symbols-outlined text-4xl mb-2" :class="form.formato === 'excel' ? 'text-primary' : 'text-gray-600'" style="font-size: 40px;">table_view</span>
                  <span class="font-bold">Excel</span>
                </label>
                <label class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-colors" :class="form.formato === 'csv' ? 'border-primary bg-primary\/10' : 'border-gray-300 hover:border-primary\/50 cursor-pointer'">
                  <input v-model="form.formato" class="sr-only" name="export-format" type="radio" value="csv"/>
                  <span class="material-symbols-outlined text-4xl mb-2" :class="form.formato === 'csv' ? 'text-primary' : 'text-gray-600'" style="font-size: 40px;">description</span>
                  <span class="font-bold">CSV</span>
                </label>
                <label class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-colors" :class="form.formato === 'json' ? 'border-primary bg-primary\/10' : 'border-gray-300 hover:border-primary\/50 cursor-pointer'">
                  <input v-model="form.formato" class="sr-only" name="export-format" type="radio" value="json"/>
                  <span class="material-symbols-outlined text-4xl mb-2" :class="form.formato === 'json' ? 'text-primary' : 'text-gray-600'" style="font-size: 40px;">code</span>
                  <span class="font-bold">JSON</span>
                </label>
              </div>
            </div>
          </div>
        </section>
        </div>
      </div>
    </main>
  </div>
 </template>

<script setup>
import { computed } from 'vue'
import { isSuperAdmin, isAdmin } from '@/utils/roles'
import SidebarAdmin from '@/components/SidebarAdmin.vue'

const canAccessAdvancedReports = computed(() => isSuperAdmin() || isAdmin())
</script>

<script>
export default {
  name: 'GeneradorReportes',
  data() {
    return {
      form: {
        nombre: '',
        descripcion: '',
        tipo: 'ejecutivo',
        rangoFechas: '',
        formato: 'pdf'
      },
      quickRange: ''
    }
  },
  methods: {
    setQuickRange(range) {
      this.quickRange = range
      const today = new Date()
      let startDate = new Date()
      
      switch(range) {
        case 'hoy':
          startDate = today
          break
        case 'ultima-semana':
          startDate.setDate(today.getDate() - 7)
          break
        case 'ultimo-mes':
          startDate.setMonth(today.getMonth() - 1)
          break
        case 'ultimo-trimestre':
          startDate.setMonth(today.getMonth() - 3)
          break
        case 'ultimo-ano':
          startDate.setFullYear(today.getFullYear() - 1)
          break
      }
      
      const formatDate = (date) => {
        return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()}`
      }
      
      this.form.rangoFechas = `${formatDate(startDate)} - ${formatDate(today)}`
    },
    guardarBorrador() {
      // TODO: Implementar guardado de borrador
      console.log('Guardando borrador...', this.form)
    },
    siguientePaso() {
      try {
        const basicConfig = {
          nombre: this.form.nombre || 'Reporte sin título',
          descripcion: this.form.descripcion || '',
          tipo: this.form.tipo || 'ejecutivo',
          rangoFechas: this.form.rangoFechas || '',
          formato: this.form.formato || 'pdf'
        }

        const existingRaw = localStorage.getItem('admin_report_config')
        let existing = {}
        if (existingRaw) {
          try { existing = JSON.parse(existingRaw) } catch (e) { existing = {} }
        }

        const newConfig = {
          basic: basicConfig,
          selection: existing.selection || null,
          filters: existing.filters || null
        }
        localStorage.setItem('admin_report_config', JSON.stringify(newConfig))
      } catch (e) {
        console.error('Error guardando configuración de reporte', e)
      }

      this.$router.push('/admin/seleccion-datos-reportes').catch(() => {})
    },
    goTo(path) {
      this.$router.push(path).catch(() => {})
    }
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.5);
}

.has-\[:checked\]:border-primary {
  border-color: theme('colors.primary');
}

.has-\[:checked\]:bg-primary\/10 {
  background-color: theme('colors.primary\/10');
}

.text-primary {
  color: theme('colors.primary');
}

.bg-primary {
  background-color: theme('colors.primary');
}

.bg-primary\/10 {
  background-color: theme('colors.primary\/10');
}

.focus\:ring-primary\/50:focus {
  --tw-ring-color: theme('colors.primary\/50');
}
</style>
