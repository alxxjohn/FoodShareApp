<template>

<h2 class="text-center">Add Donation</h2>


  <div id="food-and-quant" class="row g-3 d-flex">
    <div v-for="(item, index) in addedFoodList" :key="index" class="row g-3 align-items-end">
      <div class="col-md-1">
        <h4>{{ index+1 }}.</h4>
      </div>
      
      <div class="col-md-2">
        <label v-if="index === 0" class="form-label">Description:</label>
        <input type="text" 
          class="form-control" 
          v-model="addedFoodList[index].name" 
        />
      </div>
      
      <div class="col-md-2">
        <label v-if="index === 0" class="form-label">Quantity:</label>
        <input type="text" 
          class="form-control" 
          v-model="addedFoodList[index].quant" 
        />
      </div>

      <div class="col-md-1 d-flex">
        <button v-if="addedFoodList.length > 1" @click="removeList(index)" class="btn btn-outline-danger">-</button>

        <button v-if="index === addedFoodList.length - 1 && addedFoodList.length < maxList" 
                @click="addList" 
                class="btn btn-outline-success ms-2">+</button>
      </div>


      <div class="col-md-2" id="donation-button" v-if="index === 0">
        <button type="button" class="btn btn-primary" @click="addDonation" :disabled="disabledButton()">Add Donations</button>
      </div>

    </div>
    
  </div>

</template>

<script setup>
// import { ref, onMounted } from 'vue';
import { ref } from 'vue';
import { addDonationService } from '@/services/foodService';

const addedFoodList = ref([{name: null, quant:null}]); 
const maxList = 10; // user can add maximum 10 items at a time


//add a list
function addList(){
  
  if (addedFoodList.value.length < maxList) {
    addedFoodList.value.push({ name: null, quant: null });
  }
}

// Remove a list
function removeList(index){
  if (addedFoodList.value.length > 1) {
    //remove the element in the array by its index
    addedFoodList.value.splice(index, 1);
  }
}

//TODO: modify to adapt more sophisticate validation
function disabledButton(){
  return !(
    addedFoodList.value[0].name != null &&
    addedFoodList.value[0].quant != null
  );
}

function addDonation(){
  addDonationService(addedFoodList.value)
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


</script>