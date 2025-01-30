<script setup lang="ts">

</script>

<template>
    <header class="header">
      <router-link to="/">
        <p id="titleApplication">Monstres sous le lit</p>
      </router-link>
    </header>
</template>

<style scoped>
header {
  width: 100%;
  height: 5em;
  background-color: #727097;

  text-align:center;
  vertical-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

#titleApplication{
  color: #eaeaea;
  font-size:2em;
}
</style>