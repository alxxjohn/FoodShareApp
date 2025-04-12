<template>
  <form @submit.prevent="submitForm" name="login-form">
    <div class="form-floating mb-3">
    <input type="text" class="form-control" id="username" placeholder="Username" v-model="username">
    <label for="username">Username</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control" id="password" placeholder="Password" v-model="password">
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
 import authService from '@/services/authService';

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

    // console.log("RequestBody: " + JSON.stringify(data));

    //Call login service method
    authService.login(data)
    .then((response) => {
          
      // console.log("response.data: " + JSON.stringify(response.data));
         
      const token = response.data.access_token;
      localStorage.setItem('access_token', token);
      authService.setToken(token);
      
      //TO test access token
      // this.getCurrentUserInfo();

      //redirect to foodmap view
      this.$router.push('/foodmap');
    })
    .catch((error ) => {
      console.log(error.response);
    });

  },

  getCurrentUserInfo(){
    authService.getCurrentLoggedInUser()
      .then((response) => {
        console.log("current user: " + JSON.stringify(response.data));
      })
      .catch((error) => {
        console.log(error.message);
      });
  },

 }
 };

 </script>