import { mount } from '@vue/test-utils'
import RegistrarDenuncia from '@/views/ciudadano/RegistrarDenuncia.vue'

// Estos tests se centran en validación básica de UI. El envío real a la API
// puede mockearse más adelante (axios o servicio api).

const mountWithRouterStubs = () => {
  return mount(RegistrarDenuncia, {
    global: {
      stubs: {
        'router-link': {
          template: '<a><slot /></a>',
        },
        'router-view': true,
      },
      mocks: {
        $route: { path: '/ciudadano/denuncias/registrar' },
        $router: {
          push: vi.fn(),
        },
      },
    },
  })
}

describe('RegistrarDenuncia', () => {
  test('renderiza formulario de registro de denuncia', () => {
    const wrapper = mountWithRouterStubs()

    // El título inicial del paso 1 es "Crear Nueva Denuncia"
    expect(wrapper.text()).toContain('Crear Nueva Denuncia')
  })

  test('muestra el botón Continuar en el paso inicial', () => {
    const wrapper = mountWithRouterStubs()

    // Nos basta con verificar que el texto del botón "Continuar" aparece en la vista
    expect(wrapper.text()).toContain('Continuar')
  })
})
