<script setup>
import { Bar } from "vue-chartjs";
import { computed } from "vue";
import {
    Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend
} from "chart.js";
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const props = defineProps({
    data: { type: Array, required: true }
});

const chartData = computed(() => ({
    labels: props.data.map(e => e.id),
    datasets: [
        {
            label: "Confidence %",
            data: props.data.map(e => e.confidence)
        }
    ]
}));

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: { y: { beginAtZero: true, max: 100 } }
};
</script>

<template>
    <Bar :data="chartData" :options="chartOptions" />
</template>
