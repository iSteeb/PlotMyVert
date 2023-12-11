export default async function (endpoint, method, headers = null, body = null) {
  // const url = `http://127.0.0.1:8000/api/v1/${endpoint}/`;
  const url = `https://vert.duz.ie/api/v1/${endpoint}/`;

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
