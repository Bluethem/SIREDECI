<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4">
    <header class="text-center mb-8">
      <img :src="logo" alt="SIREDECI Logo" class="mx-auto mb-4 h-24 w-24 object-contain" />
      <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">Sistema de Registro de Denuncias Ciudadanas</h1>
      <p class="text-lg text-primary font-medium">(SIREDECI)</p>
    </header>

    <main class="w-full max-w-md">
      <div class="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-8">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Iniciar Sesión - Personal Municipal</h2>
          <p class="text-slate-500 dark:text-slate-400 mt-1">Ingrese sus credenciales para continuar</p>
        </div>

        <form class="space-y-6" @submit.prevent="onSubmit">
          <!-- Mensaje de error general -->
          <div v-if="error" class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p class="text-sm text-red-600 dark:text-red-400 flex items-center gap-2">
              <span class="material-symbols-outlined text-lg">error</span>
              {{ error }}
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1" for="email">Email</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">mail</span>
              <input 
                v-model="form.email" 
                class="w-full pl-10 pr-3 py-2 border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:ring-primary focus:border-primary" 
                id="email" 
                name="email" 
                placeholder="Ingrese su email" 
                type="email"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1" for="password">Contraseña</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">lock</span>
              <input 
                v-model="form.password" 
                class="w-full pl-10 pr-3 py-2 border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:ring-primary focus:border-primary" 
                id="password" 
                name="password" 
                placeholder="Ingrese su contraseña" 
                type="password"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <button 
            :disabled="loading"
            class="w-full bg-primary text-white font-bold py-3 px-4 rounded-md flex items-center justify-center gap-2 hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-offset-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" 
            type="submit"
          >
            <span v-if="!loading" class="material-symbols-outlined">login</span>
            <span v-if="loading" class="material-symbols-outlined animate-spin">progress_activity</span>
            {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>

      </div>
    </main>

    <footer class="mt-8 text-center">
      <p class="text-sm text-slate-500 dark:text-slate-400">© 2025 Municipalidad. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script>
import logo from '@/assets/logo.png'
import axios from 'axios'

export default {
  name: 'LoginAdmin',
  data() {
    return {
      logo: logo,
      loading: false,
      error: '',
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    async onSubmit() {
      this.loading = true
      this.error = ''

      try {
        const response = await axios.post('/api/admin/login/', {
          email: this.form.email,
          password: this.form.password
        })

        // Guardar tokens en localStorage
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('admin_user', JSON.stringify(response.data.user))
        localStorage.setItem('admin_personal', JSON.stringify(response.data.personal))

        // Configurar el header de autorización para futuras peticiones
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

        // Redirigir al dashboard de admin (cuando esté creado)
        // Por ahora comentado hasta que se cree la ruta
        // this.$router.push('/admin/dashboard').catch(() => {})
        
        // Por ahora mostrar mensaje de éxito
        console.log('Login exitoso', response.data)
        alert('Login exitoso. El dashboard de administrador será creado próximamente.')
        
      } catch (error) {
        // Manejar errores de la API
        if (error.response) {
          // El servidor respondió con un código de estado fuera del rango 2xx
          const errorData = error.response.data
          this.error = errorData.message || errorData.error || 'Error al iniciar sesión. Por favor, verifique sus credenciales.'
        } else if (error.request) {
          // La petición fue hecha pero no se recibió respuesta
          this.error = 'No se pudo conectar con el servidor. Por favor, verifique su conexión.'
        } else {
          // Algo pasó al configurar la petición
          this.error = 'Error al procesar la solicitud. Por favor, intente nuevamente.'
        }
        console.error('Error en login:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
:deep(.material-symbols-outlined) {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
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
