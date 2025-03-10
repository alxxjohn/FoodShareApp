import apiClient from "@/services/apiClient";

export default {
  health() {
    return apiClient.get("/health");
  }
};