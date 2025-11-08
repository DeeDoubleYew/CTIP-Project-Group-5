<script setup>
import { useStore } from "vuex";

const store = useStore();
</script>
<template>
  <div class="container">
    <div class="row text-start justify-content-center">
      <div class="col-sm-10 col-md-10 col-lg-4">
        <h1>Home Page</h1>
        <p v-if="store.state.user">Hello {{ store.state.user }}!</p>
        <p>
          Welcome to the home page of our application, developed as part of a
          university project for COS30043 at Swinburne University. This site
          showcases our team's efforts in designing and building an interactive
          and engaging web experience. Explore the features, view our creative
          assets, and learn more about the concepts and technologies we've
          applied throughout the project. We hope you enjoy navigating our
          application and discovering what we've accomplished!
        </p>
      </div>
      <div class="col-sm-auto col-md-6 col-lg-4 order-lg-first">
        <img src="/Item_Pedro.gif" alt="Item Pedro" class="img-fluid" width="300" />
      </div>
      <div class="col-sm-auto col-md-6 col-lg-4">
        <img src="/Item_EvilGoose.gif" alt="Item Evil Goose" class="img-fluid" width="300" />
      </div>
    </div>
  </div>
</template>
