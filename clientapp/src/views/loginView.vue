<template>
  <form name="login-form">
    <div class="form-floating mb-3">
    <input type="text" class="form-control" id="username" placeholder="Username" v-model="login_info.username">
    <label for="username">Username</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control" id="password" placeholder="Password" v-model="login_info.username">
      <label for="password">Password</label>
    </div>
    <div class="d-flex gap-2">
      <button class="btn btn-primary" type="submit">Sign In</button>
      <button class="btn btn-primary" type="button">Register</button>
    </div>
  </form> 
</template>

<!-- <button type="button" class="btn btn-secondary" onclick="alert('Hello!')">Click Me</button> 
 I need to do it for the button Register-->


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