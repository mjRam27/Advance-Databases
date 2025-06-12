<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { FilterState, Transport } from '../types'
import TransportList from '../components/TransportList.vue'
import Filters from '../components/Filters.vue'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { fetchJourney, fetchRecentJourneys } from '../api/journey'
import { format } from 'date-fns'
import { v4 as uuidv4 } from 'uuid'

const filters = ref<FilterState>({
  train: true,
  bus: true,
  tram: true,
  ice: true
})

const fromStation = ref('')
const toStation = ref('')
const departureDate = ref(new Date())
const departureTime = ref(new Date())
const journeyResult = ref<Transport[]>([])
const recentSearches = ref<Array<{ from_id: string; to_id: string }>>([])


const swapStations = () => {
  const temp = fromStation.value
  fromStation.value = toStation.value
  toStation.value = temp
}

const selectedModes = computed(() => {
  const modes: string[] = []
  if (filters.value.train) modes.push('train')
  if (filters.value.bus) modes.push('bus')
  if (filters.value.tram) modes.push('tram')
  return modes.length ? modes : ['all']
})

const searchJourney = async () => {
  if (!fromStation.value || !toStation.value) return

  try {
    const response = await fetchJourney(fromStation.value, toStation.value, selectedModes.value)
    const journeys = response.journeys || []

    journeyResult.value = journeys.map((data: any) => {
      const firstLeg = data.legs[0]
      const lastLeg = data.legs[data.legs.length - 1]
      const delay = firstLeg?.delay || 0
      const platform = firstLeg?.platform || ''
      const mode = firstLeg?.mode || 'unknown'

      return {
        id: uuidv4(),
        line: firstLeg.line || 'Unknown',
        origin: firstLeg.origin,
        destination: lastLeg.destination,
        departureTime: firstLeg.departure,
        arrivalTime: lastLeg.arrival,
        departureTimeFormatted: firstLeg.departure ? format(new Date(firstLeg.departure), 'HH:mm') : '',
        arrivalTimeFormatted: lastLeg.arrival ? format(new Date(lastLeg.arrival), 'HH:mm') : '',
        platform,
        mode,
        delay,
        gate: '',
        status: delay > 0 ? 'delayed' : 'on-time',
        statusMessage: delay > 0 ? `Delayed by ${Math.ceil(delay / 60)} min` : '',
        type: mode
      }
    })
  } catch (err) {
    console.error('Journey fetch failed', err)
  }
}

// Fetch recent user searches
const fetchRecent = async () => {
  const userId = localStorage.getItem('userId')
  if (!userId) return

  try {
    const response = await fetchRecentJourneys(userId)
    recentSearches.value = response.recent || []
  } catch (err) {
    console.error('Recent journey fetch failed', err)
  }
}

onMounted(() => {
  fetchRecent()
})
</script>

<template>
  <div class="min-h-[calc(100vh-160px)] px-4 py-8 bg-white">
    <div class="container mx-auto">
      <h2 class="text-2xl font-semibold mb-6">Transport Overview</h2>

      <!-- Recent searches -->
      <div v-if="recentSearches.length" class="mb-8">
        <h3 class="text-lg font-medium mb-2">Your Recent Searches</h3>
        <ul class="list-disc pl-5 text-gray-700">
          <li v-for="(item, idx) in recentSearches" :key="idx">
            {{ item.from_id }} → {{ item.to_id }}
          </li>
        </ul>
      </div>

      <!-- Journey Inputs -->
      <!-- (keep rest of UI as is...) -->

      <TransportList
        v-if="journeyResult.length"
        :transports="journeyResult"
        :filters="filters"
      />
    </div>
  </div>
</template>
