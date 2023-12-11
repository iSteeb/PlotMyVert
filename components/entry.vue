<template>
  <div class="entry">
    <div class="column">
      <h2>{{ session.start_datetime }}</h2>
    </div>
    <div class="column">
      <p>Count: {{ session.count }}</p>
    </div>
    <div class="column">
      <p>Average High: {{ session.averageHigh }}</p>
    </div>
    <div class="column">
      <p>Highest: {{ session.highest }}</p>
    </div>
    <div class="column">
      <Plotly :plotly="JSON.parse(session.plotly_json)" class="plotly-plot" />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  session: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-height: 100px;
  width: 100%;
  background-color: aqua;
}

.plotly-plot {
  transform: scale(0.2); /* Scale down the plot */
  background-color: red;
}
</style>
