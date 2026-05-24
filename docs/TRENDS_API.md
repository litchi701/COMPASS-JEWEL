# 热点分级查询 API 文档

## 📋 概述

新增的热点分级查询 API 提供按市场和层级获取热点列表的功能，支持高保真 Mock 数据和随机化测试。

---

## 🔗 API 端点

### 1. 获取指定市场和层级的热点列表

**请求**
```
GET /api/getTrendsByTier
```

**查询参数**
- `market_id` (必需): 市场ID
  - 可选值: `JP` (日本), `KR` (韩国), `SEA` (东南亚), `US` (美国)
- `tier` (必需): 层级
  - 可选值: `Tier-1` (长线资产), `Tier-2` (稳健验证), `Tier-3` (初期观察)
- `randomize` (可选): 是否随机化数据，默认 `false`
  - 用于测试场景，会对分数、转化率等数据进行随机波动

**响应示例**
```json
{
  "market_id": "JP",
  "tier": "Tier-1",
  "count": 3,
  "randomized": false,
  "trends": [
    {
      "id": "jp-tier1-001",
      "name": "#CHIIKAWA 错综复杂与日常黄金金饰",
      "category": "IP联名×轻量化金饰",
      "initial_score": 89,
      "current_score": 96,
      "wear_conversion_rate": 78.2,
      "social_volume": "15.3K",
      "observation_days": 14,
      "remaining_days": 16,
      "status": "长线资产确认",
      "tier": "Tier-1",
      "discovered_at": "2026-05-09T08:30:00Z",
      "key_insights": "情绪陪伴型IP与轻量化金饰的完美结合，穿戴转化率持续上升",
      "risk_level": "低",
      "recommendation": "建议启动联名合作，重点投入"
    }
  ]
}
```

**使用示例**
```bash
# 获取日本市场 Tier-1 热点
curl "http://localhost:8000/api/getTrendsByTier?market_id=JP&tier=Tier-1"

# 获取美国市场 Tier-2 热点（随机化数据）
curl "http://localhost:8000/api/getTrendsByTier?market_id=US&tier=Tier-2&randomize=true"
```

---

### 2. 根据ID获取单个热点详情

**请求**
```
GET /api/getTrendById/{trend_id}
```

**路径参数**
- `trend_id`: 热点ID（如 `jp-tier1-001`）

**响应示例**
```json
{
  "id": "jp-tier1-001",
  "name": "#CHIIKAWA 错综复杂与日常黄金金饰",
  "category": "IP联名×轻量化金饰",
  "initial_score": 89,
  "current_score": 96,
  "wear_conversion_rate": 78.2,
  "social_volume": "15.3K",
  "observation_days": 14,
  "remaining_days": 16,
  "status": "长线资产确认",
  "tier": "Tier-1",
  "discovered_at": "2026-05-09T08:30:00Z",
  "key_insights": "情绪陪伴型IP与轻量化金饰的完美结合，穿戴转化率持续上升",
  "risk_level": "低",
  "recommendation": "建议启动联名合作，重点投入"
}
```

---

### 3. 获取所有支持的市场列表

**请求**
```
GET /api/getMarkets
```

**响应示例**
```json
{
  "markets": ["JP", "KR", "SEA", "US"]
}
```

---

### 4. 获取所有层级列表

**请求**
```
GET /api/getTiers
```

**响应示例**
```json
{
  "tiers": ["Tier-1", "Tier-2", "Tier-3"]
}
```

---

### 5. 获取所有热点（可按市场筛选）

**请求**
```
GET /api/getAllTrends
```

**查询参数**
- `market_id` (可选): 市场ID，不传则返回所有市场
- `randomize` (可选): 是否随机化数据，默认 `false`

**响应示例**
```json
{
  "randomized": false,
  "markets": {
    "JP": {
      "Tier-1": [...],
      "Tier-2": [...],
      "Tier-3": [...]
    },
    "US": {
      "Tier-1": [...],
      "Tier-2": [...],
      "Tier-3": [...]
    }
  }
}
```

---

## 📊 数据字段说明

### 热点对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 热点唯一标识 |
| `name` | string | 热点名称（含话题标签） |
| `category` | string | 热点分类 |
| `initial_score` | number | 初始评分（0-100） |
| `current_score` | number | 当前评分（0-100） |
| `wear_conversion_rate` | number | 穿戴转化率（%） |
| `social_volume` | string | 社交声量（如 "15.3K"） |
| `observation_days` | number | 已观察天数 |
| `remaining_days` | number | 剩余观察天数 |
| `status` | string | 当前状态 |
| `tier` | string | 所属层级 |
| `discovered_at` | string | 发现时间（ISO 8601） |
| `key_insights` | string | 关键洞察 |
| `risk_level` | string | 风险等级（低/中/高） |
| `recommendation` | string | 建议行动 |

---

## 🎯 高保真 Mock 数据

### 日本市场 (JP)

#### Tier-1 案例
1. **#CHIIKAWA 错综复杂与日常黄金金饰**
   - 情绪陪伴型IP × 轻量化金饰
   - 穿戴转化率: 78.2%
   - 社交声量: 15.3K

2. **#ゆめかわいい 梦幻系珍珠项链**
   - 亚文化 × 珍珠饰品
   - 穿戴转化率: 72.5%

3. **#推し活 应援金色手链**
   - 粉丝经济 × 定制饰品
   - 穿戴转化率: 68.9%

#### Tier-2 案例
- #地雷系 暗黑风格银饰
- #量産型 量产系珍珠耳环

#### Tier-3 案例
- #病みかわいい 病娇系戒指
- #メンヘラ 情绪系项链

### 美国市场 (US)

#### Tier-1 案例
1. **#VintageGold 中古金饰复兴**
   - 复古风潮 × 黄金
   - 穿戴转化率: 82.4%
   - 社交声量: 28.5K
   - **PRD 重点案例**

2. **#LayeredNecklaces 叠戴项链组合**
   - 穿搭风格 × 项链
   - 穿戴转化率: 76.8%

#### Tier-2 案例
- #AstroJewelry 星座能量饰品
- #MinimalistGold 极简金饰

#### Tier-3 案例
- #CowboyCore 西部牛仔风饰品

### 韩国市场 (KR)

#### Tier-1 案例
- #미니멀주얼리 韩式极简珠宝

#### Tier-2 案例
- #Y2K주얼리 千禧风格饰品

#### Tier-3 案例
- #아이돌스타일 爱豆同款饰品

### 东南亚市场 (SEA)

#### Tier-1 案例
- #GoldInvestment 黄金投资型饰品

#### Tier-2 案例
- #IslamicJewelry 伊斯兰风格饰品

#### Tier-3 案例
- #BohemianStyle 波西米亚风饰品

---

## 🧪 测试用例

### 测试场景 1: 获取日本市场所有层级热点

```bash
# Tier-1
curl "http://localhost:8000/api/getTrendsByTier?market_id=JP&tier=Tier-1"

# Tier-2
curl "http://localhost:8000/api/getTrendsByTier?market_id=JP&tier=Tier-2"

# Tier-3
curl "http://localhost:8000/api/getTrendsByTier?market_id=JP&tier=Tier-3"
```

### 测试场景 2: 随机化数据测试

```bash
# 每次调用返回不同的数据（分数、转化率会随机波动）
curl "http://localhost:8000/api/getTrendsByTier?market_id=US&tier=Tier-1&randomize=true"
```

### 测试场景 3: 获取特定热点详情

```bash
# 获取 CHIIKAWA 热点详情
curl "http://localhost:8000/api/getTrendById/jp-tier1-001"

# 获取美国中古金热点详情
curl "http://localhost:8000/api/getTrendById/us-tier1-001"
```

### 测试场景 4: 获取所有市场数据

```bash
# 获取所有市场所有层级
curl "http://localhost:8000/api/getAllTrends"

# 只获取日本市场
curl "http://localhost:8000/api/getAllTrends?market_id=JP"
```

---

## 💻 前端调用示例

### Vue 3 组件示例

```vue
<template>
  <div>
    <h2>{{ tier }} 热点列表</h2>
    <div v-for="trend in trends" :key="trend.id">
      <h3>{{ trend.name }}</h3>
      <p>评分: {{ trend.current_score }}/100</p>
      <p>转化率: {{ trend.wear_conversion_rate }}%</p>
      <p>状态: {{ trend.status }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTrendsByTier } from '@/api/trends'

const trends = ref([])
const tier = ref('Tier-1')

onMounted(async () => {
  try {
    const data = await getTrendsByTier('JP', tier.value)
    trends.value = data.trends
  } catch (error) {
    console.error('获取热点失败:', error)
  }
})
</script>
```

### JavaScript 调用示例

```javascript
import { getTrendsByTier, getTrendById } from '@/api/trends'

// 获取日本市场 Tier-1 热点
const data = await getTrendsByTier('JP', 'Tier-1')
console.log(data.trends)

// 获取特定热点详情
const trend = await getTrendById('jp-tier1-001')
console.log(trend.name)

// 随机化数据（用于测试）
const randomData = await getTrendsByTier('US', 'Tier-2', true)
```

---

## 🔄 随机化功能说明

当 `randomize=true` 时，系统会对以下数据进行随机波动：

- **当前评分**: ±5分
- **穿戴转化率**: ±10%
- **社交声量**: ±20%
- **剩余天数**: ±3天

这个功能主要用于：
1. 测试前端组件的数据变化响应
2. 模拟真实场景中的数据波动
3. 演示时展示动态效果

---

## 📝 注意事项

1. **数据来源**: 当前使用高保真 Mock 数据，基于 PRD 中的真实案例
2. **市场代码**: 必须使用大写（JP/KR/SEA/US）
3. **层级格式**: 必须使用 `Tier-1`、`Tier-2`、`Tier-3` 格式（注意大小写和连字符）
4. **时间格式**: 所有时间使用 ISO 8601 格式（UTC）
5. **随机化**: 仅用于测试，生产环境建议关闭

---

## 🚀 快速开始

1. **启动后端**
```bash
cd backend
python main.py
```

2. **测试 API**
```bash
curl "http://localhost:8000/api/getTrendsByTier?market_id=JP&tier=Tier-1"
```

3. **查看 API 文档**
访问 http://localhost:8000/docs 查看完整的交互式 API 文档

---

## 📞 支持

如有问题，请参考：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 项目文档: `README.md` 和 `QUICKSTART.md`
