<template>
  <div :class="$style.timeline">
    <div :class="$style.header">
      <div :class="$style.title">⏱️ 时间旅行 - 热点演变观察</div>
      <div :class="$style.subtitle">长线留存观察期（14-30天）</div>
    </div>

    <div :class="$style.slider">
      <input
        type="range"
        min="1"
        max="14"
        v-model="currentDay"
        :class="$style.sliderInput"
        @input="onDayChange"
      />
      <div :class="$style.dayMarkers">
        <span
          v-for="day in [1, 7, 14]"
          :key="day"
          :class="[$style.marker, currentDay == day && $style.active]"
        >
          Day {{ day }}
        </span>
      </div>
    </div>

    <div :class="$style.snapshot">
      <div :class="$style.snapshotTitle">{{ snapshotData.title }}</div>
      <div :class="$style.metrics">
        <div :class="$style.metric">
          <div :class="$style.metricLabel">热度评分</div>
          <div :class="$style.metricValue">{{ snapshotData.score }}/100</div>
        </div>
        <div :class="$style.metric">
          <div :class="$style.metricLabel">穿戴转化率</div>
          <div :class="$style.metricValue">{{ snapshotData.wearRate }}%</div>
        </div>
        <div :class="$style.metric">
          <div :class="$style.metricLabel">社交声量</div>
          <div :class="$style.metricValue">{{ snapshotData.socialVolume }}</div>
        </div>
        <div :class="$style.metric">
          <div :class="$style.metricLabel">层级判定</div>
          <div :class="[$style.metricValue, $style.tier]">{{ snapshotData.tier }}</div>
        </div>
      </div>
      <div :class="$style.status">
        <span :class="$style.statusLabel">状态:</span>
        <span :class="$style.statusText">{{ snapshotData.status }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentDay = ref(1)

const snapshots = {
  1: {
    title: 'Day 1 - 初始爆发期',
    score: 89,
    wearRate: 12.3,
    socialVolume: '2.4K',
    tier: 'Tier 3 (待观察)',
    status: '热点刚爆发，进入观察期，暂不建议重资产投入'
  },
  7: {
    title: 'Day 7 - 稳定验证期',
    score: 92,
    wearRate: 45.8,
    socialVolume: '8.7K',
    tier: 'Tier 2 (稳健)',
    status: '穿戴转化率稳健上升，真实用户持续增长'
  },
  14: {
    title: 'Day 14 - 长线确认期',
    score: 96,
    wearRate: 78.2,
    socialVolume: '15.3K',
    tier: 'Tier 1 (长线资产)',
    status: '已晋升长线资产，建议启动联名合作'
  }
}

const snapshotData = computed(() => {
  if (currentDay.value <= 3) return snapshots[1]
  if (currentDay.value <= 10) return snapshots[7]
  return snapshots[14]
})

const onDayChange = () => {
  // 可以在这里触发动画效果
}
</script>

<style module>
.timeline {
  background: #111;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #222;
}

.title {
  color: #d4af37;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 4px;
}

.subtitle {
  color: #666;
  font-size: 11px;
}

.slider {
  margin-bottom: 20px;
}

.sliderInput {
  width: 100%;
  height: 6px;
  background: #222;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  margin-bottom: 8px;
}

.sliderInput::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: #d4af37;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(212, 175, 55, 0.4);
}

.sliderInput::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: #d4af37;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.dayMarkers {
  display: flex;
  justify-content: space-between;
  padding: 0 8px;
}

.marker {
  color: #666;
  font-size: 10px;
  transition: all 0.2s;
}

.marker.active {
  color: #d4af37;
  font-weight: 600;
}

.snapshot {
  background: #0a0a0a;
  border: 1px solid #222;
  border-radius: 6px;
  padding: 16px;
}

.snapshotTitle {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.metric {
  text-align: center;
}

.metricLabel {
  color: #999;
  font-size: 10px;
  margin-bottom: 4px;
}

.metricValue {
  color: #4ade80;
  font-size: 16px;
  font-weight: 600;
}

.metricValue.tier {
  color: #d4af37;
  font-size: 12px;
}

.status {
  padding-top: 12px;
  border-top: 1px solid #222;
}

.statusLabel {
  color: #999;
  font-size: 11px;
  margin-right: 8px;
}

.statusText {
  color: #ccc;
  font-size: 12px;
}
</style>
