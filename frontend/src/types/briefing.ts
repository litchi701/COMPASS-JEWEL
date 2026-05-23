// 简报相关类型定义
export interface Briefing {
  id: number
  marketRegion: string
  briefingDate: string
  content: BriefingContent
  createdAt: string
}

export interface BriefingContent {
  keyMarketShift?: string
  socialTrend?: string
  competitorActivity?: string
  actionableInsights?: string[]
}
