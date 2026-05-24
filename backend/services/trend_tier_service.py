"""
热点趋势分级服务
提供按市场和层级查询热点的功能
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


class TrendTierService:
    """热点分级查询服务"""

    # 高保真 Mock 数据 - 捕获珠宝消费心智转移的早期信号
    # 聚焦：日常配饰化、悦己消费、保值刚需、小众标签和情感黑话
    MOCK_TRENDS = {
        "JP": {
            "Tier-1": [
                {
                    "id": "jp-tier1-001",
                    "name": "#ちいかわ金豆豆 微小叙事解压储蓄",
                    "category": "情绪价值×保值刚需",
                    "initial_score": 89,
                    "current_score": 96,
                    "wear_conversion_rate": 78.2,
                    "social_volume": "15.3K",
                    "observation_days": 14,
                    "remaining_days": 16,
                    "status": "长线资产确认",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-09T08:30:00Z",
                    "key_insights": "年轻人将黄金从婚庆场景解放，转向日常解压+积蓄双重心智，IP联名降低心理门槛",
                    "risk_level": "低",
                    "recommendation": "抢占'金豆豆日常化'叙事，前置布局社媒内容",
                },
                {
                    "id": "jp-tier1-002",
                    "name": "#お守りジュエリー 情绪护身符珠宝",
                    "category": "悦己消费×日常配饰",
                    "initial_score": 85,
                    "current_score": 94,
                    "wear_conversion_rate": 72.5,
                    "social_volume": "12.8K",
                    "observation_days": 18,
                    "remaining_days": 12,
                    "status": "稳健增长",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-05T14:20:00Z",
                    "key_insights": "珠宝从'展示性消费'转向'情绪陪伴'，年轻人赋予饰品护身符般的心理寄托",
                    "risk_level": "低",
                    "recommendation": "挖掘情绪黑话，开发'陪伴型'产品线",
                },
                {
                    "id": "jp-tier1-003",
                    "name": "#推し貯金 偶像应援式储蓄",
                    "category": "保值刚需×粉丝经济",
                    "initial_score": 88,
                    "current_score": 93,
                    "wear_conversion_rate": 68.9,
                    "social_volume": "11.2K",
                    "observation_days": 12,
                    "remaining_days": 18,
                    "status": "快速上升期",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-11T10:15:00Z",
                    "key_insights": "粉丝将应援预算转化为黄金饰品，既满足情感需求又实现资产保值",
                    "risk_level": "中",
                    "recommendation": "结合粉丝经济+保值属性，开发定制化产品",
                },
            ],
            "Tier-2": [
                {
                    "id": "jp-tier2-001",
                    "name": "#脱婚活ジュエリー 脱离婚恋市场的自购",
                    "category": "悦己消费×日常配饰",
                    "initial_score": 76,
                    "current_score": 82,
                    "wear_conversion_rate": 45.3,
                    "social_volume": "6.8K",
                    "observation_days": 7,
                    "remaining_days": 7,
                    "status": "稳健验证期",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-16T16:45:00Z",
                    "key_insights": "年轻女性主动脱离'等待被赠予'心智，自购珠宝作为独立宣言",
                    "risk_level": "中",
                    "recommendation": "观察'自购珠宝'叙事是否能破圈，布局女性独立营销",
                },
                {
                    "id": "jp-tier2-002",
                    "name": "#通勤お守り 职场护身符配饰",
                    "category": "日常配饰×情绪价值",
                    "initial_score": 72,
                    "current_score": 79,
                    "wear_conversion_rate": 42.1,
                    "social_volume": "5.4K",
                    "observation_days": 5,
                    "remaining_days": 9,
                    "status": "初期验证",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-18T09:30:00Z",
                    "key_insights": "职场女性将珠宝从'社交展示'转向'情绪支撑'，日常佩戴需求强",
                    "risk_level": "中",
                    "recommendation": "挖掘职场情绪黑话，开发轻量化日常款",
                },
            ],
            "Tier-3": [
                {
                    "id": "jp-tier3-001",
                    "name": "#金活 黄金生活方式",
                    "category": "保值刚需×生活方式",
                    "initial_score": 68,
                    "current_score": 71,
                    "wear_conversion_rate": 18.7,
                    "social_volume": "2.1K",
                    "observation_days": 2,
                    "remaining_days": 12,
                    "status": "初始爆发期",
                    "tier": "Tier-3",
                    "discovered_at": "2026-05-21T11:20:00Z",
                    "key_insights": "年轻人将黄金从'婚庆刚需'重新定义为'日常生活方式'，微弱信号",
                    "risk_level": "高",
                    "recommendation": "持续监控，若破圈可抢占'金活'叙事红利",
                },
                {
                    "id": "jp-tier3-002",
                    "name": "#ソロウェディング 单身婚礼自购钻戒",
                    "category": "悦己消费×仪式感",
                    "initial_score": 65,
                    "current_score": 69,
                    "wear_conversion_rate": 15.2,
                    "social_volume": "1.8K",
                    "observation_days": 1,
                    "remaining_days": 13,
                    "status": "待观察",
                    "tier": "Tier-3",
                    "discovered_at": "2026-05-22T14:50:00Z",
                    "key_insights": "单身女性为自己举办婚礼并自购钻戒，挑战传统婚恋叙事",
                    "risk_level": "高",
                    "recommendation": "观察是否为小众现象，验证市场规模",
                },
            ],
        },
        "US": {
            "Tier-1": [
                {
                    "id": "us-tier1-001",
                    "name": "#VintageGold 中古金饰日常化",
                    "category": "保值刚需×可持续消费",
                    "initial_score": 91,
                    "current_score": 97,
                    "wear_conversion_rate": 82.4,
                    "social_volume": "28.5K",
                    "observation_days": 21,
                    "remaining_days": 9,
                    "status": "成熟长线资产",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-02T07:15:00Z",
                    "key_insights": "Gen Z将中古金饰从'婚庆传家'重新定义为'日常保值+可持续'，消费心智彻底转移",
                    "risk_level": "低",
                    "recommendation": "全力投入，抢占'中古金日常化'叙事主导权",
                },
                {
                    "id": "us-tier1-002",
                    "name": "#LabGrownDiamond 培育钻石情绪转折",
                    "category": "悦己消费×价值重构",
                    "initial_score": 87,
                    "current_score": 95,
                    "wear_conversion_rate": 76.8,
                    "social_volume": "22.3K",
                    "observation_days": 16,
                    "remaining_days": 14,
                    "status": "稳健增长",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-07T12:40:00Z",
                    "key_insights": "年轻人对培育钻石的情绪从'廉价替代'转向'理性选择'，钻石婚恋绑定正在瓦解",
                    "risk_level": "低",
                    "recommendation": "前置布局'培育钻石日常化'内容，抢占破圈红利",
                },
                {
                    "id": "us-tier1-003",
                    "name": "#SelfLoveRing 自爱戒指运动",
                    "category": "悦己消费×仪式感",
                    "initial_score": 88,
                    "current_score": 93,
                    "wear_conversion_rate": 68.9,
                    "social_volume": "18.7K",
                    "observation_days": 12,
                    "remaining_days": 18,
                    "status": "快速上升期",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-11T10:15:00Z",
                    "key_insights": "女性为自己购买戒指作为'自爱宣言'，彻底脱离'等待被求婚'心智",
                    "risk_level": "低",
                    "recommendation": "挖掘'自爱'情感黑话，开发自购戒指产品线",
                },
            ],
            "Tier-2": [
                {
                    "id": "us-tier2-001",
                    "name": "#GoldStacking 黄金积蓄游戏化",
                    "category": "保值刚需×游戏化储蓄",
                    "initial_score": 78,
                    "current_score": 84,
                    "wear_conversion_rate": 48.6,
                    "social_volume": "9.2K",
                    "observation_days": 8,
                    "remaining_days": 6,
                    "status": "验证期",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-15T10:25:00Z",
                    "key_insights": "年轻人将黄金购买游戏化，每月'打卡'积累金饰，储蓄+悦己双重满足",
                    "risk_level": "中",
                    "recommendation": "观察'游戏化储蓄'是否能破圈，布局社媒挑战活动",
                },
                {
                    "id": "us-tier2-002",
                    "name": "#AnxietyJewelry 焦虑缓解饰品",
                    "category": "情绪价值×日常配饰",
                    "initial_score": 74,
                    "current_score": 81,
                    "wear_conversion_rate": 44.2,
                    "social_volume": "7.8K",
                    "observation_days": 6,
                    "remaining_days": 8,
                    "status": "稳步上升",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-17T08:50:00Z",
                    "key_insights": "年轻人将珠宝赋予'焦虑缓解'功能，从装饰品转向情绪工具",
                    "risk_level": "中",
                    "recommendation": "挖掘心理健康黑话，开发'陪伴型'产品",
                },
            ],
            "Tier-3": [
                {
                    "id": "us-tier3-001",
                    "name": "#DivorceRings 离婚戒指庆祝",
                    "category": "悦己消费×人生叙事重构",
                    "initial_score": 70,
                    "current_score": 73,
                    "wear_conversion_rate": 22.5,
                    "social_volume": "3.4K",
                    "observation_days": 3,
                    "remaining_days": 11,
                    "status": "初期爆发",
                    "tier": "Tier-3",
                    "discovered_at": "2026-05-20T13:30:00Z",
                    "key_insights": "女性购买'离婚戒指'庆祝新生，挑战传统婚恋珠宝叙事",
                    "risk_level": "高",
                    "recommendation": "观察14天，评估是否为小众现象还是心智转移信号",
                },
            ],
        },
        "KR": {
            "Tier-1": [
                {
                    "id": "kr-tier1-001",
                    "name": "#소확행주얼리 小确幸珠宝",
                    "category": "悦己消费×日常配饰",
                    "initial_score": 90,
                    "current_score": 96,
                    "wear_conversion_rate": 80.3,
                    "social_volume": "18.7K",
                    "observation_days": 17,
                    "remaining_days": 13,
                    "status": "长线资产",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-06T09:20:00Z",
                    "key_insights": "年轻人将珠宝从'人生大事'降维为'日常小确幸'，轻量化消费心智转移",
                    "risk_level": "低",
                    "recommendation": "抢占'小确幸珠宝'叙事，布局日常化产品线",
                },
                {
                    "id": "kr-tier1-002",
                    "name": "#나를위한선물 给自己的礼物",
                    "category": "悦己消费×仪式感",
                    "initial_score": 88,
                    "current_score": 94,
                    "wear_conversion_rate": 75.6,
                    "social_volume": "16.2K",
                    "observation_days": 15,
                    "remaining_days": 15,
                    "status": "稳健增长",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-08T11:30:00Z",
                    "key_insights": "女性自购珠宝作为'自我奖励'，脱离'等待他人赠予'传统心智",
                    "risk_level": "低",
                    "recommendation": "挖掘'自我奖励'情感黑话，开发自购礼盒",
                },
            ],
            "Tier-2": [
                {
                    "id": "kr-tier2-001",
                    "name": "#금테크 黄金理财",
                    "category": "保值刚需×年轻化",
                    "initial_score": 75,
                    "current_score": 82,
                    "wear_conversion_rate": 46.8,
                    "social_volume": "8.1K",
                    "observation_days": 7,
                    "remaining_days": 7,
                    "status": "验证期",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-16T11:40:00Z",
                    "key_insights": "年轻人将黄金从'婚庆必备'转向'理财工具'，投资属性觉醒",
                    "risk_level": "中",
                    "recommendation": "观察'黄金理财'心智是否能破圈，布局投资型产品",
                },
                {
                    "id": "kr-tier2-002",
                    "name": "#혼주얼리 单身珠宝",
                    "category": "悦己消费×身份认同",
                    "initial_score": 72,
                    "current_score": 79,
                    "wear_conversion_rate": 42.3,
                    "social_volume": "6.9K",
                    "observation_days": 6,
                    "remaining_days": 8,
                    "status": "初期验证",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-17T14:20:00Z",
                    "key_insights": "单身群体主动购买珠宝作为身份认同，挑战'珠宝=婚恋'传统",
                    "risk_level": "中",
                    "recommendation": "观察单身经济是否能带动珠宝消费",
                },
            ],
            "Tier-3": [
                {
                    "id": "kr-tier3-001",
                    "name": "#이별반지 分手戒指",
                    "category": "悦己消费×情绪疗愈",
                    "initial_score": 72,
                    "current_score": 75,
                    "wear_conversion_rate": 25.3,
                    "social_volume": "4.2K",
                    "observation_days": 2,
                    "remaining_days": 12,
                    "status": "初期观察",
                    "tier": "Tier-3",
                    "discovered_at": "2026-05-21T15:10:00Z",
                    "key_insights": "年轻人购买'分手戒指'作为情绪疗愈，珠宝从'爱情见证'转向'自我疗愈'",
                    "risk_level": "高",
                    "recommendation": "观察是否为小众现象，验证情绪疗愈市场",
                },
            ],
        },
        "SEA": {
            "Tier-1": [
                {
                    "id": "sea-tier1-001",
                    "name": "#GoldSavings 黄金储蓄日常化",
                    "category": "保值刚需×日常配饰",
                    "initial_score": 88,
                    "current_score": 94,
                    "wear_conversion_rate": 71.5,
                    "social_volume": "14.2K",
                    "observation_days": 15,
                    "remaining_days": 15,
                    "status": "稳健增长",
                    "tier": "Tier-1",
                    "discovered_at": "2026-05-08T10:30:00Z",
                    "key_insights": "东南亚年轻人将黄金从'婚庆三金'转向'日常储蓄+佩戴'双重需求",
                    "risk_level": "低",
                    "recommendation": "强化'储蓄+佩戴'双重价值，开发轻量化产品",
                },
            ],
            "Tier-2": [
                {
                    "id": "sea-tier2-001",
                    "name": "#ModestFashion 穆斯林时尚珠宝",
                    "category": "日常配饰×文化融合",
                    "initial_score": 77,
                    "current_score": 83,
                    "wear_conversion_rate": 47.2,
                    "social_volume": "7.5K",
                    "observation_days": 6,
                    "remaining_days": 8,
                    "status": "文化验证期",
                    "tier": "Tier-2",
                    "discovered_at": "2026-05-17T14:20:00Z",
                    "key_insights": "年轻穆斯林女性将珠宝从'传统约束'转向'时尚表达'，日常化需求强",
                    "risk_level": "中",
                    "recommendation": "深入了解文化边界，开发符合教义的时尚产品",
                },
            ],
            "Tier-3": [
                {
                    "id": "sea-tier3-001",
                    "name": "#SelfGift 自我礼物文化",
                    "category": "悦己消费×节日重构",
                    "initial_score": 69,
                    "current_score": 72,
                    "wear_conversion_rate": 20.8,
                    "social_volume": "2.9K",
                    "observation_days": 3,
                    "remaining_days": 11,
                    "status": "初期观察",
                    "tier": "Tier-3",
                    "discovered_at": "2026-05-20T16:45:00Z",
                    "key_insights": "年轻人在节日为自己购买珠宝，挑战'珠宝=他人赠予'传统",
                    "risk_level": "高",
                    "recommendation": "观察自购文化是否能在东南亚破圈",
                },
            ],
        },
    }

    @classmethod
    def get_trends_by_tier(
        cls, market_id: str, tier: str, randomize: bool = False
    ) -> List[Dict[str, Any]]:
        """
        获取指定市场和层级的热点列表

        Args:
            market_id: 市场ID (JP/KR/SEA/US)
            tier: 层级 (Tier-1/Tier-2/Tier-3)
            randomize: 是否随机化数据（用于测试）

        Returns:
            热点列表
        """
        market_id = market_id.upper()

        # 获取基础数据
        if market_id not in cls.MOCK_TRENDS:
            return []

        if tier not in cls.MOCK_TRENDS[market_id]:
            return []

        trends = cls.MOCK_TRENDS[market_id][tier].copy()

        # 如果需要随机化（用于测试）
        if randomize:
            trends = cls._randomize_trends(trends)

        return trends

    @classmethod
    def _randomize_trends(cls, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """随机化热点数据，用于测试"""
        randomized = []

        for trend in trends:
            randomized_trend = trend.copy()

            # 随机化分数（±5分）
            randomized_trend["current_score"] = max(
                0, min(100, trend["current_score"] + random.randint(-5, 5))
            )

            # 随机化转化率（±10%）
            randomized_trend["wear_conversion_rate"] = max(
                0, min(100, trend["wear_conversion_rate"] + random.uniform(-10, 10))
            )
            randomized_trend["wear_conversion_rate"] = round(
                randomized_trend["wear_conversion_rate"], 1
            )

            # 随机化社交声量（±20%）
            volume_num = float(trend["social_volume"].replace("K", ""))
            volume_num = max(0, volume_num + random.uniform(-volume_num * 0.2, volume_num * 0.2))
            randomized_trend["social_volume"] = f"{volume_num:.1f}K"

            # 随机化剩余天数（±3天）
            randomized_trend["remaining_days"] = max(
                0, trend["remaining_days"] + random.randint(-3, 3)
            )

            randomized.append(randomized_trend)

        return randomized

    @classmethod
    def get_all_markets(cls) -> List[str]:
        """获取所有支持的市场"""
        return list(cls.MOCK_TRENDS.keys())

    @classmethod
    def get_all_tiers(cls) -> List[str]:
        """获取所有层级"""
        return ["Tier-1", "Tier-2", "Tier-3"]

    @classmethod
    def get_trend_by_id(cls, trend_id: str) -> Dict[str, Any]:
        """根据ID获取单个热点详情"""
        for market_trends in cls.MOCK_TRENDS.values():
            for tier_trends in market_trends.values():
                for trend in tier_trends:
                    if trend["id"] == trend_id:
                        return trend
        return None
