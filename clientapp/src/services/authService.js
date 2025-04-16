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
  loadTokenFromStorage() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.setToken(token);
    }
  },
  userRegister(userData) {
    return apiClient.post("/register/user", userData);
  },
  businessRegister(userData) {
    return apiClient.post("/register/business", userData);
  },
  getCurrentLoggedInUser(){
    return apiClient.get("/auth/user")
  },
  logout() {
    return apiClient.post("/logout");
  }
};