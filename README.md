# VidLens - AI Video Analyzer

## Overview

VidLens (AI Video Analyzer) is a Retrieval-Augmented Generation (RAG) application designed to help content creators understand, compare, and analyze the performance of short-form video content.

The system accepts two video URLs (YouTube Shorts and/or Instagram Reels), extracts available metadata and transcripts, stores transcript embeddings in a vector database, and provides a conversational AI interface that allows creators to ask questions about engagement, content strategy, hooks, audience targeting, and performance differences.

Unlike traditional analytics dashboards that only display numbers, this application enables creators to interact with video content through natural language and receive source-backed insights grounded in transcript data.

---

## Why I Built This

Short-form video platforms generate massive amounts of content every day, but creators often struggle to understand why one video performs better than another.

Views, likes, and comments provide metrics, but they do not explain:

- Why viewers engaged
- Which hook worked better
- What audience the content targets
- How a weaker video can be improved

I built this project to demonstrate how Retrieval-Augmented Generation (RAG) can combine transcript intelligence, metadata analysis, semantic search, and conversational AI to generate meaningful content insights.

---

## Features

### Video Processing

- Supports YouTube Shorts
- Supports Instagram Reels
- Automatic platform detection
- Metadata extraction
- Transcript extraction
- Whisper fallback transcription

### Metadata Extraction

The application retrieves available metadata including:

- Title
- Creator Name
- Views
- Likes
- Comments
- Duration
- Upload Date
- Hashtags
- Follower Count (when publicly available)

### Engagement Analysis

The system automatically calculates:

**Engagement Rate = (Likes + Comments) / Views × 100**

This helps creators compare audience interaction across videos.

### RAG Pipeline

- Transcript Chunking
- Embedding Generation
- Vector Storage using ChromaDB
- Semantic Retrieval
- Source Tracking

### Conversational AI

Creators can ask questions such as:

- What is Video A about?
- Compare Video A and Video B
- Why did Video A get more engagement?
- Compare the hooks in the first 5 seconds
- Who is the creator of Video B?
- What hashtags does Video A use?
- Suggest improvements for Video B
- Which audience benefits from this content?

### Chat Features

- Multi-turn memory
- Context-aware responses
- Source citations
- Cross-video comparison
- Metadata-aware retrieval

### Frontend

- Side-by-side video cards
- Metadata dashboard
- Interactive chat panel
- Source display
- Thumbnail fallback support

---

## System Architecture

```text
Video URLs
     │
     ▼
Metadata Extraction
     │
     ▼
Transcript Extraction
     │
     ▼
Chunking
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB Vector Store
     │
     ▼
Semantic Retrieval
     │
     ▼
LLM Analysis
     │
     ▼
Response + Source Citations
```

---

## How It Works

### Step 1 — Video Analysis

The user submits two video URLs.

The system:

- Detects the platform automatically
- Extracts metadata
- Retrieves transcripts

For YouTube:

- `youtube-transcript-api` is attempted first
- Whisper transcription is used as a fallback when necessary

For Instagram:

- Audio is downloaded using `yt-dlp`
- Whisper generates transcripts

### Step 2 — Knowledge Creation

The transcripts are:

- Split into chunks
- Embedded using Sentence Transformers
- Stored inside ChromaDB

Each chunk is tagged with:

- Video ID (A or B)
- Chunk Index

This enables accurate retrieval and source attribution.

### Step 3 — Retrieval-Augmented Generation

When a creator asks a question:

1. Relevant transcript chunks are retrieved from ChromaDB
2. Metadata is added to the retrieved context
3. Conversation history is included
4. The LLM generates a grounded response
5. Sources are displayed to the user

---

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios

### Backend

- FastAPI
- Python

### AI / RAG

- LangChain
- ChromaDB
- Sentence Transformers (BAAI/bge-small-en-v1.5)
- OpenRouter
- Llama 3.3 70B Instruct

### Video Processing

- yt-dlp
- OpenAI Whisper
- youtube-transcript-api

---

## Project Structure

```text
backend/
│
├── app.py
├── models.py
├── requirements.txt
│
├── services/
│   ├── youtube_service.py
│   ├── instagram_service.py
│   ├── chunking_service.py
│   ├── vector_store_service.py
│   └── rag_service.py
│
└── data/

frontend/
│
├── src/
│   ├── components/
│   │   ├── VideoCard.jsx
│   │   └── ChatPanel.jsx
│   │
│   └── App.jsx
│
└── package.json
```

---

## Assignment Requirements Coverage

### Video Input

 - YouTube Shorts

 - Instagram Reels

### Metadata Extraction

 - Creator Name

 - Views

 - Likes

 - Comments

 - Duration

 - Upload Date

 - Hashtags

 - Follower Count (available when exposed by the platform)

### Engagement Analysis

 - Engagement Rate Calculation

### RAG Pipeline

 - Chunking

 - Embeddings

 - ChromaDB Storage

 - Semantic Retrieval

### Conversational Chat

 - Multi-turn Memory
  
 - Source Citations
  
 - Video Comparison
  
 - Hook Analysis
  
 - Improvement Suggestions

### Frontend

 - Side-by-Side Video Cards

 - Chat Interface

 - Source Display

---

## Example Queries

- What is Video A about?
- What is Video B about?
- Compare Video A and Video B
- Compare the hooks in the first 5 seconds
- What hashtags does Video B use?
- Why did Video A get more engagement?
- Suggest improvements for Video B
- Who is the creator of Video B?
- Which audience benefits from Video B?
- What are the key differences between both videos?

---

## Engineering Decisions

### Why ChromaDB?

ChromaDB provides:

- Fast local development
- Zero infrastructure cost
- Simple vector storage
- Easy integration with LangChain

For large-scale production deployments, Qdrant or Pinecone would be preferred.

### Why Sentence Transformers?

The selected embedding model offers:

- Strong retrieval performance
- Low latency
- CPU-friendly execution
- Cost efficiency

### Why Whisper Fallback?

Transcript APIs are not always reliable.

By introducing Whisper fallback transcription, the application can continue functioning even when transcript retrieval APIs fail.

This improves system robustness and reliability.

---

## Scalability Considerations

The current implementation is optimized for rapid development and local deployment.

For production-scale deployment (1000+ creators/day), the following improvements can be introduced:

### Storage

- Qdrant Cloud
- Pinecone
- PostgreSQL + pgvector

### Processing

- Async background workers
- Celery task queues
- GPU-based Whisper services

### Caching

- Redis transcript cache
- Metadata cache
- Embedding cache

### Infrastructure

- Docker containers
- Kubernetes deployment
- Load balancing
- CDN asset caching

---

## Cost Optimization

This solution is designed to minimize inference and infrastructure costs.

### Cost Saving Techniques

- ChromaDB eliminates external vector database costs
- Embeddings are generated once and reused
- Retrieval reduces token consumption
- Whisper runs only when transcript APIs fail
- Metadata extraction is lightweight and fast

This balances quality, speed, and operational cost.

---

## Known Limitations

### YouTube Rate Limiting

YouTube may occasionally return:

- HTTP 429
- Sign-in verification requests

when request volume is high.

The system attempts Whisper-based fallback transcription whenever possible.

### Instagram Metadata Availability

Instagram does not consistently expose:

- View Count
- Like Count
- Follower Count

These fields are displayed whenever publicly available.

### Thumbnail Availability

Instagram thumbnail URLs may expire over time.

The frontend includes fallback handling for unavailable thumbnails.

---

## Future Improvements

- Trend detection across multiple videos
- Creator performance dashboards
- Multi-video comparison
- Audience sentiment analysis
- Topic clustering
- Advanced analytics reports
- Cloud deployment

---


## Author

**Anishwa Kasichainula**

