<template>
  <div id="nav">
    <nav class="container navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand" to="/main">
        <img src="../../public/logo.png" />
      </router-link>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <div class="navbar-nav mr-auto nav-links-container">
          <!-- 🟩 Logged in: Common Links -->
          <template v-if="isLoggedIn">
            <router-link to="/userhome" class="nav-item nav-link">User Home</router-link>

            <!-- 🟦 Conditional Links by userType -->
            <router-link v-if="isBusiness" to="/donation" class="nav-item nav-link">Add Donation</router-link>
            <router-link v-if="isBusiness" to="/reservation-list" class="nav-item nav-link">Reservation List</router-link>

            <a class="nav-item nav-link" @click="signOut" style="cursor: pointer;">Sign Out</a>
          </template>

          <!-- 🟥 Not Logged in -->
          <template v-else>
            <router-link to="/login" class="nav-item nav-link">Login</router-link>
            <router-link to="/signup" class="nav-item nav-link">Sign Up</router-link>
          </template>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { isLoggedIn, isBusiness } from '@/utils/authState'

const router = useRouter();

const signOut = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('is_business')
  
  isLoggedIn.value = false;
  isBusiness.value = false;
  router.push('/login')
}
</script>

<style scoped>
  .navbar-brand img {
    width: 200px;
    height: auto;
    margin-left: 20px;
  }
  .nav-links-container {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  margin-right: 20px;
}
.nav-item {
  margin-left: 10px; /* Optional, to add spacing between links */
}
</style>