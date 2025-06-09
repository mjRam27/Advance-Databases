<script setup lang="ts">
import { ref } from 'vue'
import type { FilterState, Transport } from '../types'
import TransportList from '../components/TransportList.vue'
import Filters from '../components/Filters.vue'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { fetchJourney } from '../api/journey'
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

const swapStations = () => {
  const temp = fromStation.value
  fromStation.value = toStation.value
  toStation.value = temp
}

const searchJourney = async () => {
  if (!fromStation.value || !toStation.value) return

  const datetime = format(
    new Date(
      departureDate.value.toDateString() + ' ' + departureTime.value.toTimeString()
    ),
    "yyyy-MM-dd'T'HH:mm"
  )

  try {
    const response = await fetchJourney(fromStation.value, toStation.value, datetime)
    const data = response.journey

    const stopovers = data.stops || []
    const firstStop = stopovers[0]
    const lastStop = stopovers[stopovers.length - 1]

    const converted: Transport = {
      id: uuidv4(),
      line: data.line || 'Unknown',
      origin: data.from,
      destination: data.to,
      departureTime: firstStop?.departure || '',
      arrivalTime: lastStop?.arrival || '',
      departureTimeFormatted: firstStop?.departure
        ? format(new Date(firstStop.departure), 'HH:mm')
        : '',
      arrivalTimeFormatted: lastStop?.arrival
        ? format(new Date(lastStop.arrival), 'HH:mm')
        : '',
      platform: data.platform || '',
      gate: '',
      status: data.delay > 0 ? 'delayed' : 'on-time',
      statusMessage: data.delay > 0 ? `Delayed by ${data.delay / 60} min` : '',
      type: data.mode || 'train'
    }

    journeyResult.value = [converted]

  } catch (err) {
    console.error('Journey fetch failed', err)
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h2 class="text-2xl font-semibold mb-6">Transport Overview</h2>

    <div class="flex justify-center items-center space-x-4 mb-6">
      <div class="bg-gray-100 p-3 rounded-md shadow-md w-64 flex items-center">
        <span class="text-sm mr-2">Start</span>
        <input v-model="fromStation" placeholder="Enter departure" class="bg-transparent outline-none flex-grow text-sm" />
        <button @click="fromStation = ''" class="text-gray-400 hover:text-red-500">✕</button>
      </div>

      <div>
        <button @click="swapStations" class="text-2xl hover:text-blue-600 transition-transform transform hover:scale-125">
          ⇄
        </button>
      </div>

      <div class="bg-gray-100 p-3 rounded-md shadow-md w-64 flex items-center">
        <span class="text-sm mr-2">To</span>
        <input v-model="toStation" placeholder="Enter destination" class="bg-transparent outline-none flex-grow text-sm" />
        <button @click="toStation = ''" class="text-gray-400 hover:text-red-500">✕</button>
      </div>
    </div>

    <div class="mb-6 flex justify-between items-center flex-wrap gap-4">
      <div class="flex space-x-4 flex-wrap">
        <div class="flex flex-col min-w-[170px]">
          <label class="text-sm font-medium text-gray-700 mb-1">Departure Date</label>
          <Datepicker v-model="departureDate" :enableTimePicker="false" autoApply :format="'MMMM do, yyyy'" />
        </div>

        <div class="flex flex-col min-w-[140px]">
          <label class="text-sm font-medium text-gray-700 mb-1">Departure Time</label>
          <Datepicker
            v-model="departureTime"
            :enableTimePicker="true"
            :timePicker="true"
            :is24="true"
            autoApply
            :format="'HH:mm'"
          />
        </div>

        <div class="flex flex-col min-w-[200px]">
          <Filters v-model:filters="filters" />
        </div>
      </div>

      <div class="mt-6">
        <button @click="searchJourney" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">Search</button>
      </div>
    </div>

    <TransportList
      v-if="journeyResult.length"
      :transports="journeyResult"
      :filters="filters"
    />
  </div>
</template>
