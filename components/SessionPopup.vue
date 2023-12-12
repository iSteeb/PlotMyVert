<template>
  <div>
    <h1>Session Details</h1>
    <h2>{{ session.start_datetime }}</h2>
    <p>Count: {{ session.count }}</p>
    <p>Average High: {{ session.averageHigh }}</p>
    <p>Highest: {{ session.highest }}</p>
    <Plotly :plotly="JSON.parse(session.plotly_json)" />
    <div v-for="jump in jumps">
      <p>
        Jump Timestamp: {{ jump.timestamp }} Jump Height: {{ jump.jump_height }}
      </p>
      <p></p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  session: {
    type: Object,
    required: true
  },
  jumps: {
    type: Object,
    required: true
  }
});
</script>
