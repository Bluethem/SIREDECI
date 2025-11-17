<template>
  <div class="font-display bg-very-light-gray text-dark-blue flex min-h-screen w-full">
    <aside class="w-64 bg-white flex flex-col border-r border-medium-gray">
      <div class="flex flex-col h-full p-4">
        <div class="flex items-center gap-3 p-2 mb-4">
          <div
            class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
            style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuBaXtYxFyHwjmkfzelKdSwckui0VVqBxvGCgbtXZGm7PLNonck59Pa-GNBQiIsq87W1Lh6EuZpvNHIl5ut6OMcMKYLyvJY29ahhMDpwOxBZPAlC0GJX4nsu6xBRTYFiYOiIbwJTgSuczE5rPIRwmep9qHnn0FoAzi8SzFgNs7b6pwFoWzm0BP_V813hr6YZomVQerH46whjBHv_QzMR-PdF8ZxV4zElToDiD0RtlSzhnMFiUQtPfDYTQ16z0SxPZYNRrHGjRBMPQV2U');"
          ></div>
          <div class="flex flex-col">
            <h1 class="text-base font-bold text-dark-blue">Plataforma de</h1>
            <p class="text-sm text-gray-500">Gestión</p>
          </div>
        </div>
        <nav class="flex flex-col gap-2">
          <a :class="navClass('/admin/dashboard')" href="#" @click.prevent="goTo('/admin/dashboard')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/dashboard') ? 'text-principal-blue' : '']">dashboard</span>
            <p class="text-sm font-medium leading-none">Dashboard</p>
          </a>
          <a :class="navClass('/admin/analisis-geografico')" href="#" @click.prevent="goTo('/admin/analisis-geografico')">
            <span class="material-symbols-outlined nofill">map</span>
            <p class="text-sm font-medium">Tendencias geograficas</p>
          </a>
          <a :class="navClass('/admin/reportes')" href="#" @click.prevent="goTo('/admin/reportes')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/reportes') ? 'text-principal-blue' : '']">bar_chart</span>
            <p class="text-sm font-medium leading-none">Reportes</p>
          </a>
          <a :class="navClass('/admin/desempeno')" href="#" @click.prevent="goTo('/admin/desempeno')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/desempeno') ? 'text-principal-blue' : '']">leaderboard</span>
            <p class="text-sm font-medium">Desempeño</p>
          </a>
          <a :class="navClass('/admin/indicadores')" href="#" @click.prevent="goTo('/admin/indicadores')">
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
export default {
  name: 'VistaPreviaReportes',
  data() {
    return {
      previewSelections: [
        'Quejas: Resumen, Por estado',
        'Rendimiento: Tiempo medio',
        'Geografía: Mapa de calor',
        'Indicadores: KPIs principales'
      ],
      summaryCards: [
        { label: 'Secciones', value: '8' },
        { label: 'Páginas (PDF)', value: '~15' },
        { label: 'Tamaño aprox.', value: '2.5 MB' }
      ],
      advancedOptions: [
        { key: 'charts', label: 'Incluir gráficos e imágenes', checked: true }
      ],
      statusSteps: [
        { label: 'Recopilando datos...', state: 'done' },
        { label: 'Procesando información...', state: 'done' },
        { label: 'Generando gráficos...', state: 'current' },
        { label: 'Exportando a PDF...', state: 'pending' }
      ],
      progressPercent: 75,
      resultActions: [
        { label: 'Descargar ahora', icon: 'download', variant: 'primary' }
      ]
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
    navClass(path) {
      return [
        'flex items-center gap-3 px-3 py-2 rounded-lg',
        this.isActive(path) ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100'
      ]
    },
    goTo(path) {
      this.$router.push(path).catch(() => {})
    },
    guardarConfiguracion() {
      console.log('Guardando configuración de vista previa...')
    },
    generarReporte() {
      console.log('Generando reporte final...')
    },
    statusTextClass(state) {
      if (state === 'done') return 'text-gray-400 dark:text-gray-500'
      if (state === 'current') return 'font-medium text-primary dark:text-primary-light'
      return 'text-gray-400 dark:text-gray-500 opacity-70'
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
