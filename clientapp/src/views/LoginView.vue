<template>
  <form name="login-form">
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
 export default {
   name: 'LoginView',
   data(){
     return{
         login_info:{
             username: "",
             password: ""
         }
     }
   }
 }
 </script>