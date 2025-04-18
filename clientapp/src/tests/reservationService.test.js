import { reserveFood, getReservationList } from "../services/reservationService";
import apiClient from "../services/apiClient";
import MockAdapter from "axios-mock-adapter";

// Create a mock adapter for apiClient
const mock = new MockAdapter(apiClient);

describe("reserveFood", () => {
  const mockRequest = {
    reservations_array:[
      {item_id: 1, item_qty:1},
      {item_id: 2, item_qty:2},
    ], 
    time: "11:30"
  };
  afterEach(() => {
    mock.reset(); // Reset mock after each test
  });

  it("should return success when API call is successful", async () => {

    mock.onPost("/reservations/", {request: mockRequest}).reply(200);

    const result = await reserveFood(mockRequest);

    expect(result.success).toBe(true);
  });

  it("should return error when API call fails", async () => {
    mock.onPost("/reservations/", {request: mockRequest}).reply(500, { message: "Internal Server Error" });

    const result = await reserveFood(mockRequest);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Internal Server Error");
  });

  it("should handle error response without message properly", async () => {
    mock.onPost("/reservations/", {request: mockRequest}).reply(500);

    const result = await reserveFood(mockRequest);
    
    expect(result.success).toBe(false);
    expect(result.error).toBeTruthy(); // Ensuring some error is returned
  });
});


describe("getReservationList", () => {
  afterEach(() => {
    mock.reset(); // Reset mock after each test
  });

  const foodbankId = 1;
  const mockResponse = [
    { id: 1, firstname: "John", lastname: "Smith", reservationTime: "15:30", status: "reserved", showedUpTime: "" },
    { id: 2, firstname: "Emily", lastname: "Johnson", reservationTime: "18:00", status: "pickedup", showedUpTime: "12:15" }
  ];

  it("should return success with foodbanks data when API call is successful", async () => {

    mock.onGet(`/reservations/${foodbankId}`).reply(200, mockResponse);

    const result = await getReservationList(foodbankId);

    expect(result.success).toBe(true);
    expect(result.data).toEqual(mockResponse);
  });

  it("should return error when API call fails", async () => {
    mock.onGet(`/reservations/${foodbankId}`).reply(500, { message: "Internal Server Error" });

    const result = await getReservationList(foodbankId);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Internal Server Error");
  });

  it("should handle error response without message properly", async () => {
    mock.onGet(`/reservations/${foodbankId}`).reply(500);

    const result = await getReservationList(foodbankId);

    expect(result.success).toBe(false);
    expect(result.error).toBeTruthy(); // Ensuring some error is returned
  });
});
