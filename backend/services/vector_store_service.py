import chromadb
from sentence_transformers import SentenceTransformer
import uuid

# Load embedding model
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# Create Chroma client
client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(
    name="video_chunks"
)


def store_chunks(chunks, video_id):

    embeddings = model.encode(
        chunks
    )

    ids = [
        f"{video_id}_{uuid.uuid4()}"
        for _ in chunks
    ]

    metadatas = [
        {
            "video_id": video_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(chunks)


def retrieve_chunks(query, n_results=8):

    query_embedding = model.encode(
        query
    )

    where_filter = None

    query_lower = query.lower()

    if "video a" in query_lower:
        where_filter = {
            "video_id": "A"
        }

    elif "video b" in query_lower:
        where_filter = {
            "video_id": "B"
        }

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results,
        where=where_filter
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    chunks = []

    for doc, meta in zip(
        documents,
        metadatas
    ):
        chunks.append(
            {
            "text": doc,
            "video_id": meta["video_id"],
            "chunk_index": meta["chunk_index"]
            }
        )

    return chunks

def get_hook_chunks():

    results = collection.get()

    hook_chunks = {}

    for doc, meta in zip(
        results["documents"],
        results["metadatas"]
    ):

        video_id = meta["video_id"]

        if (
            video_id not in hook_chunks
            or meta["chunk_index"]
               < hook_chunks[video_id]["chunk_index"]
        ):
            hook_chunks[video_id] = {
                "text": doc,
                "chunk_index": meta["chunk_index"]
            }

    return hook_chunks