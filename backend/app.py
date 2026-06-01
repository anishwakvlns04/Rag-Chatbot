from fastapi import FastAPI
from models import AnalyzeRequest, ChatRequest
from fastapi.middleware.cors import CORSMiddleware
from services.rag_service import (
    generate_answer,
    stream_answer
)


from services.video_service import (
    get_metadata,
    get_transcript
)
from services.chunking_service import (
    chunk_transcript
)

from services.vector_store_service import (
    store_chunks,
    retrieve_chunks,
    get_hook_chunks,
    clear_vector_store
)
from fastapi.responses import StreamingResponse


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

global chat_history

chat_history = []
video_metadata = {}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    global chat_history
    global video_metadata

    chat_history = []
    video_metadata = {}

    clear_vector_store()


    # Video A
    metadata_a = get_metadata(
    request.video_a_url
    )

    video_metadata["A"] = metadata_a

    transcript_a = get_transcript(
    request.video_a_url
    )

    if metadata_a.get("views") and metadata_a["views"] > 0:
        metadata_a["engagement_rate"] = round(
        (
            (metadata_a.get("likes") or 0)
            + (metadata_a.get("comments") or 0)
        )
        / metadata_a["views"]
        * 100,
        2
    )
    else:
        metadata_a["engagement_rate"] = 0

    chunks_a = []

    if transcript_a.startswith(
        "Transcript Error"
    ):
        print("Video A transcript failed")

    else:
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

    # Video B - optional
    if request.video_b_url.strip():

        metadata_b = get_metadata(
        request.video_b_url
        )

        video_metadata["B"] = metadata_b

        transcript_b = get_transcript(
        request.video_b_url
        )

        if metadata_b.get("views") and metadata_b["views"] > 0:
            metadata_b["engagement_rate"] = round(
        (
            (metadata_b.get("likes") or 0)
            + (metadata_b.get("comments") or 0)
        )
        / metadata_b["views"]
        * 100,
        2
    )
        else:
            metadata_b["engagement_rate"] = 0

        

        chunks_b = []

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
    question_lower = request.question.lower()

    if (
        "hook" in question_lower
        or "first 5 seconds" in question_lower
    ):
        hook_chunks = get_hook_chunks()

        if "A" in hook_chunks and "B" in hook_chunks:

            chunks = [
                {
                    "text": hook_chunks["A"]["text"],
                    "video_id": "A",
                    "chunk_index": 0
                },
                {
                    "text": hook_chunks["B"]["text"],
                    "video_id": "B",
                    "chunk_index": 0
                }
            ]

        else:
            chunks = retrieve_chunks(
                request.question
            )

    else:
        chunks = retrieve_chunks(
            request.question
        )

    answer = generate_answer(
        request.question,
        chunks,
        chat_history,
        video_metadata
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

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    global chat_history
    global video_metadata
    question_lower = request.question.lower()

    if (
        "hook" in question_lower
        or "first 5 seconds" in question_lower
    ):
        hook_chunks = get_hook_chunks()

        if "A" in hook_chunks and "B" in hook_chunks:

            chunks = [
                {
                    "text": hook_chunks["A"]["text"],
                    "video_id": "A",
                    "chunk_index": 0
                },
                {
                    "text": hook_chunks["B"]["text"],
                    "video_id": "B",
                    "chunk_index": 0
                }
            ]

        else:
            chunks = retrieve_chunks(
                request.question
            )

    else:
        chunks = retrieve_chunks(
            request.question
        )

    return StreamingResponse(
        stream_answer(
            request.question,
            chunks,
            chat_history,
            video_metadata
        ),
        media_type="text/plain"
    )

@app.post("/chat/sources")
def chat_sources(request: ChatRequest):

    question_lower = request.question.lower()

    if (
        "hook" in question_lower
        or "first 5 seconds" in question_lower
    ):
        hook_chunks = get_hook_chunks()

        if "A" in hook_chunks and "B" in hook_chunks:

            chunks = [
                {
                    "text": hook_chunks["A"]["text"],
                    "video_id": "A",
                    "chunk_index": 0
                },
                {
                    "text": hook_chunks["B"]["text"],
                    "video_id": "B",
                    "chunk_index": 0
                }
            ]

        else:
            chunks = retrieve_chunks(
                request.question
            )

    else:
        chunks = retrieve_chunks(
            request.question
        )

    return {
        "sources": chunks
    }

@app.post("/clear-chat")
def clear_chat():

    global chat_history

    chat_history = []

    return {
        "message": "Chat history cleared"
    }

