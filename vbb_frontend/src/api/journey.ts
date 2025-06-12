import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const loginUser = async (
  user_id: string,
  password: string) => {
  return axios.post(`${API_BASE}/auth/login`, { user_id, password })
}

export const registerUser = async (
  user_id: string,
  password: string) => {
  return axios.post(`${API_BASE}/auth/register`, { user_id, password })
}
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

// ✅ NEW: Fetch recent searches for a user
export const fetchRecentJourneys = async (user_id: string) => {
  const res = await axios.get(`${API_BASE}/journey/recent`, {
    params: { user_id }
  })
  return res.data.recent || []
}
