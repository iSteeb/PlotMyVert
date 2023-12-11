export default async function () {
  const data = await useFetch('checkLoginStatus', 'GET');
  return data.value.isLoggedIn;
}
