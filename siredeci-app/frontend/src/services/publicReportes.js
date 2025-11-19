import api from './api'

// Servicio para consumir endpoints públicos de reportes (/api/public/reportes/*)

export async function fetchPublicReportes(params = {}) {
  const response = await api.get('/public/reportes/reportes/', { params })
  return response.data
}

export async function fetchPublicReporteDetail(codigo) {
  const response = await api.get(`/public/reportes/reportes/${codigo}/`)
  return response.data
}

export async function fetchPublicDashboards(params = {}) {
  const response = await api.get('/public/reportes/dashboards/', { params })
  return response.data
}

export async function fetchPublicDashboardDetail(codigo) {
  const response = await api.get(`/public/reportes/dashboards/${codigo}/`)
  return response.data
}

export async function fetchPublicIndicadorDetail(codigo) {
  const response = await api.get(`/public/reportes/indicadores/${codigo}/`)
  return response.data
}

export async function fetchPublicIndicadorSerie(codigo, params = {}) {
  const response = await api.get(`/public/reportes/indicadores/${codigo}/serie/`, { params })
  return response.data
}

export async function fetchPublicTendencias(params = {}) {
  const response = await api.get('/public/reportes/tendencias-geograficas/', { params })
  return response.data
}

export async function fetchPublicRankingAreas(params = {}) {
  const response = await api.get('/public/reportes/ranking-areas/', { params })
  return response.data
}
