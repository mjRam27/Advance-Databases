<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { stations, loadStations } from '../data/stationStore'

const stationQuery = ref('')
const router = useRouter()

onMounted(() => {
  loadStations()
})

const filteredStations = computed(() => {
  if (!stationQuery.value) return stations.value
  return stations.value.filter(station =>
    station.name.toLowerCase().includes(stationQuery.value.toLowerCase())
  )
})

const goToLiveBoard = (stationId: string) => {
  router.push({ name: 'LiveBoard', query: { id: stationId } })
}
</script>

<template>
  <div class="container mx-auto px-6 py-8">
    <h2 class="text-2xl font-bold mb-6">Station Information</h2>

    <!-- Search -->
    <div class="mb-6">
      <input
        v-model="stationQuery"
        type="text"
        placeholder="Search for a station..."
        class="w-full max-w-lg border border-gray-300 rounded-md px-4 py-2 shadow-sm text-sm"
      />
    </div>

    <!-- Card Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="station in filteredStations"
        :key="station.station_id"
        class="bg-white border rounded-md p-4 shadow hover:shadow-md transition-shadow duration-200"
      >
        <h3 class="font-semibold text-lg">{{ station.name }}</h3>
        <p class="text-sm text-gray-500">ID: {{ station.station_id }}</p>

        <button
          @click="goToLiveBoard(station.station_id)"
          class="mt-3 inline-block bg-blue-600 text-white text-sm px-3 py-1 rounded hover:bg-blue-700"
        >
          View Live Departures
        </button>
      </div>
    </div>

    <p v-if="filteredStations.length === 0" class="mt-6 text-gray-400 text-sm">No stations found.</p>
  </div>
</template>
