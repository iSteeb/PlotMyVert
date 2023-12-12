<template>
  <main>
    <div v-if="isLoggedIn">
      <Entry
        v-for="session in sessions"
        :key="session.datetime"
        :session="session"
        @click="setActiveSession(session)" />
    </div>
    <div v-else>not logged in</div>
    <div v-if="activeSession" class="popup">
      <SessionPopup :session="activeSession" :jumps="activeSessionJumps" />
      <button @click="setActiveSession(null)">Close</button>
    </div>
  </main>
</template>

<script setup>
const isLoggedIn = useState('isLoggedIn');
const sessions = ref(null);
const activeSession = ref(null);
const activeSessionJumps = ref(null);

async function setActiveSession(session) {
  if (session) {
    activeSessionJumps.value = await getSessionJumps(session);
  } else {
    activeSessionJumps.value = null;
  }
  activeSession.value = session;
}

async function getAllSessions() {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const data = await apiFetch('getAllSessions', 'POST', headers, null);
  return data.value;
}

onMounted(async () => {
  const request = await getAllSessions();
  if (request.success) {
    sessions.value = request.sessions;
  }
});

async function getSessionJumps(session) {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const body = {
    start_datetime: session.start_datetime
  };
  const data = await apiFetch('getJumpsFromSession', 'POST', headers, body);
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
