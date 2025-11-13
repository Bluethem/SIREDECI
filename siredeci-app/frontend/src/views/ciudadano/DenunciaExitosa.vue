<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <NavbarCiudadano />
    <!-- Main Content -->
    <main class="flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
      <div class="w-full max-w-3xl bg-white dark:bg-gray-800 shadow-xl rounded-xl">
        <div class="flex flex-col items-center p-8 md:p-12">
          <!-- Success Icon -->
          <div class="flex items-center justify-center w-20 h-20 rounded-full bg-green-100 dark:bg-green-900/50 mb-6">
            <span class="material-symbols-outlined text-green-500 dark:text-green-400" style="font-size: 48px;">
              check_circle
            </span>
          </div>

          <!-- Title -->
          <h1 class="text-gray-900 dark:text-white text-3xl font-bold text-center pb-3">
            ¡Denuncia registrada exitosamente!
          </h1>

          <!-- Description -->
          <p class="text-gray-600 dark:text-gray-300 text-base text-center max-w-lg pb-8 pt-1">
            Su denuncia ha sido procesada. Guarde los siguientes códigos para referencia futura y seguimiento de su caso.
          </p>

          <!-- Codes Section -->
          <div class="w-full border-t border-b border-gray-200 dark:border-gray-700 grid grid-cols-1 sm:grid-cols-2 divide-y sm:divide-y-0 sm:divide-x divide-gray-200 dark:divide-gray-700">
            <!-- Complaint Code -->
            <div class="flex flex-col gap-1 py-5 sm:pr-4">
              <p class="text-gray-500 dark:text-gray-400 text-sm">Código de Denuncia:</p>
              <div class="flex items-center gap-2">
                <p class="text-gray-900 dark:text-white text-base font-semibold font-mono">
                  {{ codigoDenuncia }}
                </p>
                <button @click="copiarCodigo(codigoDenuncia)" 
                        aria-label="Copiar código de denuncia"
                        class="text-gray-500 dark:text-gray-400 hover:text-primary">
                  <span class="material-symbols-outlined text-lg">content_copy</span>
                </button>
              </div>
            </div>

            <!-- Tracking Number -->
            <div class="flex flex-col gap-1 py-5 sm:pl-4">
              <p class="text-gray-500 dark:text-gray-400 text-sm">Número de Seguimiento:</p>
              <div class="flex items-center gap-2">
                <p class="text-gray-900 dark:text-white text-base font-semibold font-mono">
                  {{ numeroSeguimiento }}
                </p>
                <button @click="copiarCodigo(numeroSeguimiento)"
                        aria-label="Copiar número de seguimiento"
                        class="text-gray-500 dark:text-gray-400 hover:text-primary">
                  <span class="material-symbols-outlined text-lg">content_copy</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8 w-full">
            <button @click="verDenuncia"
                    class="flex w-full sm:w-auto items-center justify-center px-6 py-3 rounded-lg bg-primary text-white font-bold hover:opacity-90 transition-opacity">
              Ver mi denuncia
            </button>
            <button @click="crearOtraDenuncia"
                    class="flex w-full sm:w-auto items-center justify-center px-6 py-3 rounded-lg bg-transparent text-primary border-2 border-primary font-bold hover:bg-primary/10 transition-colors">
              Crear otra denuncia
            </button>
          </div>

          <!-- Link to Home -->
          <router-link to="/ciudadano/dashboard"
                       class="mt-6 text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary">
            Volver al inicio
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'

const router = useRouter()
const route = useRoute()

// Códigos generados (en producción vendrían del backend)
const codigoDenuncia = ref('DEN-2025-00123')
const numeroSeguimiento = ref('TRK-9876543210')

onMounted(() => {
  // Si hay códigos en la query, usarlos
  if (route.query.codigo) {
    codigoDenuncia.value = route.query.codigo
  }
  if (route.query.seguimiento) {
    numeroSeguimiento.value = route.query.seguimiento
  }
})

const copiarCodigo = async (texto) => {
  try {
    await navigator.clipboard.writeText(texto)
    // TODO: Mostrar toast/notificación de éxito
    console.log('Código copiado:', texto)
  } catch (error) {
    console.error('Error al copiar:', error)
  }
}

const verDenuncia = () => {
  // Si hay ID en la query, ir directo al detalle
  if (route.query.id) {
    router.push({
      name: 'ciudadano-detalle-denuncia',
      params: { id: route.query.id }
    })
  } else {
    // Si no, ir a la lista de denuncias
    router.push('/ciudadano/mis-denuncias')
  }
}

const crearOtraDenuncia = () => {
  router.push('/ciudadano/registrar-denuncia')
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
</style>
