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
              <p v-if="denuncia" class="text-sm text-slate-600 mt-1">
                {{ denuncia.titulo }}
              </p>
              <p v-if="error" class="text-xs text-red-600 mt-1">{{ error }}</p>
            </div>
          </div>

          <!-- Layout de dos columnas -->
          <div class="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
            <!-- Columna izquierda -->
            <div class="space-y-4">
              <!-- Alerta posible duplicado (se mostrará cuando haya lógica de duplicadas real) -->
              <div
                v-if="false"
                class="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 flex flex-col gap-2"
              >
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[20px]">warning</span>
                  <span class="font-semibold">Atención: Posible Duplicado</span>
                </div>
                <p class="text-xs">
                  Esta denuncia podría estar relacionada con otro expediente. Revise antes de proceder.
                </p>
                <button
                  class="self-start inline-flex items-center gap-1 text-xs font-semibold text-amber-900 underline hover:text-amber-950"
                >
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
                    <p>{{ denuncia?.titulo || 'Sin título' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-medium text-slate-500 uppercase">Categoría</p>
                    <p>{{ denuncia?.categoria || 'Sin categoría' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-medium text-slate-500 uppercase">Estado</p>
                    <p>{{ denuncia?.estado || 'Sin estado' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-medium text-slate-500 uppercase">Fecha de Registro</p>
                    <p>{{ formatearFecha(denuncia?.fecha_registro) }}</p>
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

              <!-- Mapa de ubicación (placeholder con dirección real si existe) -->
              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3">
                <h2 class="text-sm font-semibold text-slate-900">Ubicación</h2>
                <div class="h-24 rounded-xl bg-slate-50 border border-dashed border-slate-200 flex items-center justify-center text-slate-500 text-xs text-center px-4">
                  <div>
                    <p v-if="denuncia?.ubicacion?.direccion">{{ denuncia.ubicacion.direccion }}</p>
                    <p v-else>Mapa y ubicación pendientes de implementar</p>
                  </div>
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
                  <p>
                    <span class="font-semibold text-slate-900">{{ denuncia?.categoria || 'Sin área definida' }}</span>
                  </p>
                </div>

                <div class="space-y-1 text-xs text-slate-600 mt-3">
                  <p class="font-medium text-slate-500 uppercase">Reasignar a otra área</p>
                  <select
                    v-model="areaSeleccionada"
                    class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  >
                    <option disabled value="">Seleccionar un área...</option>
                    <!-- Nombres de áreas según AreaResponsable.nombre -->
                    <option value="Obras Públicas">Obras Públicas</option>
                    <option value="Servicios Públicos">Servicios Públicos</option>
                    <option value="Seguridad Ciudadana">Seguridad Ciudadana</option>
                    <option value="Gestión Ambiental">Gestión Ambiental</option>
                    <option value="Alumbrado Público">Alumbrado Público</option>
                    <option value="Desarrollo Urbano">Desarrollo Urbano</option>
                  </select>
                </div>

                <button
                  class="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-amber-400 text-slate-900 text-sm font-semibold shadow-sm hover:bg-amber-300 mt-3 disabled:opacity-60 disabled:cursor-not-allowed"
                  :disabled="!areaSeleccionada || loadingReasignar"
                  @click="reasignarArea"
                >
                  <span v-if="!loadingReasignar">REASIGNAR DENUNCIA</span>
                  <span v-else>Reasignando...</span>
                </button>
              </section>

              <section class="rounded-2xl bg-white border border-slate-200 px-5 py-4 space-y-3 text-sm text-slate-700">
                <div>
                  <p class="text-xs font-medium text-slate-500 uppercase mb-1">Actualizar Estado</p>
                  <select
                    v-model="estadoSeleccionado"
                    class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  >
                    <option>En proceso</option>
                    <option>Resuelta</option>
                    <option>Rechazada</option>
                    <option>Cerrada</option>
                  </select>
                  <button
                    class="mt-2 w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-sky-600 text-white text-sm font-semibold shadow-sm hover:bg-sky-500 disabled:opacity-60 disabled:cursor-not-allowed"
                    :disabled="!estadoSeleccionado || loadingEstado"
                    @click="actualizarEstado"
                  >
                    <span v-if="!loadingEstado">GUARDAR ESTADO</span>
                    <span v-else>Guardando...</span>
                  </button>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import HistorialDenuncia from '@/components/HistorialDenuncia.vue'

const route = useRoute()
const router = useRouter()

const idDenuncia = computed(() => route.params.id || '---')

const areaSeleccionada = ref('')
const denuncia = ref(null)
const eventosHistorial = ref([])
const loading = ref(false)
const error = ref(null)
const estadoSeleccionado = ref('')
const loadingEstado = ref(false)
const loadingReasignar = ref(false)

const cargarDenuncia = async () => {
  try {
    loading.value = true
    error.value = null

    const id = route.params.id
    if (!id) {
      error.value = 'No se proporcionó un ID de denuncia.'
      return
    }

    const response = await axios.get(`/denuncias/${id}/`)
    const data = response.data || {}

    denuncia.value = {
      id: data.id_denuncia,
      titulo: data.titulo,
      descripcion: data.descripcion,
      estado: data.estado,
      prioridad: data.prioridad,
      categoria: data.categoria?.nombre || data.categoria_nombre || 'Sin categoría',
      fecha_registro: data.fecha_registro,
      ubicacion: {
        direccion: data.ubicacion?.direccion || data.direccion || ''
      },
      seguimientos: data.seguimientos || []
    }

    estadoSeleccionado.value = denuncia.value.estado

    const eventos = []

    if (data.fecha_registro) {
      eventos.push({
        titulo: 'Denuncia registrada',
        fecha: data.fecha_registro,
        descripcion: 'La denuncia fue registrada en el sistema.'
      })
    }

    ;(data.seguimientos || [])
      .filter((s) => s.es_visible !== false)
      .sort((a, b) => new Date(a.fecha_hora) - new Date(b.fecha_hora))
      .forEach((s) => {
        eventos.push({
          titulo: `Cambio de estado: ${s.estado_nuevo}`,
          fecha: s.fecha_hora,
          descripcion: s.comentario || `Estado actualizado de ${s.estado_anterior || 'N/A'} a ${s.estado_nuevo}.`
        })
      })

    eventosHistorial.value = eventos
  } catch (e) {
    console.error('Error al cargar la denuncia asignada:', e)
    error.value = 'No se pudo cargar la información de la denuncia.'
  } finally {
    loading.value = false
  }
}

onMounted(cargarDenuncia)

const formatearFecha = (fechaIso) => {
  if (!fechaIso) return '-'
  const d = new Date(fechaIso)
  if (Number.isNaN(d.getTime())) return fechaIso
  return d.toLocaleString('es-PE', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const actualizarEstado = async () => {
  if (!denuncia.value || !estadoSeleccionado.value) return

  try {
    loadingEstado.value = true
    error.value = null

    await axios.patch(`/municipal/mis-denuncias/${denuncia.value.id}/cambiar-estado/`, {
      estado: estadoSeleccionado.value
    })

    // Volver a cargar la denuncia para refrescar estado e historial
    await cargarDenuncia()
  } catch (e) {
    console.error('Error al actualizar estado desde el detalle:', e)
    const backendError =
      e.response?.data?.estado?.[0] ||
      e.response?.data?.message ||
      e.response?.data?.detail ||
      'No se pudo actualizar el estado de la denuncia.'
    error.value = backendError
  } finally {
    loadingEstado.value = false
  }
}

const reasignarArea = async () => {
  if (!denuncia.value || !areaSeleccionada.value) return

  try {
    loadingReasignar.value = true
    error.value = null

    await axios.post(`/municipal/mis-denuncias/${denuncia.value.id}/reasignar-area/`, {
      area_destino: areaSeleccionada.value
    })

    // Después de reasignar, recargamos la denuncia para refrescar datos
    await cargarDenuncia()
  } catch (e) {
    console.error('Error al reasignar denuncia:', e)
    const backendError =
      e.response?.data?.message ||
      e.response?.data?.error ||
      e.response?.data?.detail ||
      'No se pudo reasignar la denuncia.'
    error.value = backendError
  } finally {
    loadingReasignar.value = false
  }
}

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
