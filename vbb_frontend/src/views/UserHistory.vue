<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const userId = "user123"
const history = ref<JourneyLog[]>([])

interface JourneyLog {
  _id: string
  from: string
  to: string
  viewed_at: string
  departure: string
  arrival: string
  legs: {
    line: string
    mode: string
  }[]
}

onMounted(async () => {
  try {
    const local = localStorage.getItem("user_journey_history")
    if (local) {
      history.value = JSON.parse(local)
    }

    const res = await axios.get("http://localhost:8000/user-history", {
      params: { user_id: userId }
    })
    history.value = res.data.logs
    localStorage.setItem("user_journey_history", JSON.stringify(res.data.logs))
  } catch (err) {
    console.error("❌ Failed to load user history:", err)
  }
})

</script>

<template>
  <div class="container mx-auto px-6 py-6">
    <h2 class="text-2xl font-bold mb-4">Your Journey History</h2>

    <ul v-if="history.length" class="space-y-4">
      <li
        v-for="j in history"
        :key="j._id"
        class="bg-white p-4 rounded shadow border"
      >
        <div class="flex justify-between">
          <div>
            <p class="font-semibold text-blue-600">From: {{ j.from }} → To: {{ j.to }}</p>
            <p class="text-sm text-gray-500">Viewed at: {{ new Date(j.viewed_at).toLocaleString() }}</p>
            <p class="text-sm text-gray-600">Departure: {{ new Date(j.departure).toLocaleTimeString() }}</p>
            <p class="text-sm text-gray-600">Arrival: {{ new Date(j.arrival).toLocaleTimeString() }}</p>
          </div>
          <div class="text-right">
            <p class="text-sm">Line: <strong>{{ j.legs[0]?.line }}</strong></p>
            <p class="text-sm">Mode: {{ j.legs[0]?.mode }}</p>
          </div>
        </div>
      </li>
    </ul>

    <p v-else class="text-gray-400 mt-8">No history found.</p>
  </div>
</template>
