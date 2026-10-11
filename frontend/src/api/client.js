import axios from 'axios'

// In production, the frontend is served from Nginx which proxies /api
// to the backend container (see nginx.conf), so a relative base URL works
// both in local dev (via Vite proxy) and in the Dockerized deployment.
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

const client = axios.create({
  baseURL: API_BASE_URL,
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default client
