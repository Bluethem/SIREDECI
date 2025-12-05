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
              <span class="text-2xl font-bold text-slate-900">{{ denunciasFiltradas.length }} Denuncias</span>
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
                  v-model="textoBusqueda"
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
          <TablaPendientesAsignar
            :items="denunciasFiltradas"
            @ver-detalle="abrirDetalle"
            @asignar="asignarDesdeTabla"
          />
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
              <h2 class="text-lg font-bold text-slate-900">
                {{ detalleDenuncia?.titulo || denunciaSeleccionada.asunto }}
              </h2>
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
            <!-- Descripción del ciudadano -->
            <section class="space-y-2">
              <h3 class="text-sm font-semibold text-slate-900">Descripción del Ciudadano</h3>
              <p class="text-sm text-slate-700 leading-relaxed bg-white rounded-xl border border-slate-200 px-4 py-3">
                {{ detalleDenuncia?.descripcion || 'Sin descripción disponible para esta denuncia.' }}
              </p>
            </section>

            <!-- Evidencias adjuntas -->
            <section class="space-y-2">
              <h3 class="text-sm font-semibold text-slate-900">Evidencias Adjuntas</h3>
              <div
                v-if="detalleDenuncia?.evidencias?.length"
                class="grid grid-cols-2 md:grid-cols-4 gap-3"
              >
                <div
                  v-for="ev in detalleDenuncia.evidencias"
                  :key="ev.id_evidencia"
                  class="relative group aspect-square rounded-xl overflow-hidden border border-slate-200 bg-slate-100 cursor-pointer"
                  @click="abrirEnNuevaPestana(ev)"
                >
                  <img
                    v-if="ev.ruta_almacenamiento"
                    :src="buildMediaUrl(ev.ruta_almacenamiento)"
                    :alt="ev.nombre_archivo"
                    class="w-full h-full object-cover"
                  />
                  <div
                    v-else
                    class="w-full h-full flex items-center justify-center text-slate-400 text-xs px-2 text-center"
                  >
                    {{ ev.nombre_archivo }}
                  </div>
                </div>
              </div>
              <p><span class="font-semibold">Dirección:</span> {{ detalleDenuncia?.ubicacion?.direccion || 'Sin dirección detallada' }}</p>
              <p><span class="font-semibold">Distrito:</span> {{ detalleDenuncia?.ubicacion?.distrito || 'Sin distrito' }}</p>
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
                disabled
              >
                <option>
                  Área actual: {{ denunciaSeleccionada?.ubicacion || 'Según categoría de área' }}
                </option>
              </select>
            </section>

            <button
              class="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-[#0ea5e9] text-white text-sm font-semibold shadow-sm hover:bg-[#0284c7] disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="!denunciaSeleccionada || loadingAsignar"
              @click="confirmarAsignacion"
            >
              <span v-if="!loadingAsignar">CONFIRMAR Y ASIGNAR DENUNCIA</span>
              <span v-else>Asignando...</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaPendientesAsignar from '@/components/TablaPendientesAsignar.vue'

// Base para construir URLs de evidencias (remueve el sufijo /api de la URL base)
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const MEDIA_BASE = API_BASE.replace(/\/?api\/?$/, '') + '/media/'

const buildMediaUrl = (relativePath) => {
  if (!relativePath) return ''
  return `${MEDIA_BASE}${relativePath}`
}

const abrirEnNuevaPestana = (ev) => {
  if (!ev?.ruta_almacenamiento) return
  const url = buildMediaUrl(ev.ruta_almacenamiento)
  window.open(url, '_blank')
}

const router = useRouter()

const denuncias = ref([])
const textoBusqueda = ref('')
const loadingAsignar = ref(false)
const error = ref(null)

const cargarPendientes = async () => {
  try {
    const response = await axios.get('/municipal/pendientes-asignar/')
    const data = Array.isArray(response.data) ? response.data : []

    denuncias.value = data.map((d) => ({
      id: d.id_denuncia,
      asunto: d.titulo,
      fecha: d.fecha_registro ? d.fecha_registro.slice(0, 10) : '',
      prioridad: (d.prioridad || '').toLowerCase(),
      ubicacion: d.direccion || d.distrito || 'Sin ubicación',
      critica: d.prioridad === 'Urgente' || d.prioridad === 'Alta'
    }))
  } catch (error) {
    console.error('Error al cargar denuncias pendientes de asignar:', error)
    denuncias.value = []
  }
}

onMounted(cargarPendientes)

const denunciasFiltradas = computed(() => {
  return denuncias.value.filter((d) => {
    if (!textoBusqueda.value) return true
    const q = textoBusqueda.value.toLowerCase()
    return (
      `${d.id}`.includes(q) ||
      (d.asunto || '').toLowerCase().includes(q) ||
      (d.ubicacion || '').toLowerCase().includes(q)
    )
  })
})

const detalleAbierto = ref(false)
const denunciaSeleccionada = ref(null)
const detalleDenuncia = ref(null)

const cargarDetalleDenuncia = async (id) => {
  try {
    const response = await axios.get(`/denuncias/${id}/`)
    detalleDenuncia.value = response.data
  } catch (e) {
    console.error('Error al cargar detalle de denuncia pendiente:', e)
  }
}

const abrirDetalle = async (denuncia) => {
  denunciaSeleccionada.value = denuncia
  detalleAbierto.value = true
  detalleDenuncia.value = null
  await cargarDetalleDenuncia(denuncia.id)
}

const cerrarDetalle = () => {
  detalleAbierto.value = false
  denunciaSeleccionada.value = null
  detalleDenuncia.value = null
}

const removerDeLista = (id) => {
  denuncias.value = denuncias.value.filter((d) => d.id !== id)
}

const asignarDenuncia = async (denuncia) => {
  if (!denuncia) return
  try {
    loadingAsignar.value = true
    error.value = null

    await axios.post(`/municipal/pendientes-asignar/${denuncia.id}/asignar/`)

    removerDeLista(denuncia.id)
    // Redirigir a denuncias asignadas del área
    router.push('/municipal/mi-area')
  } catch (e) {
    console.error('Error al asignar denuncia pendiente:', e)
    error.value =
      e.response?.data?.message || e.response?.data?.error || e.response?.data?.detail || 'No se pudo asignar la denuncia.'
  } finally {
    loadingAsignar.value = false
  }
}

const asignarDesdeTabla = (denuncia) => {
  asignarDenuncia(denuncia)
}

const confirmarAsignacion = () => {
  if (!denunciaSeleccionada.value) return
  asignarDenuncia(denunciaSeleccionada.value)
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
