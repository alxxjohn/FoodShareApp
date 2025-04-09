<template>
    <h1>Hello {{ this.username }}</h1>
 </template>
  
  <script>
 import axios from 'axios';

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
        const token = localStorage.getItem('access_token');
    const response = axios.get('http://localhost:8000/api/auth/user', {
 headers: {
   'Accept': 'application/json',
   'Authorization': `Bearer ${token}`
 }})

 if (response && response.data) {
            // Update user_info with the response data
            this.user_info.username = response.data.username;
            this.user_info.email = response.data.email;
            this.user_info.uuid = response.data.uuid;

            // Log the updated user_info after receiving the data
            console.log('After API request:', this.user_info);
          }



const str = JSON.stringify(token);
          console.log("Data = " + str);
 const str2 = JSON.stringify(response.username);
 console.log("Username = " + str2);
    }

 }
};
  </script>