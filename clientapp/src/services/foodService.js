import apiClient from "./apiClient";


//  TODO: get user's location(long/lat) to center the map, from login info? or new api request?
// export async function getFoodbankLists() {
//   const mockData = [
//     {
//       business_id: 1,
//       company_name: "Orlando Community Food Bank",
//       lat: 28.5969,
//       lng: -81.4511,
//       address: "100 Main St",
//       city: "Orlando",
//       state: "FL",
//       zipcode: "32801",
//     },
//     {
//       business_id: 2,
//       company_name: "Central Hope Pantry",
//       lat: 28.5973,
//       lng: -81.4498,
//       address: "200 Central Ave",
//       city: "Orlando",
//       state: "FL",
//       zipcode: "32803",
//     },
//     {
//       business_id: 3,
//       company_name: "Helping Hands Food Bank",
//       lat: 28.5952,
//       lng: -81.4519,
//       address: "300 Helping Hands Way",
//       city: "Orlando",
//       state: "FL",
//       zipcode: "32805",
//     },
//     {
//       business_id: 4,
//       company_name: "Sunrise Community Pantry",
//       lat: 28.5948,
//       lng: -81.4502,
//       address: "400 Sunrise Blvd",
//       city: "Orlando",
//       state: "FL",
//       zipcode: "32806",
//     }
//   ];
  
//   return mockData;

// }


// API version
export const getFoodbankLists = () => {
  return apiClient.get("/foodbanks/")
    .then(response => {
      //log the response
      console.log("getFoodbankLists.data: " + JSON.stringify(response.data));
      
      return { success: true, data: response.data };
    })
    .catch(error => {
      return { success: false, error: error.response?.data || error.message };
    });
};

export async function getInventory(foodbankId){  
  const mockData = [
      {
        id: 1,
        availableFoods: [
          { id: 1, name: "Canned Beans", quant:1 },
          { id: 2, name: "Rice", quant:10 },
          { id: 3, name: "Bread", quant:5 },
          { id: 4, name: "Vegetables", quant:2 },
          { id: 5, name: "Cereal", quant:1 }
        ]
      },
      {
        id: 2,
        availableFoods: []
      },
      {
        id: 3,
        availableFoods: [
          { id: 6, name: "Canned Vegetables", quant:3 },
          { id: 7, name: "Rice", quant:2 },
          { id: 8, name: "Cereal", quant:10 },
          { id: 9, name: "Tomato Sauce", quant:12 },
          { id: 10, name: "Juice", quant:8 }
        ] 
      },
      {
        id: 4,
        availableFoods: [
          { id: 11, name: "Chicken", quant:3 },
          { id: 12, name: "Canned Corn", quant:12 },
          { id: 13, name: "Pasta", quant:8 },
          { id: 14, name: "Oatmeal", quant:9 },
          { id: 15, name: "Eggs", quant:1 }
        ]
      }
    
    ];

    return mockData.find(item => item.id === foodbankId);
}


//IT should retreive only available inventory from the foodbank/business
//API version
// export function getInventory(foodbankId){
//     return apiClient.get(`/foodbanks/${foodbankId}/inventory`)
  //     .then(response => {
  //       return { success: true, data: response.data };
  //     })
  //     .catch(error => {
  //       return error;
  //     });
// }



// API VERSION
export function addDonationService(request){
  //  console.log("request: "+JSON.stringify(request, null, 2)); 
  return apiClient.post("/donations/", request)
    .then(response => {
      return { success: true, data: response.data};
    })
    .catch(error =>{
      return { success: false, error: error.response?.data || error.message };
});
}

// export async function addDonationService(request){
//   console.log("request: "+JSON.stringify(request, null, 2));
//   return new Promise((resolve) => {
//     setTimeout(() => {
//       resolve({ success: true, message: "Reservation successful!" });
//     }, 500); // Simulate network delay
//   });
// }