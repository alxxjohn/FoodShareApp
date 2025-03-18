<template>
  <div id="food-map">
    <h2>Food Donations Near You</h2>
    <googleMap 
      :center="userLoc" 
      :markers="foodLocations" 
      :foodInfo="foodInfo"
      @markerClicked="handleMarkerClick" 
      />
      <!-- @markerClicked listens markerClicked event from GoogleMap.vue-->
  </div>

  <div id="food-info-box" v-if="selectedMarker">
    <div>
      <label>Name:</label>
      <span>{{ selectedMarker.name }}</span>
    </div>
    <div>
      <label>Address:</label>
      <span>{{ selectedMarker.street }}</span>
    </div>
    <div>
      <label>Phone:</label>
      <span>{{ selectedMarker.phone }}</span>
    </div>
    <div>
      <label>Open Hours:</label>
      <span>{{ selectedMarker.openHours }}</span>
    </div>
    <div>
      <label>Available Foods:</label>
      <select v-model="selectedFood">
        <option v-for="food in selectedMarker.availableFoods" :key="food.id" :value="food.id">
          {{ food.desc }}
        </option>
      </select>
    </div>
  </div>

  <div id="timepicker-form" v-if="selectedMarker"> 
    <label for="timepicker">Select a time:</label>
    <input type="time" class="form-control" id="timepicker" v-model="selectedTime" />
  </div>

  <div id="reserve-button" v-if="selectedMarker">
      <button type="button" class="btn btn-primary" @click="reserve">Reserve</button>
  </div>

</template>


<!-- TODO: Receive the available food list data from the back, and populate them into the foodLocations abjects  -->
<!-- TODO: disabled or error message if the values aren't given by the user, or availability is true. -->

<script setup>
import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import { foodLists } from '@/services/foodService'
import { reserveFood } from '@/services/reservationService'

const foodLocations = ref([]);
const foodInfo = ref([]);
const selectedId = ref(null);
const selectedMarker = ref(null);
const selectedFood = ref(null);
const selectedTime = ref(null);

//TOOD: this should be retrieved from the back (login info? from cache?)
const userLoc = ref({lat: 37.7730, lng: -122.4183});
const uuId = 1;

onMounted(() => {
  foodLists()
    .then(data => {
      foodLocations.value = data.map((location) => ({
        lat: location.address.lat,
        lng: location.address.lng,
        id: location.id
      }));

      foodInfo.value = data.map((info) => ({
        id: info.id,
        name: info.name,
        street: info.street,
        phone: info.phone,
        openHours: info.openHours,
        availability: info.availability,
        availableFoods: info.availableFoods
      }));
    })
    .catch(error => {
      console.error("Failed to fetch locations", error);
    });
});




// Handle the marker click event
function handleMarkerClick (id) {
  // Store the clicked marker's data in the selectedMarker ref
  selectedId.value = id;
  selectedMarker.value = foodInfo.value.find(info => info.id === id);
  console.log("Clicked Marker ID:", id);
}

function reserve(){
  reserveFood(uuId, selectedFood.value, selectedTime.value)
    .then(result => {
      if (result.success) {
        console.log("Reservation successful:", result.data);
      } else {
        console.error("Reservation failed:", result.error);
      }
    })
    .catch(error => {
      console.error("Unexpected error:", error);
    });
}

// what data should come from the back?
// user name (business/foodbanks name, their address(long/lat), their address(street), phone, 
// openhours, available foods list, available or not(bool), )


</script>

