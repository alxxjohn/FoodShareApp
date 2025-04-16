<template>
  <div class="container mt-4">
    <h2 class="text-center">Food Donations</h2>
    <div class="row">
      <div class="col-md-4">
        <div class="card bg-primary text-white p-3">
          <h5>Available</h5>
          <ul class="text-start">
            <span>Food&emsp;Quantity</span>
            <li v-for="food in available" :key="food.id">{{ food.name }} &emsp;{{ food.quant }}</li>
          </ul>
        </div>
        <button class="btn btn-info mt-2" @click="addDonation">Add Donation</button>

      </div>
      <div class="col-md-7">
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
                  {{ reservation.firstname }} {{ reservation.lastname }} ({{ reservation.reservationTime }})
                </div>
                <div            
                  v-if="activeReservationId === reservation.id" 
                  class="bg-light border rounded p-1 col-6"
                  @click.stop
                >
                  <div class="button-box">  
                    <button class="btn btn-sm btn-success" @click.stop="pickedUpReservation(reservation.id)">Picked Up</button>
                    <button class="btn btn-sm btn-danger" @click.stop="deleteReservation(reservation.id)">Delete</button>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { getInventory } from '@/services/foodService';
import { getReservationList, updateReservation, deleteReservationService } from '@/services/reservationService';
import { getUserByUserId } from '@/services/userService';
import authService from '@/services/authService';


const router = useRouter();
const available = ref([{name:null, quant:null}]);
const reserved = ref([]);
const activeReservationId = ref(null);
const selectedReservation = ref(null);


onMounted(async () => {
  try {
    const userInfo = await authService.getCurrentLoggedInUser();

    // get inventory
    const invRes = await getInventory(userInfo.data.uuid);
    if (invRes.success) {
      available.value = invRes.data.map(inven => ({
        name: inven.item_name,
        quant: inven.item_qty
      }));
    } else {
      if (invRes.error?.status === 404) {
        console.warn("Inventory not found for this user.");
      } else {
        console.error("Failed to fetch the inventory: ", invRes.error);
      }
    }

    // get reservations
    await loadReservations(userInfo.data.uuid);

  } catch (error) {
    console.log("Unable to retrieve the current user", error);
  }
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

function pickedUpReservation(reservationId) {
  updateReservation(reservationId)
    .then(response => {
      if (!response.success) {
        console.error("Update Reservation failed:", + JSON.stringify(response.error));
        return;
      }
    });
  activeReservationId.value = null
}

function deleteReservation(reservationId) {
  deleteReservationService(reservationId)
    .then(response => {
      if (!response.success) {
        console.error("Update Reservation failed:", + JSON.stringify(response.error));
        return;
      }
    });
  activeReservationId.value = null
}
async function parseReservation(reservation) {
  try {
    const res = await getUserByUserId(reservation.user_uuid);

    if (res.success) {
      const date = new Date(reservation.reserve_time);
      const formattedTime = date.toISOString().slice(0, 16).replace("T", " ");

      const parsed = {
        id: reservation.reservation_uuid,
        reservationTime: formattedTime,
        firstname: res.data.firstname,
        lastname: res.data.lastname,
      };

      return parsed;
    } else {
      if (res.error?.status === 404) {
        console.warn("User not found for this ID.");
      } else {
        console.error("Failed to fetch user: ", res.error);
      }
    }
  } catch (error) {
    console.error("Failed to fetch user:", error);
  }

  return null;
}

async function loadReservations(userId) {
  reserved.value = [];

  const res = await getReservationList(userId);
  if (res.success) {
    for (const reservation of res.data) {
      const parsedReservation = await parseReservation(reservation);
      if (reservation.current_status === 'reserved') {
        reserved.value.push(parsedReservation);
      } 
    }
  } else {
    if (res.error?.status === 404) {
      console.warn("Reservation not found for this user.");
    } else {
      console.error("Failed to fetch the reservation list: ", res.error);
    }
  }
}
</script>


<style scoped>
  .button-box {
    display: flex; 
    justify-content: center; 
    gap: 1rem; 
  }

</style>