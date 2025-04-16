import apiClient from "./apiClient";

export function getUserByUserId(UUID){
  return apiClient.get(`/person/${UUID}/`)
  .then(response => {
    //  Log the response
    // console.log("getUserByUserId response: "+JSON.stringify(response.data, null, 2)); 
    return { success: true, data: response.data };
  })
  .catch(error => {
    return { 
      success: false, 
      error: {
        detail: error.response?.data?.detail,
        status: error.response?.status,
      }};
  });
}