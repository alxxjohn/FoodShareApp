// import apiClient from "../services/apiClient";

//  TODO: get user's location(long/lat) to center the map, from login info? or new api request?
export async function getFoodbankLists() {
  const mockData = [
    {
      id: 1,
      name: "Green Valley Food Bank",
      address: {
        lat: 37.7749,
        lng: -122.4194,
      },
      street: "123 Green Valley Rd",
      city: "San Francisco",
      state:"CA",
      zip:"94110",
      phone: "+1 (415) 555-1234",     
      availability: true,
    },
    {
      id: 2,
      name: "Hope for All Food Bank",
      address: {
        lat: 37.7758,
        lng: -122.4180,
      },
      street: "456 Hope Ave",
      city: "Los Angeles",
      state:"CA",
      zip:"90001",
      phone: "+1 (213) 555-5678",
      availability: false,
    },
    {
      id: 3,
      name: "Sunshine Food Pantry",
      address: {
        lat: 40.7128,
        lng: -74.0060,
      },
      street: "789 Sunshine Blvd",
      city: "New York",
      state:"NY",
      zip:"10001",
      phone: "+1 (212) 555-8765",
      availability: true,
    },
    {
      id: 4,
      name: "Fresh Start Food Bank",
      address: {
        lat: 41.8781,
        lng: -87.6298,
      },
      street: "101 Fresh Start Ln",
      city: "Chicago",
      state:"IL",
      zip:"60601",
      phone: "+1 (312) 555-4321",
      availability: true,
    }
  ];
  
  return mockData;

}

// API version
// export const getFoodbankLists = () => {
//   return apiClient.get("/foodbanks")
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// };

export async function getInventory(foodbankId){
    const mockData = [
      {
        id: 1,
        availableFoods: [
          { id: 1, desc: "Canned Beans", quant:1 },
          { id: 2, desc: "Rice", quant:10 },
          { id: 3, desc: "Bread", quant:5 },
          { id: 4, desc: "Vegetables", quant:2 },
          { id: 5, desc: "Cereal", quant:1 }
        ]
      },
      {
        id: 2,
        availableFoods: []
      },
      {
        id: 3,
        availableFoods: [
          { id: 6, desc: "Canned Vegetables", quant:3 },
          { id: 7, desc: "Rice", quant:2 },
          { id: 8, desc: "Cereal", quant:10 },
          { id: 9, desc: "Tomato Sauce", quant:12 },
          { id: 10, desc: "Juice", quant:8 }
        ] 
      },
      {
        id: 4,
        availableFoods: [
          { id: 11, desc: "Chicken", quant:3 },
          { id: 12, desc: "Canned Corn", quant:12 },
          { id: 13, desc: "Pasta", quant:8 },
          { id: 14, desc: "Oatmeal", quant:9 },
          { id: 15, desc: "Eggs", quant:1 }
        ]
      }
    
    ];

    return mockData.find(item => item.id === foodbankId);
}


//API version
// export function getInventory(foodbankId){
//     return apiClient.get(`/foodbanks/${foodbankId}/inventory`)
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// }
