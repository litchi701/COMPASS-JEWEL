from fastapi import APIRouter, HTTPException

from services.hecksong_data_service import HecksongDataService

router = APIRouter()


@router.get("/{market}")
def get_live_feed(market: str, limit: int = 20):
    """
    获取指定市场的去噪后实时信息流（来自 data-in-hecksong）
    """
    try:
        return HecksongDataService.get_feed(market.upper(), limit=min(limit, 50))
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="数据文件未就绪，请先运行 scripts/sync_hecksong_data.py",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载数据失败: {e}")


@router.get("/{market}/stats")
def get_market_stats(market: str):
    """获取指定市场的过滤统计（含本轮过滤率）"""
    try:
        return HecksongDataService.get_stats(market.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计失败: {e}")
