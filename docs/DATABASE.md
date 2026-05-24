# 数据库设计文档

## 数据库概览

- **数据库名称**: `compass_jewel`
- **字符集**: `utf8mb4`
- **排序规则**: `utf8mb4_unicode_ci`

## 表结构

### 1. crawl_records（爬虫记录表）

存储 Agent 1 爬取的原始数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| url | VARCHAR(500) | 爬取的URL |
| source_platform | VARCHAR(50) | 来源平台（Twitter/Instagram/TikTok等） |
| content | TEXT | 爬取内容 |
| market_region | VARCHAR(20) | 海外市场区域（JP/KR/SEA/US） |
| keywords | VARCHAR(200) | 关键词（逗号分隔） |
| crawl_time | DATETIME | 爬取时间 |
| created_at | TIMESTAMP | 记录创建时间 |

**索引**：
- `idx_market_region`: 市场区域索引
- `idx_crawl_time`: 爬取时间索引
- `idx_keywords`: 关键词索引

**用途**：
- Agent 2 从此表读取数据进行分析
- Agent 3 从此表查询相关记录进行溯源

---

### 2. briefings（简报表）

存储 Agent 2 生成的每日简报。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| market_region | VARCHAR(20) | 市场区域 |
| briefing_date | DATE | 简报日期 |
| content | JSON | 简报内容（JSON格式） |
| created_at | TIMESTAMP | 记录创建时间 |

**索引**：
- `idx_market_date`: 市场区域和日期联合索引

**content 字段结构**：
```json
{
  "keyMarketShift": "核心市场变化描述",
  "socialTrend": "社交趋势描述",
  "competitorActivity": "竞品动态",
  "actionableInsights": [
    "可执行洞察1",
    "可执行洞察2"
  ]
}
```

---

### 3. chat_history（对话历史表）

存储 Agent 3 与用户的对话记录。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| user_question | TEXT | 用户提问 |
| agent_response | TEXT | Agent回答 |
| related_record_ids | JSON | 关联的爬虫记录ID数组 |
| created_at | TIMESTAMP | 记录创建时间 |

**索引**：
- `idx_created_at`: 创建时间索引

**related_record_ids 字段结构**：
```json
[123, 124, 125]
```

---

## 数据流向

```
Agent 1（爬虫）
    ↓ 写入
crawl_records 表
    ↓ 读取
Agent 2（分析）
    ↓ 写入
briefings 表
    ↓ 展示
前端页面

用户提问 → Agent 3
    ↓ 查询
crawl_records 表
    ↓ 写入
chat_history 表
    ↓ 展示
前端对话界面
```

## 初始化脚本

使用 `backend/database/init_db.sql` 初始化数据库：

```bash
mysql -u root -p < backend/database/init_db.sql
```

## 数据维护

### 定期清理建议

1. **crawl_records 表**：
   - 保留最近 90 天的数据
   - 旧数据可归档到历史表

2. **chat_history 表**：
   - 用户可手动删除对话记录
   - 系统可定期清理 30 天前的记录

3. **briefings 表**：
   - 保留所有历史简报
   - 按需归档

## 性能优化建议

1. 为高频查询字段添加索引
2. 定期分析慢查询日志
3. 考虑使用分区表（按日期分区）
4. 对大文本字段（content）考虑使用全文索引
