<template>
  <div :class="$style.tierSelector">
    <div :class="$style.title">战略层级</div>
    <div :class="$style.tiers">
      <div
        v-for="tier in tiers"
        :key="tier.code"
        :class="[
          $style.tierItem,
          currentTier === tier.code && $style.active
        ]"
        @click="selectTier(tier.code)"
      >
        <div :class="$style.tierCode">{{ tier.code }}</div>
        <div :class="$style.tierInfo">
          <div :class="$style.tierName">{{ tier.name }}</div>
          <div :class="$style.tierDesc">{{ tier.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMarketStore } from '@/stores/market'

const marketStore = useMarketStore()

const tiers = computed(() => marketStore.tiers)
const currentTier = computed(() => marketStore.currentTier)

const selectTier = (code) => {
  marketStore.setTier(code)
}
</script>

<style module>
.tierSelector {
  background: #0a0a0a;
  padding: 16px 24px;
  border-bottom: 1px solid #333;
}

.title {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
  margin-bottom: 12px;
}

.tiers {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tierItem {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #111;
  border: 1px solid #222;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.tierItem:hover {
  border-color: #d4af37;
  background: #1a1a1a;
}

.tierItem.active {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.tierCode {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
  min-width: 50px;
}

.tierInfo {
  flex: 1;
}

.tierName {
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 2px;
}

.tierDesc {
  color: #666;
  font-size: 10px;
  line-height: 1.3;
}
</style>
