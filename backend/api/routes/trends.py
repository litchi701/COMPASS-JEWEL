"""
热点趋势分级 API 路由
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from services.trend_tier_service import TrendTierService

router = APIRouter()


@router.get("/getTrendsByTier")
def get_trends_by_tier(
    market_id: str = Query(..., description="市场ID (JP/KR/SEA/US)"),
    tier: str = Query(..., description="层级 (Tier-1/Tier-2/Tier-3)"),
    randomize: Optional[bool] = Query(False, description="是否随机化数据（用于测试）"),
):
    """
    获取指定市场和层级的热点列表

    Args:
        market_id: 市场ID (JP/KR/SEA/US)
        tier: 层级 (Tier-1/Tier-2/Tier-3)
        randomize: 是否随机化数据（用于测试，默认 False）

    Returns:
        {
            "market_id": "JP",
            "tier": "Tier-1",
            "count": 3,
            "trends": [...]
        }
    """
    # 验证参数
    market_id = market_id.upper()
    valid_markets = TrendTierService.get_all_markets()
    valid_tiers = TrendTierService.get_all_tiers()

    if market_id not in valid_markets:
        raise HTTPException(
            status_code=400,
            detail=f"无效的市场ID。支持的市场: {', '.join(valid_markets)}",
        )

    if tier not in valid_tiers:
        raise HTTPException(
            status_code=400,
            detail=f"无效的层级。支持的层级: {', '.join(valid_tiers)}",
        )

    # 获取热点列表
    trends = TrendTierService.get_trends_by_tier(market_id, tier, randomize)

    return {
        "market_id": market_id,
        "tier": tier,
        "count": len(trends),
        "trends": trends,
        "randomized": randomize,
    }


@router.get("/getTrendById/{trend_id}")
def get_trend_by_id(trend_id: str):
    """
    根据ID获取单个热点详情

    Args:
        trend_id: 热点ID

    Returns:
        热点详细信息
    """
    trend = TrendTierService.get_trend_by_id(trend_id)

    if not trend:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {trend_id} 的热点")

    return trend


@router.get("/getMarkets")
def get_markets():
    """
    获取所有支持的市场列表

    Returns:
        {
            "markets": ["JP", "KR", "SEA", "US"]
        }
    """
    return {"markets": TrendTierService.get_all_markets()}


@router.get("/getTiers")
def get_tiers():
    """
    获取所有层级列表

    Returns:
        {
            "tiers": ["Tier-1", "Tier-2", "Tier-3"]
        }
    """
    return {"tiers": TrendTierService.get_all_tiers()}


@router.get("/getAllTrends")
def get_all_trends(
    market_id: Optional[str] = Query(None, description="市场ID（可选）"),
    randomize: Optional[bool] = Query(False, description="是否随机化数据"),
):
    """
    获取所有热点（可按市场筛选）

    Args:
        market_id: 市场ID（可选，不传则返回所有市场）
        randomize: 是否随机化数据

    Returns:
        {
            "markets": {
                "JP": {
                    "Tier-1": [...],
                    "Tier-2": [...],
                    "Tier-3": [...]
                },
                ...
            }
        }
    """
    result = {}

    markets = [market_id.upper()] if market_id else TrendTierService.get_all_markets()

    for market in markets:
        result[market] = {}
        for tier in TrendTierService.get_all_tiers():
            trends = TrendTierService.get_trends_by_tier(market, tier, randomize)
            result[market][tier] = trends

    return {"markets": result, "randomized": randomize}
