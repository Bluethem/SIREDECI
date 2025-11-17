import axios from 'axios'

// Configuración base de axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para agregar token de autenticación (DESHABILITADO para ciudadanos)
// Los ciudadanos no usan token Bearer, solo envían id_ciudadano
api.interceptors.request.use(
  (config) => {
    // NO agregar Authorization header para ciudadanos
    // La autenticación se hace por id_ciudadano en los datos
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      console.warn('⚠️ Error 401: No autenticado')
      console.warn('💡 Si el problema persiste, cierra sesión e inicia sesión nuevamente')
      
      // NO redirigir automáticamente - dejar que cada componente maneje el error
      // Esto evita interrumpir el flujo del usuario
    }
    return Promise.reject(error)
  }
)

export default api
