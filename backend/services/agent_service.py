"""
Agent 服务模块
负责调用外部 Agent API
"""

from config.settings import AGENT_API_KEY, AGENT_MODEL, AGENT_BASE_URL

class AgentService:
    """
    Agent 调用服务
    预留：Agent 2（总结分析）和 Agent 3（交互查询）的调用逻辑
    """

    def __init__(self):
        self.api_key = AGENT_API_KEY
        self.model = AGENT_MODEL
        self.base_url = AGENT_BASE_URL

    def call_summary_agent(self, crawl_data: list) -> dict:
        """
        调用 Agent 2：总结分析爬取的数据

        Args:
            crawl_data: 爬虫数据列表

        Returns:
            dict: 分析结果
        """
        # 预留：实现 Agent 2 调用逻辑
        pass

    def call_query_agent(self, question: str, context_data: list) -> dict:
        """
        调用 Agent 3：回答用户提问

        Args:
            question: 用户提问
            context_data: 相关的上下文数据

        Returns:
            dict: Agent 回答和溯源信息
        """
        # 预留：实现 Agent 3 调用逻辑
        pass
