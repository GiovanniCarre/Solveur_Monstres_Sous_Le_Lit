<script setup lang="ts">
import { onMounted, ref } from 'vue';

// Génération de la carte
const canvasRef = ref<HTMLCanvasElement | null>(null);
const loading = ref(false); // Indique si la requête est en cours

const gridSize = 3;
const cellSize = 80; // Taille d'une cellule
const padding = 10; // Espacement entre les grilles

var img_monstres = [new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image(), new Image()];
for (let i = 0; i < img_monstres.length; i++) {
  img_monstres[i].src = `/assets/img/monstres/monstres_${i + 1}.png`;
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
          ctx.drawImage(img_monstres[colorValue - 1], grid.x + col * cellSize, grid.y + row * cellSize, cellSize, cellSize);
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

onMounted(() => {
  setTimeout(drawGrid, 100);
});

// Générer un tableau d'entiers de taille nbMonster
const nbMonster = 5;
const tableauMonstres = ref<number[]>([]);

const generateMonsters = () => {
  for (let i = 0; i < nbMonster; i++) {
    tableauMonstres.value.push(Math.floor(Math.random() * 9));
  }
};

// Fonction pour envoyer une requête au backend
const checkChallenge = async () => {
  loading.value = true;

  try {
    // Envoi de la requête avec le tableauMonstres
    const response = await fetch('http://localhost:3000/testChallenge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tableauMonstres: tableauMonstres.value }),
    });

    const result = await response.json();

    // Mise à jour du statut en fonction de la réponse
    if (result.result) {
      // Afficher un indicateur vert
      alert('Défi réalisable !');
    } else {
      // Afficher un indicateur rouge
      alert('Défi non réalisable.');
    }
  } catch (error) {
    console.error('Erreur lors de la vérification du défi:', error);
  } finally {
    loading.value = false;
  }
};

generateMonsters(); // Initialisation du tableau
</script>

<template>
  <canvas id="game" ref="canvasRef"></canvas>
  <br>

  <button @click="checkChallenge">
    <span v-if="loading">😅 Envoi en cours...</span>
    <span v-else>Tester le défi</span>
  </button>

  <section class="challengeSection">
    <div class="monster" v-for="(monster, index) in tableauMonstres" :key="index">
      <input class="selectionMonsterNumber"
             type="number"
             v-model="tableauMonstres[index]"
             :min="0"
             :max="30"
             :step="1"
      />

      <img class="imgMonster" :src="`/assets/img/monstres/monstres_${monster + 1}.png`" alt="monstres monster"/>
    </div>
  </section>
</template>

<style scoped>
#game {
  width: 600px;
  height: 500px;
  display: block;
  margin-top: 1em;
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
</style>
