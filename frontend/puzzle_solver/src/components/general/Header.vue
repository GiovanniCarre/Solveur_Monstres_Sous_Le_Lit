<!-- src/components/Header.vue -->

<template>
  <header class="header">
    <nav>
      <ul>
        <li><a href="/frontend/puzzle_solver/public">Accueil</a></li>
        <li><a href="/about">À propos</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      // ici tu peux ajouter des données liées à ton header si nécessaire
    };
  },
  methods: {
    // ici tu peux ajouter des méthodes pour gérer les interactions avec le header
  }
};
</script>

<style scoped>
/* Styles CSS spécifiques au Header */
.header {
  background-color: #333;
  color: white;
  padding: 1rem;
}

nav ul {
  list-style: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 20px;
}

nav ul li a {
  text-decoration: none;
  color: white;
  font-size: 18px;
}

nav ul li a:hover {
  color: #f4a261;
}
</style>
