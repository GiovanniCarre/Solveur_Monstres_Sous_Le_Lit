<script setup lang="ts">

</script>

<template>
  <div class="footer">
    <svg class="waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
      <defs>
        <path id="gentle-wave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z"></path>
      </defs>
      <g class="parallax">
        <use xlink:href="#gentle-wave" x="48" y="0" fill="rgba(114,112,151,0.7"></use>
        <use xlink:href="#gentle-wave" x="48" y="3" fill="rgba(114,112,151,0.5)"></use>
        <use xlink:href="#gentle-wave" x="48" y="5" fill="rgba(114,112,151,0.3)"></use>
        <use xlink:href="#gentle-wave" x="48" y="7" fill="rgba(114,112,151,1)"></use>
      </g>
    </svg>
    <div class="footerRect">
      <img src="/assets/img/monstres/monstres_7.png" class="monstreAccueil"/>
      <div>L'équipe des développeurs</div>
    </div>
  </div>
</template>

<style scoped>
.footer {
  position: relative;
  width: 100%;
  height: auto;
}

.waves {
  position:relative;
  margin-top: -200px;
  width: 100%;
  height:200px;
  margin-bottom:-7px; /*Fix for safari gap*/
  min-height:100px;
  max-height:150px;
  bottom: 0px;
  z-index: -9999;
  left: 0;
}

.parallax > use {
  animation: move-forever 25s cubic-bezier(.55,.5,.45,.5)     infinite;
}
.parallax > use:nth-child(1) {
  animation-delay: -2s;
  animation-duration: 7s;
}
.parallax > use:nth-child(2) {
  animation-delay: -3s;
  animation-duration: 10s;
}
.parallax > use:nth-child(3) {
  animation-delay: -4s;
  animation-duration: 13s;
}
.parallax > use:nth-child(4) {
  animation-delay: -5s;
  animation-duration: 20s;
}
@keyframes move-forever {
  0% {
    transform: translate3d(-90px,0,0);
  }
  100% {
    transform: translate3d(85px,0,0);
  }
}


/*Shrinking for mobile*/
@media (max-width: 768px) {
  .waves {
    height:150px;
    min-height:70px;
  }

  .liste-menu a{
    font-size: 20px;
  }
}



.monstreAccueil {
  position: static;
  width: 150px;
  margin-top: -100px;
  margin-right: calc(20% - 75px);
  display: block;
  margin-left: auto;
}



.footerRect {
  background-color: #727097;
  height: 150px;
  text-align: center;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 24px;

  flex-flow: column;
}


</style>