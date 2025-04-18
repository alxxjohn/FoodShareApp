import apiClient from "./apiClient";

export const getFoodbankLists = () => {
  return apiClient.get("/foodbanks/")
    .then(response => {
      //log the response
      // console.log("getFoodbankLists.data: " + JSON.stringify(response.data));
      
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
};

export function getInventory(foodbankId){
  
  return apiClient.get(`/foodbanks/${foodbankId}/inventory`)
    .then(response => {
      // log the response
      // console.log("getInventory: " + JSON.stringify(response));
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

export function addDonationService(request){
  //log the request
  //  console.log("request: "+JSON.stringify(request, null, 2)); 
  
  return apiClient.post("/donations/", request)
    .then(response => {
      return { success: true, data: response.data};
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
