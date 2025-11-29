"""
案情分析扩展 - 提供案件分析和辩论策略
Case Analyzer Extension - Provides case analysis and debate strategy
"""
import json
from typing import Any, Dict, List
from ten_runtime import (
    AsyncExtension,
    AsyncTenEnv,
    Cmd,
    CmdResult,
    StatusCode,
)


class CaseAnalyzerExtension(AsyncExtension):
    """
    案情分析扩展
    分析案件事实、证据，生成辩论策略
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.case_info: Dict[str, Any] = {}
        self.debate_strategy: Dict[str, Any] = {}

    async def on_init(self, ten_env: AsyncTenEnv):
        """初始化案情分析器"""
        ten_env.log_info("[CaseAnalyzer] Initializing case analyzer")

        try:
            # 加载案件信息
            case_json, _ = await ten_env.get_property_to_json("case_info")
            self.case_info = json.loads(case_json)

            # 加载辩论策略
            strategy_json, _ = await ten_env.get_property_to_json("debate_strategy")
            self.debate_strategy = json.loads(strategy_json)

            ten_env.log_info("[CaseAnalyzer] Case analyzer initialized successfully")
        except Exception as e:
            ten_env.log_error(f"[CaseAnalyzer] Failed to initialize: {e}")

    async def on_start(self, ten_env: AsyncTenEnv):
        """启动扩展并注册工具"""
        ten_env.log_info("[CaseAnalyzer] Extension started")
        await self._register_tool(ten_env)

    async def on_cmd(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """处理命令"""
        cmd_name = cmd.get_name()
        ten_env.log_info(f"[CaseAnalyzer] Received command: {cmd_name}")

        if cmd_name == "tool_call":
            await self._handle_tool_call(ten_env, cmd)
        else:
            await ten_env.return_result(CmdResult.create(StatusCode.ERROR), cmd)

    async def _register_tool(self, ten_env: AsyncTenEnv):
        """注册案情分析工具"""
        tool_definition = {
            "type": "function",
            "function": {
                "name": "analyze_case",
                "description": "分析当前案件信息，提供辩论策略和要点。可以分析案件类型、角色定位、关键证据、辩论焦点等。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "aspect": {
                            "type": "string",
                            "enum": ["overview", "evidence", "strategy", "counterarguments"],
                            "description": "分析方面：overview(总体概况)、evidence(证据分析)、strategy(辩论策略)、counterarguments(反驳要点)"
                        }
                    },
                    "required": ["aspect"]
                }
            }
        }

        register_cmd = Cmd.create("tool_register")
        register_cmd.set_property_from_json("tool", json.dumps(tool_definition))

        await ten_env.send_cmd(register_cmd)
        ten_env.log_info("[CaseAnalyzer] Tool registered successfully")

    async def _handle_tool_call(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """处理工具调用 - 分析案情"""
        try:
            # 获取参数
            arguments_json, _ = await cmd.get_property_to_json("arguments")
            arguments = json.loads(arguments_json)

            aspect = arguments.get("aspect", "overview")

            ten_env.log_info(f"[CaseAnalyzer] Analyzing case: aspect='{aspect}'")

            # 执行分析
            analysis = self._analyze_case(aspect)

            # 返回结果
            result_cmd = CmdResult.create(StatusCode.OK)
            result_cmd.set_property_string("response", json.dumps(analysis, ensure_ascii=False))

            await ten_env.return_result(result_cmd, cmd)
            ten_env.log_info("[CaseAnalyzer] Analysis completed")

        except Exception as e:
            ten_env.log_error(f"[CaseAnalyzer] Error handling tool call: {e}")
            result_cmd = CmdResult.create(StatusCode.ERROR)
            result_cmd.set_property_string("response", json.dumps({"error": str(e)}))
            await ten_env.return_result(result_cmd, cmd)

    def _analyze_case(self, aspect: str) -> Dict[str, Any]:
        """
        分析案件

        Args:
            aspect: 分析方面

        Returns:
            分析结果
        """
        if aspect == "overview":
            return self._get_case_overview()
        elif aspect == "evidence":
            return self._analyze_evidence()
        elif aspect == "strategy":
            return self._get_debate_strategy()
        elif aspect == "counterarguments":
            return self._get_counterarguments()
        else:
            return {"error": "Unknown aspect"}

    def _get_case_overview(self) -> Dict[str, Any]:
        """获取案件总体概况"""
        return {
            "aspect": "案件概况",
            "case_number": self.case_info.get("case_number", "未指定"),
            "case_type": self.case_info.get("case_type", "criminal"),
            "role": self.case_info.get("role", "defendant"),
            "description": self.case_info.get("description", ""),
            "summary": f"本案为{self.case_info.get('case_type', '刑事')}案件，我方作为{self._get_role_name()}，将基于事实和法律进行充分辩护。"
        }

    def _analyze_evidence(self) -> Dict[str, Any]:
        """分析证据"""
        evidence_list = self.case_info.get("evidence", [])
        facts = self.case_info.get("facts", [])

        return {
            "aspect": "证据分析",
            "total_evidence": len(evidence_list),
            "evidence_list": evidence_list,
            "facts": facts,
            "analysis": "需要仔细审查每一项证据的合法性、真实性和关联性。重点关注证据链是否完整，是否达到'证据确实、充分'的证明标准。"
        }

    def _get_debate_strategy(self) -> Dict[str, Any]:
        """获取辩论策略"""
        return {
            "aspect": "辩论策略",
            "role": self.case_info.get("role", "defendant"),
            "focus_points": self.debate_strategy.get("focus_points", []),
            "principles": self.debate_strategy.get("defense_principles", []),
            "strategy_summary": self._generate_strategy_summary()
        }

    def _get_counterarguments(self) -> Dict[str, Any]:
        """获取反驳要点"""
        prosecution_claims = self.case_info.get("prosecution_claims", [])

        return {
            "aspect": "反驳要点",
            "prosecution_claims": prosecution_claims,
            "counterarguments": self._generate_counterarguments(prosecution_claims),
            "defense_approach": "针对控方每一项指控，逐一分析其事实认定和法律适用的问题，提出有力的反驳意见。"
        }

    def _get_role_name(self) -> str:
        """获取角色名称"""
        role = self.case_info.get("role", "defendant")
        role_map = {
            "defendant": "被告方",
            "plaintiff": "原告方",
            "defense": "辩护方",
            "prosecution": "控方"
        }
        return role_map.get(role, role)

    def _generate_strategy_summary(self) -> str:
        """生成策略摘要"""
        role = self.case_info.get("role", "defendant")
        case_type = self.case_info.get("case_type", "criminal")

        if role == "defendant" and case_type == "criminal":
            return "坚持无罪推定原则，审查证据合法性和充分性，挑战控方证据链的完整性，强调疑罪从无原则。"
        elif role == "plaintiff" and case_type == "civil":
            return "明确诉讼请求，提供充分证据证明事实主张，说明法律依据，论证赔偿或履行的合理性。"
        else:
            return "基于事实和法律，提出有理有据的辩论意见。"

    def _generate_counterarguments(self, prosecution_claims: List[str]) -> List[Dict[str, str]]:
        """生成反驳要点"""
        counterarguments = []

        for i, claim in enumerate(prosecution_claims):
            counterarguments.append({
                "claim": claim,
                "counter": f"针对该指控，需要审查其事实依据和证据支持。请对方提供确实充分的证据。",
                "legal_basis": "根据刑事诉讼法，控方负有举证责任，证明标准为'证据确实、充分'。"
            })

        return counterarguments

    async def on_stop(self, ten_env: AsyncTenEnv):
        """停止扩展"""
        ten_env.log_info("[CaseAnalyzer] Extension stopped")
