import { ref, watch } from 'vue'

// Estado reactivo para el tema
const isDark = ref(false)

// Inicializar desde localStorage o preferencia del sistema
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    // Detectar preferencia del sistema
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  
  applyTheme()
}

// Aplicar el tema al documento
const applyTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Watch para aplicar cambios automáticamente
watch(isDark, () => {
  applyTheme()
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
})

// Alternar tema
const toggleTheme = () => {
  isDark.value = !isDark.value
}

// Exportar funciones y estado
export const useTheme = () => {
  return {
    isDark,
    toggleTheme,
    initTheme
  }
}
