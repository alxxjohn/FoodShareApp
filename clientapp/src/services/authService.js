import apiClient from "./apiClient";

export default {
  login(credentials) {
    return apiClient.post(
      "/auth/login", 
      credentials,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
  },
  setToken(token){
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  },
  register(userData) {
    return apiClient.post("/register/user", userData);
  },
  logout() {
    return apiClient.post("/logout");
  }
};