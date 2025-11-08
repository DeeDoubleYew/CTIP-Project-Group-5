<script setup>
import { ref } from "vue";

// Local custom directive definition
const vAutofocus = {
  mounted(el) {
    el.focus();
  },
};

const inputFirstName = ref("");
const inputLastName = ref("");
const selectedImage = ref("");

function imageUrl() {
  if (selectedImage.value === "goose") {
    return "/Item_EvilGoose.gif";
  } else if (selectedImage.value === "pedro") {
    return "/Item_Pedro.gif";
  }
  return "";
}
</script>

<template>
  <div class="row text-start justify-content-between">
    <div class="col-sm-10 col-md-10 col-lg-4">
      <h1>About</h1>
      <p>
        This application is a Vue 3 project developed as part of a university
        assignment for COS30043 at Swinburne University. It demonstrates the use
        of modern web technologies such as Vue.js, Vue Router, Bootstrap, and
        client-side pagination. The site features a home page, an about section,
        and a news page that dynamically loads and paginates news items,
        providing users with an interactive and responsive experience.
      </p>
    </div>
    <div class="col-sm-auto col-md-6 col-lg-4">
      <div class="row">
        <div class="col-6">
          <label for="inputFirstName" class="form-label">First Name</label>
          <input name="firstName" type="text" class="form-control" id="inputFirstName" v-model="inputFirstName"
            v-autofocus />
        </div>
        <div class="col-6">
          <label for="inputLastName" class="form-label">Last Name</label>
          <input name="lastName" type="text" class="form-control" id="inputLastName" v-model="inputLastName" />
        </div>
        <div class="col-8">
          <p>Full Name: {{ inputFirstName }} {{ inputLastName }}</p>
        </div>
      </div>
    </div>
    <div class="col-sm-10 col-md-6 col-lg-4 order-lg-first">
      <div class="row">
        <div class="col-sm-12 radio-buttons">
          <label class="form-check-label m-1">
            <input class="form-check-input" type="radio" value="goose" v-model="selectedImage" />
            Goose
          </label>
          <label class="form-check-label m-1">
            <input class="form-check-input" type="radio" value="pedro" v-model="selectedImage" />
            Pedro
          </label>
        </div>
        <div class="col-sm-8" v-if="selectedImage">
          <img class="img-fluid" :src="imageUrl()" :alt="selectedImage" width="300" />
        </div>
      </div>
    </div>
  </div>
</template>
