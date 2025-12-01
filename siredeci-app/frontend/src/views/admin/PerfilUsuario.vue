<template>
  <div class="font-display bg-very-light-gray text-gray-800 flex min-h-screen">
    <SidebarAdmin />

    <!-- Contenido principal -->
    <main class="flex-1 flex flex-col p-8 overflow-y-auto">
      <!-- Cabecera con tarjeta de perfil -->
      <section class="mb-8">
        <div class="bg-white rounded-2xl border border-medium-gray shadow-sm p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div class="flex items-center gap-4">
            <div
              class="bg-center bg-no-repeat bg-cover rounded-full size-16 md:size-20 flex-shrink-0 ring-4 ring-principal-blue/10"
              :style="avatarStyle"
            ></div>
            <div class="flex flex-col min-w-0">
              <h1 class="text-2xl md:text-3xl font-extrabold text-dark-blue truncate">{{ displayName }}</h1>
              <p class="text-sm text-gray-500 truncate">{{ user?.email || 'Sin correo registrado' }}</p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span
                  v-if="user?.estado_cuenta"
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold',
                    user?.estado_cuenta === 'Activo'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="user?.estado_cuenta === 'Activo' ? 'bg-green-500' : 'bg-red-500'"></span>
                  {{ user.estado_cuenta }}
                </span>
                <span
                  v-if="roles && roles.length"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-principal-blue"
                >
                  {{ roles[0] }}
                  <span v-if="roles.length > 1" class="ml-1 text-[11px] text-principal-blue/70">+{{ roles.length - 1 }} roles</span>
                </span>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-2 items-start md:items-end">
            <p class="text-xs uppercase tracking-wide text-gray-400">Cuenta</p>
            <p class="text-sm text-gray-600">
              Código:
              <span class="font-semibold text-gray-800 ml-1">{{ user?.codigo_usuario || '-' }}</span>
            </p>
            <p class="text-sm text-gray-600">
              Usuario:
              <span class="font-semibold text-gray-800 ml-1">{{ user?.nombre_usuario || '-' }}</span>
            </p>
          </div>
        </div>
      </section>

      <!-- Detalle de cuenta y roles -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Datos de la cuenta -->
        <div class="lg:col-span-2 bg-white rounded-2xl border border-medium-gray p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-dark-blue flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">badge</span>
            Datos de la cuenta
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div class="flex flex-col gap-1">
              <span class="text-gray-500">Código de usuario</span>
              <span class="font-medium text-gray-900">{{ user?.codigo_usuario || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500">Nombre de usuario</span>
              <span class="font-medium text-gray-900">{{ user?.nombre_usuario || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500">Correo electrónico</span>
              <span class="font-medium text-gray-900 break-all">{{ user?.email || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-gray-500">Estado de cuenta</span>
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold w-fit',
                  user?.estado_cuenta === 'Activo'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                ]"
              >
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="user?.estado_cuenta === 'Activo' ? 'bg-green-500' : 'bg-red-500'"></span>
                {{ user?.estado_cuenta || '-' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Roles asignados -->
        <div class="bg-white rounded-2xl border border-medium-gray p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-dark-blue flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">verified_user</span>
            Roles asignados
          </h2>
          <ul v-if="roles && roles.length" class="space-y-2 text-sm">
            <li
              v-for="r in roles"
              :key="r"
              class="flex items-center justify-between px-3 py-2 rounded-lg bg-slate-50 border border-slate-200"
            >
              <span class="flex items-center gap-2">
                <span class="inline-flex h-2 w-2 rounded-full bg-principal-blue"></span>
                <span class="font-medium text-gray-800">{{ r }}</span>
              </span>
              <span class="text-[11px] uppercase tracking-wide text-gray-400">ROL</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500">Este usuario no tiene roles asignados.</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import SidebarAdmin from '@/components/SidebarAdmin.vue'

export default {
  name: 'PerfilUsuarioAdmin',
  components: { SidebarAdmin },
  computed: {
    user() {
      try {
        const raw = localStorage.getItem('admin_user')
        return raw ? JSON.parse(raw) : null
      } catch (e) {
        return null
      }
    },
    roles() {
      return (this.user && Array.isArray(this.user.roles)) ? this.user.roles : []
    },
    displayName() {
      if (!this.user) return 'Usuario administrador'
      return this.user.nombre_usuario || this.user.email || 'Usuario administrador'
    },
    avatarStyle() {
      const name = encodeURIComponent(this.displayName || 'Usuario')
      const url = `https://ui-avatars.com/api/?name=${name}&background=0f5dd1&color=fff`
      return `background-image: url('${url}')`
    }
  }
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
