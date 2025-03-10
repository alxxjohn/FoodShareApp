<template>
    <h1>Food Share App</h1>
    <div class="container">
      <button @click="health">healthy?</button>
      <p v-if="status ">status : {{ status  }}</p>
    </div>
  </template>
  
  <script>
  import health_check from "@/services/health-check"
  
  export default {
    data() {
      return {
        status : null,
      };
    },
    methods: {
      health(){
        health_check.health()
          .then(res => this.status = res.status)
          .catch(error =>{ 
            console.error("Login Error:", error);
            this.status = error.status;
          });
      }
    },
  };
  </script>
  
  <style>
  .container {
    text-align: center;
    margin-top: 50px;
  }
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
  p {
    margin-top: 20px;
    font-size: 18px;
    color: green;
  }
  </style>
  