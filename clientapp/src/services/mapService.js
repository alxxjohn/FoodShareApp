// import apiClient from "@/services/apiClient";

export default {
  // TODO: get user's location(long/lat) to center the map, from login info? or new api request?
  
  //WITH MOCKUP DATA till api is built
  foodLists(){

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
        availableFoods: ["Canned Beans", "Rice", "Bread", "Vegetables", "Cereal"],
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
        availableFoods: ["Canned Vegetables", "Rice", "Cereal", "Tomato Sauce", "Juice"],
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
        availableFoods: ["Chicken", "Canned Corn", "Pasta", "Oatmeal", "Eggs"],
        availability: true,
      }
    ];

    return mockData;
  }

  
    // foodLists(params) {
    //   return apiClient.get("/foodlists");
    // }
  
};