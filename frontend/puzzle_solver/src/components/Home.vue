<script setup lang="ts">

</script>

<template>
  <div class="conteneur_boutons">
    <button>
      <router-link to="/GeneratePuzzle">Générer un puzzle</router-link>
    </button>

    <button>
      Résoudre un puzzle
    </button>

    <button>
      Modifier le jeu
    </button>
  </div>

  <div class="imagesMenu">
    <img src="/assets/img/room/room.png" class="room"/>
  </div>
</template>

<style scoped>
.conteneur_boutons {
  margin: 1em auto 0 auto;
  width: fit-content;
  max-width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

button {
  width: 200px;
  background-color: #727097;
  border-color: #727097;
  border-style: solid;
  border-width: 4px;
  color: #eaeaea;
  margin: 0 25px;
  height: 4em;
  transition: background-color 0.5s;
}

button:hover{
  background-color: white;
  color: #727097;
  transition: background-color 0.5s;
}

a {
  text-decoration: none;
  color: inherit;
}

.imagesMenu {
  margin: 1em auto 0 auto;
  width: fit-content;
  max-width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}


.room {
  max-width: 85%;
  margin: 50px 25px;
  border-radius: 50px;
}

.room {
  width: 400px;
}



@media (max-width: 800px){
  button {
    min-width: 51%;
    margin: 5px auto;
  }

  .room {
    max-width: 85%;
    margin: 50px auto;
    border-radius: 50px;
    width: 400px;
  }
}
</style>