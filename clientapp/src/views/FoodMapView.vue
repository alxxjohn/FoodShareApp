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

  <div id="food-info-box" v-if="selectedMarker" >
    <div>
      <label>Name:</label>
      <span>{{ selectedMarker.name }}</span>
    </div>
    <div>
      <label>Address:</label>
      <span>{{ selectedMarker.street }}, {{ selectedMarker.city }}, {{ selectedMarker.state }} {{ selectedMarker.zip }}</span>
    </div>
<!-- PHONE VALUE ISN't in BUSINESS TABLE -->
    <!-- <div>
      <label>Phone:</label>
      <span>{{ selectedMarker.phone }}</span>
    </div> -->
  </div>

  <div id="food-and-quant" v-if="selectedMarker" class="row g-3 d-flex">
    <div v-for="(item, index) in selectedFoodList" :key="index" class="row g-3 align-items-end">
      <div class="col-md-3">
        <label v-if="index === 0" class="form-label">Available Foods:</label>
        <select class="form-select" v-model="selectedFoodList[index].food">
          <option v-for="food in selectedMarkerInv.availableFoods" :key="food.id" :value="food">
            {{ food.name }}

          </option>
        </select>
      </div>
      
      <div class="col-md-2">
        <div class="invalid-msg" v-if="invalidQuant(index)">
          Max quantity is {{selectedFoodList[index].food.quant}}!
        </div>
        <input type="text" 
          class="form-control" 
          v-model="selectedFoodList[index].quant" 
          :placeholder="selectedFoodList[index].food ? `Max quantity: ${selectedFoodList[index].food.quant}` : 'Quantity'" 
          :class="{ 'is-invalid': invalidQuant(index) }" 
        />

      </div>

      <div class="col-md-1 d-flex">
        <button v-if="selectedFoodList.length > 1" @click="removeDropdown(index)" class="btn btn-outline-danger">-</button>

        <button v-if="index === selectedFoodList.length - 1 && selectedFoodList.length < maxDropdowns" 
                @click="addDropdown" 
                class="btn btn-outline-success ms-2">+</button>
      </div>

      <div class="col-md-2" id="timepicker-form" v-if="index === 0"> 
          <label class="text-start">Select a time:</label>
          <input type="time" class="form-control" id="timepicker" v-model="selectedTime" />
      </div>

      <div class="col-md-2" id="reserve-button" v-if="index === 0">
        <button type="button" class="btn btn-primary" @click="reserve" :disabled="disabledButton() && invalidQuant">Reserve</button>

      </div>

    </div>
    
  </div>

</template>


<script setup>
// TODO: block user to add the same product in the reservation (i.e., preventing add the same product more than once)

import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import { getFoodbankLists, getInventory } from '@/services/foodService'
import { reserveFood } from '@/services/reservationService'

const foodLocations = ref([]);
const locationInfo = ref([]);
const selectedMarker = ref(null);
const selectedMarkerInv = ref(null);
const selectedTime = ref(null);
const selectedFoodList = ref([{food: null, quant:null}]); 

let maxDropdowns = 1;



//TOOD: since the user doesn't add their address when register, it can be some random address to start
//TODO: add address search bar to move around the map 
const userLoc = ref({lat: 28.596425775510205, lng: -81.4507097448979});

onMounted(() => {
  getFoodbankLists()
    .then(data => {
      console.log("data: " + JSON.stringify(data));
      // foodLocations.value = data.map((location) => ({
      //   lat: location.lat,
      //   lng: location.lng,
      //   id: location.business_id,
      //   // icon: getMarkerIcon(location.availability)
      // }));

      // locationInfo.value = data.map((info) => ({
      //   id: info.id,
      //   name: info.company_name,
      //   street: info.address,
      //   city: info.city,
      //   state: info.state,
      //   zip: info.zipcode,
        // phone: info.phone, //maybe remove
      //   // availability: info.availability,
      // }));
    })
    //when it's error, it doesn't come to catch block? :(
    .catch(error => {
      console.error("Failed to fetch locations", error);
    });
});


/*
 business_id              |   company_name    |        address        |  city   | state | zipcode |        lat         |        lng
  | is_foodbank |              assoc_user
*/


// Handle the marker click event
async function handleMarkerClick (id) {
  //reset the selectedFoodList
  selectedFoodList.value = [{ food: null, quant: null }];

  selectedMarkerInv.value = await getInventory(id);
  
  //set maxDropdown to be the number of available foods for each location
  maxDropdowns = selectedMarkerInv.value.availableFoods.length;
  
  selectedMarker.value = locationInfo.value.find(info => info.id === id); 
  
  //Log clicked marker Id
  // console.log("Clicked Marker ID:", id);
}

//Change the marker color based on each location's availability
// function getMarkerIcon(availability){
//   if (availability === true) {
//     return "http://maps.google.com/mapfiles/ms/icons/green-dot.png"; 
//   } else {
//     return "http://maps.google.com/mapfiles/ms/icons/red-dot.png"; 
//   }
// }

//return true (disable) if required values aren't given
function disabledButton(){  
    return !(
    selectedFoodList.value[0].food != null &&
    selectedFoodList.value[0].quant != null &&
    selectedTime.value != null
  );
}

//TODO: send an array of food items not a single item
function reserve(){
  const request = createRequestBody();

  reserveFood(request)

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

//add a dropdown
function addDropdown(){
  
  if (selectedFoodList.value.length < maxDropdowns) {
    selectedFoodList.value.push({ food: null, quant: null });
  }
}

// Remove a dropdown
function removeDropdown(index){
  if (selectedFoodList.value.length > 1) {
    //remove the element in the array by its index
    selectedFoodList.value.splice(index, 1);
  }
}

//TODO: valiadation should be more sophisticate?? :( 
//returns true (invalid) if the given input is invalid
function invalidQuant(index){
  const item = selectedFoodList.value[index];
  
  //there is no selected foods
  if(!item.food)
    return false;

  //given value is not a number
  if(isNaN(Number(item.quant)))
    return true;

  //if selected quantity(item.quant) is smaller or equal to max quantity (item.food.quant) for selected foods
  return item.quant > item.food.quant && item.quant < 0;


  }

  function createRequestBody(){
    const request = {
      reservations_array:[], 
      reserve_time:selectedTime.value

    };

    for(let i = 0; i < selectedFoodList.value.length; i++ ){
      const addedFood = {
        item_id:selectedFoodList.value[i].food.id, 
        item_qty:selectedFoodList.value[i].quant
      };
      request.reservations_array.push(addedFood);

    }

    return request;

  }

</script>

<style>
.invalid-msg {
  color: red;
  font-size: 0.875em;
  margin-top: 5px;
}

</style>