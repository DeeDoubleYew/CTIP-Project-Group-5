<script setup>
import { ref } from "vue";
const spamInput = ref("");
const prediction = ref(null);
const confidence = ref(null);

function processResults() {
  prediction.value = modelResult.value.prediction;
  confidence.value = modelResult.value.confidence;
}

function reset() {
  modelResult.value = null;
  prediction.value = null;
  confidence.value = null;
  spamInput.value = "";
}

//get correct gauge path based on percentage
function getGaugePath() {
  // Map 0-100% to 1-8
  const reading = Math.min(8, Math.max(1, Math.ceil((confidence.value / 100) * 8)));
  return `/gauge${reading}.jpg`;
}

//Model API Access
const APIurl = "http://127.0.0.1:8000/predict/"; // Base URL for predict function
const modelResult = ref(null); //holds results from model
const processing = ref(false);

async function modelPOST() {
  processing.value = true;
  try {
    let method = "POST";
    let endpoint = APIurl;
    const response = await fetch(endpoint, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: spamInput.value })
    });

    const responseData = await response.json();
    //alert(responseData + " :model success!"); Debug alert
    modelResult.value = responseData;
    processResults();
  } catch (error) {
    alert(error + " :model error!");
  } finally {
    processing.value = false;
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
          <div class="col-12 ">
            <img :src=getGaugePath() alt="spam detection guage" class="rounded mx-auto d-block" width="200" />
          </div>
          <div class="col-12 text-center">
            <p>This email is likely to be {{ prediction }}, be cautious!</p>
          </div>
        </div>
      </div>
      <div class="col-5 m-2 d-flex text-center text-white">
        <div class="row bg-info">
          <div class="col-12">
            <h4>CONFIDENCE SCORE: </h4>
          </div>
          <div class="col-12">
            <h4>{{ confidence }}%</h4>
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