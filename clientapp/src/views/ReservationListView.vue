<template>
  <div class="container mt-4">
    <h2 class="text-center">Food Donations</h2>
    <div class="row">
      <div class="col-md-4">
        <div class="card bg-primary text-white p-3">
          <h5>Available</h5>
          <ul class="list-unstyled">
            <li v-for="food in available" :key="food.id">{{ food.name }}: {{ food.quant }}</li>
          </ul>
        </div>
        <button class="btn btn-info mt-2" @click="addDonation">Add Donation</button>

      </div>
      <div class="col-md-4">
        <div class="card bg-danger text-white p-3">
          <h5>Reserved</h5>
          <!-- <ul class="list-unstyled">
            <li v-for="food in reservedFoods" :key="food.id">{{ food.name }} ({{ food.reservedBy }})</li>
          </ul> -->
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-secondary text-white p-3">
          <h5>Picked Up</h5>
          <!-- <ul class="list-unstyled">
            <li v-for="food in pickedUpFoods" :key="food.id" @click="selectFood(food)">{{ food.name }}</li>
          </ul> -->
        </div>
      </div>
    </div>
    <!-- <div v-if="selectedFood" class="mt-3">
      <h5>Actions for {{ selectedFood.name }}</h5>
      <button class="btn btn-warning me-2" @click="editFood">Edit</button>
      <button class="btn btn-danger" @click="removeFood">Remove</button>
    </div> -->
  </div>
</template>

<script setup>

import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { getInventory } from '@/services/foodService'


const router = useRouter();
//TODO: it should be from back api (login info?)
const foodbankId = 1;

const available = ref([{name:null, quant:null}]);

onMounted(() => {
  getInventory(foodbankId)
    .then(data => {
      console.log("data: "+JSON.stringify(data, null, 2)); 
      available.value = data.availableFoods.map((inven) => ({
        name: inven.name,
        quant: inven.quant
      }));
    })
    .catch(error => {
      console.error("Failed to fetch inventory", error);
    })
   console.log("request: "+JSON.stringify(available.value, null, 2)); 

});


//redirecto to donation page
function addDonation(){
  router.push('/donation');
}

</script>