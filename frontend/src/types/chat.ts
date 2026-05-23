// 对话相关类型定义
export interface ChatMessage {
  id: number
  type: 'user' | 'agent'
  content: string
  relatedRecords?: SourceRecord[]
  timestamp: string
}

export interface SourceRecord {
  id: number
  url: string
  sourcePlatform: string
  content: string
  crawlTime: string
}

export interface ChatQueryRequest {
  question: string
}

export interface ChatQueryResponse {
  answer: string
  relatedRecords: SourceRecord[]
}
