const BASE_URL = "/api";

export function fetchItems(params = {}) {
  const query = new URLSearchParams(params).toString();
  return fetch(`${BASE_URL}/items/?${query}`)
    .then(res => res.json());
}

export function fetchItem(id) {
  return fetch(`${BASE_URL}/items/${id}`)
    .then(res => res.json());
}

export function createItem(data) {
  return fetch(`${BASE_URL}/items`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function updateItem(id, data) {
  return fetch(`${BASE_URL}/items/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }).then(res => res.json());
}

export function deleteItem(id) {
  return fetch(`${BASE_URL}/items/${id}`, {
    method: "DELETE"
  });
}

export function markAsGiven(id) {
  return fetch(`${BASE_URL}/items/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ status: "given" })
  });
}

export function createRequest(itemId, message) {
  return fetch(`${BASE_URL}/requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      item_id: itemId,
      message: message
    })
  }).then(res => res.json());
} 