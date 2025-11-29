from pydantic import BaseModel


class CourtDebateControlConfig(BaseModel):
    greeting: str = "法庭AI辩护助手已就绪。"
    system_prompt: str = "你是一位专业的法律AI助手。"
