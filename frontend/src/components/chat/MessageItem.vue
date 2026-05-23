<template>
  <div :class="[$style.message, $style[message.type]]">
    <div :class="$style.avatar">
      {{ message.type === 'user' ? '👤' : '🤖' }}
    </div>
    <div :class="$style.content">
      <div :class="$style.text">{{ message.content }}</div>

      <!-- 溯源信息 -->
      <div v-if="message.relatedRecords && message.relatedRecords.length > 0" :class="$style.sources">
        <div :class="$style.sourcesTitle">📊 数据来源（{{ message.relatedRecords.length }}条）：</div>
        <div
          v-for="(record, index) in message.relatedRecords"
          :key="record.id"
          :class="$style.sourceItem"
        >
          <div :class="$style.sourceHeader">
            <span :class="$style.sourceIndex">{{ index + 1 }}.</span>
            <span :class="$style.sourcePlatform">{{ record.source_platform }}</span>
            <span :class="$style.sourceTime">{{ formatTime(record.crawl_time) }}</span>
          </div>
          <div :class="$style.sourceUrl">
            <a :href="record.url" target="_blank" rel="noopener">{{ record.url }}</a>
          </div>
          <div :class="$style.sourceContent">{{ truncate(record.content, 100) }}</div>
        </div>
      </div>

      <div :class="$style.time">{{ formatTime(message.timestamp) }}</div>
    </div>

    <button
      v-if="message.type === 'user'"
      :class="$style.deleteBtn"
      @click="$emit('delete', message.id)"
      title="删除此消息"
    >
      ✕
    </button>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: Object,
    required: true
  }
})

defineEmits(['delete'])

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`

  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}
</script>

<style module>
.message {
  display: flex;
  gap: 12px;
  position: relative;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.user .avatar {
  background: #d4af37;
}

.agent .avatar {
  background: #333;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.text {
  background: #111;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 12px;
  color: #ccc;
  font-size: 13px;
  line-height: 1.6;
}

.user .text {
  background: #1a1a1a;
  border-color: #d4af37;
}

.sources {
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 12px;
  margin-top: 4px;
}

.sourcesTitle {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 8px;
}

.sourceItem {
  background: #111;
  border: 1px solid #222;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 8px;
}

.sourceItem:last-child {
  margin-bottom: 0;
}

.sourceHeader {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.sourceIndex {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
}

.sourcePlatform {
  color: #999;
  font-size: 11px;
}

.sourceTime {
  color: #666;
  font-size: 10px;
  margin-left: auto;
}

.sourceUrl {
  margin-bottom: 4px;
}

.sourceUrl a {
  color: #4ade80;
  font-size: 10px;
  text-decoration: none;
  word-break: break-all;
}

.sourceUrl a:hover {
  text-decoration: underline;
}

.sourceContent {
  color: #999;
  font-size: 11px;
  line-height: 1.5;
}

.time {
  color: #666;
  font-size: 10px;
  text-align: right;
}

.user .time {
  text-align: left;
}

.deleteBtn {
  position: absolute;
  top: 0;
  right: 0;
  background: transparent;
  border: none;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  opacity: 0;
  transition: all 0.2s;
}

.message:hover .deleteBtn {
  opacity: 1;
}

.deleteBtn:hover {
  color: #d4af37;
}
</style>
