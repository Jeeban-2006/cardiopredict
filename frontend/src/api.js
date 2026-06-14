import axios from 'axios';

// Startup environment validation
if (import.meta.env.PROD && !import.meta.env.VITE_API_URL) {
  console.error("Vite Startup Error: Missing VITE_API_URL environment variable in production mode.");
}

const getBaseURL = () => {
  const url = import.meta.env.VITE_API_URL;
  if (!url) return '';
  // Strip trailing slash to avoid double slashes like: baseURL/api/predict
  return url.endsWith('/') ? url.slice(0, -1) : url;
};

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add error interceptor for easy debugging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API request failed:", {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data
    });
    return Promise.reject(error);
  }
);

export default api;
