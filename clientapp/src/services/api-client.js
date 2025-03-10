import axios from "axios";

const apiClient = axios.create({
  baseURL: "/api",  // Use relative URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;