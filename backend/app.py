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

chat_history = []

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

    # Video A
    metadata_a = get_youtube_metadata(
        request.youtube_url
    )

    transcript_a = get_youtube_transcript(
        request.youtube_url
    )

    chunks_a = chunk_transcript(
        transcript_a
    )

    store_chunks(
        chunks_a,
        "A"
    )

    response = {
        "videoA": {
            "metadata": metadata_a,
            "transcript_length": len(transcript_a),
            "total_chunks": len(chunks_a)
        }
    }

    # Video B (temporarily treat as second YouTube URL)
    if request.instagram_url.strip():

        metadata_b = get_youtube_metadata(
            request.instagram_url
        )

        transcript_b = get_youtube_transcript(
            request.instagram_url
        )

        if transcript_b.startswith(
            "Transcript Error"
        ):
            print("Video B transcript failed")
        else:

            chunks_b = chunk_transcript(
                transcript_b
            )


            store_chunks(
                chunks_b,
                "B"
            )

        response["videoB"] = {
            "metadata": metadata_b,
            "transcript_length": len(transcript_b),
            "total_chunks": len(chunks_b)
        }

    return response

@app.post("/chat")
def chat(request: ChatRequest):

    global chat_history

    chunks = retrieve_chunks(
        request.question
    )

    answer = generate_answer(
        request.question,
        chunks,
        chat_history
    )

    chat_history.append(
        {
            "question": request.question,
            "answer": answer
        }
    )

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return {
        "question": request.question,
        "answer": answer,
        "sources": chunks
    }