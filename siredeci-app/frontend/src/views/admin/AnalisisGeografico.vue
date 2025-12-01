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

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import SidebarAdmin from '@/components/SidebarAdmin.vue'

onMounted(() => {
  // TODO: Inicializar mapa y gráficos si es necesario
})

onBeforeUnmount(() => {
  // TODO: Limpiar recursos del mapa/gráficos si se agregan
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
