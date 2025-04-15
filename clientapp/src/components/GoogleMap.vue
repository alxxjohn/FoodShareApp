<template>
  <GoogleMap :api-key="API_KEY" style="width: 100%; height: 400px" :zoom="12" :center="center">
    <Marker 
      v-for="(location, index) in markers" 
      :key="index" 
      :options="{ position: location}"
      @click="onMarkerClick(location.id)"
    />
    <!-- :options="{ position: location, icon: location.icon }" -->
  </GoogleMap>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
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


// Emit the selected marker data to the parent
const emit = defineEmits(['markerClicked']);

const onMarkerClick = (id) => {
  // Emit the marker data to the parent component (FoodMapView.vue)
  emit('markerClicked', id);
};


</script>



