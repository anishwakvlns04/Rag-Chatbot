from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    video_a_url: str
    video_b_url: str


class ChatRequest(BaseModel):
    question: str