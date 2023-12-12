export default async function (endpoint, method, headers = null, body = null) {
  const baseURL = import.meta.env.VITE_BASE_URL || 'https://vert.duz.ie';
  const url = `${baseURL}/api/v1/${endpoint}/`;
  console.log(import.meta.env.VITE_BASE_URL + '/api/v1/' + endpoint + '/');
  // const url = 'http://127.0.0.1:8000/api/v1/' + endpoint + '/';
  console.log(url);
  try {
    let options = {
      method: method,
      credentials: 'include'
    };

    if (headers) {
      options.headers = headers;
    }

    if (body) {
      options.body = JSON.stringify(body);
    }
    const response = await fetch(url, options);
    const data = ref(await response.json());
    console.log(data.value);
    return data;
  } catch (error) {
    throw error;
  }
}
