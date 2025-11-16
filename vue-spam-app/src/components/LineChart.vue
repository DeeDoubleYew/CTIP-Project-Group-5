<script setup>
import { Line } from "vue-chartjs";
import { computed } from "vue";
import {
    Chart as ChartJS, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend
} from "chart.js";
ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

const props = defineProps({
    data: { type: Array, required: true }
});

const chartData = computed(() => {
    const sorted = [...props.data].sort(
        (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    );

    return {
        labels: sorted.map(e =>
            new Date(e.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        ),
        datasets: [
            {
                label: "Emails Over Time",
                data: sorted.map((_, i) => i + 1)
            }
        ]
    };
});

const chartOptions = { responsive: true, maintainAspectRatio: false };
</script>

<template>
    <Line :data="chartData" :options="chartOptions" />
</template>
