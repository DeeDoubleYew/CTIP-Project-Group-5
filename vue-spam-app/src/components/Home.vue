<script setup>
import { ref } from "vue";
const results = ref(null);
const spamInput = ref("");

function getResults() {
  results.value = 20;
}

function reset() {
  results.value = null;
}

//Model API Access
const APIurl = "http://localhost:3000/model"; // Base URL for news items
const modelResult = ref({}); //holds results from model

</script>
<template>
  <div class="container">
    <div class="row justify-content-center" name="heading">
      <div class="col-12 m-2 bg-secondary">
        <h1 class="fw-normal text-white">IAMM - Spam Detection <span v-if="!results">Help</span><span class="fw-bold"
            v-if="results">Results</span>
        </h1>
      </div>
    </div>
    <form v-if="!results">
      <div class="row justify-content-center" name="input field">
        <div class="col-10 m-2">
          <textarea class="form-control" placeholder="Not sure if it's safe? Paste text here and let me help..."
            rows="6" v-model="spamInput"></textarea>
        </div>
      </div>
      <div class="row justify-content-center" name="submit button">
        <div class="col-10 m-2 d-flex justify-content-center">
          <button type="button" class="btn btn-secondary bg-secondary" @click="getResults()">Submit</button>
        </div>
      </div>
    </form>
    <div class="row justify-content-center" v-if="results" name="results">
      <div class="col-5 m-2 d-flex justify-content-center">
        <div class="row bg-primary">
          <div class="col-12">
            <img src="/guage.png" alt="spam detection guage" class="img-fluid" width="300" />
          </div>
          <div class="col-12">
            <p>This email is likely to be spam, be cautious!</p>
          </div>
        </div>
      </div>
      <div class="col-5 m-2 d-flex justify-content-center text-white">
        <div class="row bg-info">
          <div class="col-12">
            <h4>CONFIDENCE SCORE: <span>{{ results }}%</span></h4>
          </div>
          <div class="col-12">
            <h6>Why has this email been marked as spam?</h6>
          </div>
          <div class="col-12">
            <ul>
              <li>Contains one suspicious phrase</li>
              <li>Has more than three spelling errors</li>
              <li>Has use of urgent language</li>
            </ul>
          </div>
          <div class="col-12 d-flex justify-content-center">
            <button class="btn btn-secondary bg-secondary">View Detailed Report</button>
          </div>
        </div>
      </div>
    </div>
    <div class="row justify-content-center" v-if="results">
      <div class="col-10 m-2 d-flex justify-content-center">
        <button type="button" class="btn btn-secondary bg-secondary" @click="reset()">Complete Another Search</button>
      </div>
    </div>
  </div>
</template>

<style></style>