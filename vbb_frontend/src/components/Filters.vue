<script setup lang="ts">
import { ref } from 'vue'
import type { FilterState } from '../types'

const emit = defineEmits<{
  (e: 'update:filters', filters: FilterState): void
}>()

const selectedType = ref<string>('all')

const filters = ref<FilterState>({
  train: true,
  bus: true,
  tram: true,
  ice: true
})

// Emit initial filters on load
emit('update:filters', filters.value)

// ✅ Fix: Handle change event safely in TypeScript
const updateFilter = (event: Event) => {
  const type = (event.target as HTMLSelectElement).value

  if (type === 'all') {
    filters.value = {
      train: true,
      bus: true,
      tram: true,
      ice: true
    }
  } else {
    filters.value = {
      train: type === 'train',
      bus: type === 'bus',
      tram: type === 'tram',
      ice: type === 'ice'
    }
  }

  emit('update:filters', filters.value)
}
</script>

<template>
  <div class="flex flex-col min-w-[200px]">
    <label class="text-sm font-medium text-gray-700 mb-1">Transport Type</label>
    <div class="relative">
      <select
        v-model="selectedType"
        @change="updateFilter"
        class="block w-full appearance-none border border-gray-300 bg-white text-sm px-3 py-2 pr-8 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
      >
        <option value="all">All Transport Types</option>
        <option value="train">Trains Only</option>
        <option value="bus">Buses Only</option>
        <option value="tram">Trams Only</option>
        <option value="ice">ICE Only</option>
      </select>

      <!-- Custom dropdown icon -->
      <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <svg class="w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path
            fill-rule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </div>
  </div>
</template>
