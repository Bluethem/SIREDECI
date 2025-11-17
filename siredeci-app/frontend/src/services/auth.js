import api from './api'

/**
 * Servicio de autenticación
 */
export const authService = {
  /**
   * Login de ciudadano con DNI + Fecha de Emisión
   * @param {string} dni - DNI del ciudadano
   * @param {string} fechaEmision - Fecha de emisión del DNI (YYYY-MM-DD)
   * @returns {Promise}
   */
  async loginCiudadano(dni, fechaEmision) {
    const response = await api.post('/ciudadanos/login/', {
      dni,
      fecha_emision: fechaEmision
    })
    
    // Guardar datos en localStorage
    if (response.data.ciudadano) {
      localStorage.setItem('user', JSON.stringify(response.data.ciudadano))
      localStorage.setItem('token', response.data.ciudadano.session_token)
      localStorage.setItem('tipo_usuario', 'ciudadano')
    }
    
    return response.data
  },

  /**
   * Registro de nuevo ciudadano
   * @param {Object} data - Datos del ciudadano
   * @returns {Promise}
   */
  async registrarCiudadano(data) {
    const response = await api.post('/ciudadanos/registro/', data)
    return response.data
  },

  /**
   * Logout
   */
  logout() {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    localStorage.removeItem('tipo_usuario')
  },

  /**
   * Verificar si hay sesión activa
   * @returns {boolean}
   */
  isAuthenticated() {
    return !!localStorage.getItem('token') && !!localStorage.getItem('user')
  },

  /**
   * Obtener usuario actual
   * @returns {Object|null}
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  /**
   * Verificar si es ciudadano
   * @returns {boolean}
   */
  isCiudadano() {
    return localStorage.getItem('tipo_usuario') === 'ciudadano'
  }
}

export default authService
