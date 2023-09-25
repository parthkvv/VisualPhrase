const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

export async function post(endpoint, data) {
    const promise = fetch(BASE_API_URL + endpoint, {
      method: "POST",
      body: data,
    });
    const resp = await promise;
  return await resp.json();
  }

export async function get(endpoint) {
    const promise = fetch(BASE_API_URL + endpoint);
    const resp = await promise;
  return await resp.json();
  }