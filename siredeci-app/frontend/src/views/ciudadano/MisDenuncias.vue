<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Navbar -->
    <NavbarCiudadano />

    <!-- Main Content -->
    <main class="py-4 sm:py-6">
      <!-- Page Header -->
      <div class="mb-8 px-4 sm:px-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 class="text-3xl font-black text-gray-900 dark:text-white mb-1">
              Mis Denuncias
            </h1>
            <p class="text-gray-600 dark:text-gray-400">
              Gestiona y consulta el estado de tus denuncias
            </p>
          </div>
          <div class="flex gap-3">
            <button
              @click="goToDashboard"
              class="flex items-center gap-2 px-6 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-bold hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <span class="material-symbols-outlined">arrow_back</span>
              <span>Volver</span>
            </button>
            <button
              @click="goToRegistrarDenuncia"
              class="flex items-center gap-2 px-6 py-3 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 transition-colors"
            >
              <span class="material-symbols-outlined">add</span>
              <span>Nueva Denuncia</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 px-4 sm:px-6">
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-blue-600 dark:text-blue-400">description</span>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Total</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ denuncias.length }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-green-600 dark:text-green-400">check_circle</span>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Resueltas</p>
              <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ denunciasResueltas }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center">
              <span class="material-symbols-outlined text-orange-600 dark:text-orange-400">pending</span>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Pendientes</p>
              <p class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ denunciasPendientes }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-4 mb-6 mx-4 sm:mx-6">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <label class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 block">Buscar</label>
            <div class="relative">
              <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
                <span class="material-symbols-outlined text-lg">search</span>
              </span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar por código o título..."
                class="w-full h-10 pl-10 pr-4 rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 block">Estado</label>
            <select
              v-model="filtroEstado"
              class="w-full md:w-48 h-10 px-4 rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="Registrado">Registrado</option>
              <option value="En revisión">En revisión</option>
              <option value="Asignado">Asignado</option>
              <option value="En proceso">En proceso</option>
              <option value="Resuelta">Resuelta</option>
              <option value="Rechazada">Rechazada</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <span class="material-symbols-outlined text-6xl text-gray-300 dark:text-gray-600 animate-spin mb-4">progress_activity</span>
        <p class="text-gray-600 dark:text-gray-400">Cargando denuncias...</p>
      </div>

      <!-- Denuncias List -->
      <div v-else-if="denunciasFiltradas.length > 0" class="space-y-4 px-4 sm:px-6">
        <div
          v-for="denuncia in denunciasFiltradas"
          :key="denuncia.id"
          class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl p-6 hover:shadow-xl transition-shadow duration-200"
        >
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
            <!-- Content -->
            <div class="flex-1">
              <div class="flex items-start justify-between mb-3">
                <div>
                  <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                    {{ denuncia.titulo }}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-500">
                    {{ denuncia.codigo }} • {{ formatFecha(denuncia.fecha_registro) }}
                  </p>
                </div>
              </div>

              <p class="text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                {{ denuncia.descripcion }}
              </p>

              <div class="flex flex-wrap gap-2">
                <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-primary/10 text-primary">
                  <span class="material-symbols-outlined text-sm">category</span>
                  {{ denuncia.categoria }}
                </span>
                <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-gray-300">
                  <span class="material-symbols-outlined text-sm">location_on</span>
                  {{ denuncia.distrito }}
                </span>
              </div>
            </div>

            <!-- Status & Actions -->
            <div class="flex flex-col gap-3 md:items-end">
              <div class="flex flex-col gap-2">
                <span
                  class="inline-flex items-center justify-center gap-1 px-3 py-2 rounded-lg text-sm font-bold"
                  :class="getEstadoClass(denuncia.estado)"
                >
                  <span class="material-symbols-outlined text-sm">{{ getEstadoIcon(denuncia.estado) }}</span>
                  {{ denuncia.estado }}
                </span>
                <span
                  class="inline-flex items-center justify-center gap-1 px-3 py-1 rounded-lg text-xs font-bold"
                  :class="getPrioridadClass(denuncia.prioridad)"
                >
                  {{ denuncia.prioridad }}
                </span>
              </div>

              <button
                @click="verDetalle(denuncia)"
                class="flex items-center gap-1 px-4 py-2 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 font-semibold text-sm transition-colors duration-200"
              >
                <span class="material-symbols-outlined text-sm">visibility</span>
                Ver Detalle
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <span class="material-symbols-outlined text-6xl text-gray-300 dark:text-gray-600 mb-4">inbox</span>
        <p class="text-gray-600 dark:text-gray-400 text-lg mb-2">No se encontraron denuncias</p>
        <p class="text-gray-500 dark:text-gray-500 text-sm">
          {{ searchQuery || filtroEstado ? 'Intenta ajustar los filtros de búsqueda' : 'Aún no has registrado ninguna denuncia' }}
        </p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'

const router = useRouter()
const loading = ref(true)
const searchQuery = ref('')
const filtroEstado = ref('')

// Datos de ejemplo (reemplazar con llamadas al API)
const denuncias = ref([
  {
    id: 1,
    codigo: 'DEN-2025-00001',
    titulo: 'Bache en Av. Principal',
    descripcion: 'Hay un bache grande en la Av. Principal esquina con Jr. Lima que causa problemas a los vehículos',
    estado: 'En proceso',
    prioridad: 'Media',
    categoria: 'Infraestructura Vial',
    distrito: 'Miraflores',
    fecha_registro: '2025-01-10T14:30:00'
  },
  {
    id: 2,
    codigo: 'DEN-2025-00002',
    titulo: 'Luminaria sin funcionar',
    descripcion: 'La luminaria de la esquina de Av. Arequipa con Jr. Colón no funciona desde hace una semana',
    estado: 'Resuelta',
    prioridad: 'Alta',
    categoria: 'Alumbrado Público',
    distrito: 'Miraflores',
    fecha_registro: '2025-01-08T10:15:00'
  },
  {
    id: 3,
    codigo: 'DEN-2025-00003',
    titulo: 'Acumulación de basura',
    descripcion: 'Hay basura acumulada en el parque Kennedy que no ha sido recogida',
    estado: 'En revisión',
    prioridad: 'Baja',
    categoria: 'Limpieza y Residuos',
    distrito: 'Miraflores',
    fecha_registro: '2025-01-12T16:45:00'
  }
])

const denunciasFiltradas = computed(() => {
  return denuncias.value.filter(d => {
    const matchSearch = !searchQuery.value ||
      d.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      d.codigo.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchEstado = !filtroEstado.value || d.estado === filtroEstado.value

    return matchSearch && matchEstado
  })
})

const denunciasResueltas = computed(() => {
  return denuncias.value.filter(d => d.estado === 'Resuelta').length
})

const denunciasPendientes = computed(() => {
  return denuncias.value.filter(d => d.estado !== 'Resuelta' && d.estado !== 'Rechazada').length
})

onMounted(async () => {
  // TODO: Cargar denuncias del ciudadano desde el API
  // const response = await getDenunciasCiudadano()
  // denuncias.value = response.data
  
  // Simulación de carga
  setTimeout(() => {
    loading.value = false
  }, 1000)
})

const getEstadoClass = (estado) => {
  const classes = {
    'Registrado': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'En revisión': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
    'Asignado': 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400',
    'En proceso': 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400',
    'Resuelta': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
    'Rechazada': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
    'Cerrada': 'bg-gray-100 dark:bg-gray-900/30 text-gray-700 dark:text-gray-400'
  }
  return classes[estado] || 'bg-gray-100 dark:bg-gray-900/30 text-gray-700 dark:text-gray-400'
}

const getEstadoIcon = (estado) => {
  const icons = {
    'Registrado': 'fiber_new',
    'En revisión': 'hourglass_empty',
    'Asignado': 'assignment_ind',
    'En proceso': 'sync',
    'Resuelta': 'check_circle',
    'Rechazada': 'cancel',
    'Cerrada': 'lock'
  }
  return icons[estado] || 'help'
}

const getPrioridadClass = (prioridad) => {
  const classes = {
    'Baja': 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400',
    'Media': 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400',
    'Alta': 'bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400',
    'Urgente': 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'
  }
  return classes[prioridad] || 'bg-gray-50 dark:bg-gray-900/20 text-gray-700 dark:text-gray-400'
}

const formatFecha = (fecha) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const verDetalle = (denuncia) => {
  router.push({
    name: 'ciudadano-detalle-denuncia',
    params: { id: denuncia.id }
  })
}

const goToDashboard = () => {
  router.push({ name: 'ciudadano-dashboard' })
}

const goToRegistrarDenuncia = () => {
  router.push({ name: 'ciudadano-registrar-denuncia' })
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
