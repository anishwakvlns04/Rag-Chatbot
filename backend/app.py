from fastapi import FastAPI
from models import AnalyzeRequest, ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from services.rag_service import (
    generate_answer
)

from services.youtube_service import (
    get_youtube_metadata,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Video Analyzer Backend Running"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    video_b_present = bool(
        request.instagram_url.strip()
    )

    metadata = get_youtube_metadata(
        request.youtube_url
    )

    transcript = get_youtube_transcript(
        request.youtube_url
    )

    print("\n========== TRANSCRIPT ==========")
    print(transcript[:500])
    print("================================\n")

    chunks = chunk_transcript(
        transcript
    )

    stored_count = store_chunks(
        chunks,
        "A"
    )

    return {
        "videoA": {
            "metadata": metadata,
            "transcript_length": len(transcript),
            "total_chunks": len(chunks),
            "stored_vectors": stored_count
        },
        "videoB_available": video_b_present
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