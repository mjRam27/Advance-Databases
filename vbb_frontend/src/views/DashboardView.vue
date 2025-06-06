<script setup lang="ts">
import { ref } from 'vue'
import type { FilterState } from '../types'
import { transports } from '../data/mockData'
import TransportList from '../components/TransportList.vue'
import Filters from '../components/Filters.vue'

const filters = ref<FilterState>({
  train: true,
  bus: true,
  tram: true,
  ice: true
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-2xl font-semibold mb-6">Transport Overview</h2>
    <Filters v-model:filters="filters" />
    <TransportList :transports="transports" :filters="filters" />
  </div>
</template>