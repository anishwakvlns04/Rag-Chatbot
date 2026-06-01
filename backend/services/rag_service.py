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
You are an AI assistant helping content creators analyze videos.

The provided context may contain:
- Transcript chunks
- Video metadata
- Creator information
- Engagement metrics

Use ONLY the provided context.

You can:
- Summarize videos
- Explain topics discussed in videos
- Compare Video A and Video B
- Compare engagement
- Suggest improvements
- Identify creators
- Analyze hooks and openings

When comparing videos, analyze both transcript content and engagement information if available.
For hook comparison questions:

Treat the earliest chunk from each video as the opening hook.

Do not mention missing timestamps.

Compare the opening messages, curiosity, storytelling,
clarity, and audience appeal.

For hook analysis, focus on the opening transcript sections.

Use conversation history when relevant.

Do not invent facts that are not present in the context.
Try to be simple and concise in your explanations.But donot miss important details.

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
    chat_history,
    video_metadata
):

    try:

        history_text = "\n".join(
            [
                f"User: {item['question']}\nAssistant: {item['answer']}"
                for item in chat_history
            ]
        )
        metadata_text = ""
        for video_id, metadata in video_metadata.items():

            metadata_text += f"""
        Video {video_id} Metadata:
        Title: {metadata.get('title')}
        Creator: {metadata.get('creator')}
        Views: {metadata.get('views')}
        Likes: {metadata.get('likes')}
        Comments: {metadata.get('comments')}
        Engagement Rate: {metadata.get('engagement_rate')}
        Followers: {metadata.get('followers')}
        Hashtags: {metadata.get('hashtags')}
        Duration: {metadata.get('duration')}
        Upload Date: {metadata.get('upload_date')}

        """

        transcript_context = "\n\n".join(
            [
                f"[Video {chunk['video_id']} | Chunk {chunk.get('chunk_index', 0)}]\n{chunk['text']}"
                for chunk in chunks
            ]
        )

        context = (
            metadata_text
            + "\n\nTranscript Chunks:\n\n"
            + transcript_context
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


def stream_answer(
    question,
    chunks,
    chat_history,
    video_metadata
):

    history_text = "\n".join(
        [
            f"User: {item['question']}\nAssistant: {item['answer']}"
            for item in chat_history
        ]
    )

    metadata_text = ""

    for video_id, metadata in video_metadata.items():

        metadata_text += f"""
    Video {video_id} Metadata:
    Title: {metadata.get('title')}
    Creator: {metadata.get('creator')}
    Views: {metadata.get('views')}
    Likes: {metadata.get('likes')}
    Comments: {metadata.get('comments')}
    Engagement Rate: {metadata.get('engagement_rate')}
    Followers: {metadata.get('followers')}
    Hashtags: {metadata.get('hashtags')}
    Duration: {metadata.get('duration')}
    Upload Date: {metadata.get('upload_date')}

    """

    transcript_context = "\n\n".join(
        [
            f"[Video {chunk['video_id']} | Chunk {chunk.get('chunk_index', 0)}]\n{chunk['text']}"
            for chunk in chunks
        ]
    )

    context = (
        metadata_text
        + "\n\nTranscript Chunks:\n\n"
        + transcript_context
    )
    
    chain = prompt_template | llm

    full_answer = ""

    for chunk in chain.stream(
        {
            "history": history_text,
            "context": context,
            "question": question
        }
    ):
        full_answer += chunk.content
        yield chunk.content

    chat_history.append(
        {
            "question": question,
            "answer": full_answer
        }
    )

    if len(chat_history) > 10:
        del chat_history[:-10]