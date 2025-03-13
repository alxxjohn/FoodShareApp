<template>
  <div>
    <h2>Food Donations Near You</h2>
    <!-- <googleMap :locations="foodLocations" v-if="foodLocations.length > 0" /> -->
    <googleMap/>
  </div>
</template>

<!-- <script setup>
import { ref, onMounted } from 'vue';
import googleMap from '@/components/GoogleMap.vue';
import axios from 'axios'; // Assuming your API provides food locations

const foodLocations = ref([]);

onMounted(async () => {
  try {
    const { data } = await axios.get("http://your-api.com/food-locations");
    foodLocations.value = data.map((food) => ({
      lat: food.latitude,
      lng: food.longitude,
    }));
  } catch (error) {
    console.error("Failed to fetch locations", error);
  }
});
</script> -->


<script setup>
import googleMap from '@/components/GoogleMap.vue';
</script>
