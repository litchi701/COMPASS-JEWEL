# 部署指南

## 前端部署（GitHub Pages）

### 1. 构建前端项目

```bash
cd frontend
npm install
npm run build
```

构建完成后，会在 `frontend/dist` 目录生成静态文件。

### 2. 部署到 GitHub Pages

#### 方法一：使用 GitHub Actions（推荐）

在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      
      - name: Build
        run: |
          cd frontend
          npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/dist
```

#### 方法二：手动部署

```bash
cd frontend
npm run build

# 安装 gh-pages
npm install -g gh-pages

# 部署
gh-pages -d dist
```

### 3. 配置 GitHub Pages

1. 进入 GitHub 仓库设置
2. 找到 "Pages" 选项
3. Source 选择 `gh-pages` 分支
4. 保存

访问地址：`https://<username>.github.io/<repo-name>/`

---

## 后端部署

### 方案一：Railway（推荐）

1. 注册 [Railway](https://railway.app/)
2. 创建新项目
3. 连接 GitHub 仓库
4. 选择 `backend` 目录
5. 添加环境变量：
   ```
   DATABASE_URL=mysql+pymysql://user:password@host:3306/compass_jewel
   AGENT_API_KEY=your_key
   AGENT_MODEL=your_model
   AGENT_BASE_URL=your_url
   ```
6. Railway 会自动检测 `requirements.txt` 并部署

### 方案二：Render

1. 注册 [Render](https://render.com/)
2. 创建 Web Service
3. 连接 GitHub 仓库
4. 配置：
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 添加环境变量（同上）

### 方案三：Vercel Serverless

1. 在 `backend` 目录创建 `vercel.json`：

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. 部署：
```bash
cd backend
vercel
```

---

## 数据库部署

### 方案一：PlanetScale（推荐）

1. 注册 [PlanetScale](https://planetscale.com/)
2. 创建数据库
3. 获取连接字符串
4. 运行初始化脚本：
   ```bash
   mysql -h <host> -u <user> -p < backend/database/init_db.sql
   ```

### 方案二：Railway MySQL

1. 在 Railway 项目中添加 MySQL 插件
2. 自动获取 `DATABASE_URL`
3. 连接数据库并运行初始化脚本

---

## 环境变量配置

### 前端环境变量

在 `frontend/.env.production` 中配置：

```
VITE_API_BASE_URL=https://your-backend-url.com
```

更新 `frontend/src/api/index.js`：

```javascript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  // ...
})
```

### 后端环境变量

在部署平台配置以下环境变量：

```
DATABASE_URL=mysql+pymysql://user:password@host:3306/compass_jewel
AGENT_API_KEY=your_agent_api_key
AGENT_MODEL=your_model_name
AGENT_BASE_URL=https://api.example.com
DEBUG=False
```

---

## 部署检查清单

### 前端
- [ ] 构建成功
- [ ] API 地址配置正确
- [ ] GitHub Pages 访问正常
- [ ] CORS 配置正确

### 后端
- [ ] 依赖安装成功
- [ ] 数据库连接正常
- [ ] 环境变量配置完整
- [ ] API 文档可访问（/docs）
- [ ] CORS 允许前端域名

### 数据库
- [ ] 数据库创建成功
- [ ] 表结构初始化完成
- [ ] 连接字符串正确

---

## 常见问题

### 1. CORS 错误

在 `backend/main.py` 中更新 CORS 配置：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://<username>.github.io"],  # 改为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 数据库连接失败

检查 `DATABASE_URL` 格式：
```
mysql+pymysql://username:password@host:port/database_name
```

### 3. 前端无法访问后端

确保前端 API 地址配置正确，并且后端 CORS 允许前端域名。

---

## 监控和日志

### 后端日志

使用 Railway/Render 的日志查看功能：
- Railway: 项目页面 → Deployments → Logs
- Render: Service 页面 → Logs

### 数据库监控

使用 PlanetScale 的 Insights 功能监控查询性能。

---

## 更新部署

### 前端更新
推送代码到 GitHub，GitHub Actions 会自动重新部署。

### 后端更新
推送代码到 GitHub，Railway/Render 会自动重新部署。

---

## 成本估算

- **GitHub Pages**: 免费
- **Railway**: 免费额度 $5/月
- **Render**: 免费层可用
- **PlanetScale**: 免费层 5GB 存储
- **Vercel**: 免费层可用

总计：**完全免费**（在免费额度内）
