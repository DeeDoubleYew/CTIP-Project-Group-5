<script setup>
import { ref, onMounted } from "vue";
import PieChart from "../components/PieChart.vue";
import BarChart from "../components/BarChart.vue";
import LineChart from "../components/LineChart.vue";

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
    //alert(responseData + " :model success!"); Debug alert
    resultHistory.value = responseData;
  } catch (error) {
    alert(error + " :model error!");
  }
}

onMounted(async () => {
  getHistory();
});

</script>
<template>
  <div class="container">
    <div class="row justify-content-center" name="heading">
      <div class="col-12 m-2 bg-secondary">
        <h1 class="fw-normal text-white">IAMM - Result History</h1>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="row border m-1">
        <div class="col-12 text-center">
          <h2>Spam vs Ham</h2>
        </div>
        <div class="col-12">
          <PieChart :data="resultHistory" />
        </div>
      </div>
      <div class="row border m-1">
        <div class="col-12 text-center">
          <h2>Confidence Ratings</h2>
        </div>
        <div class="col-12">
          <BarChart :data="resultHistory" />
        </div>
      </div>
      <div class="row border m-1">
        <div class="col-12 text-center">
          <h2>Dataset Size</h2>
        </div>
        <div class="col-12">
          <LineChart :data="resultHistory" />
        </div>
      </div>
      <div class="col-12 text-center">
        <h2>Raw Data</h2>
      </div>
      <div v-for="result in resultHistory" class="col-sm-10 col-md-6 col-lg-4 border m-1">
        <div class="row">
          <div class="col-12">
            <h6>Prediction: {{ result.prediction }}</h6>
          </div>
          <div class="col-12">
            <h6>Confidence: {{ result.confidence }}</h6>
          </div>
          <div class="col-12">
            <h6>Email:</h6>
            <p class="overflow-scroll" style="height: 100px">{{ result.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style></style>