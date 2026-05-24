#!/usr/bin/env python3
"""
热点分级 API 测试脚本
用于验证 /api/getTrendsByTier 等接口是否正常工作
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def test_get_trends_by_tier():
    """测试获取指定市场和层级的热点列表"""
    print("\n=== 测试 1: 获取日本市场 Tier-1 热点 ===")

    response = requests.get(
        f"{BASE_URL}/api/getTrendsByTier",
        params={"market_id": "JP", "tier": "Tier-1"}
    )

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"市场: {data['market_id']}")
        print(f"层级: {data['tier']}")
        print(f"热点数量: {data['count']}")
        print(f"\n热点列表:")
        for trend in data['trends']:
            print(f"  - {trend['name']}")
            print(f"    评分: {trend['current_score']}/100")
            print(f"    转化率: {trend['wear_conversion_rate']}%")
            print(f"    状态: {trend['status']}")
            print()
    else:
        print(f"错误: {response.text}")


def test_randomize():
    """测试随机化功能"""
    print("\n=== 测试 2: 随机化数据 ===")

    # 调用两次，对比数据是否不同
    response1 = requests.get(
        f"{BASE_URL}/api/getTrendsByTier",
        params={"market_id": "US", "tier": "Tier-1", "randomize": True}
    )

    response2 = requests.get(
        f"{BASE_URL}/api/getTrendsByTier",
        params={"market_id": "US", "tier": "Tier-1", "randomize": True}
    )

    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        trend1 = data1['trends'][0]
        trend2 = data2['trends'][0]

        print(f"第一次调用 - {trend1['name']}")
        print(f"  评分: {trend1['current_score']}")
        print(f"  转化率: {trend1['wear_conversion_rate']}%")

        print(f"\n第二次调用 - {trend2['name']}")
        print(f"  评分: {trend2['current_score']}")
        print(f"  转化率: {trend2['wear_conversion_rate']}%")

        if trend1['current_score'] != trend2['current_score']:
            print("\n✅ 随机化功能正常工作（数据有变化）")
        else:
            print("\n⚠️  数据未变化（可能是随机结果相同）")


def test_get_trend_by_id():
    """测试根据ID获取热点详情"""
    print("\n=== 测试 3: 获取 CHIIKAWA 热点详情 ===")

    response = requests.get(f"{BASE_URL}/api/getTrendById/jp-tier1-001")

    if response.status_code == 200:
        trend = response.json()
        print(f"热点名称: {trend['name']}")
        print(f"分类: {trend['category']}")
        print(f"当前评分: {trend['current_score']}/100")
        print(f"关键洞察: {trend['key_insights']}")
        print(f"建议: {trend['recommendation']}")
    else:
        print(f"错误: {response.text}")


def test_get_markets():
    """测试获取市场列表"""
    print("\n=== 测试 4: 获取所有市场 ===")

    response = requests.get(f"{BASE_URL}/api/getMarkets")

    if response.status_code == 200:
        data = response.json()
        print(f"支持的市场: {', '.join(data['markets'])}")


def test_get_tiers():
    """测试获取层级列表"""
    print("\n=== 测试 5: 获取所有层级 ===")

    response = requests.get(f"{BASE_URL}/api/getTiers")

    if response.status_code == 200:
        data = response.json()
        print(f"支持的层级: {', '.join(data['tiers'])}")


def test_all_markets_all_tiers():
    """测试所有市场所有层级"""
    print("\n=== 测试 6: 遍历所有市场和层级 ===")

    markets_response = requests.get(f"{BASE_URL}/api/getMarkets")
    tiers_response = requests.get(f"{BASE_URL}/api/getTiers")

    if markets_response.status_code == 200 and tiers_response.status_code == 200:
        markets = markets_response.json()['markets']
        tiers = tiers_response.json()['tiers']

        print(f"\n市场 × 层级统计:")
        print("-" * 60)

        for market in markets:
            print(f"\n{market} 市场:")
            for tier in tiers:
                response = requests.get(
                    f"{BASE_URL}/api/getTrendsByTier",
                    params={"market_id": market, "tier": tier}
                )
                if response.status_code == 200:
                    count = response.json()['count']
                    print(f"  {tier}: {count} 个热点")


def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试 7: 错误处理 ===")

    # 测试无效市场
    print("\n测试无效市场 (INVALID):")
    response = requests.get(
        f"{BASE_URL}/api/getTrendsByTier",
        params={"market_id": "INVALID", "tier": "Tier-1"}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 400:
        print(f"错误信息: {response.json()['detail']}")
        print("✅ 错误处理正常")

    # 测试无效层级
    print("\n测试无效层级 (Tier-99):")
    response = requests.get(
        f"{BASE_URL}/api/getTrendsByTier",
        params={"market_id": "JP", "tier": "Tier-99"}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 400:
        print(f"错误信息: {response.json()['detail']}")
        print("✅ 错误处理正常")

    # 测试不存在的热点ID
    print("\n测试不存在的热点ID:")
    response = requests.get(f"{BASE_URL}/api/getTrendById/nonexistent-id")
    print(f"状态码: {response.status_code}")
    if response.status_code == 404:
        print(f"错误信息: {response.json()['detail']}")
        print("✅ 错误处理正常")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("热点分级 API 测试")
    print("=" * 60)

    try:
        # 测试后端是否启动
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ 后端未启动，请先运行: python main.py")
            return

        print("✅ 后端已启动")

        # 运行所有测试
        test_get_trends_by_tier()
        test_randomize()
        test_get_trend_by_id()
        test_get_markets()
        test_get_tiers()
        test_all_markets_all_tiers()
        test_error_handling()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到后端服务")
        print("请确保后端已启动: cd backend && python main.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")


if __name__ == "__main__":
    main()
