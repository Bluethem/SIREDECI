<template>
  <div class="flex h-screen overflow-hidden bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden">
      <section class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-6xl mx-auto space-y-6">
          <!-- Encabezado -->
          <div class="flex items-start justify-between gap-4">
            <h1 class="text-[26px] font-bold text-slate-900">Denuncias Asignadas a Áreas y Monitoreo de Estado</h1>
          </div>

          <!-- Barra de búsqueda y filtros -->
          <div class="rounded-2xl bg-white border border-slate-200 px-4 py-3 flex flex-col gap-3 shadow-sm">
            <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:gap-4">
              <div class="flex-1 flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2">
                <span class="material-symbols-outlined text-[20px] text-slate-400">search</span>
                <input
                  type="text"
                  placeholder="Buscar por ID, asunto..."
                  class="w-full bg-transparent text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
                />
              </div>

              <div class="flex items-center gap-3">
                <button
                  class="inline-flex items-center justify-between gap-2 min-w-[160px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <span>Área Asignada</span>
                  <span class="material-symbols-outlined text-[18px] leading-none">expand_more</span>
                </button>

                <button
                  class="inline-flex items-center justify-between gap-2 min-w-[160px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <span>Estado Actual</span>
                  <span class="material-symbols-outlined text-[18px] leading-none">expand_more</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Tabla de denuncias asignadas -->
          <TablaMiAreaAsignadas :items="denuncias" @ver-detalle="irADetalle" />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaMiAreaAsignadas from '@/components/TablaMiAreaAsignadas.vue'

const router = useRouter()

const denuncias = ref([
  {
    id: 84521,
    asunto: 'Fuga de agua en vía pública',
    area: 'Servicios Urbanos',
    fecha: '2023-10-26',
    prioridad: 'alta',
    estado: 'En Proceso',
    duplicada: true,
    vinculada: false
  },
  {
    id: 84520,
    asunto: 'Construcción sin permiso',
    area: 'Fiscalización',
    fecha: '2023-10-25',
    prioridad: 'media',
    estado: 'Resuelta',
    duplicada: false,
    vinculada: false
  },
  {
    id: 84519,
    asunto: 'Poste de luz caído',
    area: 'Obras Públicas',
    fecha: '2023-10-25',
    prioridad: 'alta',
    estado: 'En Proceso',
    duplicada: false,
    vinculada: true
  },
  {
    id: 84518,
    asunto: 'Venta ambulante ilegal',
    area: 'Fiscalización',
    fecha: '2023-10-24',
    prioridad: 'baja',
    estado: 'Desestimada',
    duplicada: false,
    vinculada: false
  },
  {
    id: 84517,
    asunto: 'Acumulación de basura',
    area: 'Servicios Urbanos',
    fecha: '2023-10-23',
    prioridad: 'media',
    estado: 'Pendiente Revisión',
    duplicada: false,
    vinculada: false
  }
])

const irADetalle = (denuncia) => {
  router.push(`/municipal/mi-area/${denuncia.id}`)
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
