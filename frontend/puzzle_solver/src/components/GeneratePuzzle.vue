<script setup lang="ts">
import { onMounted, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);

const gridSize = 3;
const cellSize = 80; // Taille d'une cellule
const padding = 10; // Espacement entre les grilles

var img_monstres = [new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image()];
for (let i = 0; i < img_monstres.length; i++) {
  img_monstres[i].src = `/assets/img/monstres/monstres_${i+1}.png`;
}

// 4 grilles (2x2 disposition)
const grids = [
  { x: 0, y: 0 },
  { x: gridSize * cellSize + padding, y: 0 },
  { x: 0, y: gridSize * cellSize + padding },
  { x: gridSize * cellSize + padding, y: gridSize * cellSize + padding }
];


const valeurChambres = ref<number[][][]>([
  [[-1, -1, 8], [1, -1, 7], [2, 2, -1]],
  [[3, -1, -1], [6, -1, -1], [1, 5, 8]],
  [[2, -1, -1], [2, 6, 8], [1, 4, 7]],
  [[3, 6, 5], [1, -1, 8], [-1, -1, 7]]
]);


// false = affiché
const valeurMasques = ref<boolean[][][]>([
  [[false, true, false], [false, false, false], [false, true, false]],
  [[true, false, false], [false, false, false], [false, true, false]],
  [[false, false, false], [false, true, true], [false, false, false]],
  [[true, false, false], [false, false, false], [false, false, true]]
]);


const drawGrid = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const smallGridSize = 3; // Taille des petites grilles
  const smallCellSize = cellSize / 2.5; // Cellules plus petites

  canvas.width = 600;
  canvas.height = 500;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Dessiner les grandes grilles
  grids.forEach((grid, gridIndex) => {
    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        const colorValue = (valeurChambres.value[gridIndex]?.[row]?.[col] ?? 0);

        if (colorValue >= 0) {
          ctx.drawImage(img_monstres[colorValue-1], grid.x + col * cellSize, grid.y + row * cellSize, cellSize, cellSize);
        }
        ctx.strokeRect(grid.x + col * cellSize, grid.y + row * cellSize, cellSize, cellSize);
      }
    }
  });

  // Définition des nouvelles petites grilles (en colonne à droite)
  const smallGrids = grids.map((_, index) => ({
    x: (gridSize * cellSize) * 2 + padding * 2, // Aligné à droite des grandes grilles
    y: index * (smallGridSize * smallCellSize) + (index) * padding // Même hauteur que la grille correspondante
  }));

  // Dessiner les petites grilles
  smallGrids.forEach((smallGrid, gridIndex) => {
    for (let row = 0; row < smallGridSize; row++) {
      for (let col = 0; col < smallGridSize; col++) {
        if (valeurMasques.value[gridIndex]?.[row]?.[col] == false) {
          ctx.fillStyle = `hsl(${Math.random() * 360}, 0%, 55%)`;
          ctx.fillRect(smallGrid.x + col * smallCellSize, smallGrid.y + row * smallCellSize, smallCellSize, smallCellSize);
          ctx.strokeRect(smallGrid.x + col * smallCellSize, smallGrid.y + row * smallCellSize, smallCellSize, smallCellSize);
        }
      }
    }
  });
};

const challengesTab = ref<number[][]>([]);

async function fetchChallenges() {
  try {
    console.log("Test")
    const response = await fetch("http://localhost:3000/generateChallenge");
    if (!response.ok) alert("Erreur lors de la récupération des défis");

    challengesTab.value = await response.json();
    console.log("Défis récupérés :", challengesTab.value);
  } catch (error) {
    console.error("Erreur:", error);
  }
}


onMounted(() => {
  setTimeout(drawGrid, 100);
});

</script>

<template>
  <canvas id="game" ref="canvasRef">

  </canvas>
  <br>
  <button @click="fetchChallenges">Regénérer des défis</button>
  <br>
  <div v-if="challengesTab.length">
    <h3>Défis générés :</h3>
    <div v-for="(challenge, index) in challengesTab" :key="index" class="challenge">

        <div v-for="(num, idx) in challenge" :key="idx" class="challenge-item" >
          <div v-if="num !== 0"  class="monstreNumber">
            <p class="indicationNumberMonster">x {{ num }}</p>
            <img class="monsterImgChallenge" :src="`/assets/img/monstres/monstres_${idx}.png`" alt="Monstre" />
          </div>
        </div>
    </div>
  </div>
</template>

<style scoped>

  #game {
    width: 600px;
    height: 500px;
    display: block;
    margin-top: 1em;
  }

  .challenge-item {
    width: min-content;
    margin: auto 0 2px 0;
  }

  .challenge{
    width:80%;
    background-color: lightGray;
    border:solid 2px black;
    height:200px;
    display:flex;
    text-align:center;
    margin: 1em 0;
  }

  .monstreNumber{
    display: inline-block;
    width:150px;
    height:auto;
  }

  .monsterImgChallenge{
    width:150px;
  }

  .indicationNumberMonster{
    color:black;
    margin: 0;
  }




</style>