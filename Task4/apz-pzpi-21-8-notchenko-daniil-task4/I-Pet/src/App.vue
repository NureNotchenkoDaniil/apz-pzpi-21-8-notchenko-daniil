<template>
  <div id="content">
    <header>
      <NavBar />
    </header>
    <main>
      <hr>
      <router-view />
      
    </main>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar,
   
  }
}
</script>

<style>
#content {
  text-align: center;  
}
main {
  padding: 30px 5%;
}
</style>

