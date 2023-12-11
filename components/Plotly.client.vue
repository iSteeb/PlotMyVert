<template>
  <nuxt-plotly
    :data="plotly.data"
    :layout="plotly.layout"
    :config="{}"></nuxt-plotly>
</template>

<script setup>
const props = defineProps({
  plotly: {
    type: Object,
    required: true
  }
});
</script>
