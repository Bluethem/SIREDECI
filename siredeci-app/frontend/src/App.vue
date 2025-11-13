<script setup>
// App principal
</script>

<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  width: 100%;
  overflow-x: hidden;
  font-size: 16px;
}

body {
  width: 100%;
  min-width: 320px;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
  font-family: 'Public Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
  margin: 0 !important;
  padding: 0 !important;
}

/* Forzar sin padding/margin en el root */
.min-h-screen {
  margin: 0 !important;
}

/* Asegurar que ningún elemento cause scroll horizontal */
* {
  max-width: 100%;
}

/* Permitir que ciertos elementos sean más anchos si es necesario */
input, textarea, select {
  max-width: none;
}
</style>
