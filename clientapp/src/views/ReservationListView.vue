<template>
  <div class="container mt-4">
    <h2 class="text-center">Food Donations</h2>
    <div class="row">
      <div class="col-md-4">
        <div class="card bg-primary text-white p-3">
          <h5>Available</h5>
          <ul class="text-start">
            <li v-for="food in available" :key="food.id">{{ food.name }} {{ food.quant }}</li>
          </ul>
        </div>
        <button class="btn btn-info mt-2" @click="addDonation">Add Donation</button>

      </div>
      <div class="col-md-4">
        <div class="card bg-danger text-white p-3">
          <h5>Reserved</h5>
          
          <ul class="text-start">
            <li 
              v-for="reservation in reserved" 
              :key="reservation.id"
              @click="openReservation(reservation)"
              style="cursor: pointer;"
            > 
              <div class="row align-items-center">
                <div class="col-6">
                  {{ reservation.firstname }} ({{ reservation.reservationTime }})
                </div>
                <div            
                  v-if="activeReservationId === reservation.id" 
                  class="bg-light border rounded p-1 col-6"
                  @click.stop
                >
                  <div class="button-box">  
                    <button class="btn btn-sm btn-success" @click.stop="pickedUpReservation(reservation)">Picked Up</button>
                    <button class="btn btn-sm btn-danger" @click.stop="deleteReservation(reservation.id)">Delete</button>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary text-white p-3">
          <h5>Picked Up</h5>
          <ul class="text-start">
            <li v-for="reservation in pickedup" :key="reservation.id">{{ reservation.firstname }} ({{ reservation.showedUpTime }})</li>
          </ul>
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
import { getReservationList } from '@/services/reservationService'
import authService from '@/services/authService';



const router = useRouter();
const available = ref([{name:null, quant:null}]);
const reserved = ref([]);
const pickedup = ref([]);
const activeReservationId = ref(null);
const selectedReservation = ref(null);


onMounted(() => {
  authService.getCurrentLoggedInUser()
    .then(userInfo => {
      getInventory(userInfo.data.uuid)
        .then(res => {
          if(res.success){
            available.value = res.availableFoods.map((inven) => ({
            name: inven.name,
            quant: inven.quant
            }));
          } else {          
            if (res.error?.status === 404) {
              console.warn("Inventory not found for this user.");
            } else {
              console.error("Failed to fetch the inventory: ", res.error);
            }
          }          
        })
      getReservationList(userInfo.data.uuid)  
        .then(res => {
          if(res.success){
            res.reservationList.forEach((reservation) => {
              if (reservation.status === 'reserved'){
                reserved.value.push(reservation);
              } else if (reservation.status === 'pickedup'){
                pickedup.value.push(reservation);
              }
            })
            reserved.value.sort((a, b) => a.reservationTime.localeCompare(b.reservationTime));
            pickedup.value.sort((a, b) => a.showedUpTime.localeCompare(b.showedUpTime));
          } else {
            if (res.error?.status === 404) {
              console.warn("Reservation not found for this user.");
            } else {
              console.error("Failed to fetch the reservation list: ", res.error);
            }
          }
        })
      })
  .catch(error => {
    console.log("unable to retrieve the current user", error);
  })
});


//redirecto to donation page
function addDonation(){
  router.push('/donation');
}

function openReservation(reservation) {
  if (activeReservationId.value === reservation.id) {
    activeReservationId.value = null;
    selectedReservation.value = null;
    return;
  }
  
  activeReservationId.value = reservation.id;
  selectedReservation.value = reservation;
}

function pickedUpReservation(reservation) {
  console.log('Modify clicked:', reservation)
  activeReservationId.value = null
}

function deleteReservation(id) {
  console.log('Delete clicked for ID:', id)
  activeReservationId.value = null
}

</script>


<style>
  .button-box {
    display: flex; 
    justify-content: center; 
    gap: 1rem; 
  }

</style>