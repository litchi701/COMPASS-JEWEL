<template>
  <div v-if="isOpen" :class="$style.panel">
    <div :class="$style.header">
      <div :class="$style.title">
        <span :class="$style.icon">🤖</span>
        Agent 3 - 智能查询助手
      </div>
      <div :class="$style.actions">
        <button
          :class="$style.injectBtn"
          @click="showInjectModal = true"
          title="人类经验注入"
        >
          💡
        </button>
        <button :class="$style.clearBtn" @click="clearHistory" title="清空历史">
          🗑️
        </button>
        <button :class="$style.closeBtn" @click="closePanel">✕</button>
      </div>
    </div>

    <div :class="$style.messages" ref="messagesContainer">
      <div v-if="messages.length === 0" :class="$style.empty">
        <div :class="$style.emptyIcon">💡</div>
        <div :class="$style.emptyText">你好！我是 Agent 3，可以帮你查询和分析爬虫数据。</div>
        <div :class="$style.emptyHint">试试问我："为什么日本市场社交声量下降了？"</div>
      </div>

      <MessageItem
        v-for="message in messages"
        :key="message.id"
        :message="message"
        @delete="deleteMessage"
      />
    </div>

    <div :class="$style.input">
      <input
        v-model="inputText"
        :class="$style.inputField"
        placeholder="输入你的问题..."
        @keyup.enter="sendMessage"
        :disabled="isLoading"
      />
      <button
        :class="$style.sendBtn"
        @click="sendMessage"
        :disabled="!inputText.trim() || isLoading"
      >
        {{ isLoading ? '⏳' : '📤' }}
      </button>
    </div>

    <!-- 人类经验注入弹窗 -->
    <div v-if="showInjectModal" :class="$style.modal" @click.self="showInjectModal = false">
      <div :class="$style.modalContent">
        <div :class="$style.modalHeader">
          <div :class="$style.modalTitle">💡 人类经验注入</div>
          <button :class="$style.modalClose" @click="showInjectModal = false">✕</button>
        </div>
        <div :class="$style.modalBody">
          <div :class="$style.injectDesc">
            在此输入你的业务判断、风险评估或战略考量，Agent将结合你的经验重新推理。
          </div>
          <textarea
            v-model="humanInput"
            :class="$style.injectTextarea"
            placeholder="例如：考虑到日本市场的季节性因素，建议将观察期延长至30天..."
            rows="6"
          ></textarea>
          <div :class="$style.injectOptions">
            <label :class="$style.checkbox">
              <input type="checkbox" v-model="overrideAI" />
              <span>强制覆盖AI判断</span>
            </label>
          </div>
        </div>
        <div :class="$style.modalFooter">
          <button :class="$style.cancelBtn" @click="showInjectModal = false">取消</button>
          <button :class="$style.submitBtn" @click="submitHumanInput">注入并重新推理</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import { useMarketStore } from '@/stores/market'
import { sendQuery, clearChatHistory } from '@/api/chat'

const marketStore = useMarketStore()
const { currentMarket } = storeToRefs(marketStore)
import MessageItem from './MessageItem.vue'

const chatStore = useChatStore()
const isOpen = computed(() => chatStore.isOpen)
const messages = computed(() => chatStore.messages)

const inputText = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)
const showInjectModal = ref(false)
const humanInput = ref('')
const overrideAI = ref(false)

const closePanel = () => {
  chatStore.togglePanel()
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  const question = inputText.value.trim()
  inputText.value = ''

  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    type: 'user',
    content: question,
    timestamp: new Date().toISOString()
  }
  chatStore.addMessage(userMessage)

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  // 调用 API
  isLoading.value = true
  try {
    const response = await sendQuery(question, currentMarket.value)

    // 添加 Agent 回复
    const agentMessage = {
      id: Date.now() + 1,
      type: 'agent',
      content: response.answer,
      relatedRecords: response.related_records,
      timestamp: new Date().toISOString()
    }
    chatStore.addMessage(agentMessage)

    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
    const errorMessage = {
      id: Date.now() + 1,
      type: 'agent',
      content: '抱歉，查询失败了。请稍后再试。',
      timestamp: new Date().toISOString()
    }
    chatStore.addMessage(errorMessage)
  } finally {
    isLoading.value = false
  }
}

const deleteMessage = (id) => {
  chatStore.deleteMessage(id)
}

const clearHistory = async () => {
  if (!confirm('确定要清空所有对话历史吗？')) return

  try {
    await clearChatHistory()
    chatStore.clearMessages()
  } catch (error) {
    console.error('清空历史失败:', error)
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const submitHumanInput = async () => {
  if (!humanInput.value.trim()) {
    alert('请输入你的经验判断')
    return
  }

  showInjectModal.value = false

  // 添加人类经验注入消息
  const injectMessage = {
    id: Date.now(),
    type: 'user',
    content: `💡 [人类经验注入] ${humanInput.value}${overrideAI.value ? ' (强制覆盖AI判断)' : ''}`,
    timestamp: new Date().toISOString()
  }
  chatStore.addMessage(injectMessage)

  await nextTick()
  scrollToBottom()

  // 调用 API 重新推理
  isLoading.value = true
  try {
    const response = await sendQuery(humanInput.value, currentMarket.value)

    const agentMessage = {
      id: Date.now() + 1,
      type: 'agent',
      content: `已结合你的经验重新推理：\n\n${response.answer}`,
      relatedRecords: response.related_records,
      timestamp: new Date().toISOString()
    }
    chatStore.addMessage(agentMessage)

    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('重新推理失败:', error)
  } finally {
    isLoading.value = false
    humanInput.value = ''
    overrideAI.value = false
  }
}

// 监听消息变化，自动滚动
watch(messages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })
</script>

<style module>
.panel {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 420px;
  height: 600px;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #333;
  background: #111;
  border-radius: 12px 12px 0 0;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  font-size: 14px;
  font-weight: 600;
}

.icon {
  font-size: 18px;
}

.actions {
  display: flex;
  gap: 8px;
}

.clearBtn,
.closeBtn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.2s;
}

.clearBtn:hover,
.closeBtn:hover {
  color: #d4af37;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 40px;
}

.emptyIcon {
  font-size: 48px;
  margin-bottom: 16px;
}

.emptyText {
  color: #ccc;
  font-size: 14px;
  margin-bottom: 8px;
}

.emptyHint {
  color: #666;
  font-size: 12px;
  font-style: italic;
}

.input {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid #333;
  background: #111;
  border-radius: 0 0 12px 12px;
}

.inputField {
  flex: 1;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 10px 12px;
  color: #fff;
  font-size: 13px;
  outline: none;
  transition: all 0.2s;
}

.inputField:focus {
  border-color: #d4af37;
}

.inputField:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sendBtn {
  background: #d4af37;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.sendBtn:hover:not(:disabled) {
  background: #b8941f;
  transform: scale(1.05);
}

.sendBtn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.injectBtn {
  background: transparent;
  border: none;
  color: #d4af37;
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.2s;
}

.injectBtn:hover {
  transform: scale(1.1);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modalContent {
  background: #111;
  border: 1px solid #d4af37;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
}

.modalHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #333;
}

.modalTitle {
  color: #d4af37;
  font-size: 14px;
  font-weight: 600;
}

.modalClose {
  background: transparent;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
}

.modalClose:hover {
  color: #d4af37;
}

.modalBody {
  padding: 20px;
}

.injectDesc {
  color: #999;
  font-size: 12px;
  line-height: 1.5;
  margin-bottom: 12px;
}

.injectTextarea {
  width: 100%;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 12px;
  color: #fff;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  font-family: inherit;
}

.injectTextarea:focus {
  border-color: #d4af37;
}

.injectOptions {
  margin-top: 12px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ccc;
  font-size: 12px;
  cursor: pointer;
}

.checkbox input[type="checkbox"] {
  cursor: pointer;
}

.modalFooter {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #333;
}

.cancelBtn,
.submitBtn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.cancelBtn {
  background: #333;
  color: #fff;
}

.cancelBtn:hover {
  background: #444;
}

.submitBtn {
  background: #d4af37;
  color: #000;
}

.submitBtn:hover {
  background: #b8941f;
  transform: translateY(-1px);
}
</style>
