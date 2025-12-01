<template>
  <div class="font-display bg-theme-light-gray dark:bg-background-dark text-theme-dark-blue dark:text-gray-200 flex min-h-screen w-full">
    <SidebarAdmin />

    <main class="flex-1 p-6 lg:p-8 bg-background-light">
      <div class="max-w-7xl mx-auto">
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <h1 class="text-primary-dark text-4xl font-black leading-tight tracking-[-0.033em]">Generador de Reportes</h1>
          <button class="flex items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-white text-primary-dark text-sm font-bold leading-normal tracking-[0.015em] hover:bg-gray-200 transition-colors border border-border-gray shadow-sm">
            <span class="material-symbols-outlined mr-2">bookmark</span>
            <span class="truncate">Mis reportes guardados</span>
          </button>
        </header>

        <div class="mb-8">
          <div class="flex h-12 items-center justify-center rounded-lg bg-gray-200 p-1.5">
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 text-sm font-medium" @click.prevent="goTo('/admin/generador-reportes')">
              <span class="truncate">1. Configuración</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="1" />
            </label>
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 bg-white shadow-[0_1px_3px_rgba(0,0,0,0.1)] text-primary text-sm font-bold leading-normal">
              <span class="truncate">2. Selección de datos</span>
              <input checked class="invisible w-0" name="wizard-step" type="radio" value="2" />
            </label>
            <label
              class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 text-sm font-medium hover:text-principal-blue"
              @click.prevent="goTo('/admin/vista-previa-reportes')"
            >
              <span class="truncate">3. Vista Previa y Generación</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="3" />
            </label>
          </div>
        </div>

        <main class="bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-border-gray space-y-10">
          <section>
            <h2 class="text-primary-dark text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray mb-6">Módulos a Incluir</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div v-for="section in sections" :key="section.key" class="space-y-4">
                <div class="section-header">
                  <h3 class="font-bold text-primary-dark">{{ section.title }}</h3>
                  <div class="flex items-center gap-2">
                    <span class="section-counter">{{ sectionCounters[section.key] }}</span>
                    <div class="select-all-btns">
                      <button type="button" @click="selectAll(section.key, true)">Todo</button>
                      <button type="button" @click="selectAll(section.key, false)">Ninguno</button>
                    </div>
                  </div>
                </div>
                <div class="space-y-3 pl-2 border-l-2 border-primary-light">
                  <label v-for="item in section.items" :key="item.label" class="flex items-center space-x-3">
                    <input type="checkbox" class="form-checkbox rounded text-primary focus:ring-primary/50" v-model="item.checked" />
                    <span>{{ item.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </section>

          <section>
            <h2 class="text-primary-dark text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray mb-6">Filtros Avanzados</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-2">
                <label class="font-medium text-gray-800" for="filter-categories">Categorías específicas</label>
                <select
                  id="filter-categories"
                  multiple
                  v-model="filters.categories"
                  class="form-select w-full rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray bg-very-light-gray h-32 p-3 text-base"
                >
                  <option v-for="option in filterOptions.categories" :key="option">{{ option }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-2">
                <label class="font-medium text-gray-800" for="filter-states">Estados</label>
                <select
                  id="filter-states"
                  multiple
                  v-model="filters.states"
                  class="form-select w-full rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray bg-very-light-gray h-32 p-3 text-base"
                >
                  <option v-for="option in filterOptions.states" :key="option">{{ option }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-2">
                <label class="font-medium text-gray-800" for="filter-areas">Áreas responsables</label>
                <select
                  id="filter-areas"
                  multiple
                  v-model="filters.areas"
                  class="form-select w-full rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray bg-very-light-gray h-32 p-3 text-base"
                >
                  <option v-for="option in filterOptions.areas" :key="option">{{ option }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-2">
                <label class="font-medium text-gray-800" for="filter-priorities">Prioridades</label>
                <select
                  id="filter-priorities"
                  multiple
                  v-model="filters.priorities"
                  class="form-select w-full rounded-lg text-gray-900 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray bg-very-light-gray h-32 p-3 text-base"
                >
                  <option v-for="option in filterOptions.priorities" :key="option">{{ option }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-2 md:col-span-2">
                <label class="font-medium text-gray-800">Tipo de queja</label>
                <div class="flex gap-4 flex-wrap">
                  <label class="flex items-center space-x-2">
                    <input type="radio" class="form-radio text-primary focus:ring-primary/50" value="all" v-model="filters.complaintType" />
                    <span>Todas</span>
                  </label>
                  <label class="flex items-center space-x-2">
                    <input type="radio" class="form-radio text-primary focus:ring-primary/50" value="anonymous" v-model="filters.complaintType" />
                    <span>Anónima</span>
                  </label>
                  <label class="flex items-center space-x-2">
                    <input type="radio" class="form-radio text-primary focus:ring-primary/50" value="non-anonymous" v-model="filters.complaintType" />
                    <span>No anónima</span>
                  </label>
                </div>
              </div>
            </div>
          </section>

          <section class="pt-6 border-t border-border-gray flex flex-wrap justify-between items-center gap-4">
            <button type="button" class="flex items-center justify-center rounded-lg h-11 px-6 bg-gray-200 text-primary-dark text-base font-bold hover:bg-gray-300 transition-colors" @click="goTo('/admin/generador-reportes')">
              <span class="material-symbols-outlined mr-2">arrow_back</span>
              <span class="truncate">Volver</span>
            </button>
            <button type="button" class="flex items-center justify-center rounded-lg h-11 px-6 bg-primary text-white text-base font-bold hover:bg-primary/90 transition-colors" @click="irAVistaPrevia">
              <span class="truncate">Siguiente: Vista Previa</span>
              <span class="material-symbols-outlined ml-2">arrow_forward</span>
            </button>
          </section>
        </main>

      </div>
    </main>
  </div>
</template>

<script>
import SidebarAdmin from '@/components/SidebarAdmin.vue'

export default {
  name: 'SeleccionDatosReportes',
  components: { SidebarAdmin },
  data() {
    return {
      sections: [
        {
          key: 'quejas',
          title: 'Quejas',
          items: [
            { label: 'Resumen', checked: true },
            { label: 'Por categoría', checked: false },
            { label: 'Por estado', checked: true },
            { label: 'Por prioridad', checked: false },
            { label: 'Listado detallado', checked: true },
          ],
        },
        {
          key: 'rendimiento',
          title: 'Rendimiento',
          items: [
            { label: 'Ranking de áreas', checked: false },
            { label: 'Tiempo medio de atención', checked: true },
            { label: 'Tasa de resolución', checked: false },
            { label: 'Calificaciones ciudadanas', checked: false },
          ],
        },
        {
          key: 'geografia',
          title: 'Geografía',
          items: [
            { label: 'Tendencias por zona', checked: true },
            { label: 'Mapa de calor', checked: true },
            { label: 'Quejas por distrito', checked: false },
          ],
        },
        {
          key: 'personal',
          title: 'Personal',
          items: [
            { label: 'Asignaciones por personal', checked: false },
            { label: 'Carga de trabajo', checked: false },
            { label: 'Productividad', checked: false },
          ],
        },
        {
          key: 'indicadores',
          title: 'Indicadores',
          items: [
            { label: 'KPIs principales', checked: true },
            { label: 'Métricas personalizadas', checked: false },
          ],
        },
      ],
      filterOptions: {
        categories: ['Alumbrado Público', 'Baches', 'Recolección de basura'],
        states: ['Abierto', 'En progreso', 'Resuelto', 'Cerrado'],
        areas: ['Obras Públicas', 'Servicios Urbanos', 'Seguridad Ciudadana'],
        priorities: ['Baja', 'Media', 'Alta', 'Urgente'],
      },
      filters: {
        categories: ['Alumbrado Público'],
        states: ['Abierto'],
        areas: [],
        priorities: [],
        complaintType: 'all',
      },
    }
  },
  computed: {
    sectionCounters() {
      return this.sections.reduce((acc, section) => {
        const selected = section.items.filter((item) => item.checked).length
        acc[section.key] = `${selected}/${section.items.length}`
        return acc
      }, {})
    },
  },
  methods: {
    goTo(path) {
      this.$router.push(path).catch(() => {})
    },
    selectAll(sectionKey, value) {
      const target = this.sections.find((section) => section.key === sectionKey)
      if (target) {
        target.items.forEach((item) => {
          item.checked = value
        })
      }
    },
    irAVistaPrevia() {
      try {
        const seleccion = []
        this.sections.forEach((section) => {
          section.items.forEach((item) => {
            if (item.checked) {
              seleccion.push(`${section.title}: ${item.label}`)
            }
          })
        })

        const existingRaw = localStorage.getItem('admin_report_config')
        let existing = {}
        if (existingRaw) {
          try { existing = JSON.parse(existingRaw) } catch (e) { existing = {} }
        }

        const newConfig = {
          basic: existing.basic || null,
          selection: seleccion,
          filters: {
            categories: this.filters.categories || [],
            states: this.filters.states || [],
            areas: this.filters.areas || [],
            priorities: this.filters.priorities || [],
            complaintType: this.filters.complaintType || 'all',
          },
        }

        localStorage.setItem('admin_report_config', JSON.stringify(newConfig))
      } catch (e) {
        console.error('Error guardando selección de datos para reporte', e)
      }

      this.goTo('/admin/vista-previa-reportes')
    },
  },
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  font-size: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-counter {
  background: #afcfe3;
  color: #0b4a72;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.select-all-btns {
  display: flex;
  gap: 0.5rem;
}

.select-all-btns button {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  border: 1px solid #2a7dbd;
  color: #2a7dbd;
  background: white;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.select-all-btns button:hover {
  background: #2a7dbd;
  color: white;
}
</style>
