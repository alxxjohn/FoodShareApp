import api_client from "@/services/api-client";

export default {
  health() {
    return api_client.get("/health");
  }
};