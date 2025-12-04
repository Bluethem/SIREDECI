import { mount } from '@vue/test-utils'
import MisDenuncias from '@/views/ciudadano/MisDenuncias.vue'

// Mock del servicio de denuncias para evitar llamadas HTTP reales
vi.mock('@/services/denuncias', () => ({
  default: {
    // getMisDenuncias devuelve una lista pequeña de ejemplo
    getMisDenuncias: vi.fn().mockResolvedValue([
      {
        id_denuncia: 1,
        codigo_denuncia: 'DEN-001',
        titulo: 'Bache en la calle',
        categoria_nombre: 'Vialidad y Bacheo',
        estado: 'Registrado',
        prioridad: 'Media',
        fecha_registro: '2025-01-01T00:00:00Z',
        direccion: 'Av. Siempre Viva 123',
        distrito: 'Lima',
      },
    ]),
  },
}))

const mountWithRouterStubs = () => {
  return mount(MisDenuncias, {
    global: {
      stubs: {
        'router-link': { template: '<a><slot /></a>' },
        'router-view': true,
      },
      mocks: {
        $route: { path: '/ciudadano/mis-denuncias' },
        $router: {
          push: vi.fn(),
        },
      },
    },
  })
}

describe('MisDenuncias', () => {
  test('monta el componente de mis denuncias sin errores', async () => {
    const wrapper = mountWithRouterStubs()

    // Esperar a que se resuelva la carga inicial (onMounted + llamada mock)
    await Promise.resolve()
    await Promise.resolve()

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text().toLowerCase()).toContain('mis denuncias')
  })
})
