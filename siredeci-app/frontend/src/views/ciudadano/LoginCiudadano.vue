<template>
  <div class="min-h-screen w-full flex flex-col items-center justify-center p-4 bg-gray-50 dark:bg-[#131b1f]">
    <div class="w-full max-w-md">
      <!-- Header -->
      <header class="mb-8">
        <div class="flex flex-col items-center text-center">
          <h1 class="text-[#101619] dark:text-gray-100 tracking-light text-[32px] font-bold leading-tight">
            Sistema de Denuncias Ciudadanas
          </h1>
          <p class="text-primary text-xl font-semibold">(SIREDECI)</p>
        </div>
      </header>

      <!-- Main Card -->
      <main class="w-full">
        <div class="bg-white dark:bg-[#131b1f] dark:border dark:border-slate-800 shadow-lg rounded-xl">
          <div class="p-8">
            <!-- Title Section -->
            <div class="mb-8 text-center">
              <h2 class="text-[#101619] dark:text-gray-50 text-3xl font-black leading-tight tracking-[-0.033em] mb-2">
                Iniciar Sesión
              </h2>
              <p class="text-[#587d8d] dark:text-slate-400 text-base font-normal leading-normal">
                Ingrese sus credenciales para continuar
              </p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-6">
              <!-- DNI Input -->
              <div>
                <label for="dni" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Documento Nacional de Identidad (DNI)
                </label>
                <div class="relative">
                  <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-gray-400">
                    <span class="material-symbols-outlined text-xl">badge</span>
                  </span>
                  <input
                    v-model="formData.dni"
                    type="text"
                    id="dni"
                    maxlength="8"
                    pattern="[0-9]{8}"
                    placeholder="Ingrese su DNI (8 dígitos)"
                    required
                    class="w-full h-14 pl-12 pr-4 rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors duration-200"
                  />
                </div>
                <p v-if="errors.dni" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.dni }}</p>
              </div>

              <!-- Fecha de Emisión Input -->
              <div>
                <label for="fecha_emision" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Fecha de Emisión del DNI
                </label>
                <div class="relative">
                  <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-gray-400">
                    <span class="material-symbols-outlined text-xl">calendar_today</span>
                  </span>
                  <input
                    v-model="formData.fecha_emision"
                    type="date"
                    id="fecha_emision"
                    required
                    class="w-full h-14 pl-12 pr-4 rounded-lg border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors duration-200"
                  />
                </div>
                <p v-if="errors.fecha_emision" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.fecha_emision }}</p>
              </div>

              <!-- Error Message -->
              <div v-if="errors.general" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p class="text-sm text-red-600 dark:text-red-400 flex items-center gap-2">
                  <span class="material-symbols-outlined text-lg">error</span>
                  {{ errors.general }}
                </p>
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                :disabled="loading"
                class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-14 px-5 bg-primary text-gray-50 text-base font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] transition-colors duration-200 gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="!loading" class="material-symbols-outlined">login</span>
                <span v-if="loading" class="material-symbols-outlined animate-spin">progress_activity</span>
                <span class="truncate">{{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
              </button>

              <!-- Divider -->
              <div class="relative flex items-center justify-center my-4">
                <div class="h-px w-full bg-slate-200 dark:bg-slate-700"></div>
                <span class="absolute bg-white dark:bg-[#131b1f] px-2 text-sm text-slate-500 dark:text-slate-400">o</span>
              </div>

              <!-- Public Access Buttons -->
              <div class="space-y-3">
                <button
                  type="button"
                  @click="goToConsultaPublica"
                  class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-primary/10 text-primary dark:bg-primary/20 dark:hover:bg-primary/30 hover:bg-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] text-sm font-bold leading-normal tracking-[0.015em] transition-colors duration-200 gap-2"
                >
                  <span class="material-symbols-outlined text-lg">search</span>
                  <span class="truncate">Consultar Denuncia Pública</span>
                </button>

                <button
                  type="button"
                  @click="goToEstadisticas"
                  class="flex min-w-[84px] w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-transparent text-primary border border-primary hover:bg-primary/10 dark:hover:bg-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 dark:focus:ring-offset-[#131b1f] text-sm font-bold leading-normal tracking-[0.015em] transition-colors duration-200 gap-2"
                >
                  <span class="material-symbols-outlined text-lg">bar_chart</span>
                  <span class="truncate">Ver Estadísticas Públicas</span>
                </button>
              </div>
            </form>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)

const formData = ref({
  dni: '',
  fecha_emision: ''
})

const errors = ref({
  dni: '',
  fecha_emision: '',
  general: ''
})

const validateForm = () => {
  errors.value = { dni: '', fecha_emision: '', general: '' }
  let isValid = true

  // Validar DNI
  if (!formData.value.dni || formData.value.dni.length !== 8) {
    errors.value.dni = 'El DNI debe tener exactamente 8 dígitos'
    isValid = false
  } else if (!/^\d{8}$/.test(formData.value.dni)) {
    errors.value.dni = 'El DNI debe contener solo números'
    isValid = false
  }

  // Validar fecha de emisión
  if (!formData.value.fecha_emision) {
    errors.value.fecha_emision = 'La fecha de emisión es requerida'
    isValid = false
  } else {
    const fechaEmision = new Date(formData.value.fecha_emision)
    const hoy = new Date()
    if (fechaEmision > hoy) {
      errors.value.fecha_emision = 'La fecha de emisión no puede ser futura'
      isValid = false
    }
  }

  return isValid
}

const handleLogin = async () => {
  if (!validateForm()) return

  loading.value = true
  errors.value.general = ''

  try {
    // TODO: Llamar al API de autenticación
    // const response = await loginCiudadano(formData.value)
    
    // Simulación de login (remover cuando se integre con backend)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Si el login es exitoso, guardar token y redirigir
    // localStorage.setItem('token', response.data.token)
    // localStorage.setItem('user', JSON.stringify(response.data.user))
    
    router.push({ name: 'ciudadano-dashboard' })
  } catch (error) {
    errors.value.general = error.response?.data?.message || 'DNI o fecha de emisión incorrectos. Por favor, verifique sus datos.'
  } finally {
    loading.value = false
  }
}

const goToConsultaPublica = () => {
  router.push({ name: 'consulta-publica' })
}

const goToEstadisticas = () => {
  router.push({ name: 'estadisticas-publicas' })
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
