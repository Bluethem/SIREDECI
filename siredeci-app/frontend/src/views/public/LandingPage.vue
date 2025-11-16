<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4 sm:p-6 bg-slate-50 dark:bg-zinc-900">
    <div class="w-full max-w-lg text-center">
      <header class="mb-10">
        <img 
          alt="SIREDECI Logo" 
          class="mx-auto mb-4 h-32 w-32 object-contain" 
          src="@/assets/logo.png"
        />
        <h1 class="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white">SIREDECI</h1>
        <p class="mt-2 text-lg text-gray-600 dark:text-gray-400">Sistema de registro y denuncias ciudadanas</p>
      </header>

      <main class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
        <!-- Botón Personal Municipal -->
        <router-link 
          to="/admin/login"
          class="group flex flex-col items-center justify-center p-8 bg-white dark:bg-zinc-800 border border-gray-200 dark:border-zinc-700 rounded-lg shadow-sm hover:shadow-lg hover:border-blue-500 dark:hover:border-blue-500 transition-all duration-300 transform hover:-translate-y-1"
        >
          <div class="flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-full mb-5 transition-colors duration-300 group-hover:bg-blue-200 dark:group-hover:bg-blue-900/60">
            <span class="material-symbols-outlined text-3xl text-blue-500">admin_panel_settings</span>
          </div>
          <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100">Personal Municipal</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Acceso para administradores</p>
        </router-link>

        <!-- Botón Ciudadano -->
        <router-link 
          to="/ciudadano/login"
          class="group flex flex-col items-center justify-center p-8 bg-white dark:bg-zinc-800 border border-gray-200 dark:border-zinc-700 rounded-lg shadow-sm hover:shadow-lg hover:border-blue-500 dark:hover:border-blue-500 transition-all duration-300 transform hover:-translate-y-1"
        >
          <div class="flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-full mb-5 transition-colors duration-300 group-hover:bg-blue-200 dark:group-hover:bg-blue-900/60">
            <span class="material-symbols-outlined text-3xl text-blue-500">person</span>
          </div>
          <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100">Ciudadano</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Ingresar o ver estadísticas públicas</p>
        </router-link>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>

<style scoped>
:deep(.material-symbols-outlined) {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
