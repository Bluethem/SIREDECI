<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <!-- Navbar -->
    <NavbarCiudadano />

    <!-- Main Content -->
    <main class="py-4 sm:py-6">
      <div class="w-full">
        <!-- Breadcrumbs -->
        <nav class="flex items-center gap-2 text-sm mb-6 px-4 sm:px-6">
          <router-link to="/ciudadano/dashboard" class="text-gray-500 dark:text-gray-400 hover:text-primary">Inicio</router-link>
          <span class="text-gray-400">/</span>
          <router-link to="/ciudadano/mis-denuncias" class="text-gray-500 dark:text-gray-400 hover:text-primary">Denuncias</router-link>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900 dark:text-gray-200 font-medium">Crear Nueva Denuncia</span>
        </nav>

        <!-- Stepper -->
      <div class="flex flex-wrap gap-3 mb-6 px-4 sm:px-6">
        <div v-for="step in steps" :key="step.number" 
             :class="[
               'flex h-10 items-center justify-center gap-x-2 rounded-lg px-4',
               currentStep === step.number 
                 ? 'bg-primary/20 text-primary' 
                 : currentStep > step.number
                   ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                   : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400'
             ]">
          <span class="material-symbols-outlined text-xl">
            {{ currentStep > step.number ? 'check_circle' : 'radio_button_unchecked' }}
          </span>
          <p class="text-sm font-bold">{{ step.label }}</p>
        </div>
      </div>

      <!-- Page Heading -->
      <div class="mb-8 px-4 sm:px-6">
        <h1 class="text-3xl lg:text-4xl font-black text-gray-900 dark:text-white mb-2">
          {{ steps[currentStep - 1].title }}
        </h1>
        <p class="text-gray-600 dark:text-gray-400 text-base lg:text-lg">
          {{ steps[currentStep - 1].description }}
        </p>
      </div>

      <!-- Step 1: Category Selection -->
      <div v-if="currentStep === 1" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6 px-4 sm:px-6">
        <div v-for="category in categories" :key="category.id"
             @click="selectCategory(category)"
             :class="[
               'flex flex-col gap-4 p-5 rounded-xl border-2 transition-all cursor-pointer',
               'bg-white dark:bg-gray-800',
               selectedCategory?.id === category.id
                 ? 'border-primary shadow-lg shadow-primary/20'
                 : 'border-transparent hover:border-primary/50 hover:shadow-md'
             ]">
          <div :class="[
            'flex items-center justify-center w-16 h-16 rounded-lg',
            category.bgColor
          ]">
            <span :class="['material-symbols-outlined text-4xl', category.iconColor]">
              {{ category.icon }}
            </span>
          </div>
          <div class="flex flex-col gap-2">
            <h3 class="text-gray-900 dark:text-white text-base font-bold">{{ category.name }}</h3>
            <p class="text-gray-600 dark:text-gray-400 text-sm">{{ category.description }}</p>
            <div class="flex items-center gap-1.5 mt-2 text-gray-500 dark:text-gray-400">
              <span class="material-symbols-outlined text-base">schedule</span>
              <p class="text-xs">Promedio: {{ category.avgTime }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Details Form -->
      <div v-else-if="currentStep === 2" class="w-full px-4 sm:px-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 lg:p-8 space-y-6">
          <!-- Category Badge -->
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div class="flex items-center gap-3">
              <div :class="['flex items-center justify-center w-10 h-10 rounded-lg', selectedCategory?.bgColor]">
                <span :class="['material-symbols-outlined text-xl', selectedCategory?.iconColor]">
                  {{ selectedCategory?.icon }}
                </span>
              </div>
              <p class="text-gray-900 dark:text-white text-base">
                Categoría: <span class="font-semibold">{{ selectedCategory?.name }}</span>
              </p>
            </div>
            <button @click="currentStep = 1" class="text-primary text-sm font-bold hover:underline">
              Cambiar
            </button>
          </div>

          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Título de la denuncia *
            </label>
            <div class="relative">
              <input v-model="form.titulo" type="text" maxlength="100"
                     class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                     placeholder="Ej: Poste de luz caído en Av. Principal">
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-500">
                {{ form.titulo.length }}/100
              </span>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Describe el problema en detalle *
            </label>
            <textarea v-model="form.descripcion" rows="6"
                      class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                      placeholder="Proporcione todos los detalles relevantes, como la dirección exacta, puntos de referencia, desde cuándo existe el problema, etc."></textarea>
          </div>
        </div>
      </div>

      <!-- Step 3: Location -->
      <div v-else-if="currentStep === 3" class="w-full px-4 sm:px-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 lg:p-8 space-y-6">
          <!-- Map Container -->
          <div class="relative w-full h-[500px] rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <!-- Leaflet Map -->
            <div id="map" class="w-full h-full bg-gray-100 dark:bg-gray-900"></div>

            <!-- Location Info Panel -->
            <div class="absolute top-4 left-4 right-4 md:right-auto md:max-w-sm">
              <div class="bg-white/95 dark:bg-gray-800/95 backdrop-blur-sm p-5 rounded-lg shadow-lg space-y-4">
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Latitud</label>
                    <input v-model="form.ubicacion.latitud" type="text" readonly
                           class="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-sm">
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Longitud</label>
                    <input v-model="form.ubicacion.longitud" type="text" readonly
                           class="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-sm">
                  </div>
                </div>
                
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Dirección Aproximada *</label>
                  <input v-model="form.direccion" type="text"
                         class="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-primary"
                         placeholder="Av. Corrientes 1234">
                </div>
                
                <div>
                  <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Referencia Adicional</label>
                  <input v-model="form.referencia" type="text"
                         class="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-primary"
                         placeholder="Frente a la tienda azul...">
                </div>
                
                <button @click="useCurrentLocation"
                        class="flex w-full items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-primary/20 dark:bg-primary/30 text-primary font-bold text-sm hover:bg-primary/30 transition-colors">
                  <span class="material-symbols-outlined text-lg">my_location</span>
                  <span>Usar mi Ubicación Actual</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Evidence Upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Evidencias (Opcional)
            </label>
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-3">
              Puedes adjuntar hasta 5 fotos (máx. 5MB cada una)
            </p>
            
            <!-- Upload button -->
            <div class="relative">
              <input type="file" 
                     @change="handleFileUpload"
                     accept="image/*"
                     multiple
                     ref="fileInput"
                     class="hidden">
              <button @click="$refs.fileInput.click()"
                      type="button"
                      class="w-full flex items-center justify-center gap-2 px-4 py-8 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 hover:border-primary dark:hover:border-primary transition-colors text-gray-600 dark:text-gray-400 hover:text-primary">
                <span class="material-symbols-outlined text-4xl">add_photo_alternate</span>
                <div class="text-left">
                  <p class="font-medium">Seleccionar Imágenes</p>
                  <p class="text-xs">Haz clic para seleccionar archivos</p>
                </div>
              </button>
            </div>

            <!-- Preview grid -->
            <div v-if="evidencias.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 mt-4">
              <div v-for="(img, index) in evidencias" :key="index"
                   class="relative aspect-square group">
                <img :src="img.url" :alt="`Evidencia ${index + 1}`"
                     class="w-full h-full object-cover rounded-lg border border-gray-200 dark:border-gray-700">
                <button @click="removeImage(index)"
                        type="button"
                        class="absolute top-1 right-1 w-6 h-6 flex items-center justify-center bg-red-500 hover:bg-red-600 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                  <span class="material-symbols-outlined text-sm">close</span>
                </button>
                <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white text-xs p-1 text-center rounded-b-lg">
                  {{ index + 1 }} / 5
                </div>
              </div>
            </div>

            <!-- File size warning -->
            <p v-if="evidencias.length >= 5" class="text-xs text-amber-600 dark:text-amber-400 mt-2 flex items-center gap-1">
              <span class="material-symbols-outlined text-sm">info</span>
              Has alcanzado el límite de 5 imágenes
            </p>
            <p v-else-if="evidencias.length > 0" class="text-xs text-gray-500 dark:text-gray-400 mt-2">
              {{ evidencias.length }} de 5 imágenes agregadas
            </p>
          </div>
        </div>
      </div>

      <!-- Step 4: Confirmation -->
      <div v-else-if="currentStep === 4" class="w-full px-4 sm:px-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 lg:p-8 space-y-8">
          <h2 class="text-gray-900 dark:text-white text-2xl font-bold">Resumen de la Denuncia</h2>
          
          <!-- Category Section -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">CATEGORÍA</h3>
            <div class="flex items-center gap-4 bg-gray-50 dark:bg-gray-900/50 px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700">
              <div :class="['flex items-center justify-center rounded-lg shrink-0 size-10', selectedCategory?.bgColor]">
                <span :class="['material-symbols-outlined text-2xl', selectedCategory?.iconColor]">
                  {{ selectedCategory?.icon }}
                </span>
              </div>
              <p class="text-gray-900 dark:text-white text-base font-medium flex-1">{{ selectedCategory?.name }}</p>
            </div>
          </div>

          <!-- Details Section -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">DETALLES</h3>
            <div class="space-y-2">
              <p class="text-gray-900 dark:text-white font-bold">{{ form.titulo }}</p>
              <p class="text-sm text-gray-600 dark:text-gray-300">{{ form.descripcion }}</p>
            </div>
          </div>

          <!-- Location Section -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">UBICACIÓN REPORTADA</h3>
            <div class="flex flex-col md:flex-row gap-4 items-start">
              <div class="flex-1">
                <p class="text-gray-800 dark:text-gray-200 font-medium">{{ form.direccion }}</p>
                <p v-if="form.referencia" class="text-sm text-gray-600 dark:text-gray-300 mt-1">{{ form.referencia }}</p>
                <div class="flex gap-4 mt-2 text-xs text-gray-500">
                  <span>Lat: {{ form.ubicacion.latitud }}</span>
                  <span>Lng: {{ form.ubicacion.longitud }}</span>
                </div>
              </div>
              <div class="w-full md:w-48 h-32 rounded-lg overflow-hidden shrink-0 bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-700">
                <div class="w-full h-full flex items-center justify-center text-gray-400">
                  <span class="material-symbols-outlined text-4xl">map</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Evidence Section -->
          <div v-if="form.evidencias && form.evidencias.length > 0">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">EVIDENCIA ADJUNTA</h3>
            <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
              <div v-for="(evidencia, index) in form.evidencias" :key="index"
                   class="aspect-square bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden flex items-center justify-center">
                <span class="material-symbols-outlined text-gray-400 text-3xl">image</span>
              </div>
            </div>
          </div>

          <!-- Confirmation Checkbox -->
          <div class="pt-6 border-t border-gray-200 dark:border-gray-700">
            <label class="flex items-start gap-3 cursor-pointer">
              <input v-model="acceptedTerms" type="checkbox"
                     class="mt-1 h-5 w-5 rounded border-gray-300 dark:border-gray-600 text-primary focus:ring-primary bg-white dark:bg-gray-900">
              <span class="text-sm text-gray-700 dark:text-gray-300">
                Declaro bajo juramento que la información proporcionada es veraz y acepto los términos y condiciones del servicio.
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row justify-between gap-4 mt-8 px-4 sm:px-6">
        <button v-if="currentStep > 1" @click="previousStep"
                class="flex items-center justify-center gap-2 px-6 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-bold hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
          <span class="material-symbols-outlined">arrow_back</span>
          <span>Atrás</span>
        </button>
        <div v-else></div>
        
        <button v-if="currentStep < 4" @click="nextStep"
                :disabled="!canContinue"
                :class="[
                  'flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold transition-colors',
                  canContinue
                    ? 'bg-primary text-white hover:bg-primary/90'
                    : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                ]">
          <span>Continuar</span>
          <span class="material-symbols-outlined">arrow_forward</span>
        </button>
        <button v-else @click="submitDenuncia"
                :disabled="!acceptedTerms"
                :class="[
                  'flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold transition-colors',
                  acceptedTerms
                    ? 'bg-green-600 text-white hover:bg-green-700'
                    : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                ]">
          <span class="material-symbols-outlined">send</span>
          <span>Enviar Denuncia</span>
        </button>
      </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix para los iconos de Leaflet en Vite/Webpack
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

const ciudadano = ref({
  nombre: 'Juan',
  apellido: 'Pérez'
})

const currentStep = ref(1)

const steps = [
  { 
    number: 1, 
    label: 'Paso 1: Categoría',
    title: 'Crear Nueva Denuncia',
    description: 'Para comenzar, elija el tipo de problema que desea reportar.'
  },
  { 
    number: 2, 
    label: 'Paso 2: Detalles',
    title: 'Describe el Problema',
    description: 'Proporcione información detallada sobre el problema.'
  },
  { 
    number: 3, 
    label: 'Paso 3: Ubicación',
    title: 'Ubicación del Hecho',
    description: 'Indique dónde se encuentra el problema reportado.'
  },
  { 
    number: 4, 
    label: 'Paso 4: Confirmación',
    title: 'Confirmar y Enviar',
    description: 'Revise la información antes de enviar su denuncia.'
  }
]

const categories = ref([
  {
    id: 1,
    name: 'Alumbrado Público',
    description: 'Postes dañados, lámparas quemadas o zonas sin iluminación.',
    icon: 'lightbulb',
    iconColor: 'text-yellow-600 dark:text-yellow-400',
    bgColor: 'bg-yellow-100 dark:bg-yellow-900/50',
    avgTime: '72 horas'
  },
  {
    id: 2,
    name: 'Vialidad y Bacheo',
    description: 'Baches, pavimento dañado o problemas en calles y avenidas.',
    icon: 'route',
    iconColor: 'text-orange-600 dark:text-orange-400',
    bgColor: 'bg-orange-100 dark:bg-orange-900/50',
    avgTime: '5 días'
  },
  {
    id: 3,
    name: 'Limpia y Recolección de Basura',
    description: 'Basura acumulada en la vía pública o fallas en el servicio.',
    icon: 'recycling',
    iconColor: 'text-green-600 dark:text-green-400',
    bgColor: 'bg-green-100 dark:bg-green-900/50',
    avgTime: '48 horas'
  },
  {
    id: 4,
    name: 'Fugas de Agua',
    description: 'Tuberías rotas, alcantarillas obstruidas o desperdicio de agua.',
    icon: 'water_drop',
    iconColor: 'text-blue-600 dark:text-blue-400',
    bgColor: 'bg-blue-100 dark:bg-blue-900/50',
    avgTime: '24 horas'
  },
  {
    id: 5,
    name: 'Parques y Jardines',
    description: 'Mantenimiento de áreas verdes, juegos o mobiliario.',
    icon: 'park',
    iconColor: 'text-teal-600 dark:text-teal-400',
    bgColor: 'bg-teal-100 dark:bg-teal-900/50',
    avgTime: '7 días'
  },
  {
    id: 6,
    name: 'Semáforos Descompuestos',
    description: 'Semáforos que no funcionan o están mal sincronizados.',
    icon: 'traffic',
    iconColor: 'text-red-600 dark:text-red-400',
    bgColor: 'bg-red-100 dark:bg-red-900/50',
    avgTime: '8 horas'
  }
])

const selectedCategory = ref(null)

const form = ref({
  titulo: '',
  descripcion: '',
  ubicacion: {
    direccion: '',
    referencia: '',
    latitud: '-12.0464',
    longitud: '-77.0428'
  }
})

const evidencias = ref([])
const fileInput = ref(null)
const acceptedTerms = ref(false)

let map = null
let marker = null

const canContinue = computed(() => {
  if (currentStep.value === 1) {
    return selectedCategory.value !== null
  }
  if (currentStep.value === 2) {
    return form.value.titulo && form.value.descripcion
  }
  if (currentStep.value === 3) {
    return form.value.direccion && form.value.ubicacion.latitud && form.value.ubicacion.longitud
  }
  return true
})

const selectCategory = (category) => {
  selectedCategory.value = category
}

const nextStep = () => {
  if (canContinue.value && currentStep.value < 4) {
    currentStep.value++
    
    // Inicializar el mapa cuando llegue al paso 3
    if (currentStep.value === 3) {
      setTimeout(() => initMap(), 100)
    }
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const initMap = () => {
  const mapElement = document.getElementById('map')
  if (!mapElement || map) return
  
  // Coordenadas iniciales (Lima, Perú por defecto)
  const lat = parseFloat(form.value.ubicacion.latitud)
  const lng = parseFloat(form.value.ubicacion.longitud)
  
  // Crear el mapa con Leaflet
  map = L.map('map', {
    center: [lat, lng],
    zoom: 15,
    zoomControl: true
  })
  
  // Agregar capa de tiles de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map)
  
  // Crear marcador arrastrable en la posición inicial
  marker = L.marker([lat, lng], {
    draggable: true,
    autoPan: true
  }).addTo(map)
  
  // Popup con instrucciones
  marker.bindPopup('<b>Ubicación de la denuncia</b><br>Arrastra el marcador para ajustar').openPopup()
  
  // Actualizar coordenadas cuando se arrastra el marcador
  marker.on('dragend', function(e) {
    const position = marker.getLatLng()
    form.value.ubicacion.latitud = position.lat.toFixed(6)
    form.value.ubicacion.longitud = position.lng.toFixed(6)
    
    // Centrar el mapa en la nueva posición
    map.panTo(position)
  })
  
  // Permitir hacer clic en el mapa para mover el marcador
  map.on('click', function(e) {
    const { lat, lng } = e.latlng
    marker.setLatLng([lat, lng])
    form.value.ubicacion.latitud = lat.toFixed(6)
    form.value.ubicacion.longitud = lng.toFixed(6)
    map.panTo([lat, lng])
  })
  
  console.log('Mapa Leaflet inicializado en:', lat, lng)
}

const useCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        
        // Actualizar coordenadas en el formulario
        form.value.ubicacion.latitud = lat.toFixed(6)
        form.value.ubicacion.longitud = lng.toFixed(6)
        
        // Actualizar el mapa y marcador si están inicializados
        if (map && marker) {
          const newPosition = [lat, lng]
          marker.setLatLng(newPosition)
          map.setView(newPosition, 16) // Zoom un poco más cercano
          marker.bindPopup('<b>Tu ubicación actual</b>').openPopup()
        }
        
        console.log('Ubicación actual obtenida:', lat, lng)
      },
      (error) => {
        console.error('Error obteniendo ubicación:', error)
        let mensaje = 'No se pudo obtener tu ubicación.'
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            mensaje = 'Permiso denegado. Por favor, permite el acceso a tu ubicación en la configuración del navegador.'
            break
          case error.POSITION_UNAVAILABLE:
            mensaje = 'Información de ubicación no disponible.'
            break
          case error.TIMEOUT:
            mensaje = 'La solicitud de ubicación expiró.'
            break
        }
        
        alert(mensaje)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    )
  } else {
    alert('Tu navegador no soporta geolocalización.')
  }
}

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files)
  
  // Limitar a 5 imágenes
  const availableSlots = 5 - evidencias.value.length
  const filesToAdd = files.slice(0, availableSlots)
  
  filesToAdd.forEach(file => {
    // Validar tamaño (5MB máximo)
    if (file.size > 5 * 1024 * 1024) {
      alert(`El archivo ${file.name} excede el tamaño máximo de 5MB`)
      return
    }
    
    // Validar tipo
    if (!file.type.startsWith('image/')) {
      alert(`El archivo ${file.name} no es una imagen válida`)
      return
    }
    
    // Crear preview
    const reader = new FileReader()
    reader.onload = (e) => {
      evidencias.value.push({
        file: file,
        url: e.target.result,
        name: file.name
      })
    }
    reader.readAsDataURL(file)
  })
  
  // Limpiar input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  
  if (filesToAdd.length < files.length) {
    alert('Solo se pueden adjuntar hasta 5 imágenes. Algunas no fueron agregadas.')
  }
}

const removeImage = (index) => {
  evidencias.value.splice(index, 1)
}

const submitDenuncia = async () => {
  if (!acceptedTerms.value) return
  
  // Aquí irá la lógica para enviar al backend
  console.log('Enviando denuncia:', {
    categoria: selectedCategory.value,
    ...form.value
  })
  
  // TODO: Llamar al API para registrar la denuncia
  // const response = await api.post('/denuncias', {...})
  // const denunciaId = response.data.id
  
  // Simular respuesta del backend
  const denunciaId = Math.floor(Math.random() * 1000) + 1 // ID simulado
  const codigoDenuncia = `DEN-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 10000)).padStart(5, '0')}`
  const numeroSeguimiento = `TRK-${Date.now()}`
  
  // Redirigir a la pantalla de éxito con los códigos
  router.push({
    name: 'ciudadano-denuncia-exitosa',
    query: {
      id: denunciaId,
      codigo: codigoDenuncia,
      seguimiento: numeroSeguimiento
    }
  })
}

// Limpiar el mapa cuando el componente se desmonte para evitar memory leaks
onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    marker = null
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

/* Asegurar que el mapa de Leaflet tenga la altura correcta */
#map {
  height: 100%;
  width: 100%;
  z-index: 0;
}

/* Ajustar el panel de información sobre el mapa */
.absolute {
  z-index: 1000;
}
</style>
