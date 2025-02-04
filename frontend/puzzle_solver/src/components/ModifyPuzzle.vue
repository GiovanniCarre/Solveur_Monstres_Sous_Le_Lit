<script setup lang="ts">

import {ref} from "vue";

const nbMonster = 8;
const tableauMonstres = ref<number[]>([]);

for (let i = 0; i < nbMonster; i++) {
  tableauMonstres.value.push(Math.floor(Math.random() * 2) * Math.floor(Math.random() * 4));
}

const loading = ref(false);

async function fetchMap() {
  loading.value = true;

  try {
    console.log(JSON.stringify({tableauMonstres: tableauMonstres.value}))
    // Envoi de la requête avec le tableauMonstres
    const response = await fetch('http://localhost:3000/generateMap', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({tableauMonstres: tableauMonstres.value}),
    });

    const result = await response.json();
    console.log(result)

  } catch (error) {
    console.error('Erreur lors de la vérification du défi:', error);
  } finally {
    loading.value = false;
  }
};


</script>

<template>
  <section class="challengeSection">
    <div class="monster" v-for="(_, index) in tableauMonstres" :key="index">
      <input class="selectionMonsterNumber"
             type="number"
             v-model="tableauMonstres[index]"
             :min="0"
             :max="30"
             :step="1"
      />

      <img class="imgMonster" :src="`/assets/img/monstres/monstres_${index + 1}.png`" alt="monstres monster"/>
    </div>
  </section>

  <button id='buttonClick' @click="fetchMap">
    <span v-if="loading">Envoi en cours ⌛</span>
    <span v-else>Générer la carte et les masques</span>
  </button>

  <canvas id="game" ref="canvasRef"></canvas>

</template>

<style scoped>


.imgMonster{
  width: 150px;
}



#buttonClick{
  color:white;
}
button {
  position: relative;
  font-size: 16px;
  padding: 10px 15px;
}

button span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.challengeSection {
  margin-top: 20px;
}

.monster {
  display: inline-block;
  width:180px;
  text-align: center;
}


#game {
  width: 600px;
  height: 500px;
  display: block;
  margin-top: 1em;
}

</style>