import { getFoodbankLists, getInventory } from "../services/foodService";
import apiClient from "../services/apiClient";
import MockAdapter from "axios-mock-adapter";

// Create a mock adapter for apiClient
const mock = new MockAdapter(apiClient);

describe("getFoodbankLists", () => {
  afterEach(() => {
    mock.reset(); // Reset mock after each test
  });

  const mockResponse = [
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
    }
  ];

  it("should return success with foodbanks data when API call is successful", async () => {

    mock.onGet("/foodbanks").reply(200, mockResponse);

    const result = await getFoodbankLists();

    expect(result.success).toBe(true);
    expect(result.data).toEqual(mockResponse);
  });

  it("should return error when API call fails", async () => {
    mock.onGet("/foodbanks").reply(500, { message: "Internal Server Error" });

    const result = await getFoodbankLists();

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Internal Server Error");
  });

  it("should handle error response without message properly", async () => {
    mock.onGet("/foodbanks").reply(500);

    const result = await getFoodbankLists();

    expect(result.success).toBe(false);
    expect(result.error).toBeTruthy(); // Ensuring some error is returned
  });
});



describe("getInventory", () => {
  const foodbankId = 1;
  const mockResponse = {
    id: 1,
    availableFoods: [
      { id: 1, desc: "Canned Beans", quant:1 },
      { id: 2, desc: "Rice", quant:10 },
      { id: 3, desc: "Bread", quant:5 },
      { id: 4, desc: "Vegetables", quant:2 },
      { id: 5, desc: "Cereal", quant:1 }
    ]
  };
  afterEach(() => {
    mock.reset(); // Reset mock after each test
  });

  it("should return success with inventory data when API call is successful", async () => {

    mock.onGet(`/foodbanks/${foodbankId}/inventory`).reply(200, mockResponse);

    const result = await getInventory(foodbankId);

    expect(result.success).toBe(true);
    expect(result.data).toEqual(mockResponse);
  });

  it("should return error when API call fails", async () => {
    mock.onGet(`/foodbanks/${foodbankId}/inventory`).reply(500, { message: "Internal Server Error" });

    const result = await getInventory(foodbankId);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Internal Server Error");
  });

  it("should handle error response without message properly", async () => {
    mock.onGet(`/foodbanks/${foodbankId}/inventory`).reply(500);

    const result = await getInventory(foodbankId);
    
    expect(result.success).toBe(false);
    expect(result.error).toBeTruthy(); // Ensuring some error is returned
  });
});
