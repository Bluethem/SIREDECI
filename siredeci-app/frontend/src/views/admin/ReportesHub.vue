<template>
  <div class="font-display bg-very-light-gray text-dark-blue flex min-h-screen w-full">
    <SidebarAdmin />

    <!-- Main content -->
    <main class="flex-1 p-6 lg:p-8">
      <div class="w-full max-w-4xl mx-auto">
        <header class="mb-8">
          <h1 class="text-3xl font-black leading-tight tracking-[-0.033em]">Reportes</h1>
          <p class="text-gray-500 mt-1">Selecciona una opción para continuar</p>
        </header>

        <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            v-if="canGenerateReports"
            @click="$router.push('/admin/generador-reportes')"
            class="group flex flex-col items-center justify-center p-8 bg-white rounded-xl border border-medium-gray hover:border-principal-blue hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-principal-blue/50"
          >
            <span class="material-symbols-outlined text-5xl text-principal-blue mb-4 group-hover:scale-110 transition-transform">description</span>
            <h2 class="text-xl font-bold text-dark-blue mb-2">Generación y exportación de reportes</h2>
            <p class="text-sm text-gray-500 text-center">Crea y exporta nuevos reportes según los criterios que necesites</p>
          </button>

          <button class="group flex flex-col items-center justify-center p-8 bg-white rounded-xl border border-medium-gray hover:border-principal-blue hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-principal-blue/50">
            <span class="material-symbols-outlined text-5xl text-principal-blue mb-4 group-hover:scale-110 transition-transform">history</span>
            <h2 class="text-xl font-bold text-dark-blue mb-2">Historial de reportes</h2>
            <p class="text-sm text-gray-500 text-center">Consulta y descarga reportes generados anteriormente</p>
          </button>
        </section>
      </div>
    </main>
  </div>
 </template>

<script setup>
import { computed } from 'vue'
import SidebarAdmin from '@/components/SidebarAdmin.vue'
import { isSuperAdmin, isAdmin } from '@/utils/roles'

const canGenerateReports = computed(() => isSuperAdmin() || isAdmin())
</script>

<script>
export default {
  name: 'ReportesHub'
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
