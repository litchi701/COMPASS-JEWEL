import { defineStore } from 'pinia'

export const useMarketStore = defineStore('market', {
  state: () => ({
    currentMarket: 'JP', // 当前选中的市场
    currentTier: 'Tier-1', // 当前选中的层级
    selectedTrend: null, // 当前选中的热点
    markets: [
      { code: 'JP', name: '日本市场', flag: '🇯🇵', status: 'READY' },
      { code: 'KR', name: '韩国市场', flag: '🇰🇷', status: 'READY' },
      { code: 'SEA', name: '东南亚市场', flag: '🌏', status: 'READY' },
      { code: 'US', name: '美国市场', flag: '🇺🇸', status: '' }
    ],
    tiers: [
      { code: 'Tier-1', name: '长线资产', description: '14-30天观察期，高确定性' },
      { code: 'Tier-2', name: '稳健验证', description: '7-14天观察期，中等潜力' },
      { code: 'Tier-3', name: '初期观察', description: '1-7天观察期，待验证' }
    ]
  }),
  actions: {
    setMarket(marketCode) {
      this.currentMarket = marketCode
      // 切换市场时清空选中的热点
      this.selectedTrend = null
    },
    setTier(tierCode) {
      this.currentTier = tierCode
      // 切换层级时清空选中的热点
      this.selectedTrend = null
    },
    selectTrend(trend) {
      this.selectedTrend = trend
    },
    clearSelectedTrend() {
      this.selectedTrend = null
    }
  },
  getters: {
    currentMarketName: (state) => {
      const market = state.markets.find(m => m.code === state.currentMarket)
      return market ? market.name : ''
    },
    currentTierName: (state) => {
      const tier = state.tiers.find(t => t.code === state.currentTier)
      return tier ? tier.name : ''
    }
  }
})
