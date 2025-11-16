<template>
  <div class="font-display bg-very-light-gray text-dark-blue flex min-h-screen w-full">
    <!-- Sidebar unified -->
    <aside class="w-64 bg-white flex flex-col border-r border-medium-gray">
      <div class="flex flex-col h-full p-4">
        <div class="flex items-center gap-3 p-2 mb-4">
          <div class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" data-alt="Company logo abstract shape" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuBaXtYxFyHwjmkfzelKdSwckui0VVqBxvGCgbtXZGm7PLNonck59Pa-GNBQiIsq87W1Lh6EuZpvNHIl5ut6OMcMKYLyvJY29ahhMDpwOxBZPAlC0GJX4nsu6xBRTYFiYOiIbwJTgSuczE5rPIRwmep9qHnn0FoAzi8SzFgNs7b6pwFoWzm0BP_V813hr6YZomVQerH46whjBHv_QzMR-PdF8ZxV4zElToDiD0RtlSzhnMFiUQtPfDYTQ16z0SxPZYNRrHGjRBMPQV2U");'></div>
          <div class="flex flex-col">
            <h1 class="text-base font-bold text-dark-blue">Plataforma de</h1>
            <p class="text-sm text-gray-500">Gestión</p>
          </div>
        </div>
        <nav class="flex flex-col gap-2">
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/dashboard') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/dashboard')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/dashboard') ? 'text-principal-blue' : '']">dashboard</span>
            <p class="text-sm font-medium leading-none">Dashboard</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/analisis-geografico') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/analisis-geografico')">
            <span class="material-symbols-outlined nofill">map</span>
            <p class="text-sm font-medium">Tendencias geograficas</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/reportes') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/reportes')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/reportes') ? 'text-principal-blue' : '']">bar_chart</span>
            <p class="text-sm font-medium leading-none">Reportes</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/desempeno') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/desempeno')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/desempeno') ? 'text-principal-blue' : '']">leaderboard</span>
            <p class="text-sm font-medium">Desempeño</p>
          </a>
          <a :class="['flex items-center gap-3 px-3 py-2 rounded-lg', isActive('/admin/indicadores') ? 'bg-principal-blue/10 text-principal-blue' : 'text-gray-700 hover:bg-gray-100']" href="#" @click.prevent="$router.push('/admin/indicadores')">
            <span :class="['material-symbols-outlined nofill', isActive('/admin/indicadores') ? 'text-principal-blue' : '']">insights</span>
            <p class="text-sm font-medium">Indicadores</p>
          </a>
        </nav>
        <div class="mt-auto">
          <a class="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg" href="#">
            <span class="material-symbols-outlined nofill">help</span>
            <p class="text-sm font-medium">Ayuda</p>
          </a>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6 lg:p-8">
      <div class="w-full max-w-4xl mx-auto">
        <header class="mb-8">
          <h1 class="text-3xl font-black leading-tight tracking-[-0.033em]">Reportes</h1>
          <p class="text-gray-500 mt-1">Selecciona una opción para continuar</p>
        </header>

        <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button @click="$router.push('/admin/generador-reportes')" class="group flex flex-col items-center justify-center p-8 bg-white rounded-xl border border-medium-gray hover:border-principal-blue hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-principal-blue/50">
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

<script>
export default {
  name: 'ReportesHub',
  methods: {
    isActive(path) { try { return this.$route.path.startsWith(path) } catch { return false } }
  }
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
</style>
