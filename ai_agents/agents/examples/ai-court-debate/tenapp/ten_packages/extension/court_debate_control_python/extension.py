"""
法庭辩论控制扩展 - 主控制逻辑
Court Debate Control Extension - Main control logic
"""
import asyncio
import json
import time
import uuid
from typing import Dict, Any
from ten_runtime import (
    AsyncExtension,
    AsyncTenEnv,
    Cmd,
    Data,
)

from .helper import _send_cmd, _send_data, parse_sentences
from .config import CourtDebateControlConfig


class CourtDebateControlExtension(AsyncExtension):
    """
    法庭辩论主控制扩展
    协调 ASR、LLM、TTS 以及法律知识库和案情分析
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.ten_env: AsyncTenEnv = None
        self.config: CourtDebateControlConfig = None
        self.stopped: bool = False
        self._rtc_user_count: int = 0
        self.sentence_fragment: str = ""
        self.turn_id: int = 0
        self.session_id: str = "0"
        self.registered_tools: Dict[str, Any] = {}

    async def on_init(self, ten_env: AsyncTenEnv):
        """初始化"""
        self.ten_env = ten_env
        ten_env.log_info("[CourtDebateControl] Initializing")

        # 加载配置
        try:
            config_json, _ = await ten_env.get_property_to_json(None)
            self.config = CourtDebateControlConfig.model_validate_json(config_json)
            ten_env.log_info("[CourtDebateControl] Configuration loaded")
        except Exception as e:
            ten_env.log_error(f"[CourtDebateControl] Failed to load config: {e}")
            self.config = CourtDebateControlConfig()

    async def on_start(self, ten_env: AsyncTenEnv):
        """启动扩展"""
        ten_env.log_info("[CourtDebateControl] Extension started")

    async def on_stop(self, ten_env: AsyncTenEnv):
        """停止扩展"""
        ten_env.log_info("[CourtDebateControl] Extension stopping")
        self.stopped = True

    async def on_cmd(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """处理命令"""
        cmd_name = cmd.get_name()
        ten_env.log_info(f"[CourtDebateControl] Received command: {cmd_name}")

        if cmd_name == "on_user_joined":
            await self._on_user_joined(ten_env, cmd)
        elif cmd_name == "on_user_left":
            await self._on_user_left(ten_env, cmd)
        elif cmd_name == "tool_register":
            await self._on_tool_register(ten_env, cmd)
        else:
            ten_env.log_warn(f"[CourtDebateControl] Unknown command: {cmd_name}")

    async def on_data(self, ten_env: AsyncTenEnv, data: Data):
        """处理数据"""
        data_name = data.get_name()
        ten_env.log_info(f"[CourtDebateControl] Received data: {data_name}")

        if data_name == "asr_result":
            await self._on_asr_result(ten_env, data)
        else:
            ten_env.log_warn(f"[CourtDebateControl] Unknown data: {data_name}")

    # === Event Handlers ===

    async def _on_user_joined(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """用户加入"""
        self._rtc_user_count += 1
        ten_env.log_info(f"[CourtDebateControl] User joined, count: {self._rtc_user_count}")

        if self._rtc_user_count == 1 and self.config and self.config.greeting:
            # 发送欢迎语
            await self._send_to_tts(self.config.greeting, True)
            await self._send_transcript("assistant", self.config.greeting, True, 100)

    async def _on_user_left(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """用户离开"""
        self._rtc_user_count -= 1
        ten_env.log_info(f"[CourtDebateControl] User left, count: {self._rtc_user_count}")

    async def _on_tool_register(self, ten_env: AsyncTenEnv, cmd: Cmd):
        """注册工具"""
        try:
            tool_json, _ = await cmd.get_property_to_json("tool")
            tool = json.loads(tool_json)
            tool_name = tool.get("function", {}).get("name", "")

            if tool_name:
                self.registered_tools[tool_name] = tool
                ten_env.log_info(f"[CourtDebateControl] Tool registered: {tool_name}")

                # 将工具注册转发给 LLM
                await ten_env.send_cmd(cmd)
            else:
                ten_env.log_warn("[CourtDebateControl] Tool registration missing name")

        except Exception as e:
            ten_env.log_error(f"[CourtDebateControl] Failed to register tool: {e}")

    async def _on_asr_result(self, ten_env: AsyncTenEnv, data: Data):
        """处理 ASR 识别结果"""
        try:
            # 获取识别文本
            text, _ = await data.get_property_string("text")
            is_final, _ = await data.get_property_bool("is_final")

            if not text:
                return

            # 获取 session_id
            try:
                metadata_json, _ = await data.get_property_to_json("metadata")
                metadata = json.loads(metadata_json)
                self.session_id = metadata.get("session_id", "100")
            except:
                self.session_id = "100"

            stream_id = int(self.session_id)

            ten_env.log_info(f"[CourtDebateControl] ASR result: text='{text}', is_final={is_final}")

            # 如果用户开始说话，中断当前输出
            if is_final or len(text) > 2:
                await self._interrupt()

            if is_final:
                self.turn_id += 1

                # 发送问题到 LLM
                await self._send_to_llm(text)

            # 发送转录记录
            await self._send_transcript("user", text, is_final, stream_id)

        except Exception as e:
            ten_env.log_error(f"[CourtDebateControl] Error processing ASR result: {e}")

    # === Helper Methods ===

    async def _send_to_llm(self, text: str):
        """发送文本到 LLM"""
        try:
            # 构建包含系统提示的消息
            request_id = f"llm-request-{self.turn_id}"

            payload = {
                "request_id": request_id,
                "text": text,
                "metadata": {
                    "session_id": self.session_id,
                    "turn_id": self.turn_id
                }
            }

            await _send_data(self.ten_env, "text_data", "llm", payload)
            self.ten_env.log_info(f"[CourtDebateControl] Sent to LLM: {text}")

            # 注册回调来处理 LLM 响应
            # 在实际实现中，这里会设置一个监听器来接收 LLM 的响应
            # 简化版本中，我们假设会通过 on_data 接收 llm_response

        except Exception as e:
            self.ten_env.log_error(f"[CourtDebateControl] Error sending to LLM: {e}")

    async def _send_to_tts(self, text: str, is_final: bool):
        """发送文本到 TTS"""
        if not text:
            return

        try:
            request_id = f"tts-request-{self.turn_id}"
            payload = {
                "request_id": request_id,
                "text": text,
                "text_input_end": is_final,
                "metadata": {
                    "session_id": self.session_id,
                    "turn_id": self.turn_id
                }
            }

            await _send_data(self.ten_env, "tts_text_input", "tts", payload)
            self.ten_env.log_info(f"[CourtDebateControl] Sent to TTS: {text} (final={is_final})")

        except Exception as e:
            self.ten_env.log_error(f"[CourtDebateControl] Error sending to TTS: {e}")

    async def _send_transcript(self, role: str, text: str, is_final: bool, stream_id: int):
        """发送转录记录"""
        try:
            payload = {
                "data_type": "transcribe",
                "role": role,
                "text": text,
                "text_ts": int(time.time() * 1000),
                "is_final": is_final,
                "stream_id": stream_id,
            }

            await _send_data(self.ten_env, "message", "message_collector", payload)
            self.ten_env.log_info(f"[CourtDebateControl] Transcript sent: {role}, {text}")

        except Exception as e:
            self.ten_env.log_error(f"[CourtDebateControl] Error sending transcript: {e}")

    async def _interrupt(self):
        """中断当前输出"""
        try:
            self.sentence_fragment = ""

            # 中断 TTS
            await _send_data(
                self.ten_env,
                "tts_flush",
                "tts",
                {"flush_id": str(uuid.uuid4())}
            )

            # 中断 RTC
            await _send_cmd(self.ten_env, "flush", "agora_rtc")

            self.ten_env.log_info("[CourtDebateControl] Interrupt signal sent")

        except Exception as e:
            self.ten_env.log_error(f"[CourtDebateControl] Error during interrupt: {e}")
