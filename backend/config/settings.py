import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/compass_jewel")

# Agent API 配置（预留）
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")  # 预留：Agent API 密钥
AGENT_MODEL = os.getenv("AGENT_MODEL", "")      # 预留：Agent 模型名称
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "")  # 预留：Agent API 地址

# Hecksong 数据集（Agent 1 爬虫产出）
_backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HECKSONG_DATA_PATH = os.getenv(
    "HECKSONG_DATA_PATH",
    os.path.join(_backend_root, "data", "ALL_ARTICLES.json"),
)
HECKSONG_DATA_URL = os.getenv(
    "HECKSONG_DATA_URL",
    "https://raw.githubusercontent.com/Lby1102/data-in-hecksong/main/ALL_ARTICLES.json",
)

# 应用配置
DEBUG = os.getenv("DEBUG", "False") == "True"
