<script setup>
import { RouterView } from 'vue-router';
import Home from './components/Home.vue'
import { RouterLink } from 'vue-router';
</script>

<template>
  <nav class="navbar navbar-expand bg-primary">
    <div class="container-fluid">
      <router-link class="navbar-brand mb-0" to="/">
        <img src="/logo.png" alt="Just Mail Solutions" class="img-fluid" />
      </router-link>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link active" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link active" to="/about">About Us</router-link>
        </li>
      </ul>
    </div>
  </nav>
  <router-view />
</template>

<style></style>
