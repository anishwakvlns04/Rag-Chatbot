import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# Create Chroma client
client = chromadb.Client()

# Create collection
collection = client.get_or_create_collection(
    name="video_chunks"
)


def store_chunks(chunks):

    embeddings = model.encode(
        chunks
    )

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    return len(chunks)

def retrieve_chunks(query, n_results=3):

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