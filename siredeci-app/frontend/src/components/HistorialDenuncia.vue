<template>
  <section class="rounded-xl bg-white border border-gray-200 px-5 py-4">
    <h2 class="text-base font-bold text-gray-900 mb-3">Historial de la Denuncia (Trazabilidad)</h2>
    <ol class="relative border-l border-gray-200 ml-2 space-y-6 text-sm text-gray-700">
      <li
        v-for="(evento, index) in eventos"
        :key="index"
        class="relative pl-4">
        <!-- Punto de la línea de tiempo con icono -->
        <span
          class="absolute flex items-center justify-center w-6 h-6 bg-primary/20 rounded-full -left-3 ring-8 ring-white"
        >
          <span
            v-if="evento.icon"
            class="material-symbols-outlined text-sm text-primary"
          >
            {{ evento.icon }}
          </span>
          <span
            v-else
            class="text-[11px] font-semibold text-primary"
          >
            {{ index + 1 }}
          </span>
        </span>

        <h3 class="mb-0.5 text-sm font-semibold text-gray-900">{{ evento.titulo }}</h3>
        <p v-if="evento.fecha" class="text-[12px] text-gray-400 mb-0.5">{{ evento.fecha }}</p>
        <p v-if="evento.descripcion" class="text-[13px] leading-relaxed text-gray-600">{{ evento.descripcion }}</p>
      </li>
    </ol>
  </section>
</template>

<script setup>
defineProps({
  eventos: {
    type: Array,
    default: () => []
  }
})
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
