<template>
  <div :class="$style.feed">
    <div :class="$style.header">
      <div :class="$style.title">DE-NOISED LIVE RAW FEED</div>
      <div :class="$style.subtitle">100% 可溯源入源数据</div>
    </div>
    <div :class="$style.items">
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
import { ref } from 'vue'

const feedItems = ref([
  {
    id: 1,
    source: 'Twitter @JewelryTrends_JP',
    time: '2小时前',
    content: '"今天又支持大F KPHI新款到货，下班后在涩谷店排队了1个小时，但看到实物真的值得！"',
    tag: '【验证真实性购买】'
  },
  {
    id: 2,
    source: 'Instagram #chiikawa_jewelry',
    time: '3小时前',
    content: '"看透了那些大牌，又文又贵的实体店铺，但看到这个联名款，日常佩戴真的很百搭。"',
    tag: '【验证真实性购买】'
  }
])
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
