# API 接口文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

## 简报相关 API

### 1. 获取指定市场的最新简报

**请求**
```
GET /api/briefing/{market}
```

**路径参数**
- `market` (string): 市场代码（JP/KR/SEA/CN/US）

**响应示例**
```json
{
  "id": 1,
  "market_region": "JP",
  "briefing_date": "2026-05-23",
  "content": {
    "keyMarketShift": "核心变化描述",
    "socialTrend": "社交趋势描述",
    "competitorActivity": "竞品动态",
    "actionableInsights": ["洞察1", "洞察2"]
  },
  "created_at": "2026-05-23T08:00:00"
}
```

### 2. 获取历史简报

**请求**
```
GET /api/briefing/{market}/history
```

**路径参数**
- `market` (string): 市场代码

**响应示例**
```json
[
  {
    "id": 1,
    "market_region": "JP",
    "briefing_date": "2026-05-23",
    "content": {...},
    "created_at": "2026-05-23T08:00:00"
  }
]
```

## 对话相关 API（Agent 3）

### 3. 发送用户提问

**请求**
```
POST /api/chat/query
```

**请求体**
```json
{
  "question": "为什么说日本市场社交声量下降了？"
}
```

**响应示例**
```json
{
  "answer": "根据以下3条爬虫记录分析...",
  "related_records": [
    {
      "id": 123,
      "url": "https://twitter.com/xxx",
      "source_platform": "Twitter",
      "content": "CHIIKAWA联名款在涩谷店排队...",
      "crawl_time": "2026-05-20T14:32:00"
    }
  ]
}
```

### 4. 获取对话历史

**请求**
```
GET /api/chat/history
```

**响应示例**
```json
[
  {
    "id": 1,
    "user_question": "为什么说日本市场社交声量下降了？",
    "agent_response": "根据以下3条爬虫记录分析...",
    "related_record_ids": [123, 124, 125],
    "created_at": "2026-05-23T10:30:00"
  }
]
```

### 5. 删除指定对话记录

**请求**
```
DELETE /api/chat/history/{id}
```

**路径参数**
- `id` (integer): 对话记录ID

**响应示例**
```json
{
  "message": "Delete chat message 1"
}
```

### 6. 清空所有对话历史

**请求**
```
DELETE /api/chat/history/all
```

**响应示例**
```json
{
  "message": "Clear all chat history"
}
```

## 错误响应

所有API在发生错误时返回统一格式：

```json
{
  "detail": "错误描述信息"
}
```

常见HTTP状态码：
- `200`: 成功
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误
