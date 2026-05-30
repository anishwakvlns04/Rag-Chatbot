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
You are an AI assistant helping users analyze videos.

The context contains information from one or more videos.

Use the context to answer naturally.

If the user asks for:
- comparison
- similarities
- differences
- recommendations
- relationships between videos

analyze the retrieved information and provide a reasoned answer.

Do NOT mention Video A or Video B unless the user
explicitly asks about them.

Use conversation history when relevant.

Do not invent facts that are not present in the context.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""
)


def generate_answer(
    question,
    chunks,
    chat_history
):

    try:

        history_text = "\n".join(
            [
                f"User: {item['question']}\nAssistant: {item['answer']}"
                for item in chat_history
            ]
        )

        context = "\n\n".join(
            [
                f"[Video {chunk['video_id']}]\n{chunk['text']}"
                for chunk in chunks
            ]
        )

        chain = prompt_template | llm

        response = chain.invoke(
            {
                "history": history_text,
                "context": context,
                "question": question
            }
        )

        return response.content

    except Exception as e:
        return f"LLM Error: {str(e)}"