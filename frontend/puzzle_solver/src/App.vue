<script setup lang="ts">
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <Header msg="Vite + Vue" />
  <div class="home">
    <router-view />
  </div>
  <Footer msg="Foot" />
</template>

<style scoped>
.home {
  margin: auto;
  width: 95%;
  max-width: 950px;
  font-size: 22px;
  min-height: calc(100vh - 275px); /* 150px = réhaussement actuel du footer*/
}
</style>
