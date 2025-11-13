<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Navbar -->
    <NavbarPublico />
    
    <div class="w-full flex flex-col items-center justify-center p-4 py-12">
      <div class="w-full max-w-2xl">
        <!-- Main Card -->
        <main class="w-full">
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl">
          <div class="p-8">
            <!-- Title Section -->
            <div class="mb-8 text-center">
              <h2 class="text-[#101619] dark:text-gray-50 text-3xl font-black leading-tight tracking-[-0.033em] mb-2">
                Consulta Pública de Denuncias
              </h2>
              <p class="text-[#587d8d] dark:text-slate-400 text-base font-normal leading-normal">
                Ingrese el código de seguimiento para consultar el estado de una denuncia
              </p>
            </div>

            <!-- Search Form -->
            <form @submit.prevent="buscarDenuncia" class="mb-6">
              <div class="flex gap-3">
                <div class="flex-1 relative">
                  <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-gray-400">
                    <span class="material-symbols-outlined text-xl">search</span>
                  </span>
                  <input
                    v-model="codigoSeguimiento"
                    type="text"
                    placeholder="Ej: SEG-ABC123456"
                    class="w-full h-14 pl-12 pr-4 rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors duration-200"
                  />
                </div>
                <button
                  type="submit"
                  :disabled="loading || !codigoSeguimiento"
                  class="flex items-center justify-center px-6 h-14 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="!loading">Buscar</span>
                  <span v-else class="material-symbols-outlined animate-spin">progress_activity</span>
                </button>
              </div>
            </form>

            <!-- Error Message -->
            <div v-if="error" class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p class="text-sm text-red-600 dark:text-red-400 flex items-center gap-2">
                <span class="material-symbols-outlined text-lg">error</span>
                {{ error }}
              </p>
            </div>

            <!-- Denuncia Details -->
            <div v-if="denuncia" class="space-y-6">
              <!-- Status Badge -->
              <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-slate-900/50 rounded-lg">
                <div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">Estado actual</p>
                  <p class="text-lg font-bold" :class="getEstadoColor(denuncia.estado)">
                    {{ denuncia.estado }}
                  </p>
                </div>
                <div class="text-right">
                  <p class="text-sm text-gray-600 dark:text-gray-400">Prioridad</p>
                  <p class="text-lg font-bold" :class="getPrioridadColor(denuncia.prioridad)">
                    {{ denuncia.prioridad }}
                  </p>
                </div>
              </div>

              <!-- Denuncia Info -->
              <div class="space-y-4">
                <div>
                  <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                    {{ denuncia.titulo }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    Código: {{ denuncia.codigo_denuncia }}
                  </p>
                </div>

                <div>
                  <p class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Descripción</p>
                  <p class="text-gray-600 dark:text-gray-400">{{ denuncia.descripcion }}</p>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Categoría</p>
                    <p class="text-gray-600 dark:text-gray-400">{{ denuncia.categoria }}</p>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Fecha de Registro</p>
                    <p class="text-gray-600 dark:text-gray-400">{{ formatFecha(denuncia.fecha_registro) }}</p>
                  </div>
                </div>

                <div>
                  <p class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Ubicación</p>
                  <p class="text-gray-600 dark:text-gray-400">{{ denuncia.ubicacion }}</p>
                </div>
              </div>

              <!-- Timeline -->
              <div v-if="denuncia.seguimiento && denuncia.seguimiento.length > 0">
                <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">Historial de Seguimiento</h3>
                <div class="space-y-3">
                  <div
                    v-for="(item, index) in denuncia.seguimiento"
                    :key="index"
                    class="flex gap-4 pb-4 border-b border-gray-200 dark:border-slate-700 last:border-0"
                  >
                    <div class="flex-shrink-0">
                      <div class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                        <span class="material-symbols-outlined text-primary text-sm">schedule</span>
                      </div>
                    </div>
                    <div class="flex-1">
                      <p class="font-semibold text-gray-900 dark:text-gray-100">{{ item.estado_nuevo }}</p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ item.comentario }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">{{ formatFecha(item.fecha_hora) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- No Results -->
            <div v-else-if="searched && !loading" class="text-center py-8">
              <span class="material-symbols-outlined text-6xl text-gray-300 dark:text-gray-600 mb-4">search_off</span>
              <p class="text-gray-600 dark:text-gray-400">No se encontró ninguna denuncia con ese código</p>
            </div>

            <!-- Divider -->
            <div class="relative flex items-center justify-center my-6">
              <div class="h-px w-full bg-slate-200 dark:bg-slate-700"></div>
              <span class="absolute bg-white dark:bg-[#131b1f] px-2 text-sm text-slate-500 dark:text-slate-400">o</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-3">
              <button
                @click="goToEstadisticas"
                class="flex-1 flex items-center justify-center gap-2 h-12 px-5 rounded-lg bg-primary/10 text-primary dark:bg-primary/20 hover:bg-primary/20 dark:hover:bg-primary/30 font-bold transition-colors duration-200"
              >
                <span class="material-symbols-outlined">bar_chart</span>
                <span>Estadísticas</span>
              </button>
              <button
                @click="goToLogin"
                class="flex-1 flex items-center justify-center gap-2 h-12 px-5 rounded-lg border border-primary text-primary hover:bg-primary/10 dark:hover:bg-primary/20 font-bold transition-colors duration-200"
              >
                <span class="material-symbols-outlined">login</span>
                <span>Iniciar Sesión</span>
              </button>
            </div>
          </div>
        </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavbarPublico from '@/components/NavbarPublico.vue'

const router = useRouter()
const codigoSeguimiento = ref('')
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const denuncia = ref(null)

const buscarDenuncia = async () => {
  if (!codigoSeguimiento.value.trim()) return

  loading.value = true
  error.value = ''
  searched.value = true
  denuncia.value = null

  try {
    // TODO: Llamar al API para buscar la denuncia
    // const response = await buscarDenunciaPublica(codigoSeguimiento.value)
    
    // Simulación de datos (remover cuando se integre con backend)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Datos de ejemplo
    denuncia.value = {
      codigo_denuncia: 'DEN-2025-00001',
      titulo: 'Bache en Av. Principal',
      descripcion: 'Hay un bache grande en la Av. Principal que causa problemas a los vehículos',
      estado: 'En proceso',
      prioridad: 'Media',
      categoria: 'Infraestructura Vial',
      fecha_registro: '2025-01-10T14:30:00',
      ubicacion: 'Av. Principal 1234, Miraflores',
      seguimiento: [
        {
          estado_nuevo: 'Registrado',
          comentario: 'Denuncia registrada exitosamente',
          fecha_hora: '2025-01-10T14:30:00'
        },
        {
          estado_nuevo: 'En revisión',
          comentario: 'La denuncia está siendo revisada por el área de Obras Públicas',
          fecha_hora: '2025-01-11T10:00:00'
        },
        {
          estado_nuevo: 'En proceso',
          comentario: 'Se ha asignado un técnico para evaluar el daño',
          fecha_hora: '2025-01-12T09:15:00'
        }
      ]
    }
  } catch (err) {
    error.value = 'No se pudo encontrar la denuncia. Verifique el código de seguimiento.'
    denuncia.value = null
  } finally {
    loading.value = false
  }
}

const getEstadoColor = (estado) => {
  const colors = {
    'Registrado': 'text-blue-600 dark:text-blue-400',
    'En revisión': 'text-yellow-600 dark:text-yellow-400',
    'Asignado': 'text-purple-600 dark:text-purple-400',
    'En proceso': 'text-orange-600 dark:text-orange-400',
    'Resuelta': 'text-green-600 dark:text-green-400',
    'Rechazada': 'text-red-600 dark:text-red-400',
    'Cerrada': 'text-gray-600 dark:text-gray-400'
  }
  return colors[estado] || 'text-gray-600 dark:text-gray-400'
}

const getPrioridadColor = (prioridad) => {
  const colors = {
    'Baja': 'text-green-600 dark:text-green-400',
    'Media': 'text-yellow-600 dark:text-yellow-400',
    'Alta': 'text-orange-600 dark:text-orange-400',
    'Urgente': 'text-red-600 dark:text-red-400'
  }
  return colors[prioridad] || 'text-gray-600 dark:text-gray-400'
}

const formatFecha = (fecha) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const goToEstadisticas = () => {
  router.push({ name: 'estadisticas-publicas' })
}

const goToLogin = () => {
  router.push({ name: 'ciudadano-login' })
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
