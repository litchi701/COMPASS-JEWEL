from fastapi import APIRouter, HTTPException

from services.hecksong_data_service import HecksongDataService

router = APIRouter()


@router.get("/stats")
def get_global_stats():
    """全局数据统计（515 条文章概览）"""
    try:
        return HecksongDataService.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {e}")


@router.post("/sync")
def sync_data_from_github():
    """从 GitHub 拉取最新 ALL_ARTICLES.json"""
    try:
        count = HecksongDataService.refresh_from_remote()
        return {
            "message": "数据同步成功",
            "articles_count": count,
            "source": "https://github.com/Lby1102/data-in-hecksong",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败: {e}")
