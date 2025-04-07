// import apiClient from "./apiClient";

//IF we use back API
// export function reserveFood (request) {
// //  Log the request
// //  console.log("request: "+JSON.stringify(request, null, 2)); 

//  return apiClient.post("/reservations/reserve", { request })
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// }

export async function reserveFood (request) {
  //Log the request
  console.log("request: "+JSON.stringify(request, null, 2));
  
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true, message: "Reservation successful!" });
    }, 500); // Simulate network delay
  });
}

// API version
// Get all the reservation from the foodbank/business by their id
// export function getReservationList(foodbankId){
//   //Log the foodbankId
//   // console.log("getReservation, foodbankId:" + foodbankId);
  
//   //TODO: I need to change the api url (currently it doesn'e exist)
//   return apiClient.get(`/reservations/${foodbankId}`)
//   .then(response => {
//     return { success: true, data: response.data };
//   })
//   .catch(error => {
//     return { success: false, error: error.response?.data || error.message };
//   });
// }

export async function getReservationList(foodbankId){
  //Log the foodbankId
  // console.log("getReservation, foodbankId:" + foodbankId);
  const mockData = [
    {
      id: 1,
      reservationList: [
        { id: 1, firstname: "John", lastname: "Smith", reservationTime: "15:30", status: "reserved", showedUpTime: "" },
        { id: 2, firstname: "Emily", lastname: "Johnson", reservationTime: "18:00", status: "pickedup", showedUpTime: "12:15" },
        { id: 3, firstname: "Michael", lastname: "Brown", reservationTime: "13:00", status: "reserved", showedUpTime: "" },
        { id: 4, firstname: "Sarah", lastname: "Davis", reservationTime: "14:00", status: "pickedup", showedUpTime: "14:10" },
        { id: 5, firstname: "David", lastname: "Martinez", reservationTime: "11:30", status: "reserved", showedUpTime: "" }
      ]
    },
    {
      id: 2,
      reservationList: [
        { id: 6, firstname: "Sophia", lastname: "Taylor", reservationTime: "16:00", status: "pickedup", showedUpTime: "16:20" },
        { id: 7, firstname: "James", lastname: "Garcia", reservationTime: "17:00", status: "reserved", showedUpTime: "" },
        { id: 8, firstname: "Emma", lastname: "Thomas", reservationTime: "18:00", status: "pickedup", showedUpTime: "18:25" },
        { id: 9, firstname: "Liam", lastname: "Moore", reservationTime: "19:00", status: "reserved", showedUpTime: "" },
        { id: 10, firstname: "Olivia", lastname: "Wilson", reservationTime: "20:00", status: "pickedup", showedUpTime: "20:15" }
      ]
    }  
  ];

  return mockData.find(item => item.id === foodbankId);
}