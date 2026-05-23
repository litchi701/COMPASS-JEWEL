import apiClient from './index'

// 发送用户提问 (Agent 3)
export const sendQuery = (question) => {
  return apiClient.post('/api/chat/query', { question })
}

// 获取对话历史
export const getChatHistory = () => {
  return apiClient.get('/api/chat/history')
}

// 删除指定对话记录
export const deleteChatMessage = (id) => {
  return apiClient.delete(`/api/chat/history/${id}`)
}

// 清空所有对话历史
export const clearChatHistory = () => {
  return apiClient.delete('/api/chat/history/all')
}
