<template>
  <div class="flex h-screen overflow-hidden bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden">
      <section class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-6xl mx-auto space-y-6">
          <!-- Encabezado -->
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-[26px] font-bold text-slate-900">Dashboard del Área</h1>
            </div>
            <div class="flex items-center gap-3">
              <button
                class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-700 bg-white hover:bg-slate-50 shadow-sm"
              >
                <span class="material-symbols-outlined text-[18px] leading-none">calendar_today</span>
                <span>Últimos 30 días</span>
              </button>
            </div>
          </div>

          <!-- Tarjetas de métricas principales -->
          <div class="grid gap-4 md:grid-cols-4">
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total de Denuncias Asignadas</span>
              <span class="text-3xl font-bold text-slate-900">185</span>
            </div>

            <div class="rounded-2xl bg-[#fff4f3] border border-[#ffd0c9] px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-rose-600 uppercase tracking-wide">Denuncias Venciendo Hoy/Mañana</span>
              <span class="text-3xl font-bold text-rose-700">12</span>
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Tasa de Resolución del Área</span>
              <span class="text-3xl font-bold text-emerald-600">85%</span>
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Tiempo Promedio de Respuesta</span>
              <span class="text-3xl font-bold text-sky-600">4.5 días</span>
            </div>
          </div>

          <!-- Gráficos y carga de trabajo -->
          <div class="grid gap-4 lg:grid-cols-2">
            <div class="rounded-2xl bg-white border border-slate-200 p-6 flex flex-col gap-4 shadow-sm">
              <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-slate-900">Carga de Trabajo por Estado</h2>
              </div>
              <div class="flex flex-col items-center justify-center gap-4">
                <div class="relative flex items-center justify-center h-44 w-44">
                  <div class="absolute inset-0 rounded-full border-[12px] border-emerald-500 border-t-sky-500 border-r-amber-400 border-b-orange-500 opacity-80"></div>
                  <div class="h-24 w-24 rounded-full bg-slate-50 flex flex-col items-center justify-center">
                    <span class="text-3xl font-bold text-slate-900">185</span>
                    <span class="text-xs text-slate-500">Denuncias</span>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-x-6 gap-y-1 text-xs w-full">
                  <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 rounded-full bg-sky-500"></span>
                    <span>Nuevas (40%)</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
                    <span>En Proceso (25%)</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 rounded-full bg-orange-500"></span>
                    <span>Pend. Ciudadano (15%)</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
                    <span>Resueltas (20%)</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="rounded-2xl bg-white border border-slate-200 p-6 flex flex-col gap-4 shadow-sm">
              <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-slate-900">Flujo Operativo (Últimos 30 días)</h2>
              </div>
              <div class="flex-1 flex items-center justify-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-xl py-10">
                <span>Gráfico de líneas / barras pendiente de implementar</span>
              </div>
            </div>
          </div>

          <!-- Denuncias Pendientes Críticas -->
          <div class="rounded-2xl bg-white border border-slate-200 p-6 flex flex-col gap-4 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-sm font-semibold text-slate-900">Denuncias Pendientes Críticas</h2>
                <p class="text-xs text-slate-500 mt-0.5">Ordenadas por días abiertos, de mayor a menor.</p>
              </div>
            </div>

            <div class="overflow-hidden rounded-xl border border-slate-200">
              <table class="min-w-full divide-y divide-slate-200 text-sm">
                <thead class="bg-slate-50">
                  <tr>
                    <th class="px-4 py-2 text-left font-medium text-slate-600">ID</th>
                    <th class="px-4 py-2 text-left font-medium text-slate-600">Título / Asunto</th>
                    <th class="px-4 py-2 text-right font-medium text-slate-600">Días Abierta</th>
                    <th class="px-4 py-2 text-left font-medium text-slate-600">Estado Actual</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 bg-white">
                  <tr v-for="item in denunciasCriticas" :key="item.id" class="hover:bg-slate-50">
                    <td class="px-4 py-2 text-sky-700 font-semibold">#{{ item.id }}</td>
                    <td class="px-4 py-2 text-slate-800">{{ item.titulo }}</td>
                    <td class="px-4 py-2 text-right font-semibold" :class="item.dias >= 20 ? 'text-rose-600' : 'text-amber-600'">
                      {{ item.dias }}
                    </td>
                    <td class="px-4 py-2">
                      <span
                        class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
                        :class="estadoChipClass(item.estado)"
                      >
                        {{ item.estado }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'

const denunciasCriticas = ref([
  { id: 7834, titulo: 'Poste de luz caído en Av. Principal', dias: 22, estado: 'Nueva' },
  { id: 7855, titulo: 'Bache peligroso en calle San Martín', dias: 15, estado: 'En Proceso' },
  { id: 7861, titulo: 'Fuga de agua en Plaza Central', dias: 11, estado: 'En Proceso' },
  { id: 7800, titulo: 'Señalización en cruce peligroso', dias: 9, estado: 'Nueva' },
  { id: 7892, titulo: 'Acumulación de basura en parque infantil', dias: 7, estado: 'Nueva' }
])

const estadoChipClass = (estado) => {
  switch (estado) {
    case 'Nueva':
      return 'bg-sky-50 text-sky-700 border border-sky-200'
    case 'En Proceso':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'Resuelta':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-200'
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
}
</style>
