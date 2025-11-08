<script setup>
import { useStore } from "vuex";

const store = useStore();
</script>
<template>
  <div class="container">
    <nav class="navbar navbar-expand-md bg-body-tertiary">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Home</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link class="nav-link" to="/about">About</router-link>
            <router-link class="nav-link" to="/news">News</router-link>
            <router-link class="nav-link" to="/NewUser" v-if="!store.state.user">New User</router-link>
            <router-link class="nav-link" to="/login" v-if="!store.state.user">Login</router-link>
            <button class="btn" @click="store.commit('logout')" v-if="store.state.user">Logout</button>
          </div>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>
