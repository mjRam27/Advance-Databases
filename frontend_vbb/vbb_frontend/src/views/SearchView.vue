<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { stations, loadStations } from '../data/stationStore'

// Load station data from backend
onMounted(() => {
  loadStations()
})

const stationQuery = ref('')

// Dynamically filtered stations — if empty query, show all
const filteredStations = computed(() => {
  if (!stationQuery.value) return stations.value
  return stations.value.filter(station =>
    station.name.toLowerCase().includes(stationQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-2xl font-semibold mb-4">Station Information</h2>

    <!-- Search Input -->
    <div class="mb-6">
      <input
        v-model="stationQuery"
        type="text"
        placeholder="Search for a station..."
        class="w-full max-w-lg border border-gray-300 rounded-md px-4 py-2 shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm"
      />
    </div>

    <!-- Always Visible Station List -->
    <ul class="list-disc pl-5 text-sm text-gray-700">
      <li v-for="station in filteredStations" :key="station.station_id">
        {{ station.name }}
        ({{ station.station_id }})
      </li>
      <li v-if="filteredStations.length === 0" class="text-gray-400">
        No stations found.
      </li>
    </ul>
  </div>
</template>
