// import apiClient from "@/services/apiClient";

//IF we use back API
// export function reserveFood (userId, foodId, reservationTime) {
//   return apiClient.post("/reservations/reserve", { userId, foodId, reservationTime })
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// }

export function reserveFood (userId, foodId, reservationTime) {
  console.log("userId: "+userId);
  console.log("foodId: "+foodId);
  console.log("reservationTime: "+reservationTime);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "Reservation successful!" });
    }, 500); // Simulate network delay
  });
}