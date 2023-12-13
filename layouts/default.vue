<template>
  <header style="background-color: #f2f2f2; padding: 10px; text-align: center">
    <a href="/" style="text-decoration: none; color: #000">
      <h1>Home</h1>
    </a>
    <div v-if="isLoggedIn">
      <button @click="logout()">Logout</button>
      <button @click="showConfigPopup = true">Configure</button>
    </div>
    <div v-else>
      <button @click="(showLoginPopup = true), (showSignupPopup = false)">
        Login
      </button>
      <button @click="(showSignupPopup = true), (showLoginPopup = false)">
        Signup
      </button>
    </div>
  </header>

  <div>
    <div v-if="showLoginPopup && !isLoggedIn" class="popup">
      <h2>Login</h2>
      <input v-model="emailInput" type="email" placeholder="Email" />
      <input v-model="passwordInput" type="password" placeholder="Password" />
      <button @click="login()">Submit</button>
      <button @click="closePopups(), clearFields()">Close</button>
    </div>
    <div v-if="showSignupPopup && !isLoggedIn" class="popup">
      <h2>Signup</h2>
      <input v-model="emailInput" type="email" placeholder="Email" />
      <input v-model="passwordInput" type="password" placeholder="Password" />
      <button @click="signup()">Submit</button>
      <button @click="closePopups(), clearFields()">Close</button>
    </div>
    <div v-if="showConfigPopup" class="popup">
      <h2>Config</h2>
      <input v-model="emailInput" type="email" placeholder="Login Email" />
      <input v-model="passwordInput" type="password" placeholder="Password" />
      <input v-model="recipientInput" type="email" placeholder="Recipient" />
      <input v-model="hostInput" type="text" placeholder="Host" />
      <input v-model="portInput" type="number" placeholder="993" />
      <input v-model="sslInput" type="checkbox" />
      <button @click="configure()">Submit</button>
      <button @click="closePopups(), clearFields()">Close</button>
    </div>
  </div>
  <slot />

  <footer style="background-color: #f2f2f2; padding: 10px; text-align: center">
    <p>&copy; 2023 duz.ie all rights reserved</p>
  </footer>
</template>

<script setup>
const isLoggedIn = useState('isLoggedIn');
let showLoginPopup = ref(false);
let showSignupPopup = ref(false);
let showConfigPopup = ref(false);
let emailInput = ref('');
let passwordInput = ref('');
let recipientInput = ref('');
let hostInput = ref('');
let portInput = ref(993);
let sslInput = ref(true);

async function updateLoginStatus() {
  isLoggedIn.value = await getLoginStatus();
}

function closePopups() {
  showLoginPopup.value = false;
  showSignupPopup.value = false;
  showConfigPopup.value = false;
}

function clearFields() {
  emailInput.value = '';
  passwordInput.value = '';
  recipientInput.value = '';
  hostInput.value = '';
  portInput.value = 993;
  sslInput.value = true;
}

async function login() {
  const csrfSet = await apiFetch('setCsrfCookie', 'GET');
  if (!csrfSet.value.success) {
    return;
  }

  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const body = {
    email: emailInput.value,
    password: passwordInput.value
  };
  const data = await apiFetch('userLogin', 'POST', headers, body);
  if (data.value.success) {
    updateLoginStatus();
    closePopups();
    clearFields();
  }
}
async function signup() {
  const csrfSet = await apiFetch('setCsrfCookie', 'GET');
  if (!csrfSet.value.success) {
    return;
  }

  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const body = {
    email: emailInput.value,
    password: passwordInput.value
  };
  const data = await apiFetch('signup', 'POST', headers, body);
  if (data.value.success) {
    login();
  }
}
async function logout() {
  const data = await apiFetch('userLogout', 'GET');
  if (data.value.success) {
    updateLoginStatus();
    closePopups();
    clearFields();
  }
}
async function configure() {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.replace(
      /(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/,
      '$1'
    )
  };
  const body = {
    email: emailInput.value,
    password: passwordInput.value,
    recipient: recipientInput.value,
    host: hostInput.value,
    port: portInput.value,
    ssl: sslInput.value
  };
  const data = await apiFetch('configure', 'POST', headers, body);
  if (data.value.success) {
    closePopups();
    clearFields();
  }
}

updateLoginStatus();
</script>

<style scoped>
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #f2f2f2;
  padding: 10px;
  text-align: center;
  z-index: 1;
}
</style>
