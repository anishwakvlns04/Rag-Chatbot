import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_answer(question, chunks):

    try:

        context = "\n\n".join(
            [
                f"[Video {chunk['video_id']}]\n{chunk['text']}"
                for chunk in chunks
            ]
        )

        prompt = f"""
You are an AI assistant.

The context contains information from
multiple videos.

Do NOT mention video labels such as
Video A or Video B in the answer unless
the user specifically asks for comparison.

Write a natural answer.

Use the sources only internally.

Answer ONLY using the provided context understand the videos properly.

Context:
{context}

Question:
{question}

Answer:
"""

        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"