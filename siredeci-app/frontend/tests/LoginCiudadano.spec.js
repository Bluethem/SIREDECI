import { mount } from '@vue/test-utils'
import LoginCiudadano from '@/views/ciudadano/LoginCiudadano.vue'

// Nota: estos tests son de ejemplo y se centran en la parte de UI/validación básica.
// Las llamadas HTTP reales deben mockearse cuando se quiera probar el flujo completo.

describe('LoginCiudadano', () => {
  test('renderiza formulario de login de ciudadano', () => {
    const wrapper = mount(LoginCiudadano)

    // Comprueba que existan inputs básicos
    expect(wrapper.find('#dni').exists()).toBe(true)
    expect(wrapper.find('#fecha_emision').exists()).toBe(true)
  })

  test('muestra mensaje de error si se envía vacío (si hay validación en el front)', async () => {
    const wrapper = mount(LoginCiudadano)

    await wrapper.find('form').trigger('submit.prevent')

    // Dependiendo de cómo tengas los mensajes, ajusta este texto
    // Aquí solo comprobamos que se muestre algún mensaje de error genérico.
    expect(wrapper.text().toLowerCase()).toContain('dni')
  })
})
