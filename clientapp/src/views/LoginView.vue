<template>
  <form name="login-form" >
    <div class="mb-3">
      <label for="username">Username: </label>
      <input id="username" type="text" />
    </div>
    <div class="mb-3">
      <label for="password">Password: </label>
      <input id="password" type="password" />
    </div>
    <button class="btn btn-primary" type="submit">
      Login
    </button>
  </form>
</template>

<script>
export default {
name: 'LoginView',
}
</script>