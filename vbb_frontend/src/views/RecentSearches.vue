<template>
  <div class="mt-8">
  <h3 class="text-lg font-semibold mb-2">🕓 Recent Searches</h3>
  <ul class="bg-gray-100 p-4 rounded shadow">
    <li
      v-for="(item, index) in recentSearches"
      :key="index"
      class="mb-2 text-sm"
    >
      {{ item.from_id }} ➡ {{ item.to_id }}
    </li>
  </ul>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchRecentJourneys } from '../api/journey'  // ✅ use helper instead of direct axios

const searches = ref([])

onMounted(async () => {
  const user_id = localStorage.getItem('user_id')
  if (user_id) {
    try {
      const data = await fetchRecentJourneys(user_id)
      recentSearches.value = data
    } catch (err) {
      console.error('Failed to fetch recent journeys', err)
    }
  }
})
</script>

<style scoped>
.recent-container {
  max-width: 400px;
  margin: 2rem auto;
  background: #f8f8f8;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
