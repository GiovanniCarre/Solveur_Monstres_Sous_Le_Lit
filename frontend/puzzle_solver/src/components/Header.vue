<script setup lang="ts">
import { ref } from "vue";

const menuOpen = ref(false);

const closeMenu = () => {
  menuOpen.value = false;
};
</script>

<template>
  <header class="header">
    <router-link to="/">
      <p id="titleApplication">Monstres sous le lit</p>
    </router-link>

    <div class="menu-wrapper" :class="{ open: menuOpen }">
      <nav class="menu">
        <router-link to="/" class="menu-item" @click="closeMenu">Accueil</router-link>
        <router-link to="/generate-puzzle" class="menu-item" @click="closeMenu">Générer un puzzle </router-link>
        <router-link to="/test-challenge" class="menu-item" @click="closeMenu">Tester un défi</router-link>
        <router-link to="/modify-game" class="menu-item" @click="closeMenu">Générer des chambres</router-link>
      </nav>
    </div>

    <button @click="menuOpen = !menuOpen" class="burger-button">☰</button>
  </header>
</template>

<style scoped>
/* Style pour le header */
.header {
  width: 100%;
  height: 5em;
  background-color: #727097;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* Titre de l'application */
#titleApplication {
  color: #eaeaea;
  font-size: 2em;
}

/* Bouton burger */
.burger-button {
  position: absolute;
  right: 20px;
  padding-right: 0;
  background: none;
  border: none;
  font-size: 30px;
  cursor: pointer;
  color: white;
  z-index: 101;
}

/* Le menu burger */
.menu-wrapper {
  position: fixed;
  top: 0;
  right: -250px; /* Commence hors écran */
  width: 250px;
  height: 100%;
  background: #333;
  transition: transform 0.3s ease-in-out;
  transform: rotateY(90deg); /* Rotation lorsque fermé */
  z-index: 100;
  overflow: clip;
}

/* Si le menu est ouvert */
.menu-wrapper.open {
  transform: translateX(-250px) rotateY(0deg);
}

/* Le menu */
.menu {
  display: flex;
  flex-direction: column;
  padding: 20px;
  padding-top: 4em;
}

/* Liens du menu */
.menu-item {
  color: white;
  text-decoration: none;
  padding: 10px;
  font-size: 18px;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.2);
}

</style>
