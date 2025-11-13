<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Navbar -->
    <NavbarCiudadano />

    <!-- Main Content -->
    <main class="py-4 sm:py-6">
      <div class="flex flex-col w-full gap-6">
        
        <!-- Breadcrumbs -->
        <div class="flex flex-wrap gap-2 text-sm text-gray-500 dark:text-gray-400 px-4 sm:px-6">
          <router-link to="/ciudadano/dashboard" class="hover:text-primary">Inicio</router-link>
          <span>/</span>
          <router-link to="/ciudadano/mis-denuncias" class="hover:text-primary">Mis Denuncias</router-link>
          <span>/</span>
          <span class="text-gray-800 dark:text-gray-200 font-medium">{{ denuncia.codigo }}</span>
        </div>

        <!-- Main Card -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 sm:p-8 mx-4 sm:mx-6">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row justify-between gap-4 mb-6 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex flex-col gap-3">
              <div class="flex items-center gap-2">
                <span :class="['material-symbols-outlined text-xl', getEstadoIconColor(denuncia.estado)]">
                  {{ getEstadoIcon(denuncia.estado) }}
                </span>
                <h1 class="text-gray-800 dark:text-gray-100 text-3xl sm:text-4xl font-black leading-tight">
                  {{ denuncia.titulo }}
                </h1>
              </div>
              <p class="text-gray-500 dark:text-gray-400 text-base">
                Categoría: {{ denuncia.categoria }}
              </p>
            </div>
            <div class="flex items-start">
              <div :class="['flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-lg px-4', getEstadoClass(denuncia.estado)]">
                <p class="text-sm font-medium">{{ denuncia.estado }}</p>
              </div>
            </div>
          </div>

          <!-- Info Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-6 mb-8 text-sm">
            <div class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Código de Denuncia</p>
              <p class="text-gray-800 dark:text-gray-200 font-medium">{{ denuncia.codigo }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Número de Seguimiento</p>
              <p class="text-gray-800 dark:text-gray-200 font-medium">{{ denuncia.numeroSeguimiento }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Fecha de Registro</p>
              <p class="text-gray-800 dark:text-gray-200 font-medium">{{ formatFecha(denuncia.fechaRegistro) }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Prioridad</p>
              <p :class="['font-medium', getPrioridadColor(denuncia.prioridad)]">{{ denuncia.prioridad }}</p>
            </div>
            <div class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Distrito</p>
              <p class="text-gray-800 dark:text-gray-200 font-medium">{{ denuncia.distrito }}</p>
            </div>
            <div v-if="denuncia.fechaResolucion" class="flex flex-col gap-1">
              <p class="text-gray-500 dark:text-gray-400">Fecha de Resolución</p>
              <p class="text-gray-800 dark:text-gray-200 font-medium">{{ formatFecha(denuncia.fechaResolucion) }}</p>
            </div>
          </div>

          <!-- Description -->
          <div class="mb-8">
            <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-2">Descripción</h3>
            <p class="text-gray-600 dark:text-gray-300 text-base leading-relaxed">{{ denuncia.descripcion }}</p>
          </div>

          <!-- Location and Evidence -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <!-- Location -->
            <div>
              <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-3">Ubicación</h3>
              <div class="aspect-video w-full rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-900">
                <div id="detalle-map" class="w-full h-full"></div>
              </div>
              <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ denuncia.direccion }}</p>
              <p v-if="denuncia.referencia" class="text-xs text-gray-500 dark:text-gray-400">{{ denuncia.referencia }}</p>
            </div>

            <!-- Evidence -->
            <div>
              <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-3">Evidencias</h3>
              <div v-if="denuncia.evidencias && denuncia.evidencias.length > 0" class="grid grid-cols-3 gap-2">
                <div v-for="(evidencia, index) in denuncia.evidencias" :key="index"
                     @click="openLightbox(index)"
                     class="aspect-square bg-cover bg-center rounded-lg cursor-pointer hover:opacity-90 transition-opacity border border-gray-200 dark:border-gray-700"
                     :style="`background-image: url('${evidencia}')`">
                </div>
              </div>
              <div v-else class="flex items-center justify-center h-48 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
                <div class="text-center text-gray-400">
                  <span class="material-symbols-outlined text-4xl mb-2">image</span>
                  <p class="text-sm">Sin evidencias adjuntas</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Timeline -->
          <div class="mb-8">
            <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-4">Historial de Seguimiento</h3>
            <div class="relative pl-6 space-y-8 border-l-2 border-gray-200 dark:border-gray-600">
              <div v-for="(seguimiento, index) in denuncia.historial" :key="index" class="relative">
                <div :class="[
                  'absolute -left-[34px] top-1.5 flex h-5 w-5 items-center justify-center rounded-full ring-8 ring-white dark:ring-gray-800',
                  seguimiento.color
                ]">
                  <span class="material-symbols-outlined text-white text-sm">{{ seguimiento.icon }}</span>
                </div>
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ formatFecha(seguimiento.fecha) }}</p>
                <h4 class="text-base font-semibold text-gray-800 dark:text-gray-200">{{ seguimiento.titulo }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-300">{{ seguimiento.descripcion }}</p>
              </div>
            </div>
          </div>

          <!-- Rating Section (only if resolved) -->
          <div v-if="denuncia.estado === 'Resuelta' && !denuncia.calificacion" 
               class="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-bold text-gray-800 dark:text-gray-200 mb-1">
              ¿Cómo calificarías la resolución de tu denuncia?
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Tu opinión nos ayuda a mejorar nuestros servicios.
            </p>
            <form @submit.prevent="submitRating" class="flex flex-col gap-4">
              <div class="flex items-center gap-1">
                <span v-for="star in 5" :key="star"
                      @click="rating = star"
                      @mouseenter="hoverRating = star"
                      @mouseleave="hoverRating = 0"
                      :class="[
                        'material-symbols-outlined cursor-pointer text-3xl transition-colors',
                        (hoverRating || rating) >= star ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'
                      ]">
                  {{ (hoverRating || rating) >= star ? 'star' : 'star_outline' }}
                </span>
              </div>
              <textarea v-model="comentario"
                        class="w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 focus:ring-primary focus:border-primary text-sm"
                        placeholder="Deja un comentario adicional (opcional)"
                        rows="3"></textarea>
              <button type="submit"
                      :disabled="rating === 0"
                      :class="[
                        'flex items-center justify-center rounded-lg h-10 px-5 self-start gap-2 text-sm font-bold transition-opacity',
                        rating > 0 ? 'bg-primary text-white hover:bg-primary/90' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      ]">
                <span>Enviar Calificación</span>
              </button>
            </form>
          </div>

          <!-- Already rated -->
          <div v-else-if="denuncia.calificacion"
               class="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-800">
            <div class="flex items-center gap-2 mb-2">
              <span class="material-symbols-outlined text-green-600 dark:text-green-400">check_circle</span>
              <h3 class="text-lg font-bold text-green-900 dark:text-green-300">
                Ya calificaste esta denuncia
              </h3>
            </div>
            <div class="flex items-center gap-1 mb-2">
              <span v-for="star in 5" :key="star"
                    :class="[
                      'material-symbols-outlined text-2xl',
                      star <= denuncia.calificacion.estrellas ? 'text-yellow-400' : 'text-gray-300'
                    ]">
                star
              </span>
            </div>
            <p v-if="denuncia.calificacion.comentario" class="text-sm text-gray-600 dark:text-gray-300">
              "{{ denuncia.calificacion.comentario }}"
            </p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-wrap gap-3 px-4 sm:px-6">
          <button @click="goBack" 
                  class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-bold hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
            <span class="material-symbols-outlined">arrow_back</span>
            <span>Volver</span>
          </button>
          <button v-if="denuncia.estado !== 'Resuelta' && denuncia.estado !== 'Rechazada'"
                  class="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 transition-colors">
            <span class="material-symbols-outlined">print</span>
            <span>Descargar Comprobante</span>
          </button>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix para los iconos de Leaflet
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow
})

const router = useRouter()
const route = useRoute()

let map = null

// Rating state
const rating = ref(0)
const hoverRating = ref(0)
const comentario = ref('')

// Datos de ejemplo de la denuncia (en producción vendría del API)
const denuncia = ref({
  id: 1,
  codigo: 'DEN-2025-00001',
  numeroSeguimiento: 'TRK-9876543210',
  titulo: 'Poste de luz sin funcionar',
  descripcion: 'El poste de luz ubicado en la esquina de Calle Principal con Avenida Secundaria ha dejado de funcionar desde hace una semana. La zona queda completamente a oscuras por la noche, lo que representa un riesgo para la seguridad de los vecinos que transitan por el área.',
  estado: 'Resuelta',
  prioridad: 'Media',
  categoria: 'Alumbrado Público',
  distrito: 'Miraflores',
  fechaRegistro: '2025-01-08T10:15:00',
  fechaResolucion: '2025-01-15T14:30:00',
  direccion: 'Av. Principal 456, esquina con Jr. Lima',
  referencia: 'Frente al parque central',
  ubicacion: {
    latitud: -12.0464,
    longitud: -77.0428
  },
  evidencias: [
    'https://images.unsplash.com/photo-1621363604215-e6dc0e6f2cc8?w=400',
    'https://images.unsplash.com/photo-1518707999770-ec0c2b34f50f?w=400',
    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'
  ],
  historial: [
    {
      fecha: '2025-01-15T14:30:00',
      titulo: 'Denuncia Resuelta',
      descripcion: 'El equipo de mantenimiento reemplazó el foco y el poste ya se encuentra operativo.',
      icon: 'check',
      color: 'bg-green-500'
    },
    {
      fecha: '2025-01-10T09:00:00',
      titulo: 'Asignado a Equipo de Obras',
      descripcion: 'La denuncia ha sido asignada al equipo de alumbrado público para su revisión en terreno.',
      icon: 'construction',
      color: 'bg-primary'
    },
    {
      fecha: '2025-01-08T10:15:00',
      titulo: 'Denuncia Registrada',
      descripcion: 'Se ha recibido y registrado la denuncia en el sistema.',
      icon: 'hourglass_top',
      color: 'bg-yellow-500'
    }
  ],
  calificacion: null // Si ya fue calificada: { estrellas: 4, comentario: 'Buen servicio' }
})

onMounted(() => {
  // TODO: Cargar denuncia desde el API usando el ID de la ruta
  // const id = route.params.id
  // const response = await getDenunciaById(id)
  // denuncia.value = response.data
  
  // Inicializar mapa después de que el DOM esté listo
  setTimeout(() => initMap(), 100)
})

const initMap = () => {
  const mapElement = document.getElementById('detalle-map')
  if (!mapElement || map) return
  
  const lat = denuncia.value.ubicacion.latitud
  const lng = denuncia.value.ubicacion.longitud
  
  map = L.map('detalle-map', {
    center: [lat, lng],
    zoom: 16,
    zoomControl: true,
    dragging: true,
    scrollWheelZoom: false
  })
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
  
  const marker = L.marker([lat, lng]).addTo(map)
  marker.bindPopup(`<b>${denuncia.value.titulo}</b><br>${denuncia.value.direccion}`).openPopup()
}

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
  return classes[estado] || classes['Registrado']
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

const getEstadoIconColor = (estado) => {
  const colors = {
    'Registrado': 'text-blue-600 dark:text-blue-400',
    'En revisión': 'text-yellow-600 dark:text-yellow-400',
    'Asignado': 'text-purple-600 dark:text-purple-400',
    'En proceso': 'text-orange-600 dark:text-orange-400',
    'Resuelta': 'text-green-600 dark:text-green-400',
    'Rechazada': 'text-red-600 dark:text-red-400',
    'Cerrada': 'text-gray-600 dark:text-gray-400'
  }
  return colors[estado] || colors['Registrado']
}

const getPrioridadColor = (prioridad) => {
  const colors = {
    'Baja': 'text-green-600 dark:text-green-400',
    'Media': 'text-yellow-600 dark:text-yellow-400',
    'Alta': 'text-orange-600 dark:text-orange-400',
    'Urgente': 'text-red-600 dark:text-red-400'
  }
  return colors[prioridad] || colors['Media']
}

const formatFecha = (fecha) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-PE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const openLightbox = (index) => {
  // TODO: Implementar lightbox para ver imágenes en grande
  console.log('Abrir imagen:', index)
}

const submitRating = () => {
  if (rating.value === 0) return
  
  // TODO: Enviar calificación al backend
  console.log('Calificación enviada:', {
    denunciaId: denuncia.value.id,
    estrellas: rating.value,
    comentario: comentario.value
  })
  
  // Actualizar la denuncia con la calificación
  denuncia.value.calificacion = {
    estrellas: rating.value,
    comentario: comentario.value
  }
  
  // Limpiar form
  rating.value = 0
  comentario.value = ''
}

const goBack = () => {
  router.push('/ciudadano/mis-denuncias')
}

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}

#detalle-map {
  height: 100%;
  width: 100%;
}
</style>
