import apiClient from './index'

export const getLiveFeed = (market, limit = 20) => {
  return apiClient.get(`/api/feed/${market}`, { params: { limit } })
}

export const getFeedStats = (market) => {
  return apiClient.get(`/api/feed/${market}/stats`)
}

export const getGlobalDataStats = () => {
  return apiClient.get('/api/data/stats')
}

export const syncHecksongData = () => {
  return apiClient.post('/api/data/sync')
}
