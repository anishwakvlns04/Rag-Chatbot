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

        context = "\n\n".join(chunks)

        prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

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