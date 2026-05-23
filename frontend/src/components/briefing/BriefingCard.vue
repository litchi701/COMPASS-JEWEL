<template>
  <div :class="$style.card">
    <div :class="$style.header">
      <div :class="$style.number">{{ number }}</div>
      <div :class="$style.title">{{ title }}</div>
      <div :class="$style.score">{{ score }}<span>/100 评分</span></div>
    </div>
    <div :class="$style.content">
      <div :class="$style.subtitle">{{ subtitle }}</div>
      <p :class="$style.description">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  number: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  score: {
    type: Number,
    required: true
  },
  subtitle: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  }
})
</script>

<style module>
.card {
  background: #111;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.2s;
}

.card:hover {
  border-color: #d4af37;
  transform: translateY(-2px);
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #222;
}

.number {
  color: #d4af37;
  font-size: 14px;
  font-weight: 600;
}

.title {
  flex: 1;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
}

.score {
  color: #d4af37;
  font-size: 18px;
  font-weight: 600;
}

.score span {
  color: #666;
  font-size: 11px;
  font-weight: 400;
  margin-left: 4px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.subtitle {
  color: #999;
  font-size: 12px;
  font-weight: 500;
}

.description {
  color: #ccc;
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
}
</style>
