<template>
  <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white flex flex-col">
    <table class="min-w-full divide-y divide-slate-200 text-sm">
      <thead class="bg-slate-50">
        <tr>
          <th class="px-4 py-2 text-left font-medium text-slate-600">ID Denuncia</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Asunto/Título</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Área Responsable</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Fecha Asignación</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Prioridad</th>
          <th class="px-4 py-2 text-left font-medium text-slate-600">Estado</th>
          <th class="px-4 py-2 text-center font-medium text-slate-600">Alerta Duplicada</th>
          <th class="px-4 py-2 text-center font-medium text-slate-600">Acciones</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-200 bg-white">
        <tr
          v-for="item in itemsPaginados"
          :key="item.id"
          class="hover:bg-slate-50"
        >
          <td class="px-4 py-2 text-sky-700 font-semibold">#{{ item.id }}</td>
          <td class="px-4 py-2 text-slate-800">{{ item.asunto }}</td>
          <td class="px-4 py-2 text-slate-700">{{ item.area }}</td>
          <td class="px-4 py-2 text-slate-700">{{ item.fecha }}</td>
          <td class="px-4 py-2">
            <span
              class="inline-flex h-2.5 w-2.5 rounded-full"
              :class="prioridadColor(item.prioridad)"
            ></span>
          </td>
          <td class="px-4 py-2">
            <span
              class="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
              :class="estadoChipClass(item.estado)"
            >
              {{ item.estado }}
            </span>
          </td>
          <td class="px-4 py-2 text-center">
            <span v-if="item.duplicada" class="text-amber-500 text-lg">⚠</span>
            <span
              v-else-if="item.vinculada"
              class="text-slate-400 text-lg"
              :title="item.idDenunciaPrincipal ? `Vinculada a #${item.idDenunciaPrincipal}` : 'Denuncia vinculada'"
            >
              🔗
            </span>
          </td>
          <td class="px-4 py-2 text-center">
            <div class="inline-flex items-center gap-1">
              <button
                class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-slate-100 text-slate-500"
                @click="$emit('ver-detalle', item)"
                title="Ver detalle"
              >
                <span class="material-symbols-outlined text-[18px] leading-none">visibility</span>
              </button>
              <button
                class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-sky-50 text-sky-600 disabled:opacity-40 disabled:cursor-not-allowed"
                :disabled="item.estado === 'En proceso' || ['Resuelta', 'Rechazada', 'Cerrada'].includes(item.estado)"
                @click="$emit('cambiar-estado', { id: item.id, nuevoEstado: 'En proceso' })"
                title="Marcar en proceso"
              >
                <span class="material-symbols-outlined text-[18px] leading-none">play_arrow</span>
              </button>
              <button
                class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-emerald-50 text-emerald-600 disabled:opacity-40 disabled:cursor-not-allowed"
                :disabled="item.estado === 'Resuelta' || ['Rechazada', 'Cerrada'].includes(item.estado)"
                @click="$emit('cambiar-estado', { id: item.id, nuevoEstado: 'Resuelta' })"
                title="Marcar resuelta"
              >
                <span class="material-symbols-outlined text-[18px] leading-none">check_circle</span>
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
        <span class="font-semibold">{{ totalItems }}</span>
        denuncias
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

const emit = defineEmits(['ver-detalle', 'cambiar-estado'])

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const paginaActual = ref(1)
const tamanioPagina = ref(5)

const totalItems = computed(() => props.items.length)
const totalPaginas = computed(() => {
  return totalItems.value === 0 ? 0 : Math.ceil(totalItems.value / tamanioPagina.value)
})

const itemsPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * tamanioPagina.value
  const fin = inicio + tamanioPagina.value
  return props.items.slice(inicio, fin)
})

const rangoInicio = computed(() => {
  if (totalItems.value === 0) return 0
  return (paginaActual.value - 1) * tamanioPagina.value + 1
})

const rangoFin = computed(() => {
  if (totalItems.value === 0) return 0
  return Math.min(paginaActual.value * tamanioPagina.value, totalItems.value)
})

const irPagina = (pagina) => {
  if (pagina < 1 || pagina > totalPaginas.value) return
  paginaActual.value = pagina
}

const prioridadColor = (nivel) => {
  switch (nivel) {
    case 'alta':
      return 'bg-rose-500'
    case 'media':
      return 'bg-amber-400'
    case 'baja':
      return 'bg-emerald-400'
    default:
      return 'bg-slate-300'
  }
}

const estadoChipClass = (estado) => {
  switch (estado) {
    case 'En Proceso':
      return 'bg-sky-50 text-sky-700 border border-sky-200'
    case 'Resuelta':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    case 'Desestimada':
      return 'bg-slate-50 text-slate-600 border border-slate-200'
    case 'Pendiente Revisión':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
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
