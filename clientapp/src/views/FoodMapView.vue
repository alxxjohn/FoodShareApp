<template>
  <div>
    <h2>Food Donations Near You</h2>
    <googleMap 
      :center="userLoc" 
      :markers="foodLocations" 
      :foodInfo="foodInfo"
      @markerClicked="handleMarkerClick" 
      />
      <!-- @markerClicked listens markerClicked event from GoogleMap.vue-->
  </div>

  <div v-if="selectedInfo">
    <div>
      <label>Name:</label>
      <span>{{ selectedInfo.name }}</span>
    </div>
    <div>
      <label>Address:</label>
      <span>{{ selectedInfo.street }}</span>
    </div>
    <div>
      <label>Phone:</label>
      <span>{{ selectedInfo.phone }}</span>
    </div>
    <div>
      <label>Open Hours:</label>
      <span>{{ selectedInfo.openHours }}</span>
    </div>
    <div>
      <label>Available Foods:</label>
      <select v-model="selectedFood">
        <option v-for="food in selectedInfo.availableFoods" :key="food" :value="food">
          {{ food }}
        </option>
      </select>
    </div>
  </div>

</template>


<!-- TODO: Receive the available food list data from the back, and populate them into the foodLocations abjects  -->

<script setup>
import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import mapService from '@/services/mapService'

const foodLocations = ref([]);
const foodInfo = ref([]);
const selectedId = ref(null);
const selectedInfo = ref(null);
const selectedFood = ref(null);

//TOOD: this should be retrieved from the back (login info? from cache?)
const userLoc = ref({lat: 37.7730, lng: -122.4183});

onMounted(async () => {
  try {
    const data = mapService.foodLists();
    
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

  } catch (error) {
    console.error("Failed to fetch locations", error);
  }
});

// Handle the marker click event
const handleMarkerClick = (id) => {
  // Store the clicked marker's data in the selectedMarker ref
  selectedId.value = id;
  selectedInfo.value = foodInfo.value.find(info => info.id === id);
  console.log("Clicked Marker ID:", id);
};

// what data should come from the back?
// user name (business/foodbanks name, their address(long/lat), their address(street), phone, 
// openhours, available foods list, available or not(bool), )


</script>

