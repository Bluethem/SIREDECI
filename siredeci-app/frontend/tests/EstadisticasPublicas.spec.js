import { mount } from '@vue/test-utils'
import EstadisticasPublicas from '@/views/public/EstadisticasPublicas.vue'
import axios from 'axios'

// Mock global de axios para evitar llamadas HTTP reales y soportar axios.create usado en services/api.js
vi.mock('axios', () => {
  const instance = {
    get: vi.fn((url) => {
      if (url.includes('estadisticas/denuncias-resumen')) {
        return Promise.resolve({
          data: {
            stats: { total: 10, resueltas: 5, en_proceso: 3, tiempo_promedio_horas: 24 },
            categorias: [],
            estados: [],
            distritos: [],
          },
        })
      }
      if (url.includes('tendencias-geograficas')) {
        return Promise.resolve({ data: { results: [] } })
      }
      if (url.includes('ranking-areas')) {
        return Promise.resolve({ data: { results: [] } })
      }
      return Promise.resolve({ data: {} })
    }),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  }

  return {
    default: {
      create: vi.fn(() => instance),
      get: instance.get,
      post: instance.post,
    },
    __esModule: true,
  }
})

const mountWithRouterStubs = () => {
  return mount(EstadisticasPublicas, {
    global: {
      stubs: {
        'router-link': { template: '<a><slot /></a>' },
        'router-view': true,
      },
      mocks: {
        $route: { path: '/public/estadisticas' },
        $router: {
          push: vi.fn(),
        },
      },
    },
  })
}

// Por ahora solo comprobamos que la vista de estadísticas públicas se renderiza.

describe('EstadisticasPublicas', () => {
  test('renderiza la cabecera de estadísticas públicas', async () => {
    const wrapper = mountWithRouterStubs()

    // Esperar a que se resuelvan las llamadas iniciales en onMounted
    await Promise.resolve()
    await Promise.resolve()

    expect(wrapper.text()).toContain('Estadísticas Públicas')
  })
})
