<template>
  <div :class="$style.feed">
    <div :class="$style.header">
      <div :class="$style.title">DE-NOISED LIVE RAW FEED</div>
      <div :class="$style.subtitle">
        100% 可溯源 · {{ stats.total_passed ?? '—' }}/{{ stats.total_raw ?? '—' }} 条通过门控
      </div>
    </div>

    <div v-if="loading" :class="$style.hint">加载情报流…</div>
    <div v-else-if="error" :class="$style.error">{{ error }}</div>
    <div v-else-if="feedItems.length === 0" :class="$style.hint">当前市场暂无通过门控的数据</div>

    <div v-else :class="$style.items">
      <div
        v-for="item in feedItems"
        :key="item.id"
        :class="$style.item"
      >
        <div :class="$style.itemHeader">
          <div :class="$style.source">{{ item.source }}</div>
          <div :class="$style.time">{{ item.time }}</div>
        </div>
        <div :class="$style.itemContent">{{ item.content }}</div>
        <div v-if="item.tag" :class="$style.tag">{{ item.tag }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useMarketStore } from '@/stores/market'
import { getLiveFeed } from '@/api/feed'

const marketStore = useMarketStore()
const { currentMarket } = storeToRefs(marketStore)

const feedItems = ref([])
const stats = ref({})
const loading = ref(false)
const error = ref('')

const emit = defineEmits(['stats'])

async function loadFeed() {
  loading.value = true
  error.value = ''
  try {
    const data = await getLiveFeed(currentMarket.value, 20)
    feedItems.value = data.items || []
    stats.value = data.stats || {}
    emit('stats', stats.value)
  } catch (e) {
    error.value = '无法加载数据，请确认后端已启动（python main.py）'
    feedItems.value = []
    emit('stats', {})
  } finally {
    loading.value = false
  }
}

watch(currentMarket, loadFeed)
onMounted(loadFeed)
</script>

<style module>
.feed {
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 20px;
  height: 100%;
}

.header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #222;
}

.title {
  color: #d4af37;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  margin-bottom: 4px;
}

.subtitle {
  color: #666;
  font-size: 11px;
}

.hint,
.error {
  color: #666;
  font-size: 12px;
  padding: 24px 0;
  text-align: center;
}

.error {
  color: #f87171;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 600px;
  overflow-y: auto;
}

.item {
  background: #111;
  border: 1px solid #222;
  border-radius: 6px;
  padding: 16px;
  transition: all 0.2s;
}

.item:hover {
  border-color: #444;
}

.itemHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.source {
  color: #999;
  font-size: 11px;
}

.time {
  color: #666;
  font-size: 10px;
}

.itemContent {
  color: #ccc;
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 8px;
}

.tag {
  display: inline-block;
  color: #4ade80;
  font-size: 10px;
  padding: 4px 8px;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 3px;
}
</style>
