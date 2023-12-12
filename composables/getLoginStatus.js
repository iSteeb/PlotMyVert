export default async function () {
  const data = await apiFetch('checkLoginStatus', 'GET');
  return data.value.isLoggedIn;
}
