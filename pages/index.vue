<template>
  <main>
    <div v-if="isLoggedIn">
      <NuxtLink to="/browse/new">Fetch</NuxtLink>
      <NuxtLink to="/browse">Browse</NuxtLink>
    </div>
    <div v-else>
      <p>Basic Logged Out Home Page</p>
    </div>
  </main>
</template>

<script setup>
const isLoggedIn = useState('isLoggedIn');
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
