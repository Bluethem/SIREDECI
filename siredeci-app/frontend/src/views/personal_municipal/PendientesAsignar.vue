<template>
  <div class="flex h-screen overflow-hidden bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden">
      <section class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-6xl mx-auto space-y-6">
          <!-- Encabezado y tarjeta resumen -->
          <div class="flex items-start justify-between gap-4">
            <div>
              <h1 class="text-[26px] font-bold text-slate-900">Gestión de Denuncias Pendientes de Asignación</h1>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 px-6 py-4 flex flex-col gap-1 shadow-sm min-w-[220px]">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total Pendiente</span>
              <span class="text-2xl font-bold text-slate-900">34 Denuncias</span>
            </div>
          </div>

          <!-- Barra de búsqueda y filtros -->
          <div class="rounded-2xl bg-white border border-slate-200 px-4 py-3 flex flex-col gap-3 shadow-sm">
            <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:gap-4">
              <div class="flex-1 flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2">
                <span class="material-symbols-outlined text-[20px] text-slate-400">search</span>
                <input
                  type="text"
                  placeholder="Buscar por ID, Asunto, Dirección..."
                  class="w-full bg-transparent text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
                />
              </div>

              <div class="flex items-center gap-3">
                <button
                  class="inline-flex items-center justify-between gap-2 min-w-[180px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <span>Tipo de Denuncia</span>
                  <span class="material-symbols-outlined text-[18px] leading-none">expand_more</span>
                </button>

                <button
                  class="inline-flex items-center justify-between gap-2 min-w-[150px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <span>Antigüedad</span>
                  <span class="material-symbols-outlined text-[18px] leading-none">expand_more</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Tabla de denuncias pendientes -->
          <TablaPendientesAsignar :items="denuncias" @ver-detalle="abrirDetalle" />
        </div>
      </section>
    </main>

    <!-- Overlay de detalle de denuncia -->
    <div
      v-if="detalleAbierto && denunciaSeleccionada"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-5xl h-[90vh] flex overflow-hidden">
        <!-- Columna izquierda: detalle de denuncia -->
        <div class="flex-1 flex flex-col border-r border-slate-200 bg-slate-50">
          <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white">
            <div>
              <h2 class="text-lg font-bold text-slate-900">{{ denunciaSeleccionada.asunto }}</h2>
              <p class="text-xs text-slate-500 mt-1">ID de la Denuncia: #{{ denunciaSeleccionada.id }}</p>
            </div>
            <button
              class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-slate-100 text-slate-500"
              @click="cerrarDetalle"
            >
              <span class="material-symbols-outlined text-[20px] leading-none">close</span>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            <!-- Alerta de posible duplicado -->
            <div class="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-xs text-amber-800">
              <span class="font-semibold mr-1">POSIBLE DUPLICADO (RF-18):</span>
              Vinculada a la denuncia
              <button class="font-semibold underline hover:text-amber-900">#123123</button>.
            </div>

            <!-- Descripción del ciudadano -->
            <section class="space-y-2">
              <h3 class="text-sm font-semibold text-slate-900">Descripción del Ciudadano</h3>
              <p class="text-sm text-slate-700 leading-relaxed bg-white rounded-xl border border-slate-200 px-4 py-3">
                Hay una fuga de agua constante en la esquina de la Calle Falsa con Avenida Siempre Viva. Lleva varios
                días así y se está desperdiciando mucha agua. Además, el asfalto se está empezando a levantar y genera
                un charco grande que dificulta el paso de los peatones y vehículos. Adjunto fotos del lugar para mayor
                claridad.
              </p>
            </section>

            <!-- Evidencias adjuntas -->
            <section class="space-y-2">
              <h3 class="text-sm font-semibold text-slate-900">Evidencias Adjuntas</h3>
              <div class="grid grid-cols-3 gap-3">
                <div class="h-28 rounded-xl bg-cover bg-center bg-slate-200" style="background-image: url('https://images.pexels.com/photos/129857/pexels-photo-129857.jpeg?auto=compress&cs=tinysrgb&w=600');"></div>
                <div class="h-28 rounded-xl bg-cover bg-center bg-slate-200" style="background-image: url('https://images.pexels.com/photos/158672/broken-road-pothole-damaged-bridge-158672.jpeg?auto=compress&cs=tinysrgb&w=600');"></div>
                <div class="h-28 rounded-xl border border-slate-200 bg-white flex flex-col items-center justify-center text-xs text-slate-500 gap-1">
                  <span class="material-symbols-outlined text-[32px] text-slate-400">description</span>
                  <span>documento.pdf</span>
                </div>
              </div>
            </section>

            <!-- Ubicación de la incidencia -->
            <section class="space-y-2 pb-4">
              <h3 class="text-sm font-semibold text-slate-900">Ubicación de la Incidencia</h3>
              <div class="h-64 rounded-xl border border-slate-200 bg-slate-200 flex items-center justify-center text-slate-500 text-sm">
                300×300
              </div>
            </section>
          </div>
        </div>

        <!-- Columna derecha: panel de decisión -->
        <aside class="w-80 bg-slate-50 flex flex-col">
          <div class="px-5 py-4 border-b border-slate-200 bg-white">
            <h3 class="text-sm font-semibold text-slate-900">Panel de Decisión y Gestión</h3>
          </div>

          <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4">
            <section class="space-y-2">
              <h4 class="text-xs font-semibold text-slate-700 uppercase tracking-wide">Asignar al área responsable (RF-14)</h4>
              <select
                class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option selected>Seleccionar un área...</option>
                <option>Alumbrado Público</option>
                <option>Vialidad</option>
                <option>Seguridad</option>
              </select>
            </section>

            <button
              class="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-[#0ea5e9] text-white text-sm font-semibold shadow-sm hover:bg-[#0284c7]"
            >
              CONFIRMAR Y ASIGNAR DENUNCIA
            </button>

            <div class="border-t border-slate-200 pt-4 mt-2">
              <button
                class="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl border border-rose-300 bg-white text-sm font-semibold text-rose-600 hover:bg-rose-50"
              >
                RECHAZAR DENUNCIA
              </button>
            </div>

            <button class="mt-4 text-xs text-slate-500 underline hover:text-slate-700">
              Historial de Trazabilidad (Vacío)
            </button>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaPendientesAsignar from '@/components/TablaPendientesAsignar.vue'

const denuncias = ref([
  {
    id: 1124,
    asunto: 'Poste de luz caído',
    fecha: '2024-05-20',
    prioridad: 'alta',
    ubicacion: 'Av. Siempreviva 742',
    critica: true
  },
  {
    id: 1123,
    asunto: 'Bache peligroso en calzada',
    fecha: '2024-05-19',
    prioridad: 'alta',
    ubicacion: 'Calle Falsa 123',
    critica: true
  },
  {
    id: 1122,
    asunto: 'Ruidos molestos nocturnos',
    fecha: '2024-05-19',
    prioridad: 'media',
    ubicacion: 'Plaza Central',
    critica: false
  },
  {
    id: 1121,
    asunto: 'Acumulación de basura',
    fecha: '2024-05-18',
    prioridad: 'media',
    ubicacion: 'Esquina de Rivadavia y San Martín',
    critica: false
  }
])

const detalleAbierto = ref(false)
const denunciaSeleccionada = ref(null)

const abrirDetalle = (denuncia) => {
  denunciaSeleccionada.value = denuncia
  detalleAbierto.value = true
}

const cerrarDetalle = () => {
  detalleAbierto.value = false
  denunciaSeleccionada.value = null
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
