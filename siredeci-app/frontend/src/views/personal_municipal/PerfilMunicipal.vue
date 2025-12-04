<template>
  <div class="flex h-screen bg-[#f5f7fb]">
    <SidebarMunicipal />

    <main class="flex-1 flex flex-col overflow-hidden px-8 py-8">
      <!-- Cabecera con tarjeta de perfil -->
      <section class="mb-8">
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div class="flex items-center gap-4">
            <div
              class="bg-center bg-no-repeat bg-cover rounded-full size-16 md:size-20 flex-shrink-0 ring-4 ring-sky-500/10"
              :style="avatarStyle"
            ></div>
            <div class="flex flex-col min-w-0">
              <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 truncate">{{ displayName }}</h1>
              <p class="text-sm text-slate-500 truncate">{{ user?.email || 'Sin correo registrado' }}</p>
              <p v-if="personal" class="text-xs text-slate-500 mt-1 truncate">
                {{ personal.cargo }}
                <span v-if="personal.area_responsable_nombre"> · {{ personal.area_responsable_nombre }}</span>
              </p>
            </div>
          </div>

          <div class="flex flex-col gap-2 items-start md:items-end text-sm text-slate-600">
            <p class="text-xs uppercase tracking-wide text-slate-400">Cuenta</p>
            <p>
              Código usuario:
              <span class="font-semibold text-slate-900 ml-1">{{ user?.codigo_usuario || '-' }}</span>
            </p>
            <p>
              Usuario:
              <span class="font-semibold text-slate-900 ml-1">{{ user?.nombre_usuario || '-' }}</span>
            </p>
            <p v-if="personal">
              Código personal:
              <span class="font-semibold text-slate-900 ml-1">{{ personal.codigo_personal || '-' }}</span>
            </p>
          </div>
        </div>
      </section>

      <!-- Detalle de cuenta y datos laborales -->
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Datos de la cuenta -->
        <div class="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">badge</span>
            Datos de la cuenta
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Código de usuario</span>
              <span class="font-medium text-slate-900">{{ user?.codigo_usuario || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Nombre de usuario</span>
              <span class="font-medium text-slate-900">{{ user?.nombre_usuario || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Correo electrónico</span>
              <span class="font-medium text-slate-900 break-all">{{ user?.email || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Estado de cuenta</span>
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold w-fit',
                  user?.estado_cuenta === 'Activo'
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-rose-50 text-rose-700 border border-rose-200'
                ]"
              >
                <span
                  class="w-1.5 h-1.5 rounded-full mr-1.5"
                  :class="user?.estado_cuenta === 'Activo' ? 'bg-emerald-500' : 'bg-rose-500'"
                ></span>
                {{ user?.estado_cuenta || '-' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Datos laborales -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 flex flex-col gap-4">
          <h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px]">work</span>
            Datos laborales
          </h2>
          <div v-if="personal" class="space-y-3 text-sm">
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Nombre completo</span>
              <span class="font-medium text-slate-900">
                {{ personal.nombre }} {{ personal.apellido }}
              </span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Cargo</span>
              <span class="font-medium text-slate-900">{{ personal.cargo || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Área responsable</span>
              <span class="font-medium text-slate-900">{{ personal.area_responsable_nombre || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-500">Estado laboral</span>
              <span class="font-medium text-slate-900">{{ personal.estado_laboral || '-' }}</span>
            </div>
          </div>
          <p v-else class="text-sm text-slate-500">
            No se encontró información de personal municipal asociada a este usuario.
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import SidebarMunicipal from '@/components/SidebarMunicipal.vue'

export default {
  name: 'PerfilMunicipal',
  components: { SidebarMunicipal },
  computed: {
    user() {
      try {
        const raw = localStorage.getItem('admin_user')
        return raw ? JSON.parse(raw) : null
      } catch (e) {
        return null
      }
    },
    personal() {
      try {
        const raw = localStorage.getItem('admin_personal')
        return raw ? JSON.parse(raw) : null
      } catch (e) {
        return null
      }
    },
    displayName() {
      if (this.personal && (this.personal.nombre || this.personal.apellido)) {
        return `${this.personal.nombre || ''} ${this.personal.apellido || ''}`.trim()
      }
      if (!this.user) return 'Usuario municipal'
      return this.user.nombre_usuario || this.user.email || 'Usuario municipal'
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
