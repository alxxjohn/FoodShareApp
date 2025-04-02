<template>
    <NavBar />
    
    <router-view /> <!-- This will display the current page -->
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  
  export default {
    components: {
      NavBar
    }
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;

  /* Set max width and center */
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
}
</style>
