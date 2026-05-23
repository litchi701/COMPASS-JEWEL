<template>
  <div :class="$style.chatButton" @click="toggleChat">
    <div :class="$style.icon">💬</div>
    <div v-if="!isOpen" :class="$style.label">Agent 助手</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const isOpen = computed(() => chatStore.isOpen)

const toggleChat = () => {
  chatStore.togglePanel()
}
</script>

<style module>
.chatButton {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
  transition: all 0.3s;
  z-index: 1000;
}

.chatButton:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(212, 175, 55, 0.4);
}

.icon {
  font-size: 24px;
}

.label {
  color: #000;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}
</style>
