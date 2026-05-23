-- COMPASS JEWEL 数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS compass_jewel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE compass_jewel;

-- 爬虫记录表
CREATE TABLE IF NOT EXISTS crawl_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(500) NOT NULL,
    source_platform VARCHAR(50) COMMENT '来源平台（Twitter/Instagram等）',
    content TEXT COMMENT '爬取内容',
    market_region VARCHAR(20) COMMENT '市场区域（JP/KR/SEA）',
    keywords VARCHAR(200) COMMENT '关键词（逗号分隔）',
    crawl_time DATETIME NOT NULL COMMENT '爬取时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_market_region (market_region),
    INDEX idx_crawl_time (crawl_time),
    INDEX idx_keywords (keywords)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬虫记录表';

-- 简报表
CREATE TABLE IF NOT EXISTS briefings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    market_region VARCHAR(20) COMMENT '市场区域',
    briefing_date DATE NOT NULL COMMENT '简报日期',
    content JSON COMMENT '简报内容（JSON格式）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_market_date (market_region, briefing_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日简报表';

-- 对话历史表
CREATE TABLE IF NOT EXISTS chat_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_question TEXT NOT NULL COMMENT '用户提问',
    agent_response TEXT NOT NULL COMMENT 'Agent回答',
    related_record_ids JSON COMMENT '关联的爬虫记录ID数组',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='对话历史表';
