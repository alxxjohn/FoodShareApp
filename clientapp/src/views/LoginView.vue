<template>
  <form @submit.prevent="submitForm" name="login-form">
    <div class="form-floating mb-3">
    <input type="text" class="form-control" id="username" placeholder="Username" v-model="login_info.username">
    <label for="username">Username</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control" id="password" placeholder="Password" v-model="login_info.password">
      <label for="password">Password</label>
    </div>
    <div class="d-flex gap-2">
      <button class="btn btn-primary" type="submit">Sign In</button>
      <router-link to="/signup">
        <button class="btn btn-primary" type="button">Register</button>
      </router-link>
    </div>
  </form> 
</template>



 <script>
 //import authService from '@/services/authService';
 import axios from 'axios';

 export default {
   name: 'LoginView',
   data(){
     return{
         login_info:{
             grant_type: "",
             username: "",
             password: "",
             client_id: "",
             client_secret: ""
         }
     }
   },

 methods: {
  submitForm() {
    const data = {
      username: this.login_info.username,
      password: this.login_info.password
    };


    //authService.login(data)
    axios.post('http://localhost:8000/api/auth/login', data, {
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
  }})
    .then((response) => {
          //console.log(response);
          const token = response.data.access_token;
          localStorage.setItem('access_token', token);
          const str = JSON.stringify(token);
          console.log("Data = " + str);
          this.message = 'Login successful!';
          this.messageClass = 'success';

          this.$router.push('/userhome');
        })
        .catch((error ) => {
          console.log(error.response);
          this.message = 'Error registering name';
          this.messageClass = 'error';
        });

        
        
        

        


  }


 }
 };

 </script>