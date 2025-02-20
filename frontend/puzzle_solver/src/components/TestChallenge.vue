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

var valeurChambres = ref<number[][][]>([
  [[-1, -1, 8], [1, -1, 7], [2, 2, -1]],
  [[3, -1, -1], [6, -1, -1], [1, 5, 8]],
  [[2, -1, -1], [2, 6, 8], [1, 4, 7]],
  [[3, 6, 5], [1, -1, 8], [-1, -1, 7]]
]);


onMounted(async () => {
  const response = await fetch('http://localhost:3000/dispositionVisuelle');
  const resultTab = await response.json();

  // Remplacer tous les 0 par des -1 dans le tableau
  valeurChambres.value = resultTab.map(row =>
      row.map(innerRow =>
          innerRow.map(value => value === 0 ? -1 : value)
      )
  );
});

const loading2 = ref(false);

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


//false c'est visible, le masquie est là
var valeurMasques = ref<boolean[][][]>([
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

var pointerX = 0;
var pointerY = 0;

const tournerMasque = (index: number): void => {
  const grid2: boolean[][] = [
    [false, false, false],
    [false, false, false],
    [false, false, false]
  ];
  grid2[1][1] = valeurMasques.value[index][1][1];
  for (let i = 0; i < 3; i++) {
    grid2[0][2 - i] = valeurMasques.value[index][i][0];
    grid2[i][0] = valeurMasques.value[index][2][i];
    grid2[2][i] = valeurMasques.value[index][2 - i][2];
    grid2[2 - i][2] = valeurMasques.value[index][0][2 - i];
  }
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      valeurMasques.value[index][i][j] = grid2[i][j];
    }
  }
}

const smallGridSize = 3; // Taille des petites grilles
const smallCellSize = cellSize / 2.5; // Cellules plus petites
// Définition des nouvelles petites grilles (en colonne à droite)
const smallGrids = grids.map((_, index) => ({
  index : index,
  defaultX: (gridSize * cellSize) * 2 + padding * 2 +1.5*smallCellSize, // Aligné à droite des grandes grilles
  defaultY: index * (smallGridSize * smallCellSize) + (index) * padding+1.5*smallCellSize, // Même hauteur que la grille correspondante
  x : (gridSize * cellSize) * 2 + padding * 2 +1.5*smallCellSize,
  y : index * (smallGridSize * smallCellSize) + (index) * padding+1.5*smallCellSize,
  cellSize : smallCellSize,
  isSelected: false,
  inGrid: false,
  rotate:()=>{ tournerMasque(index) }
}));

const pointInRect = (px : number, py : number, rx : number, ry : number, w : number, h : number) => {
  if (px < rx || px > rx + w) return false;
  return (py >= ry && py <= ry + h)
}

const pointInGrid = (px : number, py : number, gridNumber : number) => {
  return pointInRect(px, py, (gridNumber%2)*(gridSize*cellSize+padding), Math.floor(gridNumber/2)*(gridSize*cellSize+padding), gridSize*cellSize, gridSize*cellSize);
}

const drawGrid = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

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

  // Dessiner les petites grilles
  smallGrids.forEach((smallGrid, gridIndex) => {
    if (smallGrid.isSelected){
      smallGrid.x = pointerX;
      smallGrid.y = pointerY;
    }
    for (let row = 0; row < smallGridSize; row++) {
      for (let col = 0; col < smallGridSize; col++) {
        if (valeurMasques.value[gridIndex]?.[row]?.[col] == false) {
          ctx.fillStyle = `hsl(${Math.random() * 360}, 0%, 55%)`;
          smallGrid.cellSize = (smallGrid.inGrid || smallGrid.isSelected) ? cellSize : smallCellSize;
          ctx.fillRect(smallGrid.x + (col - 1.5) * smallGrid.cellSize, smallGrid.y+ (row - 1.5)* smallGrid.cellSize, smallGrid.cellSize, smallGrid.cellSize);
          ctx.strokeRect(smallGrid.x + (col - 1.5) * smallGrid.cellSize, smallGrid.y + (row - 1.5)* smallGrid.cellSize, smallGrid.cellSize, smallGrid.cellSize);
        }
      }
    }
  });
};

const init = () => {
  const canvas = canvasRef.value;
  canvas?.addEventListener('mousemove', (event) => {
    pointerX = event.offsetX;
    pointerY = event.offsetY;
  });
  canvas?.addEventListener('contextmenu', (event) => {
    event.preventDefault();
    smallGrids.forEach((grid, _) => {
      if (grid.inGrid && Math.abs(pointerX - grid.x) <= 0.5 * gridSize * grid.cellSize && Math.abs(pointerY - grid.y) <= 0.5 * gridSize * grid.cellSize) {
        grid.rotate();
      }
    });
  });
  canvas?.addEventListener('click', (_) => {
    smallGrids.forEach((grid) => {
      if (grid.isSelected) {
        grid.isSelected = false;
        let inGrid = false;
        for (let i = 0; i < 4; i++) {
          if (pointInGrid(pointerX, pointerY, i)) {
            grid.x = (i % 2) * (gridSize * cellSize + padding) + gridSize * cellSize / 2;
            grid.y = Math.floor(i / 2) * (gridSize * cellSize + padding) + gridSize * cellSize / 2;
            inGrid = true;
            break;
          }
        }
        if (!inGrid) {
          grid.x = grid.defaultX;
          grid.y = grid.defaultY;
        }
        grid.inGrid = inGrid;
      } else if (Math.abs(pointerX - grid.x) <= 0.5 * gridSize * grid.cellSize && Math.abs(pointerY - grid.y) <= 0.5 * gridSize * grid.cellSize) {
        grid.isSelected = true;
      }
    });
  });

}

function reshapeArray(arr, rows, cols) {
  if (arr.length !== rows * cols) {
    throw new Error("Nombre d'éléments incompatible avec les dimensions demandées.");
  }

  let reshaped = [];
  for (let i = 0; i < arr.length; i += cols) {
    reshaped.push(arr.slice(i, i + cols));
  }
  return reshaped;
}

onMounted(() => {
  setTimeout(init, 100);
  setInterval(drawGrid, 20);
  inputNumberTS(); // Exécuter l'initialisation des événements
});

// Générer un tableau d'entiers de taille nbMonster
const nbMonster = 8;
const tableauMonstres = ref<number[]>([]);


const generateMonsters = () => {
  for (let i = 0; i < nbMonster; i++) {
    tableauMonstres.value.push(Math.floor(Math.random() * 2) * Math.floor(Math.random() * 4));
  }
  tableauMonstres.value = [0, 0, 2, 0, 0, 0, 3, 0]
};


const tableauSolutions = ref<number[]>([]);
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
    console.log(result)
    if (result.result.includes("False")) {
      alert('Défi non réalisable.');
    } else {
      alert('Défi réalisable !');
      //si tu veux reshape Dorain : tableauSolutions.value = reshapeArray(result.result, 4, 10)
      // JTM DORIAN (ps : c'est bilel)
      tableauSolutions.value = result.result

    }
  } catch (error) {
    console.error('Erreur lors de la vérification du défi:', error);
  } finally {
    loading.value = false;
  }
};

function inputNumberTS() {
  setTimeout(() => { // Ajout d'un délai pour s'assurer que le DOM est bien mis à jour
    const monsterSections = document.querySelectorAll(".monster");

    monsterSections.forEach((monster) => {
      const input = monster.querySelector(".selectionMonsterNumber");
      const decrement = monster.querySelector(".decrement");
      const increment = monster.querySelector(".increment");

      if (!input || !decrement || !increment) return;

      decrement.onclick = () => {
        let value = parseInt(input.value) || 0;
        let minValue = input.min ? parseInt(input.min) : 0;
        if (value > minValue) {
          input.value = (value - 1).toString();
          input.dispatchEvent(new Event("input")); // Met à jour Vue
        }
      };

      increment.onclick = () => {
        let value = parseInt(input.value) || 0;
        let maxValue = input.max ? parseInt(input.max) : 30;
        if (value < maxValue) {
          input.value = (value + 1).toString();
          input.dispatchEvent(new Event("input")); // Met à jour Vue
        }
      };
    });
  }, 100); // Petite temporisation pour s'assurer que Vue a mis à jour le DOM
}



function placerMasques(position: number[], nouveauxMasques: boolean[][][]): void {
  if (position.length !== 4 || rotation.length !== 4) {
    throw new Error("Both arrays must have exactly 4 elements.");
  }

  if (!position.every(num => num >= 0 && num <= 3) || !rotation.every(num => num >= 0 && num <= 3)) {
    throw new Error("All values must be between 0 and 3.");
  }

  smallGrids.forEach((grid, index) => {
        grid.x = (position[index] % 2) * (gridSize * cellSize + padding) + gridSize * cellSize / 2;
        grid.y = Math.floor(position[index] / 2) * (gridSize * cellSize + padding) + gridSize * cellSize / 2;

        grid.inGrid = true;
  });

  nouveauxMasques //
}



generateMonsters(); // Initialisation du tableau
//placerMasques([0, 1, 2, 3], [0, 0, 0, 0]);

</script>

<template>
  <canvas id="game" ref="canvasRef"></canvas>
  <br>

  <button id='buttonClick' @click="checkChallenge">
    <span v-if="loading">Envoi en cours ⌛</span>
    <span v-else>Tester le défi</span>
  </button>
  <button id='buttonClick2' @click="resetMap">
    <span v-if="loading2">⏳</span>
    <span v-else>Réinitialiser les masques et les lits</span>
  </button>
  <br>

  <section class="challengeSection">
    <div class="monster" v-for="(monster, index) in tableauMonstres" :key="index">
      <div class="inputNb">
        <button class="decrement">-</button>
        <input class="selectionMonsterNumber"
               type="number"
               v-model="tableauMonstres[index]"
               :min="0"
               :max="30"
               :step="1"
        />
        <button class="increment">+</button>
      </div>
      <img class="imgMonster" :src="`/assets/img/monstres/monstres_${index + 1}.png`" alt="monstres monster"/>
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

#buttonClick2{
  color:white;
}

#buttonClick{
  color:white;
  margin-right:2em;
}

.inputNb {
  padding: 0.5em;
  background-color: #727097;
  font-size: 16px;
  border-radius: 1em;
  border-style: none;
  margin:0.5em;
  padding: 1em 0;
}


input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}

.decrement, .increment, .selectionMonsterNumber {
  background: none;
  border: none;
  text-align: center;
  font-size: 20px;
  width: 20%;
  padding: 0;
}

.number-input {
  display: inline-flex;
  align-items: center;
}

.number-input input[type=number] {
  text-align: center;
  width: 50px;
}

.number-input button {
  width: 20px;
  height: 20px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  cursor: pointer;
  font-size: 1rem;
}

.number-input button:hover {
  background-color: #e0e0e0;
}



</style>
