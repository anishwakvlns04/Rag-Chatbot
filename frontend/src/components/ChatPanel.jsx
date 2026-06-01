import { useState } from "react";
import Message from "./Message";

function ChatPanel() {
  const [question, setQuestion] = useState("");
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Ask me anything about the video.",
    },
  ]);

   const clearChat = async () => {
    try {
      await fetch(
        "http://localhost:8000/clear-chat",
        {
          method: "POST",
        }
      );

      setMessages([
        {
          role: "assistant",
          text: "Ask me anything about the video.",
        },
      ]);
    } catch (error) {
      console.error(error);
    }
  };
  const handleSend = async () => {
    if (!question.trim()) return;
    if (sending) return;

    setSending(true);

    const userQuestion = question;

    const userMessage = {
      role: "user",
      text: userQuestion,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        role: "assistant",
        text: "",
        sources: [],
      },
    ]);

    setQuestion("");

    try {
      const response = await fetch(
        "http://localhost:8000/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder();

      let streamedText = "";

      while (true) {
        const {
          done,
          value,
        } = await reader.read();

        if (done) break;

        streamedText += decoder.decode(
          value
        );

        setMessages((prev) => {
          const updated = [...prev];

          updated[
            updated.length - 1
          ] = {
            role: "assistant",
            text: streamedText,
            sources: [],
          };

          return updated;
        });
      }

      const sourcesResponse =
  await fetch(
    "http://localhost:8000/chat/sources",
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/json",
      },
      body: JSON.stringify({
        question: userQuestion,
      }),
    }
  );

const sourcesData =
  await sourcesResponse.json();

setMessages((prev) => {
  const updated = [...prev];

  updated[
    updated.length - 1
  ] = {
    role: "assistant",
    text: streamedText,
    sources: sourcesData.sources,
  };

  return updated;
});
    } catch (error) {
      console.error(error);

      setMessages((prev) => {
        const updated = [...prev];

        updated[
          updated.length - 1
        ] = {
          role: "assistant",
          text: "Error contacting backend",
          sources: [],
        };

        return updated;
      });
    }
    finally {
  setSending(false);
}
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-4">
     <div className="flex justify-between items-center mb-4">
  <h2 className="text-xl font-semibold">
    Chat
  </h2>

  <button
    onClick={clearChat}
    className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm"
  >
    New Chat
  </button>
</div>

      <div className="h-96 overflow-y-auto">
        {messages.map((msg, index) => (
          <Message
            key={index}
            role={msg.role}
            text={msg.text}
            sources={msg.sources}
          />
        ))}
      </div>

      <div className="flex gap-2 mt-4">
        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  }}
          placeholder="Ask a question..."
          className="flex-1 border rounded-lg p-3"
        />

        <button
          onClick={handleSend}
          disabled={sending}
          className="bg-black text-white px-5 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;