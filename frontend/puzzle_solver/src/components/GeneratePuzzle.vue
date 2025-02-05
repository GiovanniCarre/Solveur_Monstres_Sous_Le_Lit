<script setup lang="ts">
import { onMounted, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);
const loading = ref(false);
const loading2 = ref(false);
const imagesLoaded = ref(false); // Track if images are loaded

const gridSize = 3;
const cellSize = 80; // Taille d'une cellule
const padding = 10; // Espacement entre les grilles


const img_monstres: HTMLImageElement[] = [];

const preloadImages = async () => {
  const promises = [];

  for (let i = 0; i < 9; i++) {
    const img = new Image();
    img.src = `/assets/img/monstres/monstres_${i + 1}.png`;

    promises.push(
        new Promise<void>((resolve) => {
          img.onload = () => resolve();
          img.onerror = () => resolve(); // Prevent blocking if an image fails
        })
    );

    img_monstres.push(img);
  }

  await Promise.all(promises);
  console.log("Images loaded");
  imagesLoaded.value = true;
  drawGrid(); // Draw the canvas only when images are ready
};


// 4 grilles (2x2 disposition)
const grids = [
  { x: 0, y: 0 },
  { x: gridSize * cellSize + padding, y: 0 },
  { x: 0, y: gridSize * cellSize + padding },
  { x: gridSize * cellSize + padding, y: gridSize * cellSize + padding }
];

//-1 = vide, n >=1 id de monstre
const valeurChambres = ref<number[][][]>([
  [[-1, 1, 2], [3, -1, 4], [5, -1, -1]],
  [[1, 6, -1], [-1, 3, 4], [5, 7, -1]],
  [[1, 2, 7], [3, 4, -1], [7, 6, 8]],
  [[-1, -1, -1], [6, 1, 8], [3, 7, 4]]
]);


onMounted(async () => {
  const response = await fetch('http://localhost:3000/dispositionVisuelle');
  const resultTab = await response.json();

  // Remplacer tous les 0 par des -1 dans le tableau
  valeurChambres.value = resultTab.map(row =>
      row.map(innerRow =>
          innerRow.map(value => value === 0 ? -1 : value)  // Remplace 0 par -1
      )
  );
});


//false masque visible, true masque cache
const valeurMasques = ref<boolean[][][]>([
  [[false, true, false], [false, false, false], [false, true, false]],
  [[true, false, false], [false, false, false], [false, true, false]],
  [[false, false, false], [false, true, true], [false, false, false]],
  [[true, false, false], [false, false, false], [false, false, true]]
]);

onMounted(async () => {
  const response = await fetch('http://localhost:3000/masquesFixes');
  const resultTab = await response.json();

  valeurMasques.value = resultTab.map(row =>
      row.map(innerRow =>
          innerRow.map(value => value !== 0)
      )
  );
});

const drawGrid = () => {
  if (!imagesLoaded.value) return;
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
  loading.value = true;
  try {
    const response = await fetch("http://localhost:3000/generateChallenge", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        valeurChambres: valeurChambres.value,
        valeurMasques: valeurMasques.value,
      }),
    });

    if (!response.ok) {
      alert("Erreur lors de la récupération des défis");
      return;
    }

    const resultTab2 = await response.json();
    challengesTab.value = resultTab2
    console.log("Défis récupérés :", resultTab2);
  } catch (error) {
    console.error("Erreur:", error);
  } finally {
    loading.value = false;
  }
}


async function resetMap() {
  loading2.value = true; // Activer le mode attente
  try {
    await fetch("http://localhost:3000/resetChallenge");
    window.location.reload();
  } catch (error) {
    console.error("Erreur:", error);
  } finally {
    loading2.value = false; // Désactiver le mode attente
  }
}


//pour la modification des masques
const estConnexe = (grid: boolean[][]): boolean => {
  const rows = grid.length;
  const cols = grid[0].length;
  let visited = Array.from({ length: rows }, () => Array(cols).fill(false));

  // Trouver la première cellule "true" (masque actif)
  let start: [number, number] | null = null;
  let totalFalseCells = 0;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (!grid[r][c]) {
        totalFalseCells++;
        if (!start) start = [r, c]; // On prend le premier élément "true"
      }
    }
  }

  if (!start) return false; // Si aucune case active, ce n'est pas connexe

  // BFS / DFS pour vérifier la connexité
  let queue: [number, number][] = [start];
  visited[start[0]][start[1]] = true;
  let visitedCount = 0;

  const directions = [
    [0, 1], [1, 0], [0, -1], [-1, 0] // Droite, Bas, Gauche, Haut
  ];

  while (queue.length) {
    const [r, c] = queue.shift()!;
    visitedCount++;

    for (const [dr, dc] of directions) {
      const nr = r + dr;
      const nc = c + dc;
      if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !grid[nr][nc] && !visited[nr][nc]) {
        visited[nr][nc] = true;
        queue.push([nr, nc]);
      }
    }
  }

  return visitedCount === totalFalseCells; // Connexe si on a visité toutes les cellules "true"
};





const handleClick = (event: MouseEvent) => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const rect = canvas.getBoundingClientRect();
  const clickX = event.clientX - rect.left;
  const clickY = event.clientY - rect.top;

  let updated = false;

  // Check if the click is in a large grid (monsters)
  grids.forEach((grid, gridIndex) => {
    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        const xStart = grid.x + col * cellSize;
        const yStart = grid.y + row * cellSize;
        const xEnd = xStart + cellSize;
        const yEnd = yStart + cellSize;

        if (clickX >= xStart && clickX < xEnd && clickY >= yStart && clickY < yEnd) {
          // Update monster value
          if (valeurChambres.value[gridIndex][row][col] !== -1) {
            valeurChambres.value[gridIndex][row][col] = (valeurChambres.value[gridIndex][row][col] + 1) % 9;
            if (valeurChambres.value[gridIndex][row][col] == 0){
              valeurChambres.value[gridIndex][row][col] = -1;
            }
            updated = true;
          } else {
            valeurChambres.value[gridIndex][row][col] = 1;
            updated = true;
          }
        }
      }
    }
  });

  // Check if the click is in a small grid (mask)
  const smallGrids = grids.map((_, index) => ({
    x: (gridSize * cellSize) * 2 + padding * 2,
    y: index * (3 * (cellSize / 2.5)) + index * padding
  }));

  smallGrids.forEach((smallGrid, gridIndex) => {
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        const xStart = smallGrid.x + col * (cellSize / 2.5);
        const yStart = smallGrid.y + row * (cellSize / 2.5);
        const xEnd = xStart + (cellSize / 2.5);
        const yEnd = yStart + (cellSize / 2.5);

        if (clickX >= xStart && clickX < xEnd && clickY >= yStart && clickY < yEnd) {
          // Toggle mask value
          valeurMasques.value[gridIndex][row][col] = !valeurMasques.value[gridIndex][row][col];
          if (estConnexe(valeurMasques.value[gridIndex])){
            updated = true;
          } else {
            valeurMasques.value[gridIndex][row][col] = !valeurMasques.value[gridIndex][row][col];
          }
        }
      }
    }
  });

  // Redraw the canvas if something was updated
  if (updated) drawGrid();
};


onMounted(() => {
  preloadImages()

  const canvas = canvasRef.value;
  if (canvas) {
    canvas.addEventListener("click", handleClick);
  }
});

</script>



<template>
  <canvas id="game" ref="canvasRef"></canvas>
  <br>
  <button id='buttonClick' @click="fetchChallenges">
    <span v-if="loading">⏳</span>
    <span v-else>Générer des défis</span>
  </button>
  <button id='buttonClick2' @click="resetMap">
    <span v-if="loading2">⏳</span>
    <span v-else>Réinitialiser les masques et les lits</span>
  </button>
  <br>
  <div v-if="challengesTab.length">
    <h3>Défis générés :</h3>
    <div v-for="(challenge, index) in challengesTab" :key="index" class="challenge">
      <div v-for="(num, idx) in challenge" :key="idx" class="challenge-item">
        <div v-if="num !== 0" class="monstreNumber">
          <p class="indicationNumberMonster">x {{ num }}</p>
          <img class="monsterImgChallenge" :src="`/assets/img/monstres/monstres_${idx}.png`" alt="Monstre" />
        </div>
      </div>
    </div>
  </div>
  <h3 v-else>Aucun défi ou pas encore lancé</h3>
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

#buttonClick{
  color:white;
  margin-right:5em;
}

#buttonClick2{
  color:white;
}

.challenge {
  width: 80%;
  background-color: rgba(114, 112, 151, 0.5);
  //border: solid 2px black;
  border-radius: 2em;
  padding: 1em;
  height: 200px;
  display: flex;
  text-align: center;
  margin: 1em 0;
}

.monstreNumber {
  display: inline-block;
  width: 150px;
  height: auto;
}

.monsterImgChallenge {
  width: 150px;
}


.indicationNumberMonster {
  color: black;
  margin: 0;
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
</style>
