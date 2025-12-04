<template>
  <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white flex flex-col">
    <table class="min-w-full divide-y divide-slate-200 text-sm">
      <thead class="bg-slate-50">
        <tr>
          <th class="px-4 py-2 text-left font-medium text-slate-600">ID Caso Primario</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Vínculos</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Área/s Involucrada/s</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Fecha Creación</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Razón del Vínculo</th>
          <th class="px-4 py-2 text-center font-medium text-slate-600">Acciones</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-200 bg-white">
        <tr
          v-for="grupo in gruposPaginados"
          :key="grupo.id"
          class="hover:bg-slate-50"
        >
          <td class="px-4 py-2 text-sky-700 font-semibold">ID-{{ grupo.id }}</td>
          <td class="px-4 py-2 text-slate-800">+{{ grupo.vinculos }} vínculo(s)</td>
          <td class="px-4 py-2 text-slate-700">{{ grupo.area }}</td>
          <td class="px-4 py-2 text-slate-700">{{ grupo.fecha }}</td>
          <td class="px-4 py-2">
            <span
              class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200"
            >
              {{ grupo.razon }}
            </span>
          </td>
          <td class="px-4 py-2">
            <div class="flex justify-center items-center gap-1">
              <button
                class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-slate-100 text-slate-500"
                @click="$emit('ver', grupo)"
                title="Ver grupo"
              >
                <span class="material-symbols-outlined text-[18px] leading-none">visibility</span>
              </button>
              <button
                class="inline-flex items-center gap-1 rounded-full bg-sky-500 hover:bg-sky-600 text-white text-xs font-semibold px-3 py-1"
                @click="$emit('gestionar', grupo)"
                title="Revisar y gestionar vínculos de este grupo"
              >
                <span class="material-symbols-outlined text-[16px] leading-none">link</span>
                <span>Gestionar vínculos</span>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <div class="flex items-center justify-between px-4 py-2 border-t border-slate-200 bg-slate-50 text-xs text-slate-600">
      <div>
        Mostrando
        <span class="font-semibold">{{ rangoInicio }}</span>
        -
        <span class="font-semibold">{{ rangoFin }}</span>
        de
        <span class="font-semibold">{{ totalGrupos }}</span>
        grupos
      </div>
      <div class="flex items-center gap-2">
        <button
          class="inline-flex items-center px-2 py-1 rounded-lg border border-slate-200 bg-white text-xs hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="paginaActual === 1"
          @click="irPagina(paginaActual - 1)"
        >
          Anterior
        </button>
        <span class="text-slate-500">
          Página {{ paginaActual }} de {{ totalPaginas || 1 }}
        </span>
        <button
          class="inline-flex items-center px-2 py-1 rounded-lg border border-slate-200 bg-white text-xs hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="paginaActual === totalPaginas || totalPaginas === 0"
          @click="irPagina(paginaActual + 1)"
        >
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  grupos: {
    type: Array,
    default: () => []
  }
})

const paginaActual = ref(1)
const tamanioPagina = ref(5)

const totalGrupos = computed(() => props.grupos.length)
const totalPaginas = computed(() => {
  return totalGrupos.value === 0 ? 0 : Math.ceil(totalGrupos.value / tamanioPagina.value)
})

const gruposPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * tamanioPagina.value
  const fin = inicio + tamanioPagina.value
  return props.grupos.slice(inicio, fin)
})

const rangoInicio = computed(() => {
  if (totalGrupos.value === 0) return 0
  return (paginaActual.value - 1) * tamanioPagina.value + 1
})

const rangoFin = computed(() => {
  if (totalGrupos.value === 0) return 0
  return Math.min(paginaActual.value * tamanioPagina.value, totalGrupos.value)
})

const irPagina = (pagina) => {
  if (pagina < 1 || pagina > totalPaginas.value) return
  paginaActual.value = pagina
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
