<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const stationId = ref<string>((route.query.id as string) || '900000003201')
const departures = ref<any[]>([])

// ⏱ Live clock
const currentTime = ref('')
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 🔁 Watch for URL changes (if user clicks different "Live Departure" buttons)
watch(() => route.query.id, (newId) => {
  if (newId) {
    stationId.value = newId as string
    fetchDepartures()
  }
})

// 🚉 Fetch departures
const fetchDepartures = async () => {
  try {
    const res = await axios.get('http://localhost:8000/departures', {
      params: { station_id: stationId.value }
    })
    departures.value = res.data
  } catch (err) {
    console.error('Fetch failed', err)
  }
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatDelay = (seconds: number | null) => {
  if (!seconds || seconds === 0) return 'On time'
  const minutes = Math.ceil(seconds / 60)
  return `+${minutes} min`
}

onMounted(() => {
  fetchDepartures()
  updateTime()
  const clockInterval = setInterval(updateTime, 1000)
  const refreshInterval = setInterval(fetchDepartures, 60000)

  onUnmounted(() => {
    clearInterval(clockInterval)
    clearInterval(refreshInterval)
  })
})
</script>

<template>
  <div class="container mx-auto px-6 py-6">
    <!-- Title and Clock -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold">Live Station Board</h2>
      <div class="bg-black text-green-400 font-mono text-lg px-4 py-2 rounded shadow tracking-widest">
        {{ currentTime }}
      </div>
    </div>

    <!-- Station ID input (optional override) -->
    <div class="mb-4">
      <label for="stationId" class="block mb-1 font-medium">Station ID</label>
      <input
        v-model="stationId"
        @input="fetchDepartures"
        id="stationId"
        class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
        placeholder="Enter station ID"
      />
    </div>

    <!-- Live Departures -->
    <ul class="space-y-4">
      <li
        v-for="dep in departures"
        :key="dep.tripId"
        class="bg-white p-4 rounded shadow border"
      >
        <div class="flex justify-between items-center">
          <div>
            <p class="font-bold">
              [{{ dep.line }}] {{ dep.direction }}
            </p>
            <p class="text-sm text-gray-600">
              Mode: {{ dep.mode }} |
              Platform: {{ dep.platform || 'N/A' }} |
              Delay: {{ formatDelay(dep.delay) }}
            </p>
          </div>
          <div class="text-sm text-gray-700">
            Departure: {{ formatTime(dep.when) }}
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
