<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <NavbarCiudadano />

    <main class="max-w-4xl mx-auto px-4 py-8">
      <header class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 class="text-2xl font-extrabold text-gray-900 dark:text-gray-50 flex items-center gap-2">
            <span class="material-symbols-outlined text-[24px]">notifications</span>
            Centro de Notificaciones
          </h1>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Aquí verás los avisos importantes sobre el estado de tus denuncias.
          </p>
        </div>
      </header>

      <!-- Preferencias de notificación -->
      <section class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-5 mb-6">
        <h2 class="text-sm font-semibold text-gray-900 dark:text-gray-50 mb-3 flex items-center gap-2">
          <span class="material-symbols-outlined text-[20px]">tune</span>
          Preferencias de notificación
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" v-model="config.recibir_email" class="rounded border-gray-300" />
            <span class="text-gray-700 dark:text-gray-200">Recibir correos electrónicos</span>
          </label>
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" v-model="config.recibir_push" class="rounded border-gray-300" />
            <span class="text-gray-700 dark:text-gray-200">Mostrar notificaciones internas</span>
          </label>
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" v-model="config.recibir_sms" class="rounded border-gray-300" />
            <span class="text-gray-700 dark:text-gray-200">Recibir SMS (si está disponible)</span>
          </label>
          <div class="flex flex-col gap-1">
            <span class="text-gray-700 dark:text-gray-200">Frecuencia de resumen</span>
            <select
              v-model="config.frecuencia_resumen"
              class="mt-1 block w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 px-3 py-2"
            >
              <option value="Inmediato">Inmediato</option>
              <option value="Diario">Diario</option>
              <option value="Semanal">Semanal</option>
              <option value="Ninguno">Ninguno</option>
            </select>
          </div>
        </div>
        <div class="mt-4 flex justify-end">
          <button
            type="button"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold bg-primary text-white hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="savingConfig"
            @click="guardarConfig"
          >
            <span class="material-symbols-outlined text-[18px]">save</span>
            Guardar preferencias
          </button>
        </div>
      </section>

      <!-- Lista de notificaciones -->
      <section class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-5">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-gray-900 dark:text-gray-50 flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">inbox</span>
            Mis notificaciones
          </h2>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ notificaciones.length }} notificaciones
          </p>
        </div>

        <div v-if="loading" class="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
          Cargando notificaciones...
        </div>
        <div v-else-if="notificaciones.length === 0" class="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
          No tienes notificaciones por el momento.
        </div>
        <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <li
            v-for="n in notificaciones"
            :key="n.id_notificacion"
            class="py-3 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2"
          >
            <div class="flex gap-3">
              <div class="mt-1">
                <span
                  class="inline-flex items-center justify-center w-8 h-8 rounded-full"
                  :class="n.estado_envio === 'Leído'
                    ? 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-300'
                    : 'bg-primary/10 text-primary'"
                >
                  <span class="material-symbols-outlined text-[18px]">notifications</span>
                </span>
              </div>
              <div class="space-y-1 text-sm">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="font-semibold text-gray-900 dark:text-gray-100">{{ n.tipo_notificacion }}</span>
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border"
                    :class="n.estado_envio === 'Leído'
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-300 dark:border-emerald-700'
                      : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:border-amber-700'"
                  >
                    {{ n.estado_envio }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatFecha(n.fecha_creacion) }}
                  </span>
                </div>
                <p class="text-gray-700 dark:text-gray-200">
                  {{ n.mensaje }}
                </p>
                <p v-if="n.denuncia" class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
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
                class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-semibold border border-primary text-primary hover:bg-primary/10 dark:hover:bg-primary/20"
                @click="marcarLeida(n)"
              >
                <span class="material-symbols-outlined text-[16px]">done</span>
                Marcar como leída
              </button>
            </div>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'
import api from '@/services/api'
import { authService } from '@/services/auth'

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
    const user = authService.getCurrentUser()
    if (!user || !user.id_usuario) {
      notificaciones.value = []
      return
    }
    const response = await api.get('/ciudadanos/notificaciones/', {
      params: { id_usuario: user.id_usuario }
    })
    notificaciones.value = response.data?.results || []
  } catch (error) {
    console.error('Error al cargar notificaciones de ciudadano:', error)
    notificaciones.value = []
  } finally {
    loading.value = false
  }
}

const cargarConfig = async () => {
  try {
    const user = authService.getCurrentUser()
    if (!user || !user.id_usuario) return

    const response = await api.get('/ciudadanos/notificaciones/config/', {
      params: { id_usuario: user.id_usuario }
    })
    config.value = {
      recibir_email: !!response.data.recibir_email,
      recibir_sms: !!response.data.recibir_sms,
      recibir_push: !!response.data.recibir_push,
      frecuencia_resumen: response.data.frecuencia_resumen || 'Diario',
      horario_preferido: response.data.horario_preferido || ''
    }
  } catch (error) {
    console.error('Error al cargar configuración de notificaciones:', error)
  }
}

const guardarConfig = async () => {
  try {
    savingConfig.value = true
    const user = authService.getCurrentUser()
    if (!user || !user.id_usuario) return

    await api.put(
      '/ciudadanos/notificaciones/config/',
      {
        recibir_email: config.value.recibir_email,
        recibir_sms: config.value.recibir_sms,
        recibir_push: config.value.recibir_push,
        frecuencia_resumen: config.value.frecuencia_resumen,
        horario_preferido: config.value.horario_preferido
      },
      {
        params: { id_usuario: user.id_usuario }
      }
    )
  } catch (error) {
    console.error('Error al guardar configuración de notificaciones:', error)
  } finally {
    savingConfig.value = false
  }
}

const marcarLeida = async (n) => {
  try {
    const user = authService.getCurrentUser()
    if (!user || !user.id_usuario) return

    await api.post('/ciudadanos/notificaciones/marcar-leida/', {
      id_notificacion: n.id_notificacion,
      id_usuario: user.id_usuario
    })

    n.estado_envio = 'Leído'
  } catch (error) {
    console.error('Error al marcar notificación como leída:', error)
  }
}

const formatFecha = (iso) => {
  if (!iso) return ''
  try {
    const d = new Date(iso)
    return d.toLocaleString()
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
