<template>
  <div class="min-h-screen bg-background-light dark:bg-background-dark">
    <NavbarCiudadano />

    <main class="max-w-3xl mx-auto px-4 py-8">
      <section class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-sm p-6 mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div class="flex items-center gap-4">
          <div
            class="bg-center bg-no-repeat bg-cover rounded-full size-20 flex-shrink-0 ring-4 ring-primary/10"
            :style="avatarStyle"
          ></div>
          <div class="flex flex-col min-w-0">
            <h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-gray-50 truncate">
              {{ displayName }}
            </h1>
            <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
              DNI {{ user?.dni || '-' }}
            </p>
            <p v-if="user?.email" class="text-xs text-gray-500 dark:text-gray-400 truncate mt-1">
              {{ user.email }}
            </p>
          </div>
        </div>

        <div class="flex flex-col gap-1 text-sm text-gray-600 dark:text-gray-300 items-start md:items-end">
          <p class="text-xs uppercase tracking-wide text-gray-400 dark:text-gray-500">Cuenta</p>
          <p>
            Código:
            <span class="font-semibold text-gray-900 dark:text-gray-100 ml-1">{{ user?.codigo_ciudadano || '-' }}</span>
          </p>
        </div>
      </section>

      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Datos personales -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-50 flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">person</span>
            Datos personales
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div class="flex flex-col gap-1">
              <span class="text-gray-500 dark:text-gray-400">Nombre</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ user?.nombre || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500 dark:text-gray-400">Apellido</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ user?.apellido || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500 dark:text-gray-400">DNI</span>
              <span class="font-medium text-gray-900 dark:text-gray-100">{{ user?.dni || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500 dark:text-gray-400">Correo electrónico</span>
              <span class="font-medium text-gray-900 dark:text-gray-100 break-all">{{ user?.email || 'No registrado' }}</span>
            </div>
          </div>
        </div>

        <!-- Preferencias simples (sólo visual por ahora) -->
        <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-50 flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">notifications</span>
            Notificaciones
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-300">
            Puedes ajustar el detalle de tus notificaciones en el centro de notificaciones.
          </p>
          <button
            type="button"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold bg-primary text-white hover:bg-primary/90 transition-colors"
            @click="goToNotificaciones"
          >
            <span class="material-symbols-outlined text-[18px]">notifications</span>
            Gestionar notificaciones
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import NavbarCiudadano from '@/components/NavbarCiudadano.vue'
import { authService } from '@/services/auth'

const router = useRouter()
const user = authService.getCurrentUser()

const displayName = computed(() => {
  if (!user) return 'Ciudadano'
  if (user.nombre || user.apellido) {
    return `${user.nombre || ''} ${user.apellido || ''}`.trim()
  }
  return 'Ciudadano'
})

const avatarStyle = computed(() => {
  const name = encodeURIComponent(displayName.value || 'Ciudadano')
  const url = `https://ui-avatars.com/api/?name=${name}&background=0f5dd1&color=fff`
  return `background-image: url('${url}')`
})

const goToNotificaciones = () => {
  router.push({ name: 'ciudadano-notificaciones' })
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
