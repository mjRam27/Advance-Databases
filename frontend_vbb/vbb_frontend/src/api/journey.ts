import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const fetchJourney = async (
  fromStation: string,
  toStation: string,
  mode: string[] | null
) => {
  const response = await axios.get(`${API_BASE}/journey`, {
    params: {
      from_station: fromStation,
      to_station: toStation,
      products: mode
    }
  })
  return response.data
}
