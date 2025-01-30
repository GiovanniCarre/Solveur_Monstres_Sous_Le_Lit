import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import GeneratePuzzle from "../components/GeneratePuzzle.vue";
import SolvePuzzle from "../components/SolvePuzzle.vue";
import ModifyPuzzle from "../components/ModifyPuzzle.vue";

// Définition des routes sans le type explicite RouteRecordRaw
const routes = [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
    {
        path: '/generate-puzzle',
        name: 'GeneratePuzzle',
        component: GeneratePuzzle,
    },
    {
        path: '/solve-puzzle',
        name: 'SolvePuzzle',
        component: SolvePuzzle,
    },{
        path: '/modify-game',
        name: 'ModifyPuzzle',
        component: ModifyPuzzle,
    }
]

// Création du routeur avec historique HTML5
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
