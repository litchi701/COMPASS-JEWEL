<template>
  <header :class="$style.header">
    <div :class="$style.left">
      <div :class="$style.logo">
        <span :class="$style.logoIcon">◆</span>
        <span :class="$style.logoText">COMPASS JEWEL</span>
      </div>
      <div :class="$style.track">TRACK A: STRATEGIC INTELLIGENCE</div>
    </div>

    <div :class="$style.right">
      <div :class="$style.date">当前节点: {{ currentDate }} Hackathon LIVE</div>
      <div :class="$style.badge">权限等级: C-SUITE EXEC ONLY</div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentDate = ref('')

onMounted(() => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  currentDate.value = `${year}.${month}.${day}`
})
</script>

<style module>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: #0a0a0a;
  border-bottom: 1px solid #333;
}

.left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logoIcon {
  color: #d4af37;
  font-size: 20px;
}

.logoText {
  color: #d4af37;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 2px;
}

.track {
  color: #999;
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.date {
  color: #999;
  font-size: 12px;
}

.badge {
  color: #d4af37;
  font-size: 11px;
  padding: 4px 12px;
  border: 1px solid #d4af37;
  border-radius: 2px;
  letter-spacing: 1px;
}
</style>
