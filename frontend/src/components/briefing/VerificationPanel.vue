<template>
  <div v-if="showPanel" :class="$style.panel">
    <div :class="$style.header">
      <div :class="$style.badge">🔔 待核验</div>
      <div :class="$style.title">每日新热点核验关卡</div>
      <button :class="$style.closeBtn" @click="closePanel">✕</button>
    </div>

    <div :class="$style.content">
      <div :class="$style.hotspot">
        <div :class="$style.hotspotHeader">
          <div :class="$style.hotspotName">{{ hotspot.name }}</div>
          <div :class="$style.hotspotRegion">{{ hotspot.region }}</div>
        </div>

        <div :class="$style.hotspotMeta">
          <span :class="$style.metaItem">
            <span :class="$style.metaLabel">首次发现:</span>
            <span :class="$style.metaValue">{{ hotspot.discoveredAt }}</span>
          </span>
          <span :class="$style.metaItem">
            <span :class="$style.metaLabel">初始评分:</span>
            <span :class="$style.metaValue">{{ hotspot.initialScore }}/100</span>
          </span>
        </div>

        <div :class="$style.hotspotDesc">
          {{ hotspot.description }}
        </div>

        <div :class="$style.aiAnalysis">
          <div :class="$style.analysisTitle">🤖 AI 初步判断:</div>
          <div :class="$style.analysisText">{{ hotspot.aiAnalysis }}</div>
        </div>
      </div>

      <div :class="$style.actions">
        <button :class="[$style.actionBtn, $style.keep]" @click="keepHotspot">
          ✓ 保留观察
        </button>
        <button :class="[$style.actionBtn, $style.adjust]" @click="showTierSelector = !showTierSelector">
          ⚙️ 调整层级
        </button>
        <button :class="[$style.actionBtn, $style.reject]" @click="rejectHotspot">
          ✕ 直接拒绝
        </button>
      </div>

      <div v-if="showTierSelector" :class="$style.tierSelector">
        <div :class="$style.tierTitle">选择观察层级:</div>
        <div :class="$style.tierOptions">
          <button
            v-for="tier in tiers"
            :key="tier.value"
            :class="[$style.tierBtn, selectedTier === tier.value && $style.selected]"
            @click="selectTier(tier.value)"
          >
            <div :class="$style.tierName">{{ tier.name }}</div>
            <div :class="$style.tierDesc">{{ tier.desc }}</div>
          </button>
        </div>
        <button :class="$style.confirmBtn" @click="confirmTier">确认调整</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showPanel = ref(true)
const showTierSelector = ref(false)
const selectedTier = ref(null)

// Mock 数据 - 可以替换为真实数据
const hotspot = ref({
  name: '#CHIIKAWA 错综复杂与日常黄金金饰',
  region: '日本市场 (JP)',
  discoveredAt: '2小时前',
  initialScore: 89,
  description: '日本社交媒体上突然爆发的CHIIKAWA（吉伊卡哇）IP与黄金饰品的联名讨论，涉及情绪陪伴型消费与轻量化金饰趋势。',
  aiAnalysis: '初步判定为"高情绪陪伴型IP + 轻量化金饰"交叉热点。建议进入14天观察期，验证穿戴转化率是否稳健。'
})

const tiers = [
  { value: 1, name: 'Tier 1 - 24h 复检', desc: '高风险，需密切监控' },
  { value: 2, name: 'Tier 2 - 7天观察', desc: '中等潜力，稳健验证' },
  { value: 3, name: 'Tier 3 - 14天留存', desc: '长线资产，深度观察' }
]

const closePanel = () => {
  showPanel.value = false
}

const keepHotspot = () => {
  alert('已保留该热点，进入默认观察期（14天）')
  closePanel()
}

const rejectHotspot = () => {
  if (confirm('确定要拒绝该热点吗？')) {
    alert('已拒绝该热点')
    closePanel()
  }
}

const selectTier = (tier) => {
  selectedTier.value = tier
}

const confirmTier = () => {
  if (!selectedTier.value) {
    alert('请先选择一个层级')
    return
  }
  alert(`已调整为 Tier ${selectedTier.value}`)
  closePanel()
}
</script>

<style module>
.panel {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 800px;
  background: #111;
  border: 2px solid #d4af37;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(212, 175, 55, 0.3);
  z-index: 999;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
  border-bottom: 1px solid #333;
  border-radius: 12px 12px 0 0;
}

.badge {
  background: #d4af37;
  color: #000;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 4px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.title {
  flex: 1;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.closeBtn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.2s;
}

.closeBtn:hover {
  color: #d4af37;
}

.content {
  padding: 20px;
}

.hotspot {
  background: #0a0a0a;
  border: 1px solid #222;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.hotspotHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.hotspotName {
  color: #d4af37;
  font-size: 15px;
  font-weight: 600;
}

.hotspotRegion {
  color: #4ade80;
  font-size: 11px;
  padding: 4px 8px;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 3px;
}

.hotspotMeta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.metaItem {
  font-size: 11px;
}

.metaLabel {
  color: #999;
  margin-right: 4px;
}

.metaValue {
  color: #fff;
  font-weight: 600;
}

.hotspotDesc {
  color: #ccc;
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.aiAnalysis {
  background: #111;
  border-left: 3px solid #4ade80;
  padding: 12px;
  border-radius: 4px;
}

.analysisTitle {
  color: #4ade80;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 6px;
}

.analysisText {
  color: #ccc;
  font-size: 12px;
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.actionBtn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.actionBtn.keep {
  background: #4ade80;
  color: #000;
}

.actionBtn.keep:hover {
  background: #22c55e;
  transform: translateY(-1px);
}

.actionBtn.adjust {
  background: #d4af37;
  color: #000;
}

.actionBtn.adjust:hover {
  background: #b8941f;
  transform: translateY(-1px);
}

.actionBtn.reject {
  background: #333;
  color: #fff;
}

.actionBtn.reject:hover {
  background: #444;
  transform: translateY(-1px);
}

.tierSelector {
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 16px;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.tierTitle {
  color: #d4af37;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
}

.tierOptions {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.tierBtn {
  flex: 1;
  background: #111;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.tierBtn:hover {
  border-color: #d4af37;
}

.tierBtn.selected {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.tierName {
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 4px;
}

.tierDesc {
  color: #999;
  font-size: 10px;
}

.confirmBtn {
  width: 100%;
  padding: 10px;
  background: #d4af37;
  border: none;
  border-radius: 6px;
  color: #000;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.confirmBtn:hover {
  background: #b8941f;
  transform: translateY(-1px);
}
</style>
