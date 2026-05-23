# 快速启动指南

## 🚀 项目已完成内容

### ✅ 前端（已实现）
- Header 组件（顶部导航栏）
- MarketSelector 组件（市场选择器）
- BriefingCard 组件（简报卡片）
- LiveFeed 组件（实时信息流）
- ChatButton 组件（Agent 3 悬浮按钮）
- ChatPanel 组件（Agent 3 对话面板）
- MessageItem 组件（消息气泡）
- Dashboard 页面（主仪表盘）
- 完整的 UI 样式（按照截图设计）

### ✅ 后端（已实现）
- 简报 API 路由（获取简报、历史简报）
- 对话 API 路由（发送提问、获取历史、删除记录）
- 数据库查询服务（关键词搜索、ID查询）
- 溯源服务（生成溯源报告）
- 数据库模型（ORM）
- 数据库初始化脚本

### ⚠️ 预留位置（待填充）
- `backend/services/agent_service.py` 中的 Agent 2 和 Agent 3 调用逻辑
- `backend/config/settings.py` 中的 Agent API 配置

---

## 📦 安装依赖

### 前端

```bash
cd frontend
npm install
```

### 后端

```bash
cd backend
pip install -r requirements.txt
```

---

## ⚙️ 配置环境

### 1. 配置数据库

复制环境变量示例文件：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填写数据库连接信息：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/compass_jewel
```

### 2. 初始化数据库

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本
source backend/database/init_db.sql

# 或者直接运行
mysql -u root -p < backend/database/init_db.sql
```

### 3. 配置 Agent API（可选）

如果你已经有 Agent API，在 `.env` 中填写：

```env
AGENT_API_KEY=your_api_key
AGENT_MODEL=your_model_name
AGENT_BASE_URL=https://api.example.com
```

然后在 `backend/services/agent_service.py` 中实现调用逻辑。

---

## 🏃 启动项目

### 启动后端

```bash
cd backend
python main.py
```

后端将运行在 `http://localhost:8000`

访问 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 启动前端

```bash
cd frontend
npm run dev
```

前端将运行在 `http://localhost:3000`

---

## 🧪 测试 API

### 1. 测试简报 API

```bash
# 获取日本市场简报
curl http://localhost:8000/api/briefing/JP
```

### 2. 测试对话 API

```bash
# 发送提问
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "为什么日本市场社交声量下降了？"}'

# 获取对话历史
curl http://localhost:8000/api/chat/history
```

---

## 📊 插入测试数据

为了测试功能，你可以手动插入一些测试数据：

```sql
-- 插入爬虫记录
INSERT INTO crawl_records (url, source_platform, content, market_region, keywords, crawl_time)
VALUES 
('https://twitter.com/test1', 'Twitter', 'CHIIKAWA联名款在涩谷店排队了1个小时', 'JP', 'CHIIKAWA,联名', NOW()),
('https://instagram.com/test2', 'Instagram', '看到这个联名款，日常佩戴真的很百搭', 'JP', 'CHIIKAWA,珠宝', NOW());

-- 插入简报
INSERT INTO briefings (market_region, briefing_date, content)
VALUES ('JP', CURDATE(), '{"keyMarketShift": "市场趋势变化", "socialTrend": "社交趋势", "competitorActivity": "竞品动态"}');
```

---

## 🎨 UI 预览

项目 UI 已按照你提供的截图实现，包括：

- 深色主题（黑色背景 + 金色强调色）
- 顶部导航栏（Logo + Track 信息 + 日期 + 权限标识）
- 左侧市场选择器（5个市场，带状态标识）
- 中间内容区：
  - 3个简报卡片（带评分）
  - 实时信息流
  - 每日战略简报
- 右下角 Agent 3 悬浮按钮
- Agent 3 对话面板（支持溯源显示）
- 左下角 Agent Pipeline 状态

---

## 🔧 下一步工作

### 1. 实现 Agent 调用逻辑

编辑 `backend/services/agent_service.py`：

```python
def call_summary_agent(self, crawl_data: list) -> dict:
    """调用 Agent 2：总结分析"""
    # 实现你的 Agent 2 调用逻辑
    # 例如：调用 OpenAI API、Claude API 等
    pass

def call_query_agent(self, question: str, context_data: list) -> dict:
    """调用 Agent 3：回答用户提问"""
    # 实现你的 Agent 3 调用逻辑
    pass
```

### 2. 连接 Agent 1（爬虫）

Agent 1 爬取数据后，将数据写入 `crawl_records` 表：

```python
from database.models import CrawlRecord
from database.connection import SessionLocal

db = SessionLocal()
record = CrawlRecord(
    url="https://example.com",
    source_platform="Twitter",
    content="爬取的内容",
    market_region="JP",
    keywords="关键词1,关键词2",
    crawl_time=datetime.now()
)
db.add(record)
db.commit()
```

### 3. 部署到 GitHub Pages

参考 `docs/DEPLOYMENT.md` 进行部署。

---

## 📚 文档

- [API 文档](docs/API.md)
- [数据库设计](docs/DATABASE.md)
- [部署指南](docs/DEPLOYMENT.md)

---

## ❓ 常见问题

### 1. 数据库连接失败

检查 `.env` 中的 `DATABASE_URL` 是否正确，确保 MySQL 服务已启动。

### 2. 前端无法访问后端

检查后端是否正常运行在 `http://localhost:8000`，并且 CORS 配置正确。

### 3. Agent 调用失败

确保在 `.env` 中配置了正确的 Agent API 密钥，并在 `agent_service.py` 中实现了调用逻辑。

---

## 🎉 完成！

项目框架已经完全搭建好，UI 已按照设计实现，后端 API 已完成（除了 Agent 调用逻辑需要你填充）。

现在你可以：
1. 启动项目查看效果
2. 填充 Agent 调用逻辑
3. 连接 Agent 1 爬虫数据
4. 部署到 GitHub Pages

有任何问题随时问我！🚀
