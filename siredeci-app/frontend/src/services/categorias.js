import api from './api'

/**
 * Servicio para gestión de categorías de denuncias
 */
export const categoriasService = {
  /**
   * Obtener lista de categorías activas (público)
   * @returns {Promise}
   */
  async getCategorias () {
    const response = await api.get('/categorias/')
    return response.data
  }
}

export default categoriasService
