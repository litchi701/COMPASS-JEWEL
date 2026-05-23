import apiClient from './index'

// 获取指定市场的最新简报
export const getBriefing = (market) => {
  return apiClient.get(`/api/briefing/${market}`)
}

// 获取历史简报
export const getBriefingHistory = (market) => {
  return apiClient.get(`/api/briefing/${market}/history`)
}
