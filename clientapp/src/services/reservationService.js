import apiClient from "./apiClient";

//IF we use back API
export function reserveFood (request) {
//  Log the request
 console.log("request: "+JSON.stringify(request, null, 2)); 

 return apiClient.post("/reservations/", request)
    .then(response => {
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

// API version
// Get all the reservation from the foodbank/business by their id
export function getReservationList(foodbankId){
  //Log the foodbankId
  // console.log("getReservation, foodbankId:" + foodbankId);
  
  //TODO: I need to change the api url (currently it doesn'e exist)
  return apiClient.get(`/reservations/${foodbankId}`)
  .then(response => {
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