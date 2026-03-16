import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5555/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests if it exists
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Handle response errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      // window.location.href = '/login'; // Let context handle this if needed
    }
    return Promise.reject(error);
  }
);

// Items API
export const getItems = (params) => api.get('/items/', { params });
export const getItem = (id) => api.get(`/items/${id}`);
export const createItem = (data) => api.post('/items/', data);
export const updateItem = (id, data) => api.put(`/items/${id}`, data);
export const deleteItem = (id) => api.delete(`/items/${id}`);
export const getMyItems = () => api.get('/items/my-items');
export const markItemAsGiven = (id) => api.patch(`/items/${id}/mark-given`);

// Categories API
export const getCategories = () => api.get('/categories/');

// Requests API
export const createRequest = (itemId, message) =>
  api.post(`/requests/item/${itemId}`, { message });
export const getIncomingRequests = () => api.get('/requests/incoming');
export const getOutgoingRequests = () => api.get('/requests/outgoing');
export const approveRequest = (id) => api.patch(`/requests/${id}/approve`);
export const rejectRequest = (id) => api.patch(`/requests/${id}/reject`);

export default api;
