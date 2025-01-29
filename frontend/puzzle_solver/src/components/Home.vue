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
  color: lightgray;
  margin: 0 25px;
  height: 4em;
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