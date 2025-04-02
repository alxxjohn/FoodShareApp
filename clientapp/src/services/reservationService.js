// import apiClient from "@/services/apiClient";

//IF we use back API
// export function reserveFood (request) {
//  Log the request
//  console.log("request: "+JSON.stringify(request, null, 2)); 
//  return apiClient.post("/reservations/reserve", { request })
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// }

export function reserveFood (request) {
  console.log("requestBody: "+JSON.stringify(request, null, 2));
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "Reservation successful!" });
    }, 500); // Simulate network delay
  });
}