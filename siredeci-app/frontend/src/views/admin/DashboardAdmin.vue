<template>
  <div class="font-display bg-very-light-gray text-gray-800 flex h-screen">
    <SidebarAdmin />

    <!-- Main -->
    <main class="flex-1 flex overflow-hidden">
      <div class="flex-1 p-6 overflow-y-auto">
        <header class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="flex flex-col">
            <h1 class="text-3xl font-extrabold text-dark-blue">Dashboard Ejecutivo</h1>
            <p class="text-sm text-gray-500">Resumen operativo de denuncias</p>
          </div>
          <div class="flex flex-wrap items-center gap-4">
            <div class="flex gap-2">
              <button
                class="h-10 shrink-0 cursor-pointer items-center justify-center gap-x-2 rounded-lg px-4 text-sm font-medium"
                :class="range === 'day'
                  ? 'bg-blue-400 text-white'
                  : 'bg-white border border-medium-gray text-gray-700 hover:bg-gray-50'"
                @click="changeRange('day')"
              >
                Hoy
              </button>
              <button
                class="h-10 shrink-0 cursor-pointer items-center justify-center gap-x-2 rounded-lg px-4 text-sm font-medium"
                :class="range === 'week'
                  ? 'bg-blue-400 text-white'
                  : 'bg-white border border-medium-gray text-gray-700 hover:bg-gray-50'"
                @click="changeRange('week')"
              >
                Esta semana
              </button>
              <button
                class="h-10 shrink-0 cursor-pointer items-center justify-center gap-x-2 rounded-lg px-4 text-sm font-medium"
                :class="range === 'month'
                  ? 'bg-blue-400 text-white'
                  : 'bg-white border border-medium-gray text-gray-700 hover:bg-gray-50'"
                @click="changeRange('month')"
              >
                Este mes
              </button>
              <button
                class="h-10 shrink-0 cursor-pointer items-center justify-center gap-x-2 rounded-lg px-4 text-sm font-medium"
                :class="range === 'year'
                  ? 'bg-blue-400 text-white'
                  : 'bg-white border border-medium-gray text-gray-700 hover:bg-gray-50'"
                @click="changeRange('year')"
              >
                Este año
              </button>
              <button
                class="h-10 shrink-0 cursor-pointer items-center justify-center gap-x-2 rounded-lg bg-white px-4 border border-medium-gray hover:bg-gray-50 text-sm font-medium text-gray-700"
                @click="toggleCustomRange"
              >
                Rango personalizado
              </button>
            </div>
            <div v-if="showCustomRange" class="flex items-center gap-2 mt-1 justify-end w-full">
              <input
                type="date"
                v-model="customFrom"
                class="h-9 rounded-md border border-medium-gray px-2 text-xs text-gray-700 focus:border-principal-blue focus:ring-principal-blue"
              />
              <span class="text-xs text-gray-500">a</span>
              <input
                type="date"
                v-model="customTo"
                class="h-9 rounded-md border border-medium-gray px-2 text-xs text-gray-700 focus:border-principal-blue focus:ring-principal-blue"
              />
              <button
                class="h-9 px-3 rounded-md bg-blue-400 text-white text-xs font-semibold hover:bg-principal-blue/90"
                @click="applyCustomRange"
              >
                Aplicar
              </button>
              <button
                class="h-9 px-3 rounded-md border border-medium-gray text-xs font-medium text-gray-600 bg-white hover:bg-gray-50"
                @click="cancelCustomRange"
              >
                Cancelar
              </button>
            </div>
            <button
              class="flex items-center justify-center gap-2 overflow-hidden rounded-lg h-10 px-4 bg-blue-400 text-white text-sm font-bold leading-normal tracking-wide hover:bg-principal-blue/90"
              @click="reloadDashboard"
            >
              <span class="material-symbols-outlined text-base nofill">refresh</span>
              <span class="truncate">Actualizar datos</span>
            </button>
            <div v-if="currentUser" class="flex items-center gap-2 pl-4 border-l border-medium-gray">
              <div
                class="bg-center bg-no-repeat bg-cover rounded-full size-9 flex-shrink-0"
                :style="`background-image: url('https://ui-avatars.com/api/?name=${encodeURIComponent(currentUserName)}&background=0f5dd1&color=fff')`"
              ></div>
              <div class="flex flex-col min-w-0">
                <span class="text-sm font-semibold truncate">{{ currentUserName }}</span>
                <span class="text-xs text-gray-500 truncate">{{ currentUser?.email }}</span>
              </div>
            </div>
          </div>
        </header>

        <!-- Top Cards -->
        <section class="grid grid-cols-1 gap-6 md:grid-cols-2 mb-6">
          <div class="flex flex-col justify-between gap-2 rounded-xl p-6 bg-white border border-medium-gray">
            <p class="text-base font-medium text-gray-600">Tiempo Promedio de Atención</p>
            <div id="tiempo-card" class="flex items-baseline gap-2">
              <p id="tiempo-valor" class="text-4xl font-bold text-dark-blue" data-value="0">0</p>
              <span class="text-lg font-medium text-gray-500">horas</span>
            </div>
            <div class="flex items-center gap-1 text-green-600">
              <span class="material-symbols-outlined text-lg nofill">arrow_downward</span>
              <p class="text-sm font-medium">vs 22.0h mes anterior</p>
            </div>
            <div class="h-16 w-full mt-2">
              <svg class="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 40">
                <path d="M 0 30 L 10 25 L 20 28 L 30 20 L 40 22 L 50 15 L 60 18 L 70 10 L 80 14 L 90 8 L 100 12" fill="none" stroke="#22c55e" stroke-width="2"></path>
              </svg>
            </div>
          </div>

          <div class="flex flex-col gap-4 rounded-xl p-6 bg-white border border-medium-gray">
            <p class="text-base font-medium text-gray-600">Denuncias por Categoría</p>
            <div class="flex items-center gap-6">
              <div class="relative w-24 h-24 shrink-0">
                <svg class="w-full h-full" viewBox="0 0 36 36">
                  <circle class="stroke-current text-gray-200" cx="18" cy="18" fill="none" r="16" stroke-width="4"></circle>
                  <circle class="stroke-current text-purple-600" cx="18" cy="18" fill="none" r="16" stroke-dasharray="45, 100" stroke-dashoffset="0" stroke-width="4" transform="rotate(-90 18 18)"></circle>
                  <circle class="stroke-current text-blue-500" cx="18" cy="18" fill="none" r="16" stroke-dasharray="25, 100" stroke-dashoffset="-45" stroke-width="4" transform="rotate(-90 18 18)"></circle>
                  <circle class="stroke-current text-cyan-400" cx="18" cy="18" fill="none" r="16" stroke-dasharray="15, 100" stroke-dashoffset="-70" stroke-width="4" transform="rotate(-90 18 18)"></circle>
                  <circle class="stroke-current text-pink-500" cx="18" cy="18" fill="none" r="16" stroke-dasharray="10, 100" stroke-dashoffset="-85" stroke-width="4" transform="rotate(-90 18 18)"></circle>
                  <circle class="stroke-current text-orange-400" cx="18" cy="18" fill="none" r="16" stroke-dasharray="5, 100" stroke-dashoffset="-95" stroke-width="4" transform="rotate(-90 18 18)"></circle>
                </svg>
              </div>
              <div class="flex flex-col gap-2 text-xs w-full min-w-0">
                <div class="flex justify-between items-center">
                  <span class="flex items-center gap-2 w-2/3 min-w-0">
                    <div class="w-2.5 h-2.5 rounded-full bg-purple-600 flex-shrink-0"></div>
                    <span id="cat1-name" class="truncate min-w-0 tooltip" data-tip="" title="">-</span>
                  </span>
                  <span id="cat1-count" class="font-medium w-1/3 text-right ml-2 truncate" title="">0 (0%)</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="flex items-center gap-2 w-2/3 min-w-0">
                    <div class="w-2.5 h-2.5 rounded-full bg-blue-500 flex-shrink-0"></div>
                    <span id="cat2-name" class="truncate min-w-0 tooltip" data-tip="" title="">-</span>
                  </span>
                  <span id="cat2-count" class="font-medium w-1/3 text-right ml-2 truncate" title="">0 (0%)</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="flex items-center gap-2 w-2/3 min-w-0">
                    <div class="w-2.5 h-2.5 rounded-full bg-cyan-400 flex-shrink-0"></div>
                    <span id="cat3-name" class="truncate min-w-0 tooltip" data-tip="" title="">-</span>
                  </span>
                  <span id="cat3-count" class="font-medium w-1/3 text-right ml-2 truncate" title="">0 (0%)</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="flex items-center gap-2 w-2/3 min-w-0">
                    <div class="w-2.5 h-2.5 rounded-full bg-pink-500 flex-shrink-0"></div>
                    <span id="cat4-name" class="truncate min-w-0 tooltip" data-tip="" title="">-</span>
                  </span>
                  <span id="cat4-count" class="font-medium w-1/3 text-right ml-2 truncate" title="">0 (0%)</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="flex items-center gap-2 w-2/3 min-w-0">
                    <div class="w-2.5 h-2.5 rounded-full bg-orange-400 flex-shrink-0"></div>
                    <span id="cat5-name" class="truncate min-w-0 tooltip" data-tip="" title="">-</span>
                  </span>
                  <span id="cat5-count" class="font-medium w-1/3 text-right ml-2 truncate" title="">0 (0%)</span>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-4 rounded-xl p-6 bg-white border border-medium-gray">
            <p class="text-base font-medium text-gray-600">Tasa de Resolución</p>
            <div class="flex items-center gap-6">
              <div class="relative w-24 h-24 shrink-0">
                <svg class="w-full h-full" viewBox="0 0 36 36">
                  <path class="stroke-current text-gray-200" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke-width="3"></path>
                  <path id="tasa-arc" class="stroke-current text-principal-blue" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke-dasharray="0, 100" stroke-linecap="round" stroke-width="3"></path>
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <span id="tasa-valor" class="text-2xl font-bold text-dark-blue">0%</span>
                  <span class="text-xs text-gray-500">Meta: 85%</span>
                </div>
              </div>
              <div class="flex flex-col gap-2 text-xs w-full">
                <p class="text-green-600 font-medium text-xs">+3.5% vs mes anterior</p>
                <div><p class="font-bold text-gray-700">Resueltas: <span class="font-normal">1,140</span></p></div>
                <div><p class="font-bold text-gray-700">En proceso: <span class="font-normal">85</span></p></div>
                <div><p class="font-bold text-gray-700">Rechazadas: <span class="font-normal">15</span></p></div>
              </div>
            </div>
          </div>

          <div class="flex flex-col justify-between gap-2 rounded-xl p-6 bg-white border border-medium-gray">
            <p class="text-base font-medium text-gray-600">Total de Denuncias</p>
            <p id="total-counter" class="text-5xl font-bold text-dark-blue" data-target="0">0</p>
            <div class="text-xs space-y-1">
              <p><span id="resueltas-count" class="font-bold">0</span> Resueltas | <span id="enproceso-count" class="font-bold">0</span> En Proceso | <span id="registradas-count" class="font-bold">0</span> Registradas</p>
            </div>
            <div class="h-16 w-full mt-2">
              <div class="flex h-full w-full items-end gap-2">
                <div class="w-1/4 bg-green-500 rounded-t-sm" style="height: 40%"></div>
                <div class="w-1/4 bg-yellow-400 rounded-t-sm" style="height: 65%"></div>
                <div class="w-1/4 bg-orange-500 rounded-t-sm" style="height: 80%"></div>
                <div class="w-1/4 bg-red-600 rounded-t-sm" style="height: 90%"></div>
              </div>
              <div class="flex text-[10px] text-center text-gray-500 mt-1">
                <span class="w-1/4">Baja</span>
                <span class="w-1/4">Media</span>
                <span class="w-1/4">Alta</span>
                <span class="w-1/4">Urgente</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Charts and lists -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 flex flex-col gap-4 rounded-xl border border-medium-gray p-6 bg-white">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p class="text-lg font-semibold text-dark-blue">Evolución Temporal</p>
                <p class="text-sm text-gray-500">Denuncias registradas vs. resueltas</p>
              </div>
              <div class="flex items-center gap-2">
                <select class="rounded-lg border-medium-gray text-sm h-9">
                  <option>Filtrar por categoría</option>
                </select>
                <select class="rounded-lg border-medium-gray text-sm h-9">
                  <option>Filtrar por estado</option>
                </select>
                <div class="flex rounded-lg border border-medium-gray p-0.5 bg-gray-100 text-sm">
                  <button
                    class="px-2 py-0.5 rounded-md"
                    :class="temporalGranularity === 'day' ? 'bg-white shadow-sm' : ''"
                    @click="changeTemporalGranularity('day')"
                  >
                    Día
                  </button>
                  <button
                    class="px-2 py-0.5 rounded-md"
                    :class="temporalGranularity === 'week' ? 'bg-white shadow-sm' : ''"
                    @click="changeTemporalGranularity('week')"
                  >
                    Semana
                  </button>
                  <button
                    class="px-2 py-0.5 rounded-md"
                    :class="temporalGranularity === 'month' ? 'bg-white shadow-sm' : ''"
                    @click="changeTemporalGranularity('month')"
                  >
                    Mes
                  </button>
                </div>
              </div>
            </div>
            <div class="h-72 w-full">
              <svg height="100%" preserveAspectRatio="none" viewBox="0 0 500 200" width="100%">
                <path d="M0 150 C 40 120, 80 160, 120 140 S 200 80, 240 100 S 320 180, 360 160 S 440 100, 500 120" fill="none" stroke="#2A7DBD" stroke-width="2"></path>
                <path d="M0 180 C 40 160, 80 190, 120 170 S 200 120, 240 140 S 320 200, 360 180 S 440 130, 500 150" fill="none" stroke="#2dd4bf" stroke-width="2"></path>
                <line stroke="#D1D5DB" stroke-width="1" x1="0" x2="500" y1="195" y2="195"></line>
                <g class="text-xs fill-current text-gray-500">
                  <text id="temporal-l1" x="0" y="210">Sem 1</text>
                  <text id="temporal-l2" x="115" y="210">Sem 2</text>
                  <text id="temporal-l3" x="230" y="210">Sem 3</text>
                  <text id="temporal-l4" x="345" y="210">Sem 4</text>
                  <text id="temporal-l5" x="470" y="210">Fin</text>
                </g>
              </svg>
            </div>
          </div>

          <div class="flex flex-col gap-4 rounded-xl border border-medium-gray p-6 bg-white">
            <p class="text-lg font-semibold text-dark-blue">Distribución por Estado</p>
            <div class="flex-1 flex flex-col justify-center gap-3 text-sm">
              <div class="grid grid-cols-4 items-center gap-2">
                <p class="col-span-1 text-gray-600">Resuelta</p>
                <div class="col-span-3 w-full bg-gray-200 rounded-full h-2.5"><div class="bg-green-500 h-2.5 rounded-full" style="width: 70%"></div></div>
                <p id="resuelta-num" class="col-span-1 font-bold text-gray-800">0</p><p id="resuelta-perc" class="col-span-3 text-gray-500">0%</p>
              </div>
              <div class="grid grid-cols-4 items-center gap-2">
                <p class="col-span-1 text-gray-600">En proceso</p>
                <div class="col-span-3 w-full bg-gray-200 rounded-full h-2.5"><div class="bg-blue-500 h-2.5 rounded-full" style="width: 20%"></div></div>
                <p id="enproceso-num" class="col-span-1 font-bold text-gray-800">0</p><p id="enproceso-perc" class="col-span-3 text-gray-500">0%</p>
              </div>
              <div class="grid grid-cols-4 items-center gap-2">
                <p class="col-span-1 text-gray-600">Asignado</p>
                <div class="col-span-3 w-full bg-gray-200 rounded-full h-2.5"><div class="bg-yellow-500 h-2.5 rounded-full" style="width: 5%"></div></div>
                <p id="asignado-num" class="col-span-1 font-bold text-gray-800">0</p><p id="asignado-perc" class="col-span-3 text-gray-500">0%</p>
              </div>
              <div class="grid grid-cols-4 items-center gap-2">
                <p class="col-span-1 text-gray-600">Registrado</p>
                <div class="col-span-3 w-full bg-gray-200 rounded-full h-2.5"><div class="bg-gray-400 h-2.5 rounded-full" style="width: 3%"></div></div>
                <p id="registrado-num" class="col-span-1 font-bold text-gray-800">0</p><p id="registrado-perc" class="col-span-3 text-gray-500">0%</p>
              </div>
              <div class="grid grid-cols-4 items-center gap-2">
                <p class="col-span-1 text-gray-600">Rechazada</p>
                <div class="col-span-3 w-full bg-gray-200 rounded-full h-2.5"><div class="bg-red-500 h-2.5 rounded-full" style="width: 2%"></div></div>
                <p id="rechazada-num" class="col-span-1 font-bold text-gray-800">0</p><p id="rechazada-perc" class="col-span-3 text-gray-500">0%</p>
              </div>
            </div>
          </div>

          <div class="lg:col-span-3 flex flex-col gap-4 rounded-xl border border-medium-gray p-6 bg-white">
            <p class="text-lg font-semibold text-dark-blue">Denuncias por Prioridad</p>
            <div class="h-64 w-full flex items-end gap-2">
              <div class="w-full flex flex-col justify-end h-full bg-gray-100 rounded-t-lg">
                <div id="prio-1-baja" class="bg-green-500" style="height: 25%"></div>
                <div id="prio-1-media" class="bg-yellow-400" style="height: 40%"></div>
                <div id="prio-1-alta" class="bg-orange-500" style="height: 20%"></div>
                <div id="prio-1-urgente" class="bg-red-600" style="height: 15%"></div>
              </div>
              <div class="w-full flex flex-col justify-end h-full bg-gray-100 rounded-t-lg">
                <div id="prio-2-baja" class="bg-green-500" style="height: 30%"></div>
                <div id="prio-2-media" class="bg-yellow-400" style="height: 35%"></div>
                <div id="prio-2-alta" class="bg-orange-500" style="height: 25%"></div>
                <div id="prio-2-urgente" class="bg-red-600" style="height: 10%"></div>
              </div>
              <div class="w-full flex flex-col justify-end h-full bg-gray-100 rounded-t-lg">
                <div id="prio-3-baja" class="bg-green-500" style="height: 15%"></div>
                <div id="prio-3-media" class="bg-yellow-400" style="height: 30%"></div>
                <div id="prio-3-alta" class="bg-orange-500" style="height: 35%"></div>
                <div id="prio-3-urgente" class="bg-red-600" style="height: 20%"></div>
              </div>
              <div class="w-full flex flex-col justify-end h-full bg-gray-100 rounded-t-lg">
                <div id="prio-4-baja" class="bg-green-500" style="height: 20%"></div>
                <div id="prio-4-media" class="bg-yellow-400" style="height: 25%"></div>
                <div id="prio-4-alta" class="bg-orange-500" style="height: 30%"></div>
                <div id="prio-4-urgente" class="bg-red-600" style="height: 25%"></div>
              </div>
            </div>
            <div class="flex justify-around text-xs text-gray-500">
              <span id="prio-l1">Semana 1</span><span id="prio-l2">Semana 2</span><span id="prio-l3">Semana 3</span><span id="prio-l4">Semana 4</span>
            </div>
            <div class="flex justify-center gap-4 text-xs">
              <span class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-full bg-red-600"></div>Urgente</span>
              <span class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-full bg-orange-500"></div>Alta</span>
              <span class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-full bg-yellow-400"></div>Media</span>
              <span class="flex items-center gap-1.5"><div class="w-3 h-3 rounded-full bg-green-500"></div>Baja</span>
            </div>
          </div>
        </section>
      </div>

      <aside class="w-80 bg-white flex flex-col border-l border-medium-gray p-6 overflow-y-auto">
        <h3 class="text-lg font-semibold mb-4 text-dark-blue">Alertas y Notificaciones</h3>
        <div class="flex flex-col gap-4 mb-8">
          <div class="flex items-start gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
            <span class="material-symbols-outlined text-red-500 mt-0.5 nofill">error</span>
            <div>
              <p class="font-semibold text-sm text-red-800">Denuncias urgentes sin asignar</p>
              <p id="alert-urgentes" class="text-xs text-red-600">0 denuncias requieren asignación inmediata.</p>
            </div>
          </div>
          <div class="flex items-start gap-3 p-3 rounded-lg bg-orange-500/10 border border-orange-500/20">
            <span class="material-symbols-outlined text-orange-500 mt-0.5 nofill">warning</span>
            <div>
              <p class="font-semibold text-sm text-orange-800">Denuncias próximas a vencer SLA</p>
              <p id="alert-sla" class="text-xs text-orange-600">0 denuncias vencen en menos de 24h.</p>
            </div>
          </div>
          <div class="flex items-start gap-3 p-3 rounded-lg bg-principal-blue/10 border border-principal-blue/20">
            <span class="material-symbols-outlined text-principal-blue mt-0.5 nofill">groups</span>
            <div>
              <p class="font-semibold text-sm text-dark-blue">Áreas con sobrecarga de trabajo</p>
              <p class="text-xs text-principal-blue">Equipo de Fraudes tiene 150% de su capacidad.</p>
            </div>
          </div>
        </div>
        <h3 class="text-lg font-semibold mb-4 text-dark-blue">Estadísticas Rápidas</h3>
        <div class="flex flex-col gap-3 rounded-xl border border-medium-gray p-4">
          <div class="flex justify-between items-center text-sm">
            <p class="text-gray-600">Denuncias hoy</p>
            <p id="denuncias-hoy" class="font-bold text-lg text-dark-blue">0</p>
          </div>
          <hr class="border-medium-gray" />
          <div class="flex justify-between items-center text-sm">
            <p class="text-gray-600">Pendientes de validación</p>
            <p id="pendientes-validacion" class="font-bold text-lg text-dark-blue">0</p>
          </div>
          <hr class="border-medium-gray" />
          <div class="flex justify-between items-center text-sm">
            <p class="text-gray-600">Satisfacción promedio</p>
            <div class="flex items-center gap-1">
              <span class="material-symbols-outlined text-yellow-500 text-xl">star</span>
              <span class="material-symbols-outlined text-yellow-500 text-xl">star</span>
              <span class="material-symbols-outlined text-yellow-500 text-xl">star</span>
              <span class="material-symbols-outlined text-yellow-500 text-xl">star</span>
              <span class="material-symbols-outlined text-yellow-500 text-xl">star_half</span>
              <span id="satisfaccion" class="font-bold text-lg text-dark-blue ml-1">0.0</span>
            </div>
          </div>
        </div>
      </aside>
    </main>
  </div>
  ...
</template>

<script>
import axios from 'axios'
import SidebarAdmin from '@/components/SidebarAdmin.vue'
export default {
  name: 'DashboardAdmin',
  components: { SidebarAdmin },
  data() {
    return {
      range: 'month',
      temporalGranularity: 'week',
      showCustomRange: false,
      customFrom: '',
      customTo: ''
    }
  },
  computed: {
  },
  mounted() {
    // Animación simple de contador
    const animateCounter = (elId, duration = 1200) => {
      const el = document.getElementById(elId)
      if (!el) return
      const target = parseInt(el.getAttribute('data-target') || el.textContent.replace(/,/g, ''), 10) || 0
      const start = 0
      const startTime = performance.now()
      const frame = (now) => {
        const progress = Math.min((now - startTime) / duration, 1)
        const value = Math.floor(progress * (target - start) + start)
        el.textContent = value.toLocaleString()
        if (progress < 1) requestAnimationFrame(frame)
      }
      requestAnimationFrame(frame)
    }

    const applyTiempoColor = () => {
      const valEl = document.getElementById('tiempo-valor')
      const card = document.getElementById('tiempo-card')
      if (!valEl || !card) return
      const val = parseFloat(valEl.getAttribute('data-value') || valEl.textContent.replace(',', '.')) || 0
      valEl.classList.remove('text-green-600', 'text-yellow-600', 'text-red-600')
      card.classList.remove('border-green-200', 'border-yellow-200', 'border-red-200')
      if (val < 24) {
        valEl.classList.add('text-green-600')
        card.classList.add('border-green-200')
      } else if (val <= 48) {
        valEl.classList.add('text-yellow-600')
        card.classList.add('border-yellow-200')
      } else {
        valEl.classList.add('text-red-600')
        card.classList.add('border-red-200')
      }
    }

    const buildParams = () => {
      const params = { range: this.range }
      if (this.range === 'custom' && this.customFrom && this.customTo) {
        params.from = this.customFrom
        params.to = this.customTo
      }
      return params
    }

    const fetchSummary = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        const { data } = await axios.get('/reportes/dashboard/summary/', { params: buildParams() })

        // Total denuncias
        const totalEl = document.getElementById('total-counter')
        if (totalEl) {
          totalEl.setAttribute('data-target', String(data.total_denuncias || 0))
          animateCounter('total-counter', 800)
        }

        // Tiempo promedio de atención (horas)
        const tEl = document.getElementById('tiempo-valor')
        if (tEl) {
          const horas = (data.avg_tiempo_atencion_horas || 0).toFixed(1)
          tEl.setAttribute('data-value', String(horas))
          tEl.textContent = horas
          applyTiempoColor()
        }

        // Distribución por estado
        const estados = data.estados || {}
        const total = data.total_denuncias || 0
        const setEstado = (key, numId, percId) => {
          const num = estados[key] || 0
          const perc = total ? Math.round((num * 10000) / total) / 100 : 0
          const numEl = document.getElementById(numId)
          const percEl = document.getElementById(percId)
          if (numEl) numEl.textContent = String(num)
          if (percEl) percEl.textContent = `${perc}%`
        }
        setEstado('Resuelta', 'resuelta-num', 'resuelta-perc')
        setEstado('En proceso', 'enproceso-num', 'enproceso-perc')
        setEstado('Asignado', 'asignado-num', 'asignado-perc')
        setEstado('Registrado', 'registrado-num', 'registrado-perc')
        setEstado('Rechazada', 'rechazada-num', 'rechazada-perc')

        // Totales por estados clave en tarjeta
        const rc = document.getElementById('resueltas-count')
        const ec = document.getElementById('enproceso-count')
        const rgc = document.getElementById('registradas-count')
        if (rc) rc.textContent = String(estados['Resuelta'] || 0)
        if (ec) ec.textContent = String(estados['En proceso'] || 0)
        if (rgc) rgc.textContent = String(estados['Registrado'] || 0)

        // Satisfacción
        const satEl = document.getElementById('satisfaccion')
        if (satEl) satEl.textContent = String((data.avg_satisfaccion || 0).toFixed(1))

        // Tasa de resolución (gauge)
        const tasa = Number(data.tasa_resolucion || 0)
        const tasaVal = document.getElementById('tasa-valor')
        if (tasaVal) tasaVal.textContent = `${tasa}%`
        const tasaArc = document.getElementById('tasa-arc')
        if (tasaArc) tasaArc.setAttribute('stroke-dasharray', `${Math.max(0, Math.min(100, tasa))}, 100`)

        // Quick stats
        const hoyEl = document.getElementById('denuncias-hoy')
        if (hoyEl) hoyEl.textContent = String(data.hoy?.denuncias_hoy || 0)
        const pendEl = document.getElementById('pendientes-validacion')
        if (pendEl) pendEl.textContent = String(data.hoy?.pendientes_validacion || 0)

      } catch (e) {
        console.error('Error cargando resumen de dashboard', e)
      }
    }

    const fetchCategorias = async () => {
      try {
        const { data } = await axios.get('/reportes/dashboard/categorias/', { params: buildParams() })
        const cats = data.categorias || []
        const setCat = (idx, nombre, count, perc) => {
          const nameEl = document.getElementById(`cat${idx}-name`)
          const countEl = document.getElementById(`cat${idx}-count`)
          if (nameEl) { nameEl.textContent = nombre; nameEl.setAttribute('title', nombre); nameEl.setAttribute('data-tip', nombre) }
          if (countEl) countEl.textContent = `${count} (${perc}%)`
        }
        for (let i = 0; i < Math.min(5, cats.length); i++) {
          setCat(i + 1, cats[i].nombre, cats[i].count, cats[i].porcentaje)
        }
      } catch (e) {
        console.error('Error categorias', e)
      }
    }

    const fetchTemporal = async () => {
      try {
        const params = buildParams()
        params.granularity = this.temporalGranularity
        const { data } = await axios.get('/reportes/dashboard/temporal/', { params })
        const series = data.series || []
        const labels = series.map(s => s.label)
        ;['temporal-l1', 'temporal-l2', 'temporal-l3', 'temporal-l4', 'temporal-l5'].forEach((id, idx) => {
          const el = document.getElementById(id)
          if (el && labels[idx]) el.textContent = labels[idx]
        })
      } catch (e) {
        console.error('Error temporal', e)
      }
    }

    const fetchPrioridades = async () => {
      try {
        const { data } = await axios.get('/reportes/dashboard/prioridades/', { params: buildParams() })
        const series = data.series || []
        const setCol = (colIdx, baja, media, alta, urgente) => {
          const total = (baja + media + alta + urgente) || 1
          const setH = (id, val) => {
            const el = document.getElementById(id)
            if (el) el.style.height = `${Math.round(val * 100 / total)}%`
          }
          setH(`prio-${colIdx}-baja`, baja)
          setH(`prio-${colIdx}-media`, media)
          setH(`prio-${colIdx}-alta`, alta)
          setH(`prio-${colIdx}-urgente`, urgente)
        }
        for (let i = 0; i < Math.min(4, series.length); i++) {
          const s = series[i]
          setCol(i + 1, s.Baja || 0, s.Media || 0, s.Alta || 0, s.Urgente || 0)
          const lbl = document.getElementById(`prio-l${i + 1}`)
          if (lbl) lbl.textContent = s.label
        }
      } catch (e) {
        console.error('Error prioridades', e)
      }
    }

    const fetchAlerts = async () => {
      try {
        const { data } = await axios.get('/reportes/dashboard/alerts/', { params: buildParams() })
        const urg = document.getElementById('alert-urgentes')
        if (urg) urg.textContent = `${data.urgentes_sin_asignar || 0} denuncias requieren asignación inmediata.`
        const sla = document.getElementById('alert-sla')
        if (sla) sla.textContent = `${data.proximas_vencer_24h || 0} denuncias vencen en menos de 24h.`
      } catch (e) {
        console.error('Error alerts', e)
      }
    }

    // Carga inicial de todos los bloques del dashboard
    fetchSummary()
    fetchCategorias()
    fetchTemporal()
    fetchPrioridades()
    fetchAlerts()
  },
  methods: {
    changeRange(newRange) {
      if (this.range === newRange) return
      this.range = newRange
      this.showCustomRange = false
      // recargar todos los bloques del dashboard con el nuevo rango
      this.$options.mounted[0].call(this)
    },
    reloadDashboard() {
      // recarga completa respetando el rango y granularidad actuales
      this.$options.mounted[0].call(this)
    },
    changeTemporalGranularity(newGran) {
      if (this.temporalGranularity === newGran) return
      this.temporalGranularity = newGran
      this.$options.mounted[0].call(this)
    },
    toggleCustomRange() {
      this.showCustomRange = !this.showCustomRange
    },
    applyCustomRange() {
      if (!this.customFrom || !this.customTo) return
      this.range = 'custom'
      this.$options.mounted[0].call(this)
    },
    cancelCustomRange() {
      this.showCustomRange = false
    }
  }
}
</script>

<style scoped>
.tooltip{ position: relative; display: inline-block }
.tooltip[data-tip]:hover::after{
  position: absolute;
  left: 0;
  top: 120%;
  white-space: nowrap;
  background: rgba(17,24,39,0.95);
  color: #fff;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  z-index: 40;
  transform: translateY(4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.tooltip[data-tip]::after{ display: none }
.tooltip[data-tip]:hover::after{ display: block }
</style>
