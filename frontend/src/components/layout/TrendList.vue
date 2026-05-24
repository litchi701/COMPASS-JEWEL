<template>
  <div :class="$style.trendList">
    <div :class="$style.header">
      <div :class="$style.title">留存热点列表</div>
      <div :class="$style.count">{{ trends.length }} 个热点</div>
    </div>

    <div v-if="loading" :class="$style.loading">
      <div :class="$style.spinner"></div>
      <div>加载中...</div>
    </div>

    <div v-else-if="error" :class="$style.error">
      {{ error }}
    </div>

    <div v-else-if="trends.length === 0" :class="$style.empty">
      <div :class="$style.emptyIcon">📊</div>
      <div :class="$style.emptyText">暂无热点数据</div>
    </div>

    <div v-else :class="$style.trends">
      <div
        v-for="trend in trends"
        :key="trend.id"
        :class="[
          $style.trendItem,
          selectedTrend?.id === trend.id && $style.active
        ]"
        @click="selectTrend(trend)"
      >
        <div :class="$style.trendHeader">
          <div :class="$style.trendName">{{ trend.name }}</div>
          <div :class="[$style.riskBadge, getRiskClass(trend.risk_level)]">
            {{ trend.risk_level }}
          </div>
        </div>

        <div :class="$style.trendCategory">{{ trend.category }}</div>

        <div :class="$style.metrics">
          <div :class="$style.metric">
            <span :class="$style.metricLabel">评分</span>
            <span :class="$style.metricValue">{{ trend.current_score }}</span>
          </div>
          <div :class="$style.metric">
            <span :class="$style.metricLabel">转化率</span>
            <span :class="$style.metricValue">{{ trend.wear_conversion_rate }}%</span>
          </div>
          <div :class="$style.metric">
            <span :class="$style.metricLabel">声量</span>
            <span :class="$style.metricValue">{{ trend.social_volume }}</span>
          </div>
        </div>

        <div :class="$style.status">
          <span :class="$style.statusIcon">●</span>
          <span :class="$style.statusText">{{ trend.status }}</span>
        </div>

        <div :class="$style.days">
          <span>已观察 {{ trend.observation_days }} 天</span>
          <span :class="$style.remaining">剩余 {{ trend.remaining_days }} 天</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useMarketStore } from '@/stores/market'
import { getTrendsByTier } from '@/api/trends'

const marketStore = useMarketStore()
const { currentMarket, currentTier, selectedTrend } = storeToRefs(marketStore)

const trends = ref([])
const loading = ref(false)
const error = ref('')

const loadTrends = async () => {
  loading.value = true
  error.value = ''

  try {
    const data = await getTrendsByTier(currentMarket.value, currentTier.value)
    trends.value = data.trends || []
  } catch (e) {
    console.error('加载热点列表失败:', e)
    error.value = '加载失败，请稍后重试'
    trends.value = []
  } finally {
    loading.value = false
  }
}

const selectTrend = (trend) => {
  marketStore.selectTrend(trend)
}

const getRiskClass = (level) => {
  const classMap = {
    '低': 'low',
    '中': 'medium',
    '高': 'high'
  }
  return classMap[level] || 'medium'
}

// 监听市场和层级变化，自动加载数据
watch([currentMarket, currentTier], loadTrends)

// 初始加载
onMounted(loadTrends)
</script>

<style module>
.trendList {
  background: #0a0a0a;
  padding: 16px 24px;
  height: calc(100vh - 200px);
  overflow-y: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #222;
}

.title {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
}

.count {
  color: #666;
  font-size: 10px;
}

.loading,
.error,
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  color: #666;
  font-size: 12px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #333;
  border-top-color: #d4af37;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #f87171;
}

.emptyIcon {
  font-size: 32px;
  margin-bottom: 8px;
}

.emptyText {
  color: #666;
  font-size: 12px;
}

.trends {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.trendItem {
  background: #111;
  border: 1px solid #222;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.trendItem:hover {
  border-color: #d4af37;
  background: #1a1a1a;
  transform: translateX(2px);
}

.trendItem.active {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
}

.trendHeader {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}

.trendName {
  flex: 1;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
}

.riskBadge {
  font-size: 9px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 2px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.riskBadge.low {
  background: rgba(74, 222, 128, 0.2);
  color: #4ade80;
}

.riskBadge.medium {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.riskBadge.high {
  background: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

.trendCategory {
  color: #999;
  font-size: 10px;
  margin-bottom: 8px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 8px;
  padding: 8px;
  background: #0a0a0a;
  border-radius: 4px;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.metricLabel {
  color: #666;
  font-size: 9px;
}

.metricValue {
  color: #4ade80;
  font-size: 12px;
  font-weight: 600;
}

.status {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.statusIcon {
  color: #4ade80;
  font-size: 8px;
}

.statusText {
  color: #ccc;
  font-size: 10px;
}

.days {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 9px;
  padding-top: 6px;
  border-top: 1px solid #222;
}

.remaining {
  color: #d4af37;
}
</style>
