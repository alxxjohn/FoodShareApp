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
