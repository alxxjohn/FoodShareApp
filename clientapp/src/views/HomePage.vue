<template>
    <h1>Food Share App</h1>
    <div class="container">
      <button @click="health">healthy?</button>
      <p v-if="status ">status : {{ status  }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        status : null,
      };
    },
    methods: {
      async health() {
        try {
          const res = await axios.get('/api/health');
            this.status = res.status;
        } catch (error) {
            console.error('Error:', error);
            this.status = 'Error connecting to api';
        }
      },
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
  