import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import GeneratePuzzle from "../components/GeneratePuzzle.vue";

// Définition des routes sans le type explicite RouteRecordRaw
const routes = [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
    {
        path: '/GeneratePuzzle',
        name: 'GeneratePuzzle',
        component: GeneratePuzzle,
    }
]

// Création du routeur avec historique HTML5
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
