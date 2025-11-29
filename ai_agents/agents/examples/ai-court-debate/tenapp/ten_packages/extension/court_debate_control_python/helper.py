import json
from typing import Any, Optional
from ten_runtime import AsyncTenEnv, Cmd, CmdResult, Data, Loc, TenError


def is_punctuation(char):
    """判断是否为标点符号"""
    if char in [",", "，", ".", "。", "?", "？", "!", "！", "；", ";", ":", "："]:
        return True
    return False


def parse_sentences(sentence_fragment, content):
    """解析句子"""
    sentences = []
    current_sentence = sentence_fragment
    for char in content:
        current_sentence += char
        if is_punctuation(char):
            stripped_sentence = current_sentence
            if any(c.isalnum() for c in stripped_sentence):
                sentences.append(stripped_sentence)
            current_sentence = ""

    remain = current_sentence
    return sentences, remain


async def _send_cmd(
    ten_env: AsyncTenEnv, cmd_name: str, dest: str, payload: Any = None
) -> tuple[Optional[CmdResult], Optional[TenError]]:
    """发送命令"""
    cmd = Cmd.create(cmd_name)
    loc = Loc("", "", dest)
    cmd.set_dests([loc])
    if payload is not None:
        cmd.set_property_from_json(None, json.dumps(payload))
    ten_env.log_debug(f"send_cmd: cmd_name {cmd_name}, dest {dest}")
    return await ten_env.send_cmd(cmd)


async def _send_data(
    ten_env: AsyncTenEnv, data_name: str, dest: str, payload: Any = None
) -> Optional[TenError]:
    """发送数据"""
    data = Data.create(data_name)
    loc = Loc("", "", dest)
    data.set_dests([loc])
    if payload is not None:
        data.set_property_from_json(None, json.dumps(payload))
    ten_env.log_debug(f"send_data: data_name {data_name}, dest {dest}")
    return await ten_env.send_data(data)
