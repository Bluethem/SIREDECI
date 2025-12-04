<template>
  <div
    v-if="open && grupo"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
  >
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-6xl h-[90vh] flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white">
        <div>
          <h2 class="text-lg font-bold text-slate-900">Gestión y Validación del Grupo de Vínculos</h2>
          <p class="text-xs text-slate-500 mt-0.5">
            ID Caso Primario:
            <span class="text-sky-600 font-semibold">ID-{{ grupo.id }}</span>
          </p>
        </div>
        <button
          class="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-slate-100 text-slate-500"
          @click="$emit('close')"
        >
          <span class="material-symbols-outlined text-[20px] leading-none">close</span>
        </button>
      </header>

      <!-- Body: 3 columns -->
      <div class="flex-1 grid gap-4 grid-cols-1 md:grid-cols-[minmax(0,2.2fr)_minmax(0,1.5fr)_minmax(0,2fr)] px-5 py-4 bg-slate-50 overflow-hidden">
        <!-- Columna 1: Denuncia original / primaria -->
        <section class="rounded-2xl bg-white border border-slate-200 flex flex-col overflow-hidden h-full">
          <header class="px-4 py-3 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <div>
              <h3 class="text-sm font-semibold text-slate-900">Denuncia Original / Primaria</h3>
              <p class="text-[11px] text-slate-500">Estado: <span class="font-semibold text-amber-600">En Análisis</span></p>
            </div>
          </header>
          <div class="flex-1 overflow-y-auto px-4 py-3 space-y-3 text-xs text-slate-700">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <p class="font-medium text-slate-500 uppercase mb-0.5">Estado</p>
                <p><span class="inline-flex rounded-full px-2 py-0.5 bg-amber-50 text-amber-700 border border-amber-200 text-[11px]">En Análisis</span></p>
              </div>
              <div>
                <p class="font-medium text-slate-500 uppercase mb-0.5">Área</p>
                <p class="text-slate-800 text-[13px]">{{ grupo.area }}</p>
              </div>
            </div>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-0.5">Descripción</p>
              <p class="text-[13px] leading-relaxed">
                {{ denunciaPrimaria?.descripcion || 'Sin descripción disponible.' }}
              </p>
            </section>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-1">Galería de Fotos</p>
              <div class="grid grid-cols-3 gap-2">
                <div class="h-16 rounded-lg bg-slate-200"></div>
                <div class="h-16 rounded-lg bg-slate-200"></div>
                <div class="h-16 rounded-lg bg-slate-200"></div>
              </div>
            </section>

            <section class="pb-2">
              <p class="font-medium text-slate-500 uppercase mb-1">Ubicación</p>
              <p class="text-[13px] text-slate-700 mb-1">
                {{ denunciaPrimaria?.ubicacion?.direccion || 'Dirección no disponible' }}
              </p>
              <p class="text-[11px] text-slate-500">
                {{ denunciaPrimaria?.ubicacion?.distrito || '' }}
              </p>
            </section>
          </div>
        </section>

        <!-- Columna 2: Denuncias vinculadas -->
        <section class="rounded-2xl bg-white border border-slate-200 flex flex-col overflow-hidden">
          <header class="px-4 py-3 border-b border-slate-200 bg-slate-50">
            <h3 class="text-sm font-semibold text-slate-900">Denuncias Vinculadas (+{{ grupo.vinculos }})</h3>
            <p class="text-[11px] text-slate-500">Seleccione una para comparar y registrar su decisión.</p>
          </header>
          <div class="flex-1 overflow-y-auto py-2">
            <button
              v-for="den in denunciasVinculadas"
              :key="den.id"
              class="w-full text-left px-4 py-2.5 text-[13px] flex flex-col gap-0.5 border-b border-slate-100 last:border-b-0"
              :class="den.id === seleccionada?.id ? 'bg-sky-50 text-sky-800' : 'bg-white hover:bg-slate-50 text-slate-800'"
              @click="seleccionar(den)"
            >
              <div class="flex items-center justify-between gap-2">
                <span class="font-semibold">ID-{{ den.id }}</span>
                <div class="flex items-center gap-1">
                  <span
                    class="inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold border"
                    :class="den.estado === 'Duplicada' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-slate-50 text-slate-700 border-slate-200'"
                  >
                    {{ den.estado }}
                  </span>
                  <span
                    v-if="decisiones[den.id] === 'confirmado'"
                    class="inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200"
                  >
                    Confirmado
                  </span>
                  <span
                    v-else-if="decisiones[den.id] === 'descartado'"
                    class="inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold bg-rose-50 text-rose-700 border border-rose-200"
                  >
                    Descartado
                  </span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500">Reportado: {{ den.hace }}</p>
            </button>
          </div>
        </section>

        <!-- Columna 3: Detalle y decisión -->
        <section class="rounded-2xl bg-white border border-slate-200 flex flex-col overflow-hidden">
          <header class="px-4 py-3 border-b border-slate-200 bg-slate-50">
            <h3 class="text-sm font-semibold text-slate-900">
              Detalle y Decisión sobre
              <span class="text-sky-600 font-semibold" v-if="seleccionada">ID-{{ seleccionada.id }}</span>
            </h3>
          </header>
          <div class="flex-1 overflow-y-auto px-4 py-3 space-y-3 text-xs text-slate-700">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <p class="font-medium text-slate-500 uppercase mb-0.5">Estado</p>
                <p>
                  <span class="inline-flex rounded-full px-2 py-0.5 bg-slate-100 text-slate-700 border border-slate-200 text-[11px]">
                    {{ seleccionada?.estado || 'Nuevo' }}
                  </span>
                </p>
              </div>
              <div>
                <p class="font-medium text-slate-500 uppercase mb-0.5">Área</p>
                <p class="text-[13px] text-slate-800">{{ seleccionada?.area || 'Tránsito' }}</p>
              </div>
            </div>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-0.5">Título</p>
              <p class="text-[13px] leading-relaxed">
                {{ seleccionada?.titulo || 'Sin título disponible.' }}
              </p>
            </section>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-0.5">Descripción</p>
              <p class="text-[13px] leading-relaxed">
                {{ seleccionada?.descripcion || 'Sin descripción disponible.' }}
              </p>
            </section>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-1">Galería de Fotos</p>
              <div class="grid grid-cols-3 gap-2">
                <div class="h-16 rounded-lg bg-slate-200"></div>
                <div class="h-16 rounded-lg bg-slate-200"></div>
                <div class="h-16 rounded-lg bg-slate-200"></div>
              </div>
            </section>

            <section>
              <p class="font-medium text-slate-500 uppercase mb-1">Nota de Justificación <span class="text-rose-500">*</span></p>
              <textarea
                rows="3"
                class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-[13px] text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
                placeholder="Obligatoria para confirmar duplicado..."
              ></textarea>
            </section>

            <section class="border-t border-amber-200 pt-3 mt-2 flex items-start gap-2 text-[11px] text-amber-700 bg-amber-50 rounded-lg px-3 py-2">
              <span class="material-symbols-outlined text-[16px] leading-none mt-0.5">warning</span>
              <p>
                Atención: Esta decisión afectará el estado de las denuncias y notificará a las áreas involucradas.
              </p>
            </section>
          </div>

          <footer class="px-4 py-3 border-t border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3">
            <button
              class="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-700 disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="!seleccionada"
              @click="descartarVinculo"
            >
              DESCARTAR VÍNCULO
            </button>
            <button
              class="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-sky-600 text-white text-xs font-semibold hover:bg-sky-700 disabled:opacity-60 disabled:cursor-not-allowed"
              :disabled="!seleccionada"
              @click="confirmarVinculo"
            >
              CONFIRMAR DUPLICADO
            </button>
          </footer>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  grupo: {
    type: Object,
    default: null
  }
})

const denunciaPrimaria = ref(null)
const denunciasVinculadas = ref([])
const seleccionada = ref(null)
const decisiones = ref({}) // id_denuncia -> 'confirmado' | 'descartado'

const cargarDetalle = async () => {
  if (!props.grupo || !props.grupo.id) {
    denunciaPrimaria.value = null
    denunciasVinculadas.value = []
    seleccionada.value = null
    return
  }

  try {
    // Detalle de denuncia primaria
    const resPrimaria = await axios.get(`/denuncias/${props.grupo.id}/`)
    denunciaPrimaria.value = resPrimaria.data || null

    const idsVinculadas = Array.isArray(props.grupo.idsVinculadas) ? props.grupo.idsVinculadas : []

    if (!idsVinculadas.length) {
      denunciasVinculadas.value = []
      seleccionada.value = null
      return
    }

    // Cargar detalles de cada denuncia vinculada
    const respuestas = await Promise.all(
      idsVinculadas.map((id) => axios.get(`/denuncias/${id}/`).catch(() => null))
    )

    const ahora = new Date()

    denunciasVinculadas.value = respuestas
      .map((res, idx) => {
        const data = res?.data
        const id = idsVinculadas[idx]
        if (!data) return null

        const fechaReg = data.fecha_registro ? new Date(data.fecha_registro) : null
        let hace = ''
        if (fechaReg && !isNaN(fechaReg.getTime())) {
          const diffMs = ahora - fechaReg
          const dias = Math.floor(diffMs / (1000 * 60 * 60 * 24))
          hace = dias === 0 ? 'Hoy' : `Hace ${dias} día(s)`
        }

        return {
          id,
          estado: data.estado,
          hace,
          titulo: data.titulo,
          descripcion: data.descripcion,
          area: data.categoria?.nombre || 'Sin categoría'
        }
      })
      .filter(Boolean)

    seleccionada.value = denunciasVinculadas.value[0] || null
  } catch (error) {
    console.error('Error al cargar detalle de denuncia duplicada:', error)
    denunciaPrimaria.value = null
    denunciasVinculadas.value = []
    seleccionada.value = null
  }
}

const seleccionar = (den) => {
  seleccionada.value = den
}

const confirmarVinculo = () => {
  if (!seleccionada.value) return
  decisiones.value = {
    ...decisiones.value,
    [seleccionada.value.id]: 'confirmado'
  }
}

const descartarVinculo = () => {
  if (!seleccionada.value) return
  decisiones.value = {
    ...decisiones.value,
    [seleccionada.value.id]: 'descartado'
  }
}

watch(
  () => props.open,
  (nuevo) => {
    if (nuevo) {
      cargarDetalle()
    }
  }
)
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
