from fastapi import FastAPI
from models import AnalyzeRequest, ChatRequest

from services.rag_service import (
    generate_answer
)

from services.youtube_service import (
    get_youtube_transcript
)

from services.chunking_service import (
    chunk_transcript
)

from services.vector_store_service import (
    store_chunks,
    retrieve_chunks
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Video Analyzer Backend Running"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    transcript = get_youtube_transcript(
        request.youtube_url
    )

    chunks = chunk_transcript(
        transcript
    )

    stored_count = store_chunks(
        chunks
    )

    return {
        "transcript_length": len(transcript),
        "total_chunks": len(chunks),
        "stored_vectors": stored_count
    }


@app.post("/chat")
def chat(request: ChatRequest):

    chunks = retrieve_chunks(
        request.question
    )

    answer = generate_answer(
        request.question,
        chunks
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": chunks
    }