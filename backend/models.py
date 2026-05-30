from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    youtube_url: str
    instagram_url: str = ""


class ChatRequest(BaseModel):
    question: str