# 数据源说明

## 仓库

- **GitHub**: [Lby1102/data-in-hecksong](https://github.com/Lby1102/data-in-hecksong)
- **说明**: 黑客松珠宝海外市场情报爬虫数据（日本、韩国、东南亚、全球共 **515** 条）

## 目录结构（数据仓）

| 分区 | 对应前端市场 | 约条数 |
|------|-------------|--------|
| Japan | JP | 57 |
| Korea | KR | 55 |
| Southeast_Asia | SEA | 259 |
| Global | 各市场共享参考 | 144 |

## 本项目如何使用

1. **本地文件**: `backend/data/ALL_ARTICLES.json`（已可随仓库提交或自行同步）
2. **同步最新数据**:
   ```bash
   cd backend
   source venv/bin/activate
   python scripts/sync_hecksong_data.py
   ```
3. **API**
   - `GET /api/feed/{market}` — 去噪后的实时信息流（JP/KR/SEA/US）
   - `GET /api/feed/{market}/stats` — 含「本轮过滤率」
   - `GET /api/data/stats` — 全局统计
   - `POST /api/data/sync` — 从 GitHub 拉取最新 JSON

4. **导入 MySQL**（供 Agent 3 溯源，可选）:
   ```bash
   python scripts/import_hecksong_to_db.py
   ```

## 过滤率计算

对当前市场原始条数，经「珠宝/金饰」关键词门控后：

`过滤率 = (1 - 通过条数 / 原始条数) × 100%`

左下角「本轮过滤率」由该统计动态展示，随左侧市场切换而变化。
