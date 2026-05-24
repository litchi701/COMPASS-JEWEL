#!/usr/bin/env python3
"""从 GitHub 同步 data-in-hecksong 数据集到 backend/data/"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.hecksong_data_service import HecksongDataService


def main():
    count = HecksongDataService.refresh_from_remote()
    stats = HecksongDataService.get_stats()
    print(f"已同步 {count} 条文章")
    print(f"全局过滤率: {stats['filter_rate']}%")
    print(f"分区统计: {stats['by_region']}")


if __name__ == "__main__":
    main()
