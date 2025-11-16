<script setup>
import { ref } from "vue";


//Model API Access
const APIurl = "http://127.0.0.1:8000/history/"; // Base URL history db
const resultHistory = ref([])

async function getHistory() {
  try {
    let method = "GET";
    let endpoint = APIurl;
    const response = await fetch(endpoint, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      }
    });

    const responseData = await response.json();
    alert(responseData + " :model success!");
    resultHistory.value = responseData;
  } catch (error) {
    alert(error + " :model error!");
  }
}

</script>
<template>
  <div class="container">
    <div class="row justify-content-center" name="heading">
      <div class="col-12 m-2 bg-secondary">
        <h1 class="fw-normal text-white" v-if="!processing">IAMM - Spam Detection <span
            v-if="!modelResult">Help</span><span class="fw-bold" v-if="modelResult">Results</span>
        </h1>
        <h1 class="fw-normal text-white" v-if="processing">ANALYZING @</h1>
      </div>
    </div>
    <form v-if="!modelResult && !processing">
      <div class="row justify-content-center" name="input field">
        <div class="col-10 m-2">
          <textarea class="form-control" placeholder="Not sure if it's safe? Paste text here and let me help..."
            rows="6" v-model="spamInput"></textarea>
        </div>
      </div>
      <div class="row justify-content-center" name="submit button">
        <div class="col-10 m-2 d-flex justify-content-center">
          <button type="button" class="btn btn-secondary bg-secondary" @click="modelPOST()">Submit</button>
        </div>
      </div>
    </form>
    <div class="row justify-content-center" v-if="modelResult" name="results">
      <div class="col-5 m-2 d-flex justify-content-center">
        <div class="row bg-primary">
          <div class="col-12">
            <img src="/guage.png" alt="spam detection guage" class="img-fluid" width="300" />
          </div>
          <div class="col-12">
            <p>This email is likely to be {{ prediction }}, be cautious!</p>
          </div>
        </div>
      </div>
      <div class="col-5 m-2 d-flex justify-content-center text-white">
        <div class="row bg-info">
          <div class="col-12">
            <h4>CONFIDENCE SCORE: <span>{{ confidence }}%</span></h4>
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
    <div class="row justify-content-center" v-if="modelResult">
      <div class="col-10 m-2 d-flex justify-content-center">
        <button type="button" class="btn btn-secondary bg-secondary" @click="reset()">Complete Another Search</button>
      </div>
    </div>
  </div>
</template>

<style></style>