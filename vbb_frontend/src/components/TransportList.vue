<script setup lang="ts">
import type { Transport, FilterState } from '../types'
import { computed } from 'vue'
import { formatTime } from '../utils/dateFormatter'




const props = defineProps<{
  transports: Transport[]
  filters: FilterState
}>()

const filteredTransports = computed(() =>
  props.transports.filter(t => props.filters[t.type])
)

const getStatusClass = (status: string): string => {
  switch (status) {
    case 'on-time':
      return 'badge-success'
    case 'delayed':
      return 'badge-warning'
    case 'cancelled':
      return 'badge-error'
    default:
      return 'badge-success'
  }
}

// ✅ Add journey logging function here
const logJourney = async (journey: Transport) => {
  const payload = {
    user_id: "user123",
    from_station: journey.origin,
    to_station: journey.destination,
    journey_id: journey.id
  }

  await fetch("http://localhost:8000/log-journey", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })

  // 💾 Save locally for persistence
  const history = JSON.parse(localStorage.getItem("user_journey_history") || "[]")
  localStorage.setItem("user_journey_history", JSON.stringify([payload, ...history]))
}

</script>

<template>
  <div class="space-y-4">
     <!--✅ Add this click -->
    <div
      v-for="transport in filteredTransports"
      :key="transport.id"
      class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow duration-200 cursor-pointer"
      @click="logJourney(transport)" 
    >
      <div class="flex justify-between items-start">
        <div>
          <div class="flex items-center space-x-2">
            <span class="font-semibold">{{ transport.line }}</span>
            <span class="badge" :class="getStatusClass(transport.status)">
              {{ transport.status.charAt(0).toUpperCase() + transport.status.slice(1) }}
            </span>
          </div>
          <p class="text-gray-700">{{ transport.origin }} → {{ transport.destination }}</p>
        </div>

        <div class="text-right text-sm text-gray-600">
          <p>Departure: {{ formatTime(transport.departureTime) }}</p>
          <p v-if="transport.arrivalTime">Arrival: {{ formatTime(transport.arrivalTime) }}</p>
          <p>Mode: {{ transport.type }}</p>
          <p v-if="transport.platform">Platform: {{ transport.platform }}</p>
          <p>
            Delay: 
            <span v-if="transport.statusMessage">
              {{ transport.statusMessage }}
            </span>
            <span v-else>
              On time
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
