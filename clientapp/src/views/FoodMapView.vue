<template>
  <div>
    <h2>Food Donations Near You</h2>
    <googleMap :center="userLoc" :markers="foodLocations"/>
  </div>
</template>


<!-- TODO: Receive the available food list data from the back, and populate them into the foodLocations abjects  -->

<script setup>
import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import mapService from '@/services/mapService'

const foodLocations = ref([]);
const foodinfo = ref([]);

//TOOD: this should be retrieved from the back
const userLoc = ref({lat: 37.7730, lng: -122.4183});

onMounted(async () => {
  try {
    const data = mapService.foodLists();
    
    foodLocations.value = data.map((location) => ({
      lat: location.address.lat,
      lng: location.address.lng,
    }));

    

  } catch (error) {
    console.error("Failed to fetch locations", error);
  }
});

// what data should come from the back?
// user name (business/foodbanks name, their address(long/lat), their address(street), phone, 
// openhours, available foods list, available or not(bool), )


</script>

