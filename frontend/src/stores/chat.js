import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [], // 对话历史
    isOpen: false // 对话面板是否打开
  }),
  actions: {
    addMessage(message) {
      this.messages.push(message)
    },
    clearMessages() {
      this.messages = []
    },
    deleteMessage(id) {
      this.messages = this.messages.filter(msg => msg.id !== id)
    },
    togglePanel() {
      this.isOpen = !this.isOpen
    }
  }
})
