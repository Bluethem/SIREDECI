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
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Total de Denuncias Marcadas como Duplicadas</span>
              <span class="text-3xl font-bold text-sky-600">{{ grupos.length }}</span>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Grupos Resueltos (UI demo)</span>
              <span class="text-3xl font-bold text-emerald-600">-</span>
            </div>
            <div class="rounded-2xl bg-white border border-slate-200 px-5 py-4 flex flex-col gap-1 shadow-sm">
              <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Eficiencia de Detección (UI demo)</span>
              <span class="text-3xl font-bold text-slate-900">-</span>
            </div>
          </div>

          <!-- Tabla de denuncias marcadas como duplicadas -->
          <div class="rounded-2xl border border-slate-200 bg-white shadow-sm" v-if="grupos.length">
            <TablaDuplicadasVinculadas
              :grupos="grupos"
              @gestionar="gestionarVinculos"
              @ver="abrirModal"
            />
          </div>
          <div
            v-else
            class="rounded-2xl border border-dashed border-slate-300 bg-slate-50 py-10 flex flex-col items-center justify-center text-xs text-slate-500 gap-2"
          >
            <span class="material-symbols-outlined text-[32px] text-slate-300">link_off</span>
            <p class="max-w-md text-center">
              Por el momento no se han detectado denuncias marcadas como duplicadas o vinculadas en tu área.
            </p>
          </div>
        </div>
      </section>
    </main>
    <ModalGrupoVinculos :open="modalAbierto" :grupo="grupoSeleccionado" @close="cerrarModal" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'
import TablaDuplicadasVinculadas from '@/components/TablaDuplicadasVinculadas.vue'
import ModalGrupoVinculos from '@/components/ModalGrupoVinculos.vue'

const grupos = ref([])

const cargarGruposDuplicadasVinculadas = async () => {
  try {
    // Relaciones de vinculadas y listado de denuncias del área
    const [resVinculadas, resDenunciasArea] = await Promise.all([
      axios.get('/municipal/vinculadas/'),
      axios.get('/municipal/mi-area/denuncias/')
    ])

    const dataVinculadas = Array.isArray(resVinculadas.data) ? resVinculadas.data : []
    const dataArea = Array.isArray(resDenunciasArea.data) ? resDenunciasArea.data : []

    // Mapa rápido id_denuncia -> info básica para área/fecha
    const mapaDenuncias = new Map()
    dataArea.forEach((d) => {
      mapaDenuncias.set(d.id_denuncia, {
        area: d.categoria_nombre || 'Sin categoría',
        fecha: d.fecha_registro ? d.fecha_registro.slice(0, 10) : ''
      })
    })

    // Agrupar por denuncia principal
    const mapaGrupos = new Map()

    dataVinculadas.forEach((rel) => {
      if (!rel || typeof rel.id_principal !== 'number' || typeof rel.id_denuncia !== 'number') return

      const principalId = rel.id_principal
      const dupId = rel.id_denuncia

      if (!mapaGrupos.has(principalId)) {
        const infoPrincipal = mapaDenuncias.get(principalId) || {}
        mapaGrupos.set(principalId, {
          id: principalId,
          idsVinculadas: [],
          area: infoPrincipal.area || 'Sin categoría',
          fecha: infoPrincipal.fecha || '',
          razon: 'Marcada como duplicada'
        })
      }

      const grupo = mapaGrupos.get(principalId)
      if (!grupo.idsVinculadas.includes(dupId)) {
        grupo.idsVinculadas.push(dupId)
      }
    })

    grupos.value = Array.from(mapaGrupos.values()).map((g) => ({
      id: g.id,
      vinculos: g.idsVinculadas.length,
      area: g.area,
      fecha: g.fecha,
      razon: g.razon,
      idsVinculadas: g.idsVinculadas
    }))
  } catch (error) {
    console.error('Error al cargar grupos de denuncias duplicadas/vinculadas:', error)
    grupos.value = []
  }
}

onMounted(cargarGruposDuplicadasVinculadas)

const gestionarVinculos = (grupo) => {
  // Uso típico: abrir el mismo modal centrado en la acción de gestión de vínculos
  abrirModal(grupo)
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
