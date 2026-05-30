import os

from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

prompt_template = ChatPromptTemplate.from_template(
    """
You are an AI assistant.

The context contains information from multiple videos.

Do NOT mention Video A or Video B unless the user
explicitly asks for comparison.

Write natural answers.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
)


def generate_answer(question, chunks):

    try:

        context = "\n\n".join(
            [
                f"[Video {chunk['video_id']}]\n{chunk['text']}"
                for chunk in chunks
            ]
        )

        chain = prompt_template | llm

        response = chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        return response.content

    except Exception as e:
        return f"LLM Error: {str(e)}"