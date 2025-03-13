<template>
  <GoogleMap :api-key="API_KEY" style="width: 100%; height: 400px" :zoom="12" :center="center">
    <Marker 
      v-for="(location, index) in markers" 
      :key="index" 
      :options="{ position: location }"
      @click="onMarkerClick(location, index)" 
    />
  </GoogleMap>
</template>

<script setup>
import { defineProps, ref } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";

const API_KEY = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;

// Accept props from FoodMapView.vue
defineProps({
  center: {
    type: Object,
    required: true,
  },
  markers: {
    type: Array,
    required: true,
  },
});

// Store the selected marker information
const selectedMarker = ref(null);

// Handle the click event on a marker
const onMarkerClick = (location, index) => {
  // Set the selected marker's information (you could pass more data if needed)
  selectedMarker.value = {
    ...location,  // Include lat/lng if needed
    name: `Food Bank ${index + 1}`,
    street: `Street for location ${index + 1}`,
    availableFoods: ["Canned Beans", "Rice", "Bread"], // You can replace these with actual data
  };
};


</script>



