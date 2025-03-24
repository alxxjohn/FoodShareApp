// import apiClient from "@/services/apiClient";

//  TODO: get user's location(long/lat) to center the map, from login info? or new api request?
export async function foodLists() {
  const mockData = [
    {
      id: 1,
      name: "Green Valley Food Bank",
      address: {
        lat: 37.7749,
        lng: -122.4194,
      },
      street: "123 Green Valley Rd, San Francisco, CA 94110",
      phone: "+1 (415) 555-1234",
      openHours: "Mon-Fri 9:00 AM - 6:00 PM, Sat 10:00 AM - 2:00 PM",
      availableFoods: [
        { id: 1, desc: "Canned Beans" },
        { id: 2, desc: "Rice" },
        { id: 3, desc: "Bread" },
        { id: 4, desc: "Vegetables" },
        { id: 5, desc: "Cereal" }
      ],      
      availability: true,
    },
    {
      id: 2,
      name: "Hope for All Food Bank",
      address: {
        lat: 37.7758,
        lng: -122.4180,
      },
      street: "456 Hope Ave, Los Angeles, CA 90001",
      phone: "+1 (213) 555-5678",
      openHours: "Mon-Fri 8:00 AM - 5:00 PM",
      availableFoods: [],
      availability: false,
    },
    {
      id: 3,
      name: "Sunshine Food Pantry",
      address: {
        lat: 40.7128,
        lng: -74.0060,
      },
      street: "789 Sunshine Blvd, New York, NY 10001",
      phone: "+1 (212) 555-8765",
      openHours: "Mon-Sat 9:00 AM - 4:00 PM",
      availableFoods: [
        { id: 6, desc: "Canned Vegetables" },
        { id: 7, desc: "Rice" },
        { id: 8, desc: "Cereal" },
        { id: 9, desc: "Tomato Sauce" },
        { id: 10, desc: "Juice" }
      ],
      availability: true,
    },
    {
      id: 4,
      name: "Fresh Start Food Bank",
      address: {
        lat: 41.8781,
        lng: -87.6298,
      },
      street: "101 Fresh Start Ln, Chicago, IL 60601",
      phone: "+1 (312) 555-4321",
      openHours: "Tue-Sun 10:00 AM - 6:00 PM",
      availableFoods: [
        { id: 11, desc: "Chicken" },
        { id: 12, desc: "Canned Corn" },
        { id: 13, desc: "Pasta" },
        { id: 14, desc: "Oatmeal" },
        { id: 15, desc: "Eggs" }
      ], 
      availability: true,
    }
  ];
  
  return mockData;

}

//If it uses data from the back api
// export const foodLists = () => {
//   return apiClient.get("/foodlists")
//     .then(response => {
//       return { success: true, data: response.data };
//     })
//     .catch(error => {
//       return { success: false, error: error.response?.data || error.message };
//     });
// };