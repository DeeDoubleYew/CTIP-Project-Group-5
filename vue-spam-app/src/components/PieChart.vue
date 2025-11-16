<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { computed } from "vue";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
    data: { type: Array, required: true }
});

const chartData = computed(() => {
    const spamCount = props.data.filter(e => e.prediction === "spam").length;
    const hamCount = props.data.filter(e => e.prediction === "ham").length;

    return {
        labels: ["Spam", "Ham"],
        datasets: [{ data: [spamCount, hamCount] }]
    };
});

const chartOptions = { responsive: true, maintainAspectRatio: false };
</script>

<template>
    <Pie :data="chartData" :options="chartOptions" />
</template>
