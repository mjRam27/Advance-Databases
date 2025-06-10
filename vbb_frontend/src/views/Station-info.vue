<script setup lang="ts">
import { ref } from 'vue'

const stationQuery = ref('')
const stationResults = ref<string[]>([])

// 🔍 Simulate station search — replace this with API call later
const searchStations = () => {
  if (!stationQuery.value) {
    stationResults.value = []
    return
  }

  // Dummy result filtering
  const allStations = ['Berlin Hauptbahnhof', 'Frankfurt Hbf', 'Potsdam Hbf', 'Leipzig', 'Cottbus']
  stationResults.value = allStations.filter(station =>
    station.toLowerCase().includes(stationQuery.value.toLowerCase())
  )
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-2xl font-semibold mb-4">Station Information</h2>

    <div class="mb-6">
      <input
        v-model="stationQuery"
        @input="searchStations"
        type="text"
        placeholder="Search for a station..."
        class="w-full max-w-lg border border-gray-300 rounded-md px-4 py-2 shadow-sm focus:ring-primary-500 focus:border-primary-500 text-sm"
      />
    </div>

    <div v-if="stationQuery">
      <h3 class="text-lg font-semibold mb-2">Results:</h3>
      <ul class="list-disc pl-5 text-sm text-gray-700">
        <li v-for="(station, index) in stationResults" :key="index">
          {{ station }}
        </li>
        <li v-if="stationResults.length === 0" class="text-gray-400">No stations found.</li>
      </ul>
    </div>
  </div>
</template>
