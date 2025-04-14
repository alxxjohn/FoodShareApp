import apiClient from "./apiClient";

export default {
  login(credentials) {
    return apiClient.post("/login", credentials);
  },
  register(userData) {
    return apiClient.post("/register/user", userData);
  },
  logout() {
    return apiClient.post("/logout");
  }
};