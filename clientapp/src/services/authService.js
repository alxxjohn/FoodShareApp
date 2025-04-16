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
  setIsBusiness(is_business){
    apiClient.defaults.headers.common['is_business'] = `${is_business}`;
  },
  loadTokenFromStorage() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.setToken(token);
    }
    const is_business = localStorage.getItem('is_business');
    if (is_business){
      this.setIsBusiness(is_business);
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