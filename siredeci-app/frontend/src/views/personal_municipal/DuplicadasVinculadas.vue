<template>
  <div class="flex h-screen overflow-hidden bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden">
      <section class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-6xl mx-auto space-y-6">
          <!-- Encabezado y botón exportar -->
          <div class="flex flex-wrap items-center justify-between gap-3">
            <h1 class="text-[26px] font-bold text-slate-900">
              Denuncias Marcadas: Revisión de Duplicidad y Vínculos (RF-18)
            </h1>
            <button
              class="inline-flex items-center gap-2 rounded-full bg-sky-100 text-sky-700 text-xs font-semibold px-4 py-2 hover:bg-sky-200"
            >
              <span class="material-symbols-outlined text-[18px] leading-none">download</span>
              <span>Exportar Datos</span>
            </button>
          </div>

          <p class="text-xs text-slate-500">
            Gestione y resuelva grupos de denuncias potencialmente duplicadas o vinculadas.
          </p>

          <!-- Tarjetas de métricas -->
          <div class="grid gap-4 md:grid-cols-3">
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total de Grupos Pendientes de Revisión</span>
              <span class="text-3xl font-bold text-sky-600">15</span>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Grupos Resueltos (Últimos 30d)</span>
              <span class="text-3xl font-bold text-emerald-600">42</span>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Eficiencia de Detección</span>
              <span class="text-3xl font-bold text-slate-900">92%</span>
            </div>
          </div>

          <!-- Tabla de grupos duplicados/vinculados -->
          <TablaDuplicadasVinculadas
            :grupos="grupos"
            @gestionar="gestionarVinculos"
            @ver="abrirModal"
          />
        </div>
      </section>
    </main>
    <ModalGrupoVinculos :open="modalAbierto" :grupo="grupoSeleccionado" @close="cerrarModal" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaDuplicadasVinculadas from '@/components/TablaDuplicadasVinculadas.vue'
import ModalGrupoVinculos from '@/components/ModalGrupoVinculos.vue'

const grupos = ref([
  {
    id: 98765,
    vinculos: 3,
    area: 'Fiscalización, Servicios Urbanos',
    fecha: '2023-10-25',
    razon: 'Misma Dirección y Asunto'
  },
  {
    id: 98762,
    vinculos: 2,
    area: 'Obras Públicas',
    fecha: '2023-10-24',
    razon: 'Mismo Denunciante y Asunto'
  },
  {
    id: 98755,
    vinculos: 5,
    area: 'Tránsito',
    fecha: '2023-10-22',
    razon: 'Misma Zona y Tipo de Incidencia'
  },
  {
    id: 98741,
    vinculos: 2,
    area: 'Servicios Urbanos',
    fecha: '2023-10-21',
    razon: 'Misma Dirección'
  }
])

const gestionarVinculos = (grupo) => {
  // Más adelante aquí se navegará a un page de gestión de vínculos para el grupo seleccionado
  console.log('Gestionar vínculos para grupo', grupo)
}

const modalAbierto = ref(false)
const grupoSeleccionado = ref(null)

const abrirModal = (grupo) => {
  grupoSeleccionado.value = grupo
  modalAbierto.value = true
}

const cerrarModal = () => {
  modalAbierto.value = false
  grupoSeleccionado.value = null
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
