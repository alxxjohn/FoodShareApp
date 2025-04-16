import apiClient from "./apiClient";

//IF we use back API
export function reserveFood (request) {
//  Log the request
//  console.log("reserveFood request: "+JSON.stringify(request, null, 2)); 

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

// Get all the reservation from the foodbank/business by their id
export function getReservationList(foodbankId){
  //Log the foodbankId
  // console.log("getReservationList, foodbankId:" + foodbankId);
  
  return apiClient.get(`/reservations/foodbank/${foodbankId}`)
  .then(response => {
    //  Log the request
    // console.log("getReservationList response: "+JSON.stringify(response.data, null, 2)); 
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