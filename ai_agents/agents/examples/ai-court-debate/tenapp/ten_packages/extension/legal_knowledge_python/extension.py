"""
法律知识库扩展 - 提供法律条文检索和引用功能
Legal Knowledge Extension - Provides legal article search and citation
"""
import json
from typing import Any, Dict
from ten_runtime import (
    AsyncExtension,
    AsyncTenEnv,
    Cmd,
    CmdResult,
    StatusCode,
)


class LegalKnowledgeExtension(AsyncExtension):
    """
    法律知识库扩展
    支持检索刑法、民法等相关法律条文
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.legal_database: Dict[str, Any] = {}

    async def on_init(self, ten_env: AsyncTenEnv):
        """初始化法律知识库"""
        ten_env.log_info("[LegalKnowledge] Initializing legal knowledge database")

        # 加载法律知识库配置
        try:
            config_json, _ = await ten_env.get_property_to_json("legal_database")
            self.legal_database = json.loads(config_json)
            ten_env.log_info(f"[LegalKnowledge] Loaded {len(self.legal_database)} legal categories")
        except Exception as e:
            ten_env.log_error(f"[LegalKnowledge] Failed to load legal database: {e}")
            self.legal_database = {}

    async def on_start(self, ten_env: AsyncTenEnv):
        """启动扩展并注册工具"""
        ten_env.log_info("[LegalKnowledge] Extension started")

        # 注册为 LLM 可调用工具
        await self._register_tool(ten_env)

    async def on_cmd(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """处理命令"""
        cmd_name = cmd.get_name()
        ten_env.log_info(f"[LegalKnowledge] Received command: {cmd_name}")

        if cmd_name == "tool_call":
            await self._handle_tool_call(ten_env, cmd)
        else:
            await ten_env.return_result(CmdResult.create(StatusCode.ERROR), cmd)

    async def _register_tool(self, ten_env: AsyncTenEnv):
        """注册法律知识检索工具"""
        tool_definition = {
            "type": "function",
            "function": {
                "name": "search_legal_knowledge",
                "description": "搜索相关的法律条文和案例。可以根据关键词检索刑法、民法等法律条文，用于支持法庭辩论和答辩。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词，如：盗窃、诈骗、合同纠纷等"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["criminal_law", "civil_law", "all"],
                            "description": "法律类别：criminal_law(刑法)、civil_law(民法)、all(全部)"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

        register_cmd = Cmd.create("tool_register")
        register_cmd.set_property_from_json("tool", json.dumps(tool_definition))

        await ten_env.send_cmd(register_cmd)
        ten_env.log_info("[LegalKnowledge] Tool registered successfully")

    async def _handle_tool_call(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """处理工具调用 - 搜索法律知识"""
        try:
            # 获取参数
            arguments_json, _ = await cmd.get_property_to_json("arguments")
            arguments = json.loads(arguments_json)

            query = arguments.get("query", "")
            category = arguments.get("category", "all")

            ten_env.log_info(f"[LegalKnowledge] Searching: query='{query}', category='{category}'")

            # 执行搜索
            results = self._search_legal_articles(query, category)

            # 返回结果
            result_cmd = CmdResult.create(StatusCode.OK)
            result_cmd.set_property_string("response", json.dumps(results, ensure_ascii=False))

            await ten_env.return_result(result_cmd, cmd)
            ten_env.log_info(f"[LegalKnowledge] Search completed, found {len(results)} results")

        except Exception as e:
            ten_env.log_error(f"[LegalKnowledge] Error handling tool call: {e}")
            result_cmd = CmdResult.create(StatusCode.ERROR)
            result_cmd.set_property_string("response", json.dumps({"error": str(e)}))
            await ten_env.return_result(result_cmd, cmd)

    def _search_legal_articles(self, query: str, category: str = "all") -> list:
        """
        搜索法律条文

        Args:
            query: 搜索关键词
            category: 法律类别

        Returns:
            匹配的法律条文列表
        """
        results = []
        query_lower = query.lower()

        # 确定搜索范围
        categories_to_search = []
        if category == "all":
            categories_to_search = list(self.legal_database.keys())
        elif category in self.legal_database:
            categories_to_search = [category]

        # 执行搜索
        for cat in categories_to_search:
            cat_data = self.legal_database.get(cat, {})
            for law_type, law_info in cat_data.items():
                # 检查关键词匹配
                keywords = law_info.get("keywords", [])
                content = law_info.get("content", "")

                # 匹配条件：关键词匹配或内容包含查询词
                if any(query_lower in kw.lower() for kw in keywords) or query_lower in content.lower():
                    results.append({
                        "category": cat,
                        "type": law_type,
                        "article": law_info.get("article", ""),
                        "content": content,
                        "relevance": "high" if any(query_lower in kw.lower() for kw in keywords) else "medium"
                    })

        # 按相关性排序
        results.sort(key=lambda x: 0 if x["relevance"] == "high" else 1)

        return results

    async def on_stop(self, ten_env: AsyncTenEnv):
        """停止扩展"""
        ten_env.log_info("[LegalKnowledge] Extension stopped")
