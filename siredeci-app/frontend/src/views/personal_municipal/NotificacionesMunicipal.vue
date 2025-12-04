<template>
  <div class="flex h-screen bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden px-8 py-8">
      <section class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 class="text-2xl font-extrabold text-slate-900 flex items-center gap-2">
            <span class="material-symbols-outlined text-[24px] text-sky-600">notifications</span>
            Notificaciones del Área
          </h1>
          <p class="text-sm text-slate-500 mt-1">
            Avisos internos sobre asignaciones y cambios en las denuncias que gestionas.
          </p>
        </div>
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] gap-6 h-full overflow-hidden">
        <!-- Lista de notificaciones -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
          <header class="px-5 py-3 border-b border-slate-200 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="text-sm font-semibold text-slate-900 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[20px] text-sky-600">inbox</span>
                Notificaciones recientes
              </h2>
            </div>
            <p class="text-xs text-slate-500">
              {{ notificaciones.length }} notificaciones
            </p>
          </header>

          <div class="flex-1 overflow-y-auto">
            <div v-if="loading" class="py-8 text-center text-sm text-slate-500">
              Cargando notificaciones...
            </div>
            <div v-else-if="notificaciones.length === 0" class="py-8 text-center text-sm text-slate-500">
              No hay notificaciones por el momento.
            </div>
            <ul v-else class="divide-y divide-slate-200">
              <li
                v-for="n in notificaciones"
                :key="n.id_notificacion"
                class="px-5 py-3 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2"
              >
                <div class="flex gap-3">
                  <div class="mt-1">
                    <span
                      class="inline-flex items-center justify-center w-8 h-8 rounded-full"
                      :class="n.estado_envio === 'Leído'
                        ? 'bg-slate-100 text-slate-500'
                        : 'bg-sky-50 text-sky-600'"
                    >
                      <span class="material-symbols-outlined text-[18px]">notifications</span>
                    </span>
                  </div>
                  <div class="space-y-1 text-sm">
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="font-semibold text-slate-900">{{ n.tipo_notificacion }}</span>
                      <span
                        class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border"
                        :class="n.estado_envio === 'Leído'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-amber-50 text-amber-700 border-amber-200'"
                      >
                        {{ n.estado_envio }}
                      </span>
                      <span class="text-xs text-slate-500">
                        {{ formatFecha(n.fecha_creacion) }}
                      </span>
                    </div>
                    <p class="text-slate-700">{{ n.mensaje }}</p>
                    <p v-if="n.denuncia" class="text-xs text-slate-500 flex items-center gap-1">
                      <span class="material-symbols-outlined text-[14px]">description</span>
                      <span>
                        Denuncia {{ n.denuncia.codigo_denuncia || n.denuncia.numero_seguimiento }} ·
                        {{ n.denuncia.titulo }}
                      </span>
                    </p>
                  </div>
                </div>
                <div class="flex items-center gap-2 justify-end">
                  <button
                    v-if="n.estado_envio !== 'Leído'"
                    type="button"
                    class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-semibold border border-sky-500 text-sky-600 hover:bg-sky-50"
                    @click="marcarLeida(n)"
                  >
                    <span class="material-symbols-outlined text-[16px]">done</span>
                    Marcar leída
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Configuración -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col">
          <header class="px-5 py-3 border-b border-slate-200">
            <h2 class="text-sm font-semibold text-slate-900 flex items-center gap-2">
              <span class="material-symbols-outlined text-[20px] text-sky-600">tune</span>
              Preferencias de notificación
            </h2>
          </header>
          <div class="flex-1 overflow-y-auto px-5 py-4 space-y-4 text-sm">
            <p class="text-slate-600 text-sm">
              Ajusta cómo deseas recibir las notificaciones internas relacionadas a tus denuncias.
            </p>
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="config.recibir_email" class="rounded border-slate-300" />
              <span class="text-slate-700">Recibir correos electrónicos</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="config.recibir_push" class="rounded border-slate-300" />
              <span class="text-slate-700">Recibir notificaciones internas</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" v-model="config.recibir_sms" class="rounded border-slate-300" />
              <span class="text-slate-700">Recibir SMS (si está disponible)</span>
            </label>
            <div class="flex flex-col gap-1">
              <span class="text-slate-700">Frecuencia de resumen</span>
              <select
                v-model="config.frecuencia_resumen"
                class="mt-1 block w-full rounded-lg border border-slate-300 bg-white text-sm text-slate-900 px-3 py-2"
              >
                <option value="Inmediato">Inmediato</option>
                <option value="Diario">Diario</option>
                <option value="Semanal">Semanal</option>
                <option value="Ninguno">Ninguno</option>
              </select>
            </div>
          </div>
          <footer class="px-5 py-3 border-t border-slate-200 flex justify-end">
            <button
              type="button"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold bg-sky-600 text-white hover:bg-sky-700 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="savingConfig"
              @click="guardarConfig"
            >
              <span class="material-symbols-outlined text-[18px]">save</span>
              Guardar preferencias
            </button>
          </footer>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'

const notificaciones = ref([])
const loading = ref(true)
const savingConfig = ref(false)
const config = ref({
  recibir_email: true,
  recibir_sms: false,
  recibir_push: true,
  frecuencia_resumen: 'Diario',
  horario_preferido: ''
})

const cargarNotificaciones = async () => {
  try {
    const response = await axios.get('/notificaciones/usuario/')
    notificaciones.value = response.data?.results || []
  } catch (error) {
    console.error('Error al cargar notificaciones internas (municipal):', error)
    notificaciones.value = []
  } finally {
    loading.value = false
  }
}

const cargarConfig = async () => {
  try {
    const response = await axios.get('/notificaciones/usuario/config/')
    config.value = {
      recibir_email: !!response.data.recibir_email,
      recibir_sms: !!response.data.recibir_sms,
      recibir_push: !!response.data.recibir_push,
      frecuencia_resumen: response.data.frecuencia_resumen || 'Diario',
      horario_preferido: response.data.horario_preferido || ''
    }
  } catch (error) {
    console.error('Error al cargar configuración de notificaciones internas (municipal):', error)
  }
}

const guardarConfig = async () => {
  try {
    savingConfig.value = true
    await axios.put('/notificaciones/usuario/config/', {
      recibir_email: config.value.recibir_email,
      recibir_sms: config.value.recibir_sms,
      recibir_push: config.value.recibir_push,
      frecuencia_resumen: config.value.frecuencia_resumen,
      horario_preferido: config.value.horario_preferido
    })
  } catch (error) {
    console.error('Error al guardar configuración de notificaciones internas (municipal):', error)
  } finally {
    savingConfig.value = false
  }
}

const marcarLeida = async (n) => {
  try {
    await axios.post('/notificaciones/usuario/marcar-leida/', {
      id_notificacion: n.id_notificacion
    })
    n.estado_envio = 'Leído'
  } catch (error) {
    console.error('Error al marcar notificación interna como leída (municipal):', error)
  }
}

const formatFecha = (iso) => {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}

onMounted(async () => {
  await Promise.all([cargarNotificaciones(), cargarConfig()])
})
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
