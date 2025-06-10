// src/data/stationStore.ts
import { ref } from 'vue'
import axios from 'axios'

export const stations = ref<{ station_id: string; name: string }[]>([])

export async function loadStations() {
  const response = await axios.get('http://localhost:8000/stations')
  stations.value = response.data.stations
}
