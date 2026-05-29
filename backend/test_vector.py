from services.vector_store_service import store_chunks

chunks = [
    "FastAPI is a Python web framework",
    "React is used for frontend development"
]

count = store_chunks(chunks)

print(count)