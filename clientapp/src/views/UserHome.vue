<template>
    <h1>Hello {{ user_info.username }}</h1>

    <button @click="goToMap">
    Go to map
  </button>
 </template>
   
  <script>
 import authService from '@/services/authService';

export default {
  data(){
    return{
        user_info: {
            uuid: '',
            username: "",
            email: ''
         }
    }
  },
mounted() {
    this.getUserData();
},

methods: {
    async getUserData() {
    authService.getCurrentLoggedInUser()
      .then(response => {

      if (response?.data?.username) {
        this.user_info.username = response.data.username;
        this.user_info.email = response.data.email;
        this.user_info.uuid = response.data.uuid;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    })
  },

  goToMap() {
      this.$router.push('/foodmap'); // Replace with your desired route
  }

 }
};
  </script>