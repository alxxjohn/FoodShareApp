<template>
    <h1>Hello {{ user_info.username }}</h1>
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
    const response = await axios.get('http://localhost:8000/api/auth/user', {
 headers: {
   'Accept': 'application/json',
   'Authorization': `Bearer ${token}`
 }})


  this.user_info.username = response.data.username;
  this.user_info.email = response.data.email;
  this.user_info.uuid = response.data.uuid;

  console.log('After API request:', this.user_info);


const str = JSON.stringify(token);
          console.log("Data = " + str);
 const str2 = JSON.stringify(response.data.username);
 console.log("response = " + str2);
    }

 }
};
  </script>