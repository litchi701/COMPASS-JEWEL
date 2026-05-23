<template>
  <div :class="$style.selector">
    <div :class="$style.title">GLOBAL MARKETS</div>
    <div :class="$style.markets">
      <div
        v-for="market in markets"
        :key="market.code"
        :class="[
          $style.marketItem,
          currentMarket === market.code && $style.active
        ]"
        @click="selectMarket(market.code)"
      >
        <div :class="$style.flag">{{ market.flag }}</div>
        <div :class="$style.info">
          <div :class="$style.name">{{ market.name }}</div>
          <div :class="$style.code">{{ market.code }}</div>
        </div>
        <div v-if="market.status" :class="$style.status">{{ market.status }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMarketStore } from '@/stores/market'

const marketStore = useMarketStore()

const markets = computed(() => marketStore.markets)
const currentMarket = computed(() => marketStore.currentMarket)

const selectMarket = (code) => {
  marketStore.setMarket(code)
}
</script>

<style module>
.selector {
  background: #0a0a0a;
  padding: 24px;
  border-right: 1px solid #333;
  min-width: 220px;
  height: 100vh;
}

.title {
  color: #d4af37;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
  margin-bottom: 16px;
}

.markets {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.marketItem {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #111;
  border: 1px solid #222;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.marketItem:hover {
  border-color: #d4af37;
  background: #1a1a1a;
}

.marketItem.active {
  border-color: #d4af37;
  background: #1a1a1a;
}

.flag {
  font-size: 24px;
}

.info {
  flex: 1;
}

.name {
  color: #fff;
  font-size: 13px;
  margin-bottom: 2px;
}

.code {
  color: #666;
  font-size: 11px;
}

.status {
  color: #4ade80;
  font-size: 10px;
  padding: 2px 6px;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 2px;
  letter-spacing: 1px;
}
</style>
