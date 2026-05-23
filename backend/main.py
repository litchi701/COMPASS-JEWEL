from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import briefing, chat

app = FastAPI(
    title="COMPASS JEWEL API",
    description="Strategic Intelligence Backend API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要修改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(briefing.router, prefix="/api/briefing", tags=["briefing"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def root():
    return {"message": "COMPASS JEWEL API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
