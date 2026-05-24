# COMPASS JEWEL - Strategic Intelligence System

珠宝行业多Agent情报系统，为珠宝公司提供海外市场（日本、韩国、东南亚、美国）的战略情报分析。

## 项目结构

```
compass-jewel/
├── frontend/          # 前端项目（Vue 3 + TypeScript）
├── backend/           # 后端项目（FastAPI + Python）
└── docs/              # 项目文档
```

## 功能特性

### 三个核心 Agent

1. **Agent 1（爬虫Agent）**：每日爬取市场信息
   - 记录爬取URL到SQL数据库
   - 保留爬虫记录
   - 注意：此部分代码不在本项目中

2. **Agent 2（分析Agent）**：总结和分析爬取的信息
   - 生成每日战略简报
   - 分析关键市场变化、竞品动态、IP联名等

3. **Agent 3（交互查询Agent）**：用户对话式查询
   - 右下角悬浮按钮入口
   - 从SQL数据库查找相关爬虫记录
   - 生成可溯源的报告
   - 支持删除历史对话记录

### 前端功能

- 海外市场选择（日本、韩国、东南亚、美国）
- 当前拦截信息展示
- 去噪后的实时原始信息流
- 每日战略简报
- AI营销工具包
- Agent 3 对话界面（右下角悬浮）

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

### 后端

```bash
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写数据库和 Agent API 配置

# 初始化数据库
mysql -u root -p < database/init_db.sql

# 启动服务
python main.py
```

## 技术栈

### 前端
- Vue 3 + TypeScript
- Pinia（状态管理）
- Axios（HTTP客户端）
- CSS Modules（样式）
- Vite（构建工具）

### 后端
- FastAPI（Web框架）
- SQLAlchemy（ORM）
- MySQL（数据库）
- Python 3.9+

## 部署

- **前端**：GitHub Pages（静态托管）
- **后端**：Railway / Render / Vercel（推荐）

详见 [部署指南](docs/DEPLOYMENT.md)

## API 文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

详见 [API 文档](docs/API.md)

## 数据源

爬虫数据来自队友仓库 [data-in-hecksong](https://github.com/Lby1102/data-in-hecksong)，已接入实时信息流与过滤率统计。详见 [数据说明](docs/DATA.md)。

## 数据库设计

详见 [数据库设计文档](docs/DATABASE.md)

## 预留接口

### Agent API 配置
在 `backend/config/settings.py` 中预留了 Agent API 配置：
- `AGENT_API_KEY`：Agent API 密钥
- `AGENT_MODEL`：Agent 模型名称
- `AGENT_BASE_URL`：Agent API 地址

### Agent 调用服务
在 `backend/services/agent_service.py` 中预留了：
- `call_summary_agent()`：调用 Agent 2
- `call_query_agent()`：调用 Agent 3

## 开发团队

COMPASS JEWEL - Track A: Strategic Intelligence

## License

MIT
