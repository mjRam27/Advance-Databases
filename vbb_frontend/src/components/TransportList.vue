<script setup lang="ts">
import { computed } from 'vue'
import type { Transport, FilterState } from '../types'
import { formatDate } from '../utils/dateFormatter'

const props = defineProps<{
  transports: Transport[]
  filters: FilterState
}>()

const filteredTransports = computed(() => {
  return props.transports.filter(transport => {
    return props.filters[transport.type]
  })
})

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
</script>

<template>
  <div class="space-y-4">
    <div v-for="transport in filteredTransports" :key="transport.id" 
      class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow duration-200">
      <div class="flex justify-between items-start">
        <div>
          <div class="flex items-center space-x-2">
            <span class="font-semibold">{{ transport.line }}</span>
            <span class="badge" :class="getStatusClass(transport.status)">
              {{ transport.status.charAt(0).toUpperCase() + transport.status.slice(1) }}
            </span>
          </div>
          <p class="text-gray-600">{{ transport.origin }} → {{ transport.destination }}</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-gray-500">Departure: {{ formatDate(transport.departureTime) }}</p>
          <p class="text-sm text-gray-500">Arrival: {{ formatDate(transport.arrivalTime) }}</p>
          <p v-if="transport.platform" class="text-sm text-gray-600">Platform: {{ transport.platform }}</p>
          <p v-if="transport.gate" class="text-sm text-gray-600">Gate: {{ transport.gate }}</p>
        </div>
      </div>
      <div v-if="transport.statusMessage" class="mt-2 text-sm text-gray-500">
        {{ transport.statusMessage }}
      </div>
    </div>
  </div>
</template>