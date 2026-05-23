import { defineStore } from 'pinia'

export const useMarketStore = defineStore('market', {
  state: () => ({
    currentMarket: 'JP', // 当前选中的市场
    markets: [
      { code: 'CN', name: '中国市场', flag: '🇨🇳', status: '' },
      { code: 'JP', name: '日本市场', flag: '🇯🇵', status: 'READY' },
      { code: 'KR', name: '韩国市场', flag: '🇰🇷', status: 'READY' },
      { code: 'SEA', name: '东南亚市场', flag: '🌏', status: 'READY' },
      { code: 'US', name: '美国市场', flag: '🇺🇸', status: '' }
    ]
  }),
  actions: {
    setMarket(marketCode) {
      this.currentMarket = marketCode
    }
  }
})
