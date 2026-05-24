import apiClient from './index'

/**
 * 获取指定市场和层级的热点列表
 * @param {string} marketId - 市场ID (JP/KR/SEA/US)
 * @param {string} tier - 层级 (Tier-1/Tier-2/Tier-3)
 * @param {boolean} randomize - 是否随机化数据（用于测试）
 * @returns {Promise}
 */
export const getTrendsByTier = (marketId, tier, randomize = false) => {
  return apiClient.get('/api/getTrendsByTier', {
    params: { market_id: marketId, tier, randomize }
  })
}

/**
 * 根据ID获取单个热点详情
 * @param {string} trendId - 热点ID
 * @returns {Promise}
 */
export const getTrendById = (trendId) => {
  return apiClient.get(`/api/getTrendById/${trendId}`)
}

/**
 * 获取所有支持的市场列表
 * @returns {Promise}
 */
export const getMarkets = () => {
  return apiClient.get('/api/getMarkets')
}

/**
 * 获取所有层级列表
 * @returns {Promise}
 */
export const getTiers = () => {
  return apiClient.get('/api/getTiers')
}

/**
 * 获取所有热点（可按市场筛选）
 * @param {string} marketId - 市场ID（可选）
 * @param {boolean} randomize - 是否随机化数据
 * @returns {Promise}
 */
export const getAllTrends = (marketId = null, randomize = false) => {
  const params = { randomize }
  if (marketId) {
    params.market_id = marketId
  }
  return apiClient.get('/api/getAllTrends', { params })
}
