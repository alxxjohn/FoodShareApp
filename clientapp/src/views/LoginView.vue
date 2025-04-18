<template>
  <div class="login-container">
    <form @submit.prevent="submitForm" name="login-form" class="login-form">
      <div class="form-floating mb-3">
        <input type="text" class="form-control" id="username" placeholder="Username" v-model="username">
        <label for="username">Username</label>
      </div>
      <div class="form-floating mb-3">
        <input type="password" class="form-control" id="password" placeholder="Password" v-model="password">
        <label for="password">Password</label>
      </div>
      <div class="d-flex justify-content-between gap-2">
        <button class="btn btn-primary w-100" type="submit">Sign In</button>
        <router-link to="/signup" class="w-100">
          <button class="btn btn-secondary w-100" type="button">Register</button>
        </router-link>
      </div>
    </form>
  </div>
</template>



 <script>
 import authService from '@/services/authService';
 import { isLoggedIn, isBusiness } from '@/utils/authState'


 export default {
   name: 'LoginView',
   data(){
     return{
      grant_type: "",
      username: "",
      password: "",
      client_id: "",
      client_secret: ""
     }
   },

 methods: {
  submitForm() {
    const data = {
      username: this.username,
      password: this.password
    };

    //Call login service method
    authService.login(data)
    .then((response) => {
          
      console.log("response.data: " + JSON.stringify(response.data));
         
      const token = response.data.access_token;
      localStorage.setItem('access_token', token);
      authService.setToken(token);
      
      isLoggedIn.value = true;

      this.redirectBasedOnUserType();
    })
    .catch((error ) => {
      console.log(error.response);
    });

  },

  redirectBasedOnUserType(){
    authService.getCurrentLoggedInUser()
      .then((response) => {
        localStorage.setItem('is_business', response.data.is_business);
        authService.setIsBusiness(response.data.is_business);
        isBusiness.value = response.data.is_business;

        if(response.data.is_business){
          this.$router.push('/reservation-list');
        } else {
          this.$router.push('/foodmap');
        }        
      })
      .catch((error) => {
        console.log(error.message);
      });
  },

 }
 };

 </script>

<style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    padding-top: 60px; 
  }

  .login-form {
    max-width: 400px;
    width: 100%;
  }
 </style>