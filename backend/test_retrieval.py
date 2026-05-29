from services.vector_store_service import (
    store_chunks,
    retrieve_chunks
)

chunks = [
    "FastAPI is a Python web framework",
    "React is used for frontend development",
    "Dependency Injection is used in FastAPI"
]

store_chunks(chunks)

results = retrieve_chunks(
    "How does dependency injection work?"
)

print(results)