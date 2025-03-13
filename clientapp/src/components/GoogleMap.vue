<template>
  <GoogleMap :api-key="API_KEY" style="width: 100%; height: 400px" :center="center" :zoom="12">
    <Marker v-for="(location, index) in locations" :key="index" :options="{ position: location }" />
  </GoogleMap>
</template>

<script setup>
import { ref } from "vue";
import { GoogleMap, Marker } from "vue3-google-map";

const API_KEY = process.env.VUE_APP_GOOGLE_MAPS_API_KEY;

const center = ref({ lat: 37.7749, lng: -122.4194 });
const locations = ref([
  { lat: 37.7749, lng: -122.4194 },
  { lat: 37.7849, lng: -122.4294 },
]);
</script>

