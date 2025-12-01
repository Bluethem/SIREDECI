// Utilidades de roles/permisos para el frontend admin

const getAdminUser = () => {
  try {
    const raw = localStorage.getItem('admin_user')
    if (!raw) return null
    return JSON.parse(raw)
  } catch (e) {
    return null
  }
}

export const getRoles = () => {
  const user = getAdminUser()
  return Array.isArray(user?.roles) ? user.roles : []
}

export const hasRole = (codigoRol) => {
  return getRoles().includes(codigoRol)
}

export const hasAnyRole = (roles) => {
  const current = new Set(getRoles())
  return (roles || []).some((r) => current.has(r))
}

export const isSuperAdmin = () => hasRole('ROL-001')
export const isAdmin = () => hasRole('ROL-002')
export const isJefeArea = () => hasRole('ROL-003')
export const isOperador = () => hasRole('ROL-004')
export const isAuditor = () => hasRole('ROL-006')

// Ruta "home" recomendada según rol principal
export const getDefaultAdminRoute = () => {
  if (isSuperAdmin() || isAdmin()) return '/admin/dashboard'
  if (isJefeArea()) return '/municipal/dashboard'
  if (isOperador()) return '/municipal/mi-area'
  if (isAuditor()) return '/admin/reportes'
  return '/admin/dashboard'
}
