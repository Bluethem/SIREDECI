import api from './api'

/**
 * Servicio para gestión de denuncias
 */
export const denunciasService = {
  /**
   * Obtener todas las denuncias del ciudadano autenticado
   * @param {Object} params - Parámetros de filtrado (estado, search, etc.)
   * @returns {Promise}
   */
  async getMisDenuncias(params = {}) {
    try {
      // Obtener id_ciudadano del localStorage
      const userStr = localStorage.getItem('user')
      if (userStr) {
        try {
          const user = JSON.parse(userStr)
          if (user.id_ciudadano) {
            params.id_ciudadano = user.id_ciudadano
          }
        } catch (e) {
          console.error('Error parseando user:', e)
        }
      }
      
      const response = await api.get('/denuncias/mis-denuncias/', { params })
      
      // El backend puede retornar un array directamente o un objeto con results
      if (Array.isArray(response.data)) {
        return response.data
      } else if (response.data && Array.isArray(response.data.results)) {
        // Si hay paginación, retornar solo los resultados
        return response.data.results
      } else {
        console.error('Formato de respuesta inesperado:', response.data)
        return []
      }
    } catch (error) {
      // En desarrollo, si no hay token, retornar array vacío
      if (import.meta.env.DEV && error.response?.status === 401) {
        console.warn('⚠️ No hay token de autenticación. Retornando denuncias vacías.')
        return []
      }
      throw error
    }
  },

  /**
   * Obtener detalle de una denuncia
   * @param {number} id - ID de la denuncia
   * @returns {Promise}
   */
  async getDenuncia(id) {
    const response = await api.get(`/denuncias/${id}/`)
    return response.data
  },

  /**
   * Crear una nueva denuncia
   * @param {Object|FormData} denunciaData - Datos de la denuncia o FormData (cuando se envían evidencias)
   * @returns {Promise}
   */
  async crearDenuncia(denunciaData) {
    const config = {}

    // Si se envía FormData, ajustar encabezado para multipart
    if (denunciaData instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      }
    }

    const response = await api.post('/denuncias/', denunciaData, config)
    return response.data
  },

  /**
   * Actualizar una denuncia
   * @param {number} id - ID de la denuncia
   * @param {Object} denunciaData - Datos a actualizar
   * @returns {Promise}
   */
  async actualizarDenuncia(id, denunciaData) {
    const response = await api.patch(`/denuncias/${id}/`, denunciaData)
    return response.data
  },

  /**
   * Cerrar una denuncia
   * @param {number} id - ID de la denuncia
   * @returns {Promise}
   */
  async cerrarDenuncia(id) {
    const response = await api.delete(`/denuncias/${id}/`)
    return response.data
  },

  /**
   * Obtener estadísticas de denuncias
   * @param {number} idCiudadano - ID del ciudadano (opcional)
   * @returns {Promise}
   */
  async getEstadisticas(idCiudadano = null) {
    const params = idCiudadano ? { id_ciudadano: idCiudadano } : {}
    const response = await api.get('/denuncias/estadisticas/', { params })
    return response.data
  },

  /**
   * Consultar denuncia por número de seguimiento (público)
   * @param {string} numeroSeguimiento - Número de seguimiento
   * @returns {Promise}
   */
  async consultarPorSeguimiento(numeroSeguimiento) {
    const response = await api.get(`/publico/denuncias/seguimiento/${numeroSeguimiento}/`)
    return response.data
  },

  /**
   * Listar denuncias públicas
   * @param {Object} params - Parámetros de filtrado
   * @returns {Promise}
   */
  async getDenunciasPublicas(params = {}) {
    const response = await api.get('/publico/denuncias/', { params })
    return response.data
  },

  /**
   * Buscar denuncia pública por código o número de seguimiento
   * @param {string} codigo - Código de denuncia o número de seguimiento
   * @returns {Promise}
   */
  async buscarDenunciaPublica(codigo) {
    try {
      // Buscar usando el parámetro de búsqueda
      const response = await api.get('/publico/denuncias/', {
        params: { search: codigo }
      })
      
      // El backend puede retornar un array directamente o un objeto con results
      let denuncias = []
      if (Array.isArray(response.data)) {
        denuncias = response.data
      } else if (response.data && Array.isArray(response.data.results)) {
        denuncias = response.data.results
      }
      
      console.log('Denuncias encontradas:', denuncias)
      
      // Si encuentra resultados, retornar el primero
      if (denuncias.length > 0) {
        // Si es una búsqueda exacta por código, encontrar la coincidencia exacta
        const exactMatch = denuncias.find(
          d => d.codigo_denuncia === codigo || d.numero_seguimiento === codigo
        )
        return exactMatch || denuncias[0]
      }
      
      throw new Error('No se encontró la denuncia')
    } catch (error) {
      throw error
    }
  }
}

export default denunciasService
