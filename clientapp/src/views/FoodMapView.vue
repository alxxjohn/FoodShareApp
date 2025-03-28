<template>
  <div id="food-map">
    <h2>Food Donations Near You</h2>
    <googleMap 
      :center="userLoc" 
      :markers="foodLocations" 
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
      <span>{{ selectedMarker.street }}, {{ selectedMarker.city }}, {{ selectedMarker.state }} {{ selectedMarker.zip }}</span>
    </div>
    <div>
      <label>Phone:</label>
      <span>{{ selectedMarker.phone }}</span>
    </div>
    <div>
      <label>Available Foods:</label>
      <select v-model="selectedFood">
        <option v-for="food in selectedMarkerInv.availableFoods" :key="food.id" :value="food">
          {{ food.desc }}
        </option>
      </select>
    </div>
    <div v-if="selectedFood">
      <label>Quantity: </label>
      <input type="text" class="form-control" v-model="selectedQuant" aria-describedby="maxQuantHelp">
      <div id="maxQuantHelp" class="form-text">The maximum quantity is {{ selectedFood.quant }}</div>
    </div>
  </div>

  <div id="timepicker-form" v-if="selectedMarker"> 
    <label>Select a time:</label>
    <input type="time" class="form-control" id="timepicker" v-model="selectedTime" />
  </div>

  <div id="reserve-button" v-if="selectedMarker">
      <button type="button" class="btn btn-primary" @click="reserve" :disabled="disabledButton()">Reserve</button>
  </div>

</template>


<!-- TODO: Receive the available food list data from the back, and populate them into the foodLocations abjects  -->
<!-- TODO: disabled or error message if the values aren't given by the user, or availability is true. -->

<script setup>
import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import { getFoodbankLists, getInventory } from '@/services/foodService'
import { reserveFood } from '@/services/reservationService'

const foodLocations = ref([]);
const locationInfo = ref([]);
const selectedMarker = ref(null);
const selectedMarkerInv = ref([]);
const selectedFood = ref(null);
const selectedTime = ref(null);
const selectedQuant = ref(null);

//TOOD: this should be retrieved from the back (login info? from cache?)
const userLoc = ref({lat: 37.7730, lng: -122.4183});
const uuId = 1;

onMounted(() => {
  getFoodbankLists()
    .then(data => {
      foodLocations.value = data.map((location) => ({
        lat: location.address.lat,
        lng: location.address.lng,
        id: location.id,
        icon: getMarkerIcon(location.availability)
      }));

      locationInfo.value = data.map((info) => ({
        id: info.id,
        name: info.name,
        street: info.street,
        city: info.city,
        state: info.state,
        zip: info.zip,
        phone: info.phone,
        availability: info.availability,
      }));
    })
    .catch(error => {
      console.error("Failed to fetch locations", error);
    });
});




// Handle the marker click event
async function handleMarkerClick (id) {
  selectedMarkerInv.value = await getInventory(id);
  
  selectedMarker.value = locationInfo.value.find(info => info.id === id);

  console.log("Clicked Marker ID:", id);


}

//Change the marker color based on each location's availability
function getMarkerIcon(availability){
  if (availability === true) {
    return "http://maps.google.com/mapfiles/ms/icons/green-dot.png"; 
  } else {
    return "http://maps.google.com/mapfiles/ms/icons/red-dot.png"; 
  }
}

//Diable reserve button if there is no availiabity at the location, or user didn't add all inforamtion
function disabledButton(){  
  return !(
    selectedMarker.value.availability === true &&
    uuId != null && 
    selectedFood.value != null && 
    selectedTime.value != null &&
    selectedQuant.value > 0 &&
    selectedQuant.value <= selectedFood.value.quant
  );
}

function reserve(){
  reserveFood(uuId, selectedFood.value.id, selectedTime.value)
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

