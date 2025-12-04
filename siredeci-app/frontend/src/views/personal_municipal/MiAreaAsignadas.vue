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
                  v-model="textoBusqueda"
                  class="w-full bg-transparent text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
                />
              </div>

              <div class="flex items-center gap-3">
                <select
                  v-model="estadoFiltro"
                  class="inline-flex items-center justify-between gap-2 min-w-[160px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <option value="">Todos los estados</option>
                  <option
                    v-for="estado in estadosDisponibles"
                    :key="estado"
                    :value="estado"
                  >
                    {{ estado }}
                  </option>
                </select>

                <select
                  v-model="prioridadFiltro"
                  class="inline-flex items-center justify-between gap-2 min-w-[160px] px-3 py-2 rounded-xl border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50"
                >
                  <option value="">Todas las prioridades</option>
                  <option value="alta">Alta</option>
                  <option value="media">Media</option>
                  <option value="baja">Baja</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Tabla de denuncias asignadas -->
          <TablaMiAreaAsignadas
            :items="denunciasFiltradas"
            @ver-detalle="irADetalle"
            @cambiar-estado="cambiarEstadoDenuncia"
          />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaMiAreaAsignadas from '@/components/TablaMiAreaAsignadas.vue'

const router = useRouter()

const denuncias = ref([])
const textoBusqueda = ref('')
const estadoFiltro = ref('')
const prioridadFiltro = ref('')

const cargarDenuncias = async () => {
  try {
    // Denuncias asignadas al personal
    const [resMisDenuncias, resDuplicadas] = await Promise.all([
      axios.get('/municipal/mis-denuncias/'),
      axios.get('/municipal/duplicadas/')
    ])

    const data = Array.isArray(resMisDenuncias.data) ? resMisDenuncias.data : []
    const dataDuplicadas = Array.isArray(resDuplicadas.data) ? resDuplicadas.data : []

    const idsDuplicadas = new Set(dataDuplicadas.map((d) => d.id_denuncia))

    denuncias.value = data.map((d) => ({
      id: d.id_denuncia,
      asunto: d.titulo,
      area: d.categoria_nombre || 'Sin categoría',
      fecha: d.fecha_registro ? d.fecha_registro.slice(0, 10) : '',
      prioridad: (d.prioridad || '').toLowerCase(),
      estado: d.estado,
      // Marcamos duplicadas según backend
      duplicada: idsDuplicadas.has(d.id_denuncia),
      // Por ahora no tenemos modelado explícito de vinculadas; se mantiene en false
      vinculada: false
    }))
  } catch (error) {
    console.error('Error al cargar denuncias asignadas o duplicadas:', error)
    denuncias.value = []
  }
}

onMounted(cargarDenuncias)

const estadosDisponibles = computed(() => {
  const estados = new Set(denuncias.value.map((d) => d.estado).filter(Boolean))
  return Array.from(estados)
})

const denunciasFiltradas = computed(() => {
  return denuncias.value.filter((d) => {
    const matchTexto = textoBusqueda.value
      ? `${d.id} ${d.asunto}`.toLowerCase().includes(textoBusqueda.value.toLowerCase())
      : true

    const matchEstado = estadoFiltro.value ? d.estado === estadoFiltro.value : true
    const matchPrioridad = prioridadFiltro.value ? d.prioridad === prioridadFiltro.value : true

    return matchTexto && matchEstado && matchPrioridad
  })
})

const irADetalle = (denuncia) => {
  router.push(`/municipal/mi-area/${denuncia.id}`)
}

const cambiarEstadoDenuncia = async ({ id, nuevoEstado }) => {
  try {
    await axios.patch(`/municipal/mis-denuncias/${id}/cambiar-estado/`, {
      estado: nuevoEstado
    })

    denuncias.value = denuncias.value.map((d) =>
      d.id === id
        ? { ...d, estado: nuevoEstado }
        : d
    )
  } catch (error) {
    console.error('Error al cambiar estado de denuncia asignada:', error)
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
