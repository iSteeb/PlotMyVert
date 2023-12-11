export default async function (endpoint, method, headers = null, body = null) {
  const baseURL =
    window.location.hostname === 'vert.duz.ie'
      ? 'https://vert.duz.ie'
      : 'http://127.0.0.1:8000';
  const url = `${baseURL}/api/v1/${endpoint}/`;

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
    console.log(response);
    const data = ref(await response.json());
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
