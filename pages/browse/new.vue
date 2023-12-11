<template>
  <main>
    <div v-if="isLoggedIn">
      <Entry
        v-for="session in sessions"
        :key="session.datetime"
        :session="session"
        @click="activeSession.value = session" />
    </div>
    <div v-else>not logged in</div>
    <div v-if="activeSession" class="popup">
      <SessionPopup
        :session="activeSession"
        :jumps="getActiveSessionJumps(activeSession)" />
      <button @click="activeSession.value = null">Close</button>
    </div>
  </main>
</template>

<script setup>
const isLoggedIn = useState('isLoggedIn');
const sessions = ref(null);
const activeSession = ref(null);

async function fetchNewSessions() {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const data = await useFetch('getNewSessionsFromEmail', 'POST', headers, null);
  return data.value;
}

onMounted(async () => {
  const request = await fetchNewSessions();
  if (request.success) {
    sessions.value = request.sessions;
  }
});

async function getActiveSessionJumps() {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const body = {
    start_datetime: activeSession.value.start_datetime
  };
  const data = await useFetch('getJumpsFromSession', 'POST', headers, body);
  if (data.value.success) {
    return data.value.jumps;
  }
}
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
