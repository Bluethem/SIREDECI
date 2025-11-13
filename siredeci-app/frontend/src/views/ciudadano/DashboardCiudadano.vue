<template>
  <div class="min-h-screen w-full flex flex-col items-center justify-center p-4 bg-background-light dark:bg-background-dark">
    <div class="w-full max-w-md">
      <!-- Header -->
      <header class="mb-8">
        <div class="flex flex-col items-center text-center">
          <h1 class="text-gray-900 dark:text-gray-100 tracking-light text-[32px] font-bold leading-tight">
            Sistema de Denuncias Ciudadanas
          </h1>
          <p class="text-primary text-xl font-semibold">(SIREDECI)</p>
        </div>
      </header>

      <!-- Main Card -->
      <main class="w-full">
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg rounded-xl">
          <div class="p-8">
            <!-- Welcome Section -->
            <div class="mb-8 text-center">
              <h2 class="text-[#101619] dark:text-gray-50 text-3xl font-black leading-tight tracking-[-0.033em] mb-2">
                Bienvenido, {{ nombreCiudadano }}
              </h2>
              <p class="text-[#587d8d] dark:text-slate-400 text-base font-normal leading-normal">
                ¿Qué deseas hacer hoy?
              </p>
            </div>

            <!-- Action Buttons -->
            <div class="space-y-4">
              <!-- Mis Denuncias Button -->
              <button
                @click="goToMisDenuncias"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-14 px-5 bg-primary text-gray-50 text-base font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] transition-colors duration-200 gap-2"
              >
                <span class="material-symbols-outlined">search</span>
                <span class="truncate">Consultar mis Denuncias</span>
              </button>

              <!-- Nueva Denuncia Button -->
              <button
                @click="goToNuevaDenuncia"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-14 px-5 bg-primary text-gray-50 text-base font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] transition-colors duration-200 gap-2"
              >
                <span class="material-symbols-outlined">add_circle</span>
                <span class="truncate">Registrar Nueva Denuncia</span>
              </button>

              <!-- Estadísticas Públicas Button -->
              <button
                @click="goToEstadisticas"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-14 px-5 bg-primary/10 text-primary dark:bg-primary/20 dark:hover:bg-primary/30 hover:bg-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] text-base font-bold leading-normal tracking-[0.015em] transition-colors duration-200 gap-2"
              >
                <span class="material-symbols-outlined">bar_chart</span>
                <span class="truncate">Ver Estadísticas Públicas</span>
              </button>

              <!-- Divider -->
              <div class="relative flex items-center justify-center my-4">
                <div class="h-px w-full bg-slate-200 dark:bg-slate-700"></div>
                <span class="absolute bg-white dark:bg-[#131b1f] px-2 text-sm text-slate-500 dark:text-slate-400">o</span>
              </div>

              <!-- Consulta Pública Button -->
              <button
                @click="goToConsultaPublica"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-transparent text-primary border border-primary hover:bg-primary/10 dark:hover:bg-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] text-base font-bold leading-normal tracking-[0.015em] transition-colors duration-200 gap-2"
              >
                <span class="material-symbols-outlined">public</span>
                <span class="truncate">Consultar Denuncia Pública</span>
              </button>

              <!-- Cerrar Sesión Button -->
              <button
                @click="handleLogout"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-transparent text-red-600 dark:text-red-400 border border-red-600 dark:border-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500/50 dark:focus:ring-offset-[#131b1f] text-base font-bold leading-normal tracking-[0.015em] transition-colors duration-200 gap-2"
              >
                <span class="material-symbols-outlined">logout</span>
                <span class="truncate">Cerrar Sesión</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          © 2025 Municipalidad. Todos los derechos reservados.
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const nombreCiudadano = ref('Juan Pérez')

onMounted(() => {
  // TODO: Obtener el nombre del ciudadano del localStorage o API
  // const user = JSON.parse(localStorage.getItem('user'))
  // nombreCiudadano.value = user.nombre + ' ' + user.apellido
})

const goToMisDenuncias = () => {
  router.push({ name: 'ciudadano-mis-denuncias' })
}

const goToNuevaDenuncia = () => {
  // TODO: Implementar ruta de nueva denuncia
  router.push({ name: 'ciudadano-registrar-denuncia' })
}

const goToEstadisticas = () => {
  router.push({ name: 'estadisticas-publicas' })
}

const goToConsultaPublica = () => {
  router.push({ name: 'consulta-publica' })
}

const handleLogout = () => {
  // TODO: Limpiar localStorage y redirigir
  // localStorage.removeItem('token')
  // localStorage.removeItem('user')
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
</style>
