import chromadb
from sentence_transformers import SentenceTransformer

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
        f"{video_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "video_id": video_id
        }
        for _ in chunks
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

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )

    return results["documents"][0]