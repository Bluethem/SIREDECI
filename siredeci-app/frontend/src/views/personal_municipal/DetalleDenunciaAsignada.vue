<template>
  <div class="flex h-screen overflow-hidden bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden">
      <section class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-6xl mx-auto space-y-6">
          <!-- Botón volver -->
          <button
            class="inline-flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900 mb-1"
            @click="volverALista"
          >
            <span class="material-symbols-outlined text-[18px]">arrow_back</span>
            <span>Volver a Denuncias Asignadas</span>
          </button>

          <!-- Encabezado -->
          <div class="flex items-start justify-between gap-4">
            <div>
              <h1 class="text-[26px] font-bold text-slate-900">Detalle de la Denuncia</h1>
            </div>
          </div>

          <!-- Layout de dos columnas -->
          <div class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
            <!-- Columna izquierda -->
            <div class="space-y-4">
              <!-- Alerta posible duplicado -->
              <div class="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[20px]">warning</span>
                  <span class="font-semibold">Atención: Posible Duplicado</span>
                </div>
                <p class="text-xs">
                  Esta denuncia podría estar relacionada con el expediente #54321. Revise antes de proceder.
                </p>
                <button class="self-start inline-flex items-center gap-1 text-xs font-semibold text-amber-900 underline hover:text-amber-950">
                  Ver Denuncia Original
                  <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
                </button>
              </div>

              <!-- Información del expediente -->
              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3">
                <h2 class="text-sm font-semibold text-slate-900">Información del Expediente</h2>
                <div class="grid gap-3 sm:grid-cols-2 text-sm text-slate-700">
                  <div>
                    <p class="text-xs font-medium text-slate-500 uppercase">ID de Expediente</p>
                    <p>#{{ idDenuncia }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-medium text-slate-500 uppercase">Título de la Denuncia</p>
                    <p>Poste de luz caído en la vía pública</p>
                  </div>
                </div>
              </section>

              <!-- Fotos de evidencia del ciudadano -->
              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3">
                <h2 class="text-sm font-semibold text-slate-900">Fotos de Evidencia del Ciudadano</h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div class="h-28 rounded-xl bg-slate-200"></div>
                  <div class="h-28 rounded-xl bg-slate-200"></div>
                  <div class="h-28 rounded-xl bg-slate-200"></div>
                  <div class="h-28 rounded-xl bg-slate-200"></div>
                </div>
              </section>

              <!-- Mapa de ubicación -->
              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3">
                <h2 class="text-sm font-semibold text-slate-900">Mapa de Ubicación</h2>
                <div class="h-64 rounded-xl bg-slate-200 flex items-center justify-center text-slate-500 text-sm">
                  800×400 (mapa pendiente)
                </div>
              </section>

              <!-- Historial de la Denuncia (Trazabilidad) -->
              <HistorialDenuncia class="mb-4" :eventos="eventosHistorial" />
            </div>

            <!-- Columna derecha: panel de gestión -->
            <aside class="space-y-4">
              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3">
                <h2 class="text-sm font-semibold text-slate-900">Panel de Gestión Operativa</h2>
                <div class="space-y-1 text-xs text-slate-600">
                  <p class="font-medium text-slate-500 uppercase">Área asignada actualmente</p>
                  <p><span class="font-semibold text-slate-900">Obras Públicas</span></p>
                </div>

                <div class="space-y-1 text-xs text-slate-600 mt-3">
                  <p class="font-medium text-slate-500 uppercase">Reasignar a otra área</p>
                  <select
                    v-model="areaSeleccionada"
                    class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  >
                    <option disabled value="">Seleccionar un área...</option>
                    <!-- No incluir 'Obras Públicas' para evitar reasignar a la misma área -->
                    <option value="Servicios Urbanos">Servicios Urbanos</option>
                    <option value="Fiscalización">Fiscalización</option>
                    <option value="Seguridad Ciudadana">Seguridad Ciudadana</option>
                  </select>
                </div>

                <button
                  class="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-amber-400 text-slate-900 text-sm font-semibold shadow-sm hover:bg-amber-300 mt-3 disabled:opacity-60 disabled:cursor-not-allowed"
                  :disabled="!areaSeleccionada"
                >
                  REASIGNAR DENUNCIA
                </button>
              </section>

              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3 text-sm text-slate-700">
                <div>
                  <p class="text-xs font-medium text-slate-500 uppercase mb-1">Actualizar Estado</p>
                  <select
                    class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  >
                    <option>En Proceso</option>
                    <option>Resuelta</option>
                    <option>Desestimada</option>
                    <option>Pendiente Revisión</option>
                  </select>
                </div>

                <div>
                  <p class="text-xs font-medium text-slate-500 uppercase mb-1">Evidencias Fotográficas de la Resolución</p>
                  <div
                    class="mt-1 rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-xs text-slate-500 flex flex-col items-center gap-1 text-center"
                  >
                    <span class="material-symbols-outlined text-[28px] text-slate-400">cloud_upload</span>
                    <span>Click para subir o arrastrar y soltar</span>
                    <span class="text-[11px] text-slate-400">PNG, JPG (MAX. 800x400px)</span>
                  </div>
                </div>

                <div>
                  <p class="text-xs font-medium text-slate-500 uppercase mb-1">Comunicación con el Ciudadano</p>
                  <textarea
                    rows="3"
                    class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
                    placeholder="Escriba su mensaje aquí..."
                  ></textarea>
                </div>
              </section>
            </aside>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import HistorialDenuncia from '@/components/HistorialDenuncia.vue'

const route = useRoute()
const router = useRouter()

const idDenuncia = computed(() => route.params.id || '12345')

const areaSeleccionada = ref('')

const eventosHistorial = ref([
  {
    titulo: 'Denuncia Creada',
    fecha: '10 de Julio, 2024 – 09:30 AM',
    descripcion: 'Expediente creado por el ciudadano. Asignación automática a "Mesa de Entradas".'
  },
  {
    titulo: 'Asignación a Obras Públicas',
    fecha: '10 de Julio, 2024 – 10:00 AM',
    descripcion: 'Asignado por "Ana Gómez" (Mesa de Entradas) al área "Obras Públicas".'
  },
  {
    titulo: 'Cambio de Estado: En Proceso',
    fecha: '16 de Julio, 2024 – 08:15 AM',
    descripcion: 'El estado fue actualizado por "Juan Pérez" (Jefe Obras Públicas). La cuadrilla está en camino.'
  }
])

const volverALista = () => {
  router.push('/municipal/mi-area')
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
