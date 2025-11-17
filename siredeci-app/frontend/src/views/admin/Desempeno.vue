<template>
  <div class="font-display bg-background-light dark:bg-background-dark text-gray-800 dark:text-gray-200 flex min-h-screen w-full">
    <!-- Sidebar identical to Dashboard -->
    <aside class="w-64 bg-white flex flex-col border-r border-medium-gray">
      <div class="flex flex-col h-full p-4">
        <div class="flex items-center gap-3 p-2 mb-4">
          <div class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" data-alt="Company logo" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBaXtYxFyHwjmkfzelKdSwckui0VVqBxvGCgbtXZGm7PLNonck59Pa-GNBQiIsq87W1Lh6EuZpvNHIl5ut6OMcMKYLyvJY29ahhMDpwOxBZPAlC0GJX4nsu6xBRTYFiYOiIbwJTgSuczE5rPIRwmep9qHnn0FoAzi8SzFgNs7b6pwFoWzm0BP_V813hr6YZomVQerH46whjBHv_QzMR-PdF8ZxV4zElToDiD0RtlSzhnMFiUQtPfDYTQ16z0SxPZYNRrHGjRBMPQV2U");'></div>
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
          <a class="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg" href="#">
            <span class="material-symbols-outlined nofill">bar_chart</span>
            <p class="text-sm font-medium leading-none">Reportes</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/desempeno') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/desempeno')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/desempeno') ? 'text-principal-blue' : '']">leaderboard</span>
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
    <main class="flex-1 p-4 sm:p-6 md:p-8 lg:p-10">
      <div class="max-w-7xl mx-auto">
        <header class="flex flex-wrap justify-between items-center gap-4 mb-8">
          <h1 class="text-primary-dark dark:text-white text-4xl font-black leading-tight tracking-[-0.033em] min-w-72">Generador de Reportes</h1>
          <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-white dark:bg-gray-800 text-primary-dark dark:text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors border border-border-gray dark:border-gray-700 shadow-sm">
            <span class="material-symbols-outlined mr-2">bookmark</span>
            <span class="truncate">Mis reportes guardados</span>
          </button>
        </header>

        <!-- Steps -->
        <div class="mb-8">
          <div class="flex h-12 flex-1 items-center justify-center rounded-lg bg-gray-200 dark:bg-gray-800 p-1.5">
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 bg-white dark:bg-gray-900 shadow-[0_1px_3px_rgba(0,0,0,0.1)] text-primary text-sm font-bold leading-normal">
              <span class="truncate">1. Configuración</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="1">
            </label>
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 dark:text-gray-400 text-sm font-medium leading-normal has-[:checked]:bg-white dark:has-[:checked]:bg-gray-900 has-[:checked]:shadow-[0_1px_3px_rgba(0,0,0,0.1)] has-[:checked]:text-primary has-[:checked]:font-bold">
              <span class="truncate">2. Selección de datos</span>
              <input checked class="invisible w-0" name="wizard-step" type="radio" value="2">
            </label>
            <label class="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-lg px-2 text-gray-500 dark:text-gray-400 text-sm font-medium leading-normal has-[:checked]:bg-white dark:has-[:checked]:bg-gray-900 has-[:checked]:shadow-[0_1px_3px_rgba(0,0,0,0.1)] has-[:checked]:text-primary has-[:checked]:font-bold">
              <span class="truncate">3. Vista Previa y Generación</span>
              <input class="invisible w-0" name="wizard-step" type="radio" value="3">
            </label>
          </div>
        </div>

        <!-- Main card -->
        <main class="bg-white dark:bg-gray-900/50 p-6 sm:p-8 rounded-xl shadow-sm border border-border-gray dark:border-gray-800">
          <!-- Step 2 content -->
          <div class="space-y-10" id="step-2">
            <!-- Modules -->
            <div>
              <h2 class="text-primary-dark dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray dark:border-gray-700 mb-6">Módulos a Incluir</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="space-y-4">
                  <div class="section-header">
                    <h3 class="font-bold text-primary-dark dark:text-white">Quejas</h3>
                    <div class="flex gap-2 items-center">
                      <span class="section-counter" data-section="quejas">0/5</span>
                      <div class="select-all-btns">
                        <button @click="selectAllInSection('quejas', true)">Todo</button>
                        <button @click="selectAllInSection('quejas', false)">Ninguno</button>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 pl-2 border-l-2 border-primary-light" data-section-group="quejas">
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="quejas" @change="updateSectionCounter('quejas')"><span>Resumen</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="quejas" @change="updateSectionCounter('quejas')"><span>Por categoría</span></label>
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="quejas" @change="updateSectionCounter('quejas')"><span>Por estado</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="quejas" @change="updateSectionCounter('quejas')"><span>Por prioridad</span></label>
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="quejas" @change="updateSectionCounter('quejas')"><span>Listado detallado</span></label>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="section-header">
                    <h3 class="font-bold text-primary-dark dark:text-white">Rendimiento</h3>
                    <div class="flex gap-2 items-center">
                      <span class="section-counter" data-section="rendimiento">0/4</span>
                      <div class="select-all-btns">
                        <button @click="selectAllInSection('rendimiento', true)">Todo</button>
                        <button @click="selectAllInSection('rendimiento', false)">Ninguno</button>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 pl-2 border-l-2 border-primary-light" data-section-group="rendimiento">
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="rendimiento" @change="updateSectionCounter('rendimiento')"><span>Ranking de áreas</span></label>
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="rendimiento" @change="updateSectionCounter('rendimiento')"><span>Tiempo medio de atención</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="rendimiento" @change="updateSectionCounter('rendimiento')"><span>Tasa de resolución</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="rendimiento" @change="updateSectionCounter('rendimiento')"><span>Calificaciones ciudadanas</span></label>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="section-header">
                    <h3 class="font-bold text-primary-dark dark:text-white">Geografía</h3>
                    <div class="flex gap-2 items-center">
                      <span class="section-counter" data-section="geografia">0/3</span>
                      <div class="select-all-btns">
                        <button @click="selectAllInSection('geografia', true)">Todo</button>
                        <button @click="selectAllInSection('geografia', false)">Ninguno</button>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 pl-2 border-l-2 border-primary-light" data-section-group="geografia">
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="geografia" @change="updateSectionCounter('geografia')"><span>Tendencias por zona</span></label>
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="geografia" @change="updateSectionCounter('geografia')"><span>Mapa de calor</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="geografia" @change="updateSectionCounter('geografia')"><span>Quejas por distrito</span></label>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="section-header">
                    <h3 class="font-bold text-primary-dark dark:text-white">Personal</h3>
                    <div class="flex gap-2 items-center">
                      <span class="section-counter" data-section="personal">0/3</span>
                      <div class="select-all-btns">
                        <button @click="selectAllInSection('personal', true)">Todo</button>
                        <button @click="selectAllInSection('personal', false)">Ninguno</button>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 pl-2 border-l-2 border-primary-light" data-section-group="personal">
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="personal" @change="updateSectionCounter('personal')"><span>Asignaciones por personal</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="personal" @change="updateSectionCounter('personal')"><span>Carga de trabajo</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="personal" @change="updateSectionCounter('personal')"><span>Productividad</span></label>
                  </div>
                </div>
                <div class="space-y-4">
                  <div class="section-header">
                    <h3 class="font-bold text-primary-dark dark:text-white">Indicadores</h3>
                    <div class="flex gap-2 items-center">
                      <span class="section-counter" data-section="indicadores">0/2</span>
                      <div class="select-all-btns">
                        <button @click="selectAllInSection('indicadores', true)">Todo</button>
                        <button @click="selectAllInSection('indicadores', false)">Ninguno</button>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-3 pl-2 border-l-2 border-primary-light" data-section-group="indicadores">
                    <label class="flex items-center space-x-3"><input checked class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="indicadores" @change="updateSectionCounter('indicadores')"><span>KPIs principales</span></label>
                    <label class="flex items-center space-x-3"><input class="form-checkbox rounded text-primary focus:ring-primary/50" type="checkbox" data-section="indicadores" @change="updateSectionCounter('indicadores')"><span>Métricas personalizadas</span></label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Filtros Avanzados (display only) -->
            <div>
              <h2 class="text-primary-dark dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] pb-4 border-b border-border-gray dark:border-gray-700 mb-6">Filtros Avanzados</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                  <label class="font-medium" for="filter-categories">Categorías específicas</label>
                  <div class="relative"><select class="form-select w-full rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray dark:border-gray-700 bg-background-light dark:bg-background-dark h-12 p-3 text-base" id="filter-categories" multiple><option>Alumbrado Público</option><option>Baches</option><option>Recolección de basura</option></select></div>
                </div>
                <div class="flex flex-col gap-2">
                  <label class="font-medium" for="filter-states">Estados</label>
                  <div class="relative"><select class="form-select w-full rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray dark:border-gray-700 bg-background-light dark:bg-background-dark h-12 p-3 text-base" id="filter-states" multiple><option>Abierto</option><option>En progreso</option><option>Resuelto</option><option>Cerrado</option></select></div>
                </div>
                <div class="flex flex-col gap-2">
                  <label class="font-medium" for="filter-areas">Áreas responsables</label>
                  <div class="relative"><select class="form-select w-full rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray dark:border-gray-700 bg-background-light dark:bg-background-dark h-12 p-3 text-base" id="filter-areas" multiple><option>Obras Públicas</option><option>Servicios Urbanos</option><option>Seguridad Ciudadana</option></select></div>
                </div>
                <div class="flex flex-col gap-2">
                  <label class="font-medium" for="filter-priorities">Prioridades</label>
                  <div class="relative"><select class="form-select w-full rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-border-gray dark:border-gray-700 bg-background-light dark:bg-background-dark h-12 p-3 text-base" id="filter-priorities" multiple><option>Baja</option><option>Media</option><option>Alta</option><option>Urgente</option></select></div>
                </div>
                <div class="flex flex-col gap-2 md:col-span-2">
                  <label class="font-medium">Tipo de queja</label>
                  <div class="flex gap-4">
                    <label class="flex items-center space-x-2"><input checked class="form-radio text-primary focus:ring-primary/50" name="complaint-type" type="radio" value="all"><span>Todas</span></label>
                    <label class="flex items-center space-x-2"><input class="form-radio text-primary focus:ring-primary/50" name="complaint-type" type="radio" value="anonymous"><span>Anónima</span></label>
                    <label class="flex items-center space-x-2"><input class="form-radio text-primary focus:ring-primary/50" name="complaint-type" type="radio" value="non-anonymous"><span>No anónima</span></label>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-10 pt-6 border-t border-border-gray dark:border-gray-700 flex flex-wrap justify-between items-center gap-4">
              <button class="flex min-w-[84px] items-center justify-center overflow-hidden rounded-lg h-11 px-6 bg-gray-200 dark:bg-gray-700 text-primary-dark dark:text-white text-base font-bold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
                <span class="material-symbols-outlined mr-2">arrow_back</span>
                <span class="truncate">Volver</span>
              </button>
              <button class="flex min-w-[84px] items-center justify-center overflow-hidden rounded-lg h-11 px-6 bg-primary text-white text-base font-bold hover:bg-primary/90 transition-colors">
                <span class="truncate">Siguiente: Vista Previa</span>
                <span class="material-symbols-outlined ml-2">arrow_forward</span>
              </button>
            </div>
          </div>

          <!-- Step 3 (placeholder) -->
          <div class="hidden space-y-10" id="step-3">
            <!-- Content omitted for brevity in this SFC -->
          </div>
        </main>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'DesempenoAdmin',
  methods: {
    isActive(path) { try { return this.$route.path.startsWith(path) } catch { return false } },
    updateSectionCounter(sectionName) {
      const checkboxes = document.querySelectorAll(`input[data-section="${sectionName}"]`)
      const checked = document.querySelectorAll(`input[data-section="${sectionName}"]:checked`).length
      const total = checkboxes.length
      const counter = document.querySelector(`.section-counter[data-section="${sectionName}"]`)
      if (counter) counter.textContent = `${checked}/${total}`
    },
    selectAllInSection(sectionName, selectAll) {
      const checkboxes = document.querySelectorAll(`input[data-section="${sectionName}"]`)
      checkboxes.forEach(cb => { cb.checked = !!selectAll })
      this.updateSectionCounter(sectionName)
    }
  },
  mounted() {
    ;['quejas','rendimiento','geografia','personal','indicadores'].forEach(s => this.updateSectionCounter(s))
  }
}
</script>

<style scoped>
.material-symbols-outlined{ font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24 }
:root{
  --primary:#2A7DBD; --primary-light:#AFCFE3; --primary-dark:#0B4A72; --border-gray:#D1D5DB;
}
.section-header{ display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem }
.section-counter{ background:#AFCFE3; color:#0B4A72; padding:0.25rem 0.75rem; border-radius:9999px; font-size:0.875rem; font-weight:600 }
.select-all-btns{ display:flex; gap:0.5rem }
.select-all-btns button{ padding:0.25rem 0.75rem; font-size:0.75rem; border:1px solid var(--primary); color:var(--primary); background:white; border-radius:0.25rem; cursor:pointer; font-weight:500; transition:all .2s }
.select-all-btns button:hover{ background:var(--primary); color:white }
</style>
