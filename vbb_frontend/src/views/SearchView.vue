<script setup lang="ts">
import { ref, computed } from 'vue'
import { transports } from '../data/mockData'
import type { Transport } from '../types'
import TransportList from '../components/TransportList.vue'

const searchQuery = ref('')
const filters = ref({
  train: true,
  bus: true,
  tram: true,
  ice: true
})

const searchResults = computed(() => {
  if (!searchQuery.value) return []
  
  return transports.filter(transport => 
    transport.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    transport.line.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    transport.origin.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    transport.destination.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-2xl font-semibold mb-6">Search Transport</h2>
    
    <div class="mb-8">
      <div class="max-w-xl">
        <label for="search" class="block text-sm font-medium text-gray-700 mb-2">
          Search by ID, Line, Origin, or Destination
        </label>
        <input
          type="text"
          id="search"
          v-model="searchQuery"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          placeholder="Enter search terms..."
        >
      </div>
    </div>

    <div v-if="searchQuery">
      <h3 class="text-lg font-semibold mb-4">Search Results</h3>
      <TransportList 
        v-if="searchResults.length"
        :transports="searchResults"
        :filters="filters"
      />
      <p v-else class="text-gray-500">No results found for "{{ searchQuery }}"</p>
    </div>
  </div>
</template>